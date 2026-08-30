"""
Runs voice and text emotion classifiers side by side on the same utterance
and records both outputs plus (during the study) the user's self-reported
ground-truth label, so H1 accuracy/precision/recall/F1 can be computed later.

This module does NOT decide which prediction is "correct" — that judgment
comes only from the participant's self-label or the RAVDESS/TESS ground
truth during offline evaluation (see training/scripts/evaluate_h1_classifiers.py).
"""

from dataclasses import asdict, dataclass

from src.emotion.text_emotion import TextEmotionClassifier
from src.emotion.voice_emotion import CNNLSTMVoiceEmotionClassifier


@dataclass
class H1ComparisonResult:
    transcript: str
    voice_label: str
    voice_confidence: float
    text_label: str
    text_confidence: float
    agreement: bool


class EmotionComparisonPipeline:
    def __init__(self):
        self.voice_classifier = CNNLSTMVoiceEmotionClassifier()
        self.text_classifier = TextEmotionClassifier()

    def analyze(self, audio_path: str, transcript: str) -> H1ComparisonResult:
        voice_pred = self.voice_classifier.predict(audio_path)
        text_pred = self.text_classifier.predict(transcript)

        return H1ComparisonResult(
            transcript=transcript,
            voice_label=voice_pred.label,
            voice_confidence=voice_pred.confidence,
            text_label=text_pred.label,
            text_confidence=text_pred.confidence,
            agreement=voice_pred.label == text_pred.label,
        )

    def analyze_as_dict(self, audio_path: str, transcript: str) -> dict:
        return asdict(self.analyze(audio_path, transcript))
