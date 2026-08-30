# Emotionally Adaptive AI Companion — Research Platform

Research platform for the final year project:
**"Designing an Emotionally Adaptive AI Companion Using Voice Emotion Recognition and Long-Term Emotional Memory"**

SLTC Research University — Department of Data Science / Software Engineering

This platform is built to directly test **H1, H2, and H3** as defined in the research proposal, using a
free-tier cloud stack suitable for a controlled study with ~20 participants.

---

## 1. Research Mapping

| Hypothesis | What it tests | Where in this codebase |
|---|---|---|
| **H1** | Voice-based emotion recognition vs. text-only emotion recognition (Accuracy, Precision, Recall, F1) | `src/emotion/voice_emotion.py`, `src/emotion/text_emotion.py`, `training/scripts/evaluate_h1_classifiers.py` |
| **H2** | Structured long-term emotional memory vs. memory-disabled condition (personalization, trust, companionship) | `src/memory/`, `src/conditions/memory_enabled.py` |
| **H3** | Fully integrated system vs. conventional memoryless/text-only baseline (overall satisfaction) | `src/conditions/baseline.py`, `src/conditions/memory_enabled.py`, `src/conditions/session_manager.py` |

See `docs/research_proposal_mapping.md` for the full traceability between proposal sections and code.

## 2. System Architecture

```
User (voice) ──► ASR (Speech-to-Text) ──► Text Emotion Classifier ──┐
      │                                                              ├──► Fusion / Comparison (H1)
      └────────► Voice Emotion Classifier (CNN-LSTM / Wav2Vec2) ────┘
                              │
                              ▼
                  Emotional Memory Store (SQLite/Turso + ChromaDB)
                              │
                              ▼
                   Emotional Profiling Module
                              │
                              ▼
                    LLM Response Generation (Groq / Gemini)
                              │
                              ▼
                  Text-to-Speech (Edge-TTS) ──► User (voice reply)
```

Full diagram and tier descriptions: `docs/system_architecture.md`.

## 3. Tech Stack (100% free-tier)

| Layer | Tool | Hosting |
|---|---|---|
| App (frontend + backend) | Streamlit | Streamlit Community Cloud |
| Relational DB | SQLite (dev) / Turso (prod, persistent) | Turso free tier |
| Vector memory | ChromaDB | Chroma Cloud free tier |
| ASR (speech-to-text) | Whisper via Groq API | Groq free tier |
| TTS (text-to-speech) | Edge-TTS | Runs in-app, no hosting needed |
| LLM (response generation) | Groq (Llama) or Gemini | Free tier |
| Voice emotion model | CNN-LSTM + Wav2Vec2 (fine-tuned) | Trained on Colab, runs in-app (CPU) |
| Text emotion model | DistilRoBERTa (fine-tuned) | Trained on Colab, runs in-app (CPU) |
| Model training | Google Colab (free GPU) | One-time, not hosted |

## 4. Folder Structure

```
emotion-ai-companion-research/
├── config/                # environment & settings management
├── src/
│   ├── app.py             # Streamlit entrypoint
│   ├── asr/                # speech-to-text
│   ├── tts/                # text-to-speech
│   ├── emotion/            # voice + text emotion classifiers (H1)
│   ├── memory/             # SQLite/Turso + ChromaDB memory (H2)
│   ├── llm/                # response generation
│   ├── conditions/         # experimental conditions (baseline / memory-enabled)
│   ├── ui/                 # Streamlit pages per study session
│   └── utils/              # logging, validation helpers
├── models/                 # trained model weights (gitignored)
├── training/                # notebooks + scripts to train/evaluate H1 models
├── data/                    # raw/processed data + DB schema
├── surveys/                 # validated survey instruments for H2/H3
├── docs/                    # architecture, ethics, deployment docs
├── tests/                   # unit tests
└── scripts/                 # setup & run helpers
```

## 5. Quick Start (local development)

```bash
git clone <your-repo-url>
cd emotion-ai-companion-research
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # fill in your API keys
streamlit run src/app.py
```

## 6. Deployment (free)

See `docs/deployment_guide.md` for step-by-step instructions to deploy to Streamlit Community Cloud
with Turso and Chroma Cloud as persistent storage.

## 7. Study Sessions

This platform implements the **within-subject, repeated-measures design** described in the proposal:

| Session | Condition | Hypotheses tested |
|---|---|---|
| Session 1 (Week 1) | Voice input + live emotion self-labeling, no memory | H1 (accuracy vs. self-reported ground truth), H2 baseline |
| Session 2 (Week 2) | System recalls Session 1, full integrated experience | H2 (memory-enabled), H3 (integrated arm) |
| Session 3 (Week 2) | Plain memoryless, text-only chatbot, same LLM | H3 (baseline arm) |

Session flow lives in `src/ui/pages/` (one Streamlit page per session) and is orchestrated by
`src/conditions/session_manager.py`.

## 8. Ethics & Data Handling

All participant data (voice-derived features, transcripts, emotion labels, memory records, survey
responses) is collected only after informed consent and SLTC Ethics Review Committee approval.
See `docs/ethics_consent_template.md`. Raw audio is not persisted by default — only extracted
features and transcripts are stored, to minimize sensitive data retention.

## 9. Contributing & Version Control

This repo follows trunk-based development with short-lived feature
branches, [Conventional Commits](https://www.conventionalcommits.org/),
and [Semantic Versioning](https://semver.org/). CI runs tests and linting
on every push via GitHub Actions.

**Before contributing, read `CONTRIBUTING.md`** — it covers branch naming,
commit format, the PR process, and how to set up pre-commit hooks
(`pip install pre-commit && pre-commit install`).

See `CHANGELOG.md` for the version history.

## 10. License

For academic research use. See `LICENSE`.
