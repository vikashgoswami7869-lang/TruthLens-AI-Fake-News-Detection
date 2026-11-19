# Backend Architecture & REST API Specifications Report

**Project Name:** TruthLens AI &mdash; AI-Based Fake News Detection System  
**Document Category:** Backend Architecture & API Specifications  
**Tech Stack:** Python 3.14, Flask 3.1, RESTful JSON Protocol, SQLite 3  
**PDF Document:** [Backend_Architecture_Report.pdf](file:///C:/Users/Vikash/.gemini/antigravity/scratch/fake-news-detector/docs_and_reports/Backend_Architecture_Report.pdf)  

---

## 1. Server Architecture & Bootstrap

TruthLens AI backend is powered by **Python 3.14** and the **Flask** microframework (`app.py`). The application uses a decoupled modular design:

```
[ HTTP Requests: Client / Browser / cURL ]
                    │
                    ▼
          [ app.py (Flask Server) ]
       • Route Routing & Validation
       • JSON Request Parsing & Error Handling
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
 [ predictor.py ]         [ database.py ]
 • Model Singleton        • SQLite CRUD Operations
 • Preprocessing Hook     • Audit Logging
 • Heuristic Calibrator   • Corpus Management
        │                       │
        ▼                       ▼
 [ ml_models.py ]        [ truthlens.db ]
 • Logistic Regression   • articles table
 • Naive Bayes           • predictions table
```

Upon server launch:
1. `database.init_database()` is invoked, ensuring tables exist.
2. `predictor_instance` preloads `model_bundle.pkl` into resident memory, eliminating per-request disk deserialization.
3. The Flask application serves on `http://127.0.0.1:5000`.

---

## 2. API Endpoints Directory

### 1. `POST /api/predict`
Executes full NLP preprocessing, linguistic analysis, and machine learning inference.

#### Request Payload
```json
{
  "text": "NASA James Webb Space Telescope discovers ancient galaxy cluster...",
  "model": "logistic_regression"
}
```
*Options for `model`: `"logistic_regression"` (default) or `"naive_bayes"`.*

#### Success Response (200 OK)
```json
{
  "success": true,
  "prediction_id": 1,
  "label": "Real",
  "confidence": 81.4,
  "credibility_score": 81.4,
  "probabilities": {
    "Real": 81.4,
    "Fake": 18.6
  },
  "model_used": "Logistic Regression",
  "model_key": "logistic_regression",
  "linguistic_analysis": {
    "sensational_score": 5.7,
    "clickbait_risk": "Low",
    "tone": "Neutral",
    "caps_ratio": 9.52,
    "exclamation_count": 0,
    "question_count": 0,
    "word_count": 12,
    "sensational_hits": [],
    "credible_hits": []
  },
  "influential_words": [
    { "word": "distant", "impact": "Real", "score": 0.445 },
    { "word": "galaxy", "impact": "Real", "score": 0.411 },
    { "word": "telescope", "impact": "Real", "score": 0.411 }
  ],
  "explanation": [
    "Article exhibits neutral tone and terminology consistent with credible journalistic standards"
  ]
}
```

#### Error Response (400 Bad Request)
```json
{
  "success": false,
  "error": "Text input cannot be empty. Please provide a news headline or article."
}
```

---

### 2. `GET /api/history`
Returns chronological verification audit logs and summary statistics.

#### Response
```json
{
  "success": true,
  "history": [
    {
      "id": 1,
      "input_text": "NASA James Webb Space Telescope...",
      "predicted_label": "Real",
      "confidence": 81.4,
      "timestamp": "2026-10-23 18:23:41"
    }
  ],
  "stats": {
    "total_predictions": 1,
    "fake_predictions": 0,
    "real_predictions": 1,
    "average_confidence": 81.4
  }
}
```

---

### 3. `POST /api/clear-history`
Truncates all prediction records from SQLite.
```json
{ "success": true, "message": "History cleared successfully." }
```

---

### 4. `GET /api/metrics`
Returns benchmark evaluation metrics for both models:
```json
{
  "success": true,
  "active_model": "logistic_regression",
  "metrics": {
    "logistic_regression": {
      "accuracy": 100.0,
      "precision": 100.0,
      "recall": 100.0,
      "f1_score": 100.0,
      "confusion_matrix": { "tp": 11, "tn": 9, "fp": 0, "fn": 0 }
    },
    "naive_bayes": {
      "accuracy": 100.0,
      "precision": 100.0,
      "recall": 100.0,
      "f1_score": 100.0,
      "confusion_matrix": { "tp": 11, "tn": 9, "fp": 0, "fn": 0 }
    }
  }
}
```

---

### 5. `GET /api/health`
Service health check:
```json
{
  "status": "healthy",
  "platform": "TruthLens AI - AI-Based Fake News Detection System",
  "version": "2.0.0",
  "capabilities": [
    "TF-IDF NLP Vectorizer",
    "Logistic Regression L2",
    "Multinomial Naive Bayes",
    "Linguistic Heuristics"
  ]
}
```
