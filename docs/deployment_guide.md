# Deployment Guide (Free Tier)

## 1. Train the models first (Google Colab)

1. Open each notebook in `training/notebooks/` in Google Colab (free T4 GPU runtime).
2. Upload RAVDESS + TESS to Colab or mount from Google Drive.
3. Run `training/scripts/prepare_ravdess_tess.py` locally or in Colab to build `manifest.csv`.
4. Train all three models (CNN-LSTM, Wav2Vec2, DistilRoBERTa).
5. Download the resulting weights into your local `models/voice_emotion/` and `models/text_emotion/` folders.
6. Run `training/scripts/evaluate_h1_classifiers.py` to get your H1 accuracy/F1 numbers before deploying anything.

## 2. Set up free-tier hosted storage

### Turso (relational DB)
1. Sign up at https://turso.tech (free tier).
2. Create a database: `turso db create emotion-companion-db`
3. Get the connection URL and auth token: `turso db show emotion-companion-db --url` / `turso db tokens create emotion-companion-db`
4. Add these to your `.env` as `TURSO_DATABASE_URL` and `TURSO_AUTH_TOKEN`.
5. Run the schema in `data/schema/database_schema.sql` against your Turso DB once, using the Turso CLI or `libsql-client`.

### Chroma Cloud (vector DB)
1. Sign up at https://www.trychroma.com/cloud (free tier).
2. Create a database and get your API key, tenant ID.
3. Add these to your `.env` as `CHROMA_API_KEY`, `CHROMA_TENANT`, `CHROMA_DATABASE`.

### Groq (ASR + LLM)
1. Sign up at https://console.groq.com (free tier).
2. Generate an API key, add to `.env` as `GROQ_API_KEY`.

### (Optional) Gemini as an LLM alternative
1. Get a free API key at https://aistudio.google.com.
2. Add to `.env` as `GEMINI_API_KEY`, and set `LLM_PROVIDER=gemini`.

## 3. Deploy the Streamlit app

1. Push this repository to GitHub (make sure `.env`, `models/*` weights, and `data/raw|processed` are excluded per `.gitignore` — commit model weights via Git LFS or host them externally if needed, since GitHub has file size limits).
2. Go to https://share.streamlit.io and connect your GitHub repo.
3. Set the main file path to `src/app.py`.
4. In the app's "Secrets" settings (equivalent to `.streamlit/secrets.toml`), paste in all the same key/value pairs from your `.env` file, plus `ADMIN_PASSWORD` for the dashboard.
5. Deploy. Streamlit Cloud will install `requirements.txt` automatically.

## 4. Handling model weights on a free host

Trained model weights (especially Wav2Vec2 and DistilRoBERTa fine-tunes)
can be large. Options for free hosting of weights:
- Push small models (CNN-LSTM, a few MB) directly via Git LFS (GitHub free tier includes some LFS storage).
- Host larger HuggingFace-format models (Wav2Vec2, DistilRoBERTa) on the **HuggingFace Hub** (free, unlimited public model hosting) and load them directly with `from_pretrained("your-username/model-name")` instead of a local path.

## 5. Known free-tier limitations to plan around

- Streamlit Community Cloud apps sleep after inactivity — the first request after sleep takes ~30-50 seconds. Brief participants about this before a scheduled session, or "wake" the app a few minutes early.
- Groq's free tier has rate limits — space out concurrent participant sessions if running multiple at once.
- Turso and Chroma Cloud free tiers have storage/row caps — more than sufficient for a 20-participant study, but do not use this stack for a production consumer app without upgrading.

## 6. Pre-launch checklist

- [ ] Ethics approval obtained
- [ ] Consent form distributed and signed
- [ ] Pilot test completed with 2-3 non-study participants
- [ ] All models trained and evaluated (H1 baseline numbers in hand)
- [ ] Admin password set in Streamlit secrets
- [ ] `STORE_RAW_AUDIO=false` confirmed unless ethics approval explicitly covers audio retention
