"""
TruthLens AI - Backend REST API & Web Application
"""

import os
from flask import Flask, request, jsonify, render_template
from predictor import predictor_instance
import database

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

database.init_database()


@app.route('/')
def home():
    metrics = predictor_instance.metrics
    stats = database.get_prediction_stats()
    return render_template('index.html', metrics=metrics, stats=stats)


@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json(silent=True) or {}
    text = data.get('text', '')
    model_type = data.get('model', 'logistic_regression')

    if not text or not str(text).strip():
        return jsonify({
            'success': False,
            'error': 'Text input cannot be empty. Please provide a news headline or article.'
        }), 400

    result = predictor_instance.predict(text, model_type=model_type, log_to_db=True)
    return jsonify(result)


@app.route('/api/history', methods=['GET'])
def api_history():
    history = database.get_recent_predictions(limit=30)
    stats = database.get_prediction_stats()
    return jsonify({
        'success': True,
        'history': history,
        'stats': stats
    })


@app.route('/api/clear-history', methods=['POST'])
def api_clear_history():
    database.clear_history()
    return jsonify({'success': True, 'message': 'History cleared successfully.'})


@app.route('/api/metrics', methods=['GET'])
def api_metrics():
    return jsonify({
        'success': True,
        'metrics': predictor_instance.metrics,
        'active_model': 'logistic_regression'
    })


@app.route('/api/health', methods=['GET'])
def api_health():
    return jsonify({
        'status': 'healthy',
        'platform': 'TruthLens AI - AI-Based Fake News Detection System',
        'version': '2.0.0',
        'capabilities': ['TF-IDF NLP Vectorizer', 'Logistic Regression L2', 'Multinomial Naive Bayes', 'Linguistic Heuristics']
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting TruthLens AI Engine on http://127.0.0.1:{port}")
    app.run(host='127.0.0.1', port=port, debug=False)
