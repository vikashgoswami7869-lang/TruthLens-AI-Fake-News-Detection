"""
TruthLens AI - Database Management Module
Persistence for Reference Articles and User Verification Logs (SQLite)
"""

import sqlite3
import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "truthlens.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            label TEXT NOT NULL,
            source TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT NOT NULL,
            predicted_label TEXT NOT NULL,
            confidence REAL NOT NULL,
            timestamp TEXT NOT NULL
        );
    """)

    conn.commit()
    conn.close()


def insert_article(text: str, label: str, source: str = "curated"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO articles (text, label, source)
        VALUES (?, ?, ?)
    """, (text, label, source))
    conn.commit()
    conn.close()


def insert_prediction(input_text: str, predicted_label: str, confidence: float) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO predictions (input_text, predicted_label, confidence, timestamp)
        VALUES (?, ?, ?, ?)
    """, (input_text, predicted_label, confidence, timestamp))
    conn.commit()
    pred_id = cursor.lastrowid
    conn.close()
    return pred_id


def get_recent_predictions(limit: int = 25) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, input_text, predicted_label, confidence, timestamp
        FROM predictions
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_prediction_stats() -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS total FROM predictions")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS fake_cnt FROM predictions WHERE predicted_label = 'Fake'")
    fake_cnt = cursor.fetchone()["fake_cnt"]

    cursor.execute("SELECT COUNT(*) AS real_cnt FROM predictions WHERE predicted_label = 'Real'")
    real_cnt = cursor.fetchone()["real_cnt"]

    cursor.execute("SELECT AVG(confidence) AS avg_conf FROM predictions")
    avg_conf = cursor.fetchone()["avg_conf"] or 0.0

    conn.close()
    return {
        'total_predictions': total,
        'fake_predictions': fake_cnt,
        'real_predictions': real_cnt,
        'average_confidence': round(avg_conf, 1)
    }


def clear_history():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_database()
    print("Database initialized successfully at:", DB_PATH)
