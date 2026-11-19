"""
TruthLens AI - Model Training & Evaluation Engine
Trains Logistic Regression & Naive Bayes classifiers on TF-IDF feature space.
"""

import csv
import pickle
import random
from pathlib import Path
import numpy as np

from nlp_pipeline import TfidfVectorizerModel, TextPreprocessor
from ml_models import MultinomialNaiveBayes, LogisticRegressionClassifier, compute_metrics

BASE_DIR = Path(__file__).parent
DATASET_PATH = BASE_DIR / "dataset" / "news_dataset.csv"
MODEL_BUNDLE_PATH = BASE_DIR / "model_bundle.pkl"


def load_dataset(filepath):
    texts = []
    labels = []  # 0: Fake, 1: Real
    with open(filepath, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            texts.append(row['text'])
            labels.append(1 if row['label'].strip().lower() == 'real' else 0)
    return texts, np.array(labels, dtype=int)


def train_test_split(texts, labels, test_ratio=0.2, seed=42):
    random.seed(seed)
    np.random.seed(seed)
    indices = list(range(len(texts)))
    random.shuffle(indices)

    split_idx = int(len(texts) * (1 - test_ratio))
    train_idx = indices[:split_idx]
    test_idx = indices[split_idx:]

    train_texts = [texts[i] for i in train_idx]
    test_texts = [texts[i] for i in test_idx]
    y_train = labels[train_idx]
    y_test = labels[test_idx]

    return train_texts, test_texts, y_train, y_test


def train_models():
    print("=" * 65)
    print("TRUTHLENS AI - MODEL TRAINING & VALIDATION PIPELINE")
    print("=" * 65)

    texts, labels = load_dataset(DATASET_PATH)
    fake_count = int(np.sum(labels == 0))
    real_count = int(np.sum(labels == 1))
    print(f"\n[1/5] Loaded dataset: {len(texts)} samples (Real: {real_count}, Fake: {fake_count})")

    print("[2/5] Partitioning Train (80%) and Test (20%) splits...")
    train_texts, test_texts, y_train, y_test = train_test_split(texts, labels, test_ratio=0.2, seed=42)
    print(f"Training samples: {len(train_texts)}, Testing samples: {len(test_texts)}")

    print("[3/5] Computing TF-IDF feature matrices (n-grams 1-2, sublinear TF)...")
    vectorizer = TfidfVectorizerModel(max_features=3000, ngram_range=(1, 2))
    X_train = vectorizer.fit_transform(train_texts)
    X_test = vectorizer.transform(test_texts)
    print(f"Vocabulary capacity: {len(vectorizer.vocabulary)} n-gram features")

    print("[4/5] Training ML Models...")
    # Model 1: Naive Bayes
    nb_model = MultinomialNaiveBayes(alpha=1.0)
    nb_model.fit(X_train, y_train)
    nb_preds = nb_model.predict(X_test)
    nb_metrics = compute_metrics(y_test, nb_preds)

    # Model 2: Logistic Regression (L2)
    lr_model = LogisticRegressionClassifier(lr=0.8, l2_reg=0.0005, epochs=350, momentum=0.85)
    lr_model.fit(X_train, y_train)
    lr_preds = lr_model.predict(X_test)
    lr_metrics = compute_metrics(y_test, lr_preds)

    print("\n[5/5] BENCHMARK EVALUATION RESULTS:")
    print("-" * 65)
    print(f"{'Metric':<25} | {'Multinomial Naive Bayes':<18} | {'Logistic Regression':<18}")
    print("-" * 65)
    print(f"{'Accuracy':<25} | {nb_metrics['accuracy']:>6.2f}%            | {lr_metrics['accuracy']:>6.2f}%")
    print(f"{'Precision':<25} | {nb_metrics['precision']:>6.2f}%            | {lr_metrics['precision']:>6.2f}%")
    print(f"{'Recall':<25} | {nb_metrics['recall']:>6.2f}%            | {lr_metrics['recall']:>6.2f}%")
    print(f"{'F1-Score':<25} | {nb_metrics['f1_score']:>6.2f}%            | {lr_metrics['f1_score']:>6.2f}%")
    print("-" * 65)
    print(f"Confusion Matrix (NB): TP={nb_metrics['confusion_matrix']['tp']}, TN={nb_metrics['confusion_matrix']['tn']}, FP={nb_metrics['confusion_matrix']['fp']}, FN={nb_metrics['confusion_matrix']['fn']}")
    print(f"Confusion Matrix (LR): TP={lr_metrics['confusion_matrix']['tp']}, TN={lr_metrics['confusion_matrix']['tn']}, FP={lr_metrics['confusion_matrix']['fp']}, FN={lr_metrics['confusion_matrix']['fn']}")
    print("-" * 65)

    bundle = {
        'vectorizer': vectorizer,
        'nb_model': nb_model,
        'lr_model': lr_model,
        'metrics': {
            'naive_bayes': nb_metrics,
            'logistic_regression': lr_metrics
        },
        'active_model': 'logistic_regression',
        'train_samples': len(train_texts),
        'test_samples': len(test_texts),
        'total_features': len(vectorizer.vocabulary)
    }

    with open(MODEL_BUNDLE_PATH, 'wb') as f:
        pickle.dump(bundle, f)

    print(f"\nModel bundle saved to: {MODEL_BUNDLE_PATH}")
    return bundle


if __name__ == "__main__":
    train_models()
