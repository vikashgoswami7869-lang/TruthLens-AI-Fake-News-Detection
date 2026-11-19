"""
Machine Learning Classifiers for Fake News Detection
Production-grade implementations of:
1. Multinomial Naive Bayes (Laplace smoothing)
2. Logistic Regression (L2 Regularized with Momentum Gradient Descent)
"""

import numpy as np


class MultinomialNaiveBayes:
    """
    Multinomial Naive Bayes Classifier with Laplace Additive Smoothing.
    Class 0: Fake
    Class 1: Real
    """
    def __init__(self, alpha: float = 1.0):
        self.alpha = alpha
        self.class_log_prior_ = None
        self.feature_log_prob_ = None
        self.classes_ = np.array([0, 1])

    def fit(self, X: np.ndarray, y: np.ndarray):
        n_samples, n_features = X.shape
        n_classes = len(self.classes_)

        self.class_log_prior_ = np.zeros(n_classes)
        self.feature_log_prob_ = np.zeros((n_classes, n_features))

        for c_idx, c in enumerate(self.classes_):
            X_c = X[y == c]
            count_c = len(X_c)
            self.class_log_prior_[c_idx] = np.log(count_c / n_samples)
            feature_counts = X_c.sum(axis=0) + self.alpha
            total_count = feature_counts.sum()
            self.feature_log_prob_[c_idx] = np.log(feature_counts / total_count)

        return self

    def predict_log_proba(self, X: np.ndarray) -> np.ndarray:
        return X @ self.feature_log_prob_.T + self.class_log_prior_

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        log_prob = self.predict_log_proba(X)
        max_log = np.max(log_prob, axis=1, keepdims=True)
        exp_prob = np.exp(log_prob - max_log)
        return exp_prob / np.sum(exp_prob, axis=1, keepdims=True)

    def predict(self, X: np.ndarray) -> np.ndarray:
        proba = self.predict_proba(X)
        return np.argmax(proba, axis=1)


class LogisticRegressionClassifier:
    """
    Logistic Regression Classifier with L2 Regularization & Momentum.
    Class 0: Fake
    Class 1: Real
    """
    def __init__(self, lr: float = 0.5, l2_reg: float = 0.001, epochs: int = 250, momentum: float = 0.9):
        self.lr = lr
        self.l2_reg = l2_reg
        self.epochs = epochs
        self.momentum = momentum
        self.weights = None
        self.bias = 0.0

    @staticmethod
    def _sigmoid(z):
        z = np.clip(z, -25.0, 25.0)
        return 1.0 / (1.0 + np.exp(-z))

    def fit(self, X: np.ndarray, y: np.ndarray):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features, dtype=np.float64)
        self.bias = 0.0

        v_w = np.zeros_like(self.weights)
        v_b = 0.0

        for epoch in range(self.epochs):
            linear_model = np.dot(X, self.weights) + self.bias
            y_pred = self._sigmoid(linear_model)

            error = y_pred - y
            dw = (1.0 / n_samples) * np.dot(X.T, error) + (self.l2_reg * self.weights)
            db = (1.0 / n_samples) * np.sum(error)

            v_w = self.momentum * v_w + self.lr * dw
            v_b = self.momentum * v_b + self.lr * db

            self.weights -= v_w
            self.bias -= v_b

        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        linear_model = np.dot(X, self.weights) + self.bias
        p_real = self._sigmoid(linear_model)
        p_fake = 1.0 - p_real
        return np.column_stack([p_fake, p_real])

    def predict(self, X: np.ndarray) -> np.ndarray:
        proba = self.predict_proba(X)
        return (proba[:, 1] >= 0.5).astype(int)


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    tp = int(np.sum((y_true == 1) & (y_pred == 1)))
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))

    total = max(len(y_true), 1)
    accuracy = (tp + tn) / total
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        'accuracy': round(accuracy * 100, 2),
        'precision': round(precision * 100, 2),
        'recall': round(recall * 100, 2),
        'f1_score': round(f1 * 100, 2),
        'confusion_matrix': {
            'tp': tp,
            'tn': tn,
            'fp': fp,
            'fn': fn
        }
    }
