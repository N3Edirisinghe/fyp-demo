"""
Evaluates and directly compares the voice-based and text-only emotion
classifiers on the same held-out test set, producing the Accuracy,
Precision, Recall, and F1-score figures required to test H1 (Section 5.5).

Usage:
    python training/scripts/evaluate_h1_classifiers.py \
        --manifest training/data/processed/manifest.csv \
        --transcripts training/data/processed/transcripts.csv

`transcripts.csv` should map each audio filepath to its ASR transcript
(generate this once with src/asr/speech_to_text.py over the manifest, so
the text classifier sees the same real ASR output the live system would
produce — not a hand-typed ground-truth transcript).
"""

import argparse
import csv

from sklearn.metrics import classification_report, accuracy_score

from src.emotion.text_emotion import TextEmotionClassifier
from src.emotion.voice_emotion import CNNLSTMVoiceEmotionClassifier, Wav2Vec2VoiceEmotionClassifier


def load_manifest(path: str) -> list[dict]:
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def load_transcripts(path: str) -> dict[str, str]:
    with open(path, newline="") as f:
        return {row["filepath"]: row["transcript"] for row in csv.DictReader(f)}


def evaluate(manifest_path: str, transcripts_path: str):
    manifest = load_manifest(manifest_path)
    transcripts = load_transcripts(transcripts_path)

    voice_model = CNNLSTMVoiceEmotionClassifier()
    wav2vec2_model = Wav2Vec2VoiceEmotionClassifier()
    text_model = TextEmotionClassifier()

    y_true, y_pred_voice, y_pred_wav2vec2, y_pred_text = [], [], [], []

    for row in manifest:
        filepath, true_label = row["filepath"], row["label"]
        transcript = transcripts.get(filepath)
        if not transcript:
            continue

        y_true.append(true_label)
        y_pred_voice.append(voice_model.predict(filepath).label)
        y_pred_wav2vec2.append(wav2vec2_model.predict(filepath).label)
        y_pred_text.append(text_model.predict(transcript).label)

    print("\n=== CNN-LSTM (voice) vs. ground truth ===")
    print(f"Accuracy: {accuracy_score(y_true, y_pred_voice):.4f}")
    print(classification_report(y_true, y_pred_voice))

    print("\n=== Wav2Vec2 (voice) vs. ground truth ===")
    print(f"Accuracy: {accuracy_score(y_true, y_pred_wav2vec2):.4f}")
    print(classification_report(y_true, y_pred_wav2vec2))

    print("\n=== DistilRoBERTa (text-only) vs. ground truth ===")
    print(f"Accuracy: {accuracy_score(y_true, y_pred_text):.4f}")
    print(classification_report(y_true, y_pred_text))

    print(
        "\nH1 comparison: use the accuracy/F1 figures above in a paired "
        "significance test (paired t-test or Wilcoxon, per Section 5.5) "
        "between the best voice model and the text-only model."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="training/data/processed/manifest.csv")
    parser.add_argument("--transcripts", default="training/data/processed/transcripts.csv")
    args = parser.parse_args()
    evaluate(args.manifest, args.transcripts)
