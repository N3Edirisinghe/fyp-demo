"""
Tests for the relational memory store (H2). Uses a temporary SQLite file
so tests never touch real participant data.
"""

import pytest

from config.settings import settings
from src.memory.db import get_participant_history, log_interaction, log_survey_response


@pytest.fixture(autouse=True)
def use_temp_db(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "local_db_path", str(tmp_path / "test.db"))
    yield


def test_log_and_retrieve_interaction():
    log_interaction(
        participant_id="P99",
        session=1,
        condition="no_memory",
        transcript="I had a rough day",
        voice_emotion_label="sad",
        voice_emotion_confidence=0.82,
        text_emotion_label="sad",
        text_emotion_confidence=0.75,
        self_reported_emotion="sad",
    )

    history = get_participant_history("P99")
    assert len(history) == 1
    assert history[0]["transcript"] == "I had a rough day"
    assert history[0]["self_reported_emotion"] == "sad"


def test_participant_isolation():
    log_interaction(participant_id="P01", session=1, condition="no_memory", transcript="hello")
    log_interaction(participant_id="P02", session=1, condition="no_memory", transcript="hi there")

    p01_history = get_participant_history("P01")
    assert len(p01_history) == 1
    assert p01_history[0]["transcript"] == "hello"


def test_log_survey_response_does_not_raise():
    log_survey_response(
        participant_id="P99",
        session=1,
        hypothesis="H2",
        scale_name="baseline",
        item="The companion felt personalized to me.",
        response=4,
    )
