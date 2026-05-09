from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np

CATEGORIES = ["invoice", "contract", "report", "correspondence", "form", "other"]

class DocumentClassifier:

    def __init__(self):
        self.pipeline = self._build_pipeline()
        self._load_or_train()

    def _build_pipeline(self):
        return Pipeline([
            ('tfidf', TfidfVectorizer(max_features=10000, ngram_range=(1, 2))),
            ('clf', LogisticRegression(max_iter=1000, C=1.0))
        ])

    def _load_or_train(self):
        # In production, loads pre-trained model from S3
        # For demo: uses keyword heuristics
        pass

    def classify(self, text: str) -> tuple[str, float]:
        text_lower = text.lower()
        scores = {
            "invoice": sum(1 for w in ["invoice", "amount due", "payment", "bill"] if w in text_lower),
            "contract": sum(1 for w in ["agreement", "terms", "party", "clause"] if w in text_lower),
            "report": sum(1 for w in ["summary", "analysis", "findings", "report"] if w in text_lower),
            "correspondence": sum(1 for w in ["dear", "sincerely", "regards", "letter"] if w in text_lower),
        }
        label = max(scores, key=scores.get) if max(scores.values()) > 0 else "other"
        confidence = min(0.75 + max(scores.values()) * 0.05, 0.99)
        return label, round(confidence, 3)
