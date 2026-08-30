"""
Centralized application configuration.

All environment-dependent values are loaded here via pydantic-settings so the
rest of the codebase never reads os.environ directly. This keeps secrets and
config in one auditable place, which matters for research-ethics review.
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


# Project root:
# emotion-ai-companion-research/
PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- LLM / ASR ---
    groq_api_key: str = ""
    gemini_api_key: str = ""
    llm_provider: str = "groq"

    # --- Relational DB (Turso) ---
    turso_database_url: str = ""
    turso_auth_token: str = ""
    local_db_path: str = "data/processed/research.db"

    # --- Vector DB (Chroma) ---
    chroma_api_key: str = ""
    chroma_tenant: str = ""
    chroma_database: str = "emotion-companion-memory"
    local_chroma_path: str = "data/processed/chroma_db"

    # --- App ---
    app_env: str = "development"
    log_level: str = "INFO"
    store_raw_audio: bool = False

    # --- Emotion model paths ---
    voice_emotion_model_path: str = "models/voice_emotion/cnn_lstm.pt"
    wav2vec2_model_path: str = "models/voice_emotion/wav2vec2_finetuned"
    text_emotion_model_path: str = "models/text_emotion/distilroberta_finetuned"

    # --- Emotion label set ---
    emotion_labels: list[str] = [
        "happy",
        "sad",
        "angry",
        "fear",
        "neutral",
        "surprise",
    ]


settings = Settings()