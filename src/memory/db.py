"""
Relational storage for structured interaction records (Section 5.2).

Uses Turso (libSQL, SQLite-compatible) in production for persistence across
Streamlit Community Cloud restarts, falling back to a local SQLite file
during development. Every interaction is stored with: timestamp, participant
id, transcript, detected emotion + confidence, and which experimental
condition/session it belongs to (needed to separate H1/H2/H3 data later).
"""

import sqlite3
from datetime import datetime, timezone

from config.settings import settings

SCHEMA = """
CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    participant_id TEXT NOT NULL,
    session INTEGER NOT NULL,          -- 1, 2, or 3
    condition TEXT NOT NULL,           -- 'baseline' | 'memory_enabled' | 'no_memory'
    timestamp TEXT NOT NULL,
    transcript TEXT,
    voice_emotion_label TEXT,
    voice_emotion_confidence REAL,
    text_emotion_label TEXT,
    text_emotion_confidence REAL,
    self_reported_emotion TEXT,        -- ground truth for H1
    embedding_id TEXT                  -- links to the ChromaDB vector record
);

CREATE TABLE IF NOT EXISTS survey_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    participant_id TEXT NOT NULL,
    session INTEGER NOT NULL,
    hypothesis TEXT NOT NULL,          -- 'H2' | 'H3'
    scale_name TEXT NOT NULL,          -- e.g. 'personalization', 'trust', 'companionship', 'satisfaction'
    item TEXT NOT NULL,
    response INTEGER NOT NULL,         -- 1-5 Likert
    timestamp TEXT NOT NULL
);
"""


def _get_connection() -> sqlite3.Connection:
    """
    Returns a SQLite connection. In production, swap this for a libsql-client
    connection to Turso (see docs/deployment_guide.md) — the schema and
    queries below are libSQL-compatible with no changes needed.
    """
    conn = sqlite3.connect(settings.local_db_path, check_same_thread=False)
    conn.executescript(SCHEMA)
    return conn


def log_interaction(
    participant_id: str,
    session: int,
    condition: str,
    transcript: str,
    voice_emotion_label: str | None = None,
    voice_emotion_confidence: float | None = None,
    text_emotion_label: str | None = None,
    text_emotion_confidence: float | None = None,
    self_reported_emotion: str | None = None,
    embedding_id: str | None = None,
) -> int:
    conn = _get_connection()
    cursor = conn.execute(
        """
        INSERT INTO interactions (
            participant_id, session, condition, timestamp, transcript,
            voice_emotion_label, voice_emotion_confidence,
            text_emotion_label, text_emotion_confidence,
            self_reported_emotion, embedding_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            participant_id,
            session,
            condition,
            datetime.now(timezone.utc).isoformat(),
            transcript,
            voice_emotion_label,
            voice_emotion_confidence,
            text_emotion_label,
            text_emotion_confidence,
            self_reported_emotion,
            embedding_id,
        ),
    )
    conn.commit()
    interaction_id = cursor.lastrowid
    conn.close()
    return interaction_id


def get_participant_history(participant_id: str, session: int | None = None) -> list[dict]:
    conn = _get_connection()
    conn.row_factory = sqlite3.Row
    if session is not None:
        rows = conn.execute(
            "SELECT * FROM interactions WHERE participant_id = ? AND session = ? ORDER BY timestamp",
            (participant_id, session),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM interactions WHERE participant_id = ? ORDER BY timestamp",
            (participant_id,),
        ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def log_survey_response(
    participant_id: str, session: int, hypothesis: str, scale_name: str, item: str, response: int
) -> None:
    conn = _get_connection()
    conn.execute(
        """
        INSERT INTO survey_responses (
            participant_id, session, hypothesis, scale_name, item, response, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            participant_id,
            session,
            hypothesis,
            scale_name,
            item,
            response,
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    conn.commit()
    conn.close()
