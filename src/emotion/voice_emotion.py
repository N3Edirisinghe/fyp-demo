"""
Voice-based emotion recognition (H1 — primary architecture).

Extracts MFCC/pitch/energy features with Librosa and classifies emotion
using a CNN-LSTM model trained on RAVDESS + TESS (see training/notebooks/).
A fine-tuned Wav2Vec2 model is used as the comparison architecture — see
`Wav2Vec2VoiceEmotionClassifier` below.

Both classifiers return the same output shape so they can be benchmarked
against each other and against the text-only classifier on identical
evaluation data, per Section 5.1 / 5.5 of the research proposal.
"""

from dataclasses import dataclass

import librosa
import numpy as np
import torch

from config.settings import settings


@dataclass
class EmotionPrediction:
    label: str
    confidence: float
    all_scores: dict[str, float]


def extract_audio_features(audio_path: str, sr: int = 22050) -> np.ndarray:
    """
    Extract MFCC, pitch, and energy features from an audio file, matching
    the preprocessing described in Section 5.1 of the proposal.
    """
    y, sr = librosa.load(audio_path, sr=sr)

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    mfcc_mean = np.mean(mfcc.T, axis=0)

    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_mean = np.mean(pitches[pitches > 0]) if np.any(pitches > 0) else 0.0

    energy = np.mean(librosa.feature.rms(y=y))

    return np.concatenate([mfcc_mean, [pitch_mean, energy]])


class CNNLSTMVoiceEmotionClassifier:
    """Primary voice emotion model (Section 5.1)."""

    def __init__(self, model_path: str = settings.voice_emotion_model_path):
        self.model_path = model_path
        self.labels = settings.emotion_labels
        self.model = self._load_model()

    def _load_model(self):
        try:
            model = torch.load(self.model_path, map_location="cpu")
            model.eval()
            return model
        except FileNotFoundError:
            print(
                f"[VoiceEmotion] No trained model found at {self.model_path}. "
                "Train it first using training/notebooks/train_voice_emotion_cnn_lstm.ipynb"
            )
            return None

    def predict(self, audio_path: str) -> EmotionPrediction:
        if self.model is None:
            raise RuntimeError("Voice emotion model not loaded — train it first.")

        features = extract_audio_features(audio_path)
        tensor_input = torch.tensor(features, dtype=torch.float32).unsqueeze(0)

        with torch.no_grad():
            logits = self.model(tensor_input)
            probs = torch.softmax(logits, dim=-1).squeeze().tolist()

        scores = dict(zip(self.labels, probs, strict=False))
        top_label = max(scores, key=scores.get)
        return EmotionPrediction(label=top_label, confidence=scores[top_label], all_scores=scores)


class Wav2Vec2VoiceEmotionClassifier:
    """Comparison architecture (Section 5.1) — fine-tuned Wav2Vec2."""

    def __init__(self, model_path: str = settings.wav2vec2_model_path):
        from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2ForSequenceClassification

        self.labels = settings.emotion_labels
        try:
            self.extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_path)
            self.model = Wav2Vec2ForSequenceClassification.from_pretrained(model_path)
            self.model.eval()
        except OSError:
            print(
                f"[VoiceEmotion] No fine-tuned Wav2Vec2 model found at {model_path}. "
                "Train it first using training/notebooks/train_voice_emotion_wav2vec2.ipynb"
            )
            self.extractor = None
            self.model = None

    def predict(self, audio_path: str) -> EmotionPrediction:
        if self.model is None:
            raise RuntimeError("Wav2Vec2 model not loaded — train it first.")

        y, sr = librosa.load(audio_path, sr=16000)
        inputs = self.extractor(y, sampling_rate=sr, return_tensors="pt")

        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = torch.softmax(logits, dim=-1).squeeze().tolist()

        scores = dict(zip(self.labels, probs, strict=False))
        top_label = max(scores, key=scores.get)
        return EmotionPrediction(label=top_label, confidence=scores[top_label], all_scores=scores)
