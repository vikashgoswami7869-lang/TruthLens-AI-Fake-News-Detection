"""
TruthLens AI - NLP Preprocessing & Feature Extraction Engine
Natural Language Processing pipeline for textual credibility assessment.
"""

import re
import math
from collections import Counter
import numpy as np

# Standard English stopwords
DEFAULT_STOPWORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'aren\'t',
    'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by',
    'can\'t', 'cannot', 'could', 'couldn\'t', 'did', 'didn\'t', 'do', 'does', 'doesn\'t', 'doing', 'don\'t',
    'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'hadn\'t', 'has', 'hasn\'t', 'have',
    'haven\'t', 'having', 'he', 'he\'d', 'he\'ll', 'he\'s', 'her', 'here', 'here\'s', 'hers', 'herself',
    'him', 'himself', 'his', 'how', 'how\'s', 'i', 'i\'d', 'i\'ll', 'i\'m', 'i\'ve', 'if', 'in', 'into',
    'is', 'isn\'t', 'it', 'it\'s', 'its', 'itself', 'let\'s', 'me', 'more', 'most', 'mustn\'t', 'my',
    'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our',
    'ours', 'ourselves', 'out', 'over', 'own', 'same', 'shan\'t', 'she', 'she\'d', 'she\'ll', 'she\'s',
    'should', 'shouldn\'t', 'so', 'some', 'such', 'than', 'that', 'that\'s', 'the', 'their', 'theirs',
    'them', 'themselves', 'then', 'there', 'there\'s', 'these', 'they', 'they\'d', 'they\'ll', 'they\'re',
    'they\'ve', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'wasn\'t',
    'we', 'we\'d', 'we\'ll', 'we\'re', 'we\'ve', 'were', 'weren\'t', 'what', 'what\'s', 'when', 'when\'s',
    'where', 'where\'s', 'which', 'while', 'who', 'who\'s', 'whom', 'why', 'why\'s', 'with', 'won\'t',
    'would', 'wouldn\'t', 'you', 'you\'d', 'you\'ll', 'you\'re', 'you\'ve', 'your', 'yours', 'yourself',
    'yourselves'
}

# Clickbait & sensationalism keywords
SENSATIONAL_KEYWORDS = {
    'shocking', 'unbelievable', 'miracle', 'secret', 'banned', 'exposed', 'illuminati',
    'proof', 'cure', 'hidden', 'scandal', 'mind-blowing', 'warning', 'urgent',
    'conspiracy', 'magic', 'disaster', 'hoax', 'alien', 'ufo', 'deepstate', 'classified',
    'bombshell', 'breaking', 'omg', 'must see', 'they don\'t want you to know',
    'censored', 'terrified', 'destroy', 'freemason', 'truth revealed', 'viral alert'
}

# Credibility and objective journalistic attribution markers
CREDIBLE_MARKERS = {
    'according to', 'spokesperson', 'official', 'statement', 'published', 'researchers',
    'peer-reviewed', 'university', 'clinical trial', 'bureau', 'confirmed', 'department',
    'consortium', 'authorized', 'organization', 'reported', 'investigation', 'reuters',
    'associated press', 'statistics', 'documented', 'ministry', 'authorities'
}


class TextPreprocessor:
    """
    Handles text cleaning, tokenization, stopword removal,
    and advanced linguistic heuristics.
    """
    def __init__(self, stopwords=None):
        self.stopwords = stopwords if stopwords is not None else DEFAULT_STOPWORDS

    def clean_text(self, text: str) -> str:
        """Cleans input text: removes URLs, HTML tags, special chars."""
        if not text or not isinstance(text, str):
            return ""
        text = re.sub(r'http\S+|www\.\S+', ' ', text)
        text = re.sub(r'<.*?>', ' ', text)
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        text = text.lower()
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def tokenize(self, text: str, remove_stopwords: bool = True, ngram_range: tuple = (1, 2)) -> list:
        cleaned = self.clean_text(text)
        tokens = cleaned.split()
        if remove_stopwords:
            tokens = [t for t in tokens if t not in self.stopwords and len(t) > 2]

        all_tokens = list(tokens)
        min_n, max_n = ngram_range
        if max_n >= 2 and len(tokens) >= 2:
            bigrams = [f"{tokens[i]}_{tokens[i+1]}" for i in range(len(tokens) - 1)]
            all_tokens.extend(bigrams)

        return all_tokens

    def extract_linguistic_features(self, raw_text: str) -> dict:
        """
        Extracts deep linguistic markers:
        - Emotional/Sensationalism index
        - Objective credibility markers
        - Case shouting ratio
        - Punctuation urgency
        """
        if not raw_text:
            return {
                'length': 0,
                'word_count': 0,
                'caps_ratio': 0.0,
                'exclamation_count': 0,
                'question_count': 0,
                'sensational_hits': [],
                'credible_hits': [],
                'sensational_score': 0.0,
                'clickbait_risk': 'Low',
                'tone': 'Neutral'
            }

        length = len(raw_text)
        words = raw_text.split()
        word_count = len(words)
        caps_count = sum(1 for c in raw_text if c.isupper())
        caps_ratio = round((caps_count / max(length, 1)) * 100, 2)
        exclamation_count = raw_text.count('!')
        question_count = raw_text.count('?')

        lower_text = raw_text.lower()
        sensational_hits = [k for k in SENSATIONAL_KEYWORDS if k in lower_text]
        credible_hits = [k for k in CREDIBLE_MARKERS if k in lower_text]

        # Calculate Sensationalism Score (0 - 100)
        sensational_score = (len(sensational_hits) * 22.0) + (exclamation_count * 12.0) + (caps_ratio * 0.6)
        sensational_score = round(min(100.0, max(0.0, sensational_score)), 1)

        # Tone estimation
        if sensational_score >= 60:
            clickbait_risk = "High"
            tone = "Alarmist / Clickbait"
        elif sensational_score >= 25:
            clickbait_risk = "Moderate"
            tone = "Sensational"
        else:
            clickbait_risk = "Low"
            tone = "Objective / Formal" if len(credible_hits) > 0 else "Neutral"

        return {
            'length': length,
            'word_count': word_count,
            'caps_ratio': caps_ratio,
            'exclamation_count': exclamation_count,
            'question_count': question_count,
            'sensational_hits': sensational_hits,
            'credible_hits': credible_hits,
            'sensational_score': sensational_score,
            'clickbait_risk': clickbait_risk,
            'tone': tone
        }


class TfidfVectorizerModel:
    """
    Pure NumPy implementation of TF-IDF Vectorizer with smooth IDF & L2 normalization.
    """
    def __init__(self, max_features: int = 5000, ngram_range: tuple = (1, 2)):
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.preprocessor = TextPreprocessor()
        self.vocabulary = {}
        self.idf_ = None
        self.feature_names = []

    def fit(self, raw_documents: list):
        doc_count = len(raw_documents)
        df_counter = Counter()

        for doc in raw_documents:
            tokens = self.preprocessor.tokenize(doc, ngram_range=self.ngram_range)
            unique_terms = set(tokens)
            for term in unique_terms:
                df_counter[term] += 1

        most_common = df_counter.most_common(self.max_features)
        self.vocabulary = {term: idx for idx, (term, _) in enumerate(most_common)}
        self.feature_names = [term for term, _ in most_common]

        num_features = len(self.feature_names)
        self.idf_ = np.zeros(num_features, dtype=np.float64)
        for term, idx in self.vocabulary.items():
            df = df_counter[term]
            self.idf_[idx] = math.log((1.0 + doc_count) / (1.0 + df)) + 1.0

        return self

    def transform(self, raw_documents: list) -> np.ndarray:
        num_docs = len(raw_documents)
        num_features = len(self.vocabulary)
        matrix = np.zeros((num_docs, num_features), dtype=np.float64)

        for doc_idx, doc in enumerate(raw_documents):
            tokens = self.preprocessor.tokenize(doc, ngram_range=self.ngram_range)
            term_counts = Counter(tokens)
            doc_len = len(tokens)
            if doc_len == 0:
                continue

            for term, count in term_counts.items():
                if term in self.vocabulary:
                    term_idx = self.vocabulary[term]
                    tf = 1.0 + math.log(count)
                    matrix[doc_idx, term_idx] = tf * self.idf_[term_idx]

            norm = np.linalg.norm(matrix[doc_idx])
            if norm > 0:
                matrix[doc_idx] /= norm

        return matrix

    def fit_transform(self, raw_documents: list) -> np.ndarray:
        return self.fit(raw_documents).transform(raw_documents)
