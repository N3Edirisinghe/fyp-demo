"""
Unit tests for the voice emotion module. These test feature extraction and
prediction-object shape, not model accuracy (accuracy is evaluated
separately and offline via training/scripts/evaluate_h1_classifiers.py).
"""

import numpy as np

from src.emotion.voice_emotion import extract_audio_features


def test_extract_audio_features_shape(tmp_path):
    import soundfile as sf

    # Generate a short synthetic sine wave as a stand-in test audio file.
    sr = 22050
    duration = 1.0
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    audio = 0.5 * np.sin(2 * np.pi * 440 * t)

    audio_path = tmp_path / "test_tone.wav"
    sf.write(audio_path, audio, sr)

    features = extract_audio_features(str(audio_path))

    # 40 MFCC coefficients + pitch + energy = 42 features
    assert features.shape[0] == 42
    assert not np.isnan(features).any()
