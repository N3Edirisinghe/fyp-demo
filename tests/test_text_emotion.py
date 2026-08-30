"""
Tests for text emotion module error handling. Full prediction tests require
a trained model checkpoint and are intended to run after Phase 2 training
(see training/notebooks/train_text_emotion_distilroberta.ipynb).
"""

import pytest

from src.emotion.text_emotion import TextEmotionClassifier


def test_classifier_raises_when_model_missing():
    classifier = TextEmotionClassifier(model_path="models/text_emotion/does_not_exist_yet")
    assert classifier.model is None

    with pytest.raises(RuntimeError):
        classifier.predict("I feel great today")
