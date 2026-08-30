"""
Downloads/organizes RAVDESS and TESS into a unified structure with a common
6-class label set (happy, sad, angry, fear, neutral, surprise), matching
Section 5.1 of the proposal. RAVDESS/TESS have slightly different native
label sets (e.g. RAVDESS includes 'calm' and 'disgust') — this script maps
both onto the shared 6-class scheme and drops classes with no equivalent,
noting the mapping decision in the output manifest for the methodology
write-up.

Usage:
    python training/scripts/prepare_ravdess_tess.py \
        --ravdess_dir training/data/ravdess_raw \
        --tess_dir training/data/tess_raw \
        --output_dir training/data/processed
"""

import argparse
import csv
import os

# RAVDESS filename emotion code -> our unified 6-class label.
# RAVDESS 'calm' has no direct equivalent -> mapped to 'neutral'.
# RAVDESS 'disgust' has no equivalent in our 6-class scheme -> excluded.
RAVDESS_EMOTION_MAP = {
    "01": "neutral",
    "02": "neutral",  # calm -> neutral
    "03": "happy",
    "04": "sad",
    "05": "angry",
    "06": "fear",
    "07": None,  # disgust -> excluded
    "08": "surprise",
}

# TESS folder names typically encode emotion directly, e.g. "OAF_happy"
TESS_EMOTION_MAP = {
    "happy": "happy",
    "sad": "sad",
    "angry": "angry",
    "fear": "fear",
    "neutral": "neutral",
    "surprise": "surprise",  # sometimes named "ps" (pleasant surprise) in TESS
    "ps": "surprise",
    "disgust": None,
}


def parse_ravdess(ravdess_dir: str) -> list[tuple[str, str]]:
    entries = []
    for root, _, files in os.walk(ravdess_dir):
        for fname in files:
            if not fname.endswith(".wav"):
                continue
            parts = fname.split("-")
            if len(parts) < 3:
                continue
            emotion_code = parts[2]
            label = RAVDESS_EMOTION_MAP.get(emotion_code)
            if label:
                entries.append((os.path.join(root, fname), label))
    return entries


def parse_tess(tess_dir: str) -> list[tuple[str, str]]:
    entries = []
    for root, _, files in os.walk(tess_dir):
        folder_name = os.path.basename(root).lower()
        matched_label = None
        for key, label in TESS_EMOTION_MAP.items():
            if key in folder_name:
                matched_label = label
                break
        if matched_label is None:
            continue
        for fname in files:
            if fname.endswith(".wav"):
                entries.append((os.path.join(root, fname), matched_label))
    return entries


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ravdess_dir", default="training/data/ravdess_raw")
    parser.add_argument("--tess_dir", default="training/data/tess_raw")
    parser.add_argument("--output_dir", default="training/data/processed")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    manifest_path = os.path.join(args.output_dir, "manifest.csv")

    entries = []
    if os.path.isdir(args.ravdess_dir):
        entries += parse_ravdess(args.ravdess_dir)
    if os.path.isdir(args.tess_dir):
        entries += parse_tess(args.tess_dir)

    with open(manifest_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["filepath", "label", "source"])
        for filepath, label in entries:
            source = "ravdess" if "ravdess" in filepath.lower() else "tess"
            writer.writerow([filepath, label, source])

    print(f"Wrote {len(entries)} labeled entries to {manifest_path}")


if __name__ == "__main__":
    main()
