# agents/sentiment_analyzer.py
from transformers import pipeline
from pydantic import BaseModel
from typing import Literal


class SentimentResult(BaseModel):
    label: Literal["POSITIVE", "NEGATIVE", "NEUTRAL"]
    score: float


class SentimentAnalyzer:
    def __init__(self):
        # Remove leading underscore from field name
        self.analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )

    def analyze(self, text: str) -> SentimentResult:
        if not text.strip():
            return {"label": "NEUTRAL", "score": 0.5}

        result = self.analyzer(text)[0]
        return {
            "label": result["label"],
            "score": result["score"]
        }