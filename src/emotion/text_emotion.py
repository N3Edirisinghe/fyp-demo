"""
Text-based emotion recognition (H1 — comparison baseline).

Uses a fine-tuned DistilRoBERTa classifier on the transcribed ASR output,
evaluated on the same test set as the voice-based classifiers so that
H1's accuracy/precision/recall/F1 comparison is fair (Section 5.1, 5.5).
"""

from dataclasses import dataclass

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from config.settings import settings


@dataclass
class EmotionPrediction:
    label: str
    confidence: float
    all_scores: dict[str, float]


class TextEmotionClassifier:
    def __init__(self, model_path: str = settings.text_emotion_model_path):
        self.labels = settings.emotion_labels
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
            self.model.eval()
        except OSError:
            print(
                f"[TextEmotion] No fine-tuned model found at {model_path}. "
                "Train it first using training/notebooks/train_text_emotion_distilroberta.ipynb"
            )
            self.tokenizer = None
            self.model = None

    def predict(self, text: str) -> EmotionPrediction:
        if self.model is None:
            raise RuntimeError("Text emotion model not loaded — train it first.")

        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)

        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = torch.softmax(logits, dim=-1).squeeze().tolist()

        scores = dict(zip(self.labels, probs, strict=False))
        top_label = max(scores, key=scores.get)
        return EmotionPrediction(label=top_label, confidence=scores[top_label], all_scores=scores)
