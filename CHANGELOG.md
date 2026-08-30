# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and versioning follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Planned
- H1 model training and evaluation results
- H2 memory pipeline end-to-end test with real ASR
- Streamlit Cloud deployment
- Pilot test with 2–3 non-study participants

## [0.1.0] — 2026-08-26

### Added
- Initial project scaffold: `src/` modules for ASR, TTS, voice/text emotion
  classification, memory (relational + vector), LLM response generation,
  and experimental conditions (baseline / memory-enabled).
- Streamlit UI: Session 1 (H1 + H2 baseline), Session 2 (H2 post + H3
  integrated), Session 3 (H3 baseline), and an Admin Dashboard.
- Training notebooks (Colab-ready) for CNN-LSTM, Wav2Vec2, and
  DistilRoBERTa, plus a RAVDESS/TESS dataset preparation script and an
  H1 evaluation script.
- Documentation: system architecture, deployment guide, ethics/consent
  template, and a research-proposal-to-code traceability document.
- Survey instrument templates for H2 and H3.
- Starter unit test suite.
- Free-tier deployment target: Streamlit Community Cloud, Turso, Chroma
  Cloud, Groq, Edge-TTS.
