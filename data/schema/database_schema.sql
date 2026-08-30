-- Reference copy of the schema used in src/memory/db.py.
-- Kept here separately so it can be reviewed/versioned independently of
-- application code, and handed to a supervisor or ethics committee as a
-- clear description of exactly what data is stored.

CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    participant_id TEXT NOT NULL,      -- anonymized code only, e.g. 'P01'
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
    scale_name TEXT NOT NULL,          -- 'baseline' | 'post' | 'integrated' | 'baseline'
    item TEXT NOT NULL,
    response INTEGER NOT NULL,         -- 1-5 Likert
    timestamp TEXT NOT NULL
);

-- Note: raw audio is NOT stored in this schema by default (see
-- config/settings.py: STORE_RAW_AUDIO). Only derived features/labels and
-- transcripts are persisted, to minimize sensitive data retention per the
-- ethics framework in docs/ethics_consent_template.md.
