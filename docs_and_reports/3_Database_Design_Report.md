# Database Architecture & Data Design Report

**Project Name:** TruthLens AI &mdash; AI-Based Fake News Detection System  
**Document Category:** Relational Database Architecture & Schema Specification  
**Database Engine:** SQLite 3 (Embedded Serverless Relational Database)  
**Database File:** `truthlens.db`  
**PDF Document:** [Database_Design_Report.pdf](file:///C:/Users/Vikash/.gemini/antigravity/scratch/fake-news-detector/docs_and_reports/Database_Design_Report.pdf)  

---

## 1. Engine Selection & Rationale
For TruthLens AI, SQLite 3 was selected as the embedded relational storage engine for the following architectural reasons:

1. **Zero External Dependency:** Does not require a standalone daemon or network port (like MySQL or MongoDB), removing service connection failure points.
2. **Atomic In-Process Operations:** Database read and write operations execute inside the Python application process with microsecond latency.
3. **Full ACID Compliance:** Guarantees transaction atomicity, consistency, isolation, and durability.
4. **Single-File Portability:** The entire relational database lives in `truthlens.db`, allowing effortless backup, testing, and migration.

---

## 2. Entity Relationship & Schema Details

```
┌───────────────────────────────────────┐
│              ARTICLES                 │
├───────────────────────────────────────┤
│ id        : INTEGER (PK, AUTOINCREMENT)│
│ text      : TEXT    (NOT NULL)        │
│ label     : TEXT    (NOT NULL)        │
│ source    : TEXT    (DEFAULT 'curated')│
└───────────────────────────────────────┘

┌───────────────────────────────────────┐
│             PREDICTIONS               │
├───────────────────────────────────────┤
│ id              : INTEGER (PK, AUTO)  │
│ input_text      : TEXT    (NOT NULL)  │
│ predicted_label : TEXT    (NOT NULL)  │
│ confidence      : REAL    (NOT NULL)  │
│ timestamp       : TEXT    (NOT NULL)  │
└───────────────────────────────────────┘
```

### Table 1: `articles`
Contains curated training samples and reference benchmark articles.

| Column | Type | Nullable | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | INTEGER | NO | AUTOINCREMENT | Unique primary key identifier |
| `text` | TEXT | NO | None | News headline or editorial paragraph content |
| `label` | TEXT | NO | None | Ground truth classification: `'Real'` or `'Fake'` |
| `source` | TEXT | YES | `'curated'` | Publisher, journal, or feed attribution |

#### DDL Statement
```sql
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    label TEXT NOT NULL,
    source TEXT
);
```

---

### Table 2: `predictions`
Maintains an immutable historical audit trail of all verification queries initiated by users or API callers.

| Column | Type | Nullable | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | INTEGER | NO | AUTOINCREMENT | Audit log transaction identifier |
| `input_text` | TEXT | NO | None | Submitted news snippet evaluated by engine |
| `predicted_label` | TEXT | NO | None | Engine verdict: `'Real'` or `'Fake'` |
| `confidence` | REAL | NO | None | Prediction confidence percentage ($0.0 - 100.0$) |
| `timestamp` | TEXT | NO | None | Formatted ISO timestamp (`YYYY-MM-DD HH:MM:SS`) |

#### DDL Statement
```sql
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_text TEXT NOT NULL,
    predicted_label TEXT NOT NULL,
    confidence REAL NOT NULL,
    timestamp TEXT NOT NULL
);
```

---

## 3. Data Access Layer (`database.py`)
The database module exposes high-level Python abstractions:

```python
# 1. Initialize schema
database.init_database()

# 2. Insert labeled article
database.insert_article(text="NASA James Webb...", label="Real", source="NASA")

# 3. Insert user prediction record
pred_id = database.insert_prediction(
    input_text="Scientists discover new solar system",
    predicted_label="Real",
    confidence=88.5
)

# 4. Fetch recent logs
logs = database.get_recent_predictions(limit=25)

# 5. Aggregate statistics
stats = database.get_prediction_stats()
# Returns: {'total_predictions': 15, 'fake_predictions': 6, 'real_predictions': 9, 'average_confidence': 86.4}

# 6. Clear audit logs
database.clear_history()
```

---

## 4. Concurrency & Performance
- Connection management utilizes a helper context manager ensuring that connections and cursors are committed and closed promptly.
- Row results are mapped to dictionary structures using `conn.row_factory = sqlite3.Row`.
- Indexing is automatically enforced on the primary key `id` columns, providing $O(1)$ point lookups.
