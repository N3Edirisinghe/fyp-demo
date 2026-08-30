# System Architecture

## Overview

```
                        ┌─────────────────────────┐
                        │   Participant (Streamlit)│
                        │   voice / text input      │
                        └────────────┬─────────────┘
                                     │
                     ┌───────────────┼────────────────┐
                     ▼                                 ▼
        ┌────────────────────────┐          ┌───────────────────────┐
        │  ASR (Groq Whisper)     │          │  Raw audio (transient)│
        │  audio -> transcript    │          └───────────────────────┘
        └───────────┬─────────────┘
                     │
        ┌────────────┴─────────────┐
        ▼                           ▼
┌──────────────────────┐   ┌──────────────────────────┐
│ Voice Emotion Model    │   │ Text Emotion Model        │
│ (CNN-LSTM / Wav2Vec2)  │   │ (DistilRoBERTa)           │
│ src/emotion/voice_*.py │   │ src/emotion/text_*.py     │
└──────────┬─────────────┘   └────────────┬──────────────┘
           │                              │
           └───────────────┬──────────────┘
                            ▼
                 ┌────────────────────────┐
                 │ H1 Comparison / Fusion  │
                 │ src/emotion/fusion.py   │
                 └───────────┬─────────────┘
                             │
             ┌───────────────┴────────────────┐
             ▼                                 ▼
 ┌────────────────────────┐        ┌────────────────────────────┐
 │ Vector Memory (Chroma)   │        │ Relational Store (Turso)    │
 │ semantic retrieval        │        │ time-series + survey data   │
 │ src/memory/vector_store  │        │ src/memory/db.py             │
 └────────────┬─────────────┘        └──────────────┬───────────────┘
              │                                       │
              └───────────────┬───────────────────────┘
                               ▼
                  ┌─────────────────────────┐
                  │ Emotional Profiling       │
                  │ src/memory/profiling.py   │
                  └────────────┬──────────────┘
                               ▼
                  ┌─────────────────────────┐
                  │ LLM Response Generation   │
                  │ (Groq / Gemini)           │
                  │ src/llm/response_gen.py   │
                  └────────────┬──────────────┘
                               ▼
                  ┌─────────────────────────┐
                  │ Text-to-Speech (Edge-TTS) │
                  │ src/tts/text_to_speech.py │
                  └────────────┬──────────────┘
                               ▼
                    Response delivered to participant
```

## Experimental Conditions

| Condition | Emotion detection | Memory | LLM prompt | Used for |
|---|---|---|---|---|
| `no_memory` (Session 1) | Yes (both voice + text, for H1) | No | Emotion-aware, no memory context | H1, H2 baseline |
| `memory_enabled` (Session 2) | Yes | Yes | Emotion-aware + retrieved memory | H2 post, H3 integrated |
| `baseline` (Session 3) | No | No | Plain, same LLM | H3 control |

## Hosting Map (all free tier)

| Component | Service |
|---|---|
| App (frontend + backend) | Streamlit Community Cloud |
| Relational DB | Turso |
| Vector DB | Chroma Cloud |
| ASR | Groq (hosted Whisper) |
| TTS | Edge-TTS (runs in-process, no external host) |
| LLM | Groq (Llama) or Gemini |
| Model training | Google Colab |
| Model inference | Runs inside the Streamlit app process (CPU) |

See `docs/deployment_guide.md` for step-by-step deployment instructions.
