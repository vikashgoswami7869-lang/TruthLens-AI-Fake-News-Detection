"""
TruthLens AI - Prediction & Credibility Inference Engine
"""

import pickle
from pathlib import Path
import numpy as np

from nlp_pipeline import TextPreprocessor
from database import insert_prediction

BASE_DIR = Path(__file__).parent
MODEL_BUNDLE_PATH = BASE_DIR / "model_bundle.pkl"


class NewsPredictor:
    def __init__(self):
        self.bundle = None
        self.vectorizer = None
        self.nb_model = None
        self.lr_model = None
        self.metrics = None
        self.preprocessor = TextPreprocessor()
        self.load_model()

    def load_model(self):
        if not MODEL_BUNDLE_PATH.exists():
            raise FileNotFoundError("Model bundle not found. Please run train.py first.")
        with open(MODEL_BUNDLE_PATH, 'rb') as f:
            self.bundle = pickle.load(f)
        self.vectorizer = self.bundle['vectorizer']
        self.nb_model = self.bundle['nb_model']
        self.lr_model = self.bundle['lr_model']
        self.metrics = self.bundle['metrics']

    def predict(self, raw_text: str, model_type: str = 'logistic_regression', log_to_db: bool = True) -> dict:
        if not raw_text or not raw_text.strip():
            return {
                'success': False,
                'error': 'Please provide news text or a headline to analyze.'
            }

        text = raw_text.strip()
        linguistic = self.preprocessor.extract_linguistic_features(text)

        X_vec = self.vectorizer.transform([text])

        if model_type == 'naive_bayes':
            proba = self.nb_model.predict_proba(X_vec)[0]
            model_name = "Multinomial Naive Bayes"
        else:
            proba = self.lr_model.predict_proba(X_vec)[0]
            model_name = "Logistic Regression"

        p_fake = float(proba[0])
        p_real = float(proba[1])

        # Linguistic weighting: sensationalism increases fake probability, credible attribution markers increase real probability
        sensational_boost = (linguistic['sensational_score'] / 100.0) * 0.18
        credible_boost = (len(linguistic['credible_hits']) * 0.08)

        adjusted_p_fake = min(1.0, max(0.0, p_fake + sensational_boost - credible_boost))
        adjusted_p_real = 1.0 - adjusted_p_fake

        # Credibility Index: 0 (Definitely Fake) to 100 (Definitely Credible Real)
        credibility_score = round(adjusted_p_real * 100.0, 1)

        if adjusted_p_fake >= 0.50:
            predicted_label = "Fake"
            confidence = round(adjusted_p_fake * 100.0, 1)
        else:
            predicted_label = "Real"
            confidence = round(adjusted_p_real * 100.0, 1)

        # Word-level explainability
        tokens = self.preprocessor.tokenize(text, remove_stopwords=True, ngram_range=(1, 1))
        influential_words = []
        if model_type == 'logistic_regression' and self.lr_model.weights is not None:
            for token in set(tokens):
                if token in self.vectorizer.vocabulary:
                    idx = self.vectorizer.vocabulary[token]
                    weight = self.lr_model.weights[idx]
                    influential_words.append({
                        'word': token,
                        'impact': 'Real' if weight > 0 else 'Fake',
                        'score': round(float(abs(weight)), 3)
                    })
        elif model_type == 'naive_bayes' and self.nb_model.feature_log_prob_ is not None:
            for token in set(tokens):
                if token in self.vectorizer.vocabulary:
                    idx = self.vectorizer.vocabulary[token]
                    diff = self.nb_model.feature_log_prob_[1, idx] - self.nb_model.feature_log_prob_[0, idx]
                    influential_words.append({
                        'word': token,
                        'impact': 'Real' if diff > 0 else 'Fake',
                        'score': round(float(abs(diff)), 3)
                    })

        influential_words = sorted(influential_words, key=lambda x: x['score'], reverse=True)[:10]

        # Contextual explanation & warnings
        reasons = []
        if linguistic['sensational_score'] > 35:
            reasons.append(f"Sensationalism warning: clickbait / alarmist language detected (Score: {linguistic['sensational_score']}/100)")
        if linguistic['exclamation_count'] > 0:
            reasons.append(f"Contains urgent punctuation marks ({linguistic['exclamation_count']} exclamation marks) typical of viral hoaxes")
        if linguistic['caps_ratio'] > 15:
            reasons.append(f"Excessive capitalization ({linguistic['caps_ratio']}%) signaling emotional or exaggerated tone")
        if linguistic['credible_hits']:
            reasons.append(f"Identified verified attribution markers: {', '.join(linguistic['credible_hits'])}")
        
        if predicted_label == "Real" and not reasons:
            reasons.append("Article exhibits neutral tone and terminology consistent with credible journalistic standards")
        elif predicted_label == "Fake" and not reasons:
            reasons.append("Statistical word distribution strongly correlates with known disinformation articles")

        pred_id = None
        if log_to_db:
            try:
                pred_id = insert_prediction(text, predicted_label, confidence)
            except Exception as e:
                print("Database logging notice:", e)

        return {
            'success': True,
            'prediction_id': pred_id,
            'label': predicted_label,
            'confidence': confidence,
            'credibility_score': credibility_score,
            'probabilities': {
                'Fake': round(adjusted_p_fake * 100, 1),
                'Real': round(adjusted_p_real * 100, 1)
            },
            'model_used': model_name,
            'model_key': model_type,
            'linguistic_analysis': linguistic,
            'influential_words': influential_words,
            'explanation': reasons
        }


predictor_instance = NewsPredictor()
