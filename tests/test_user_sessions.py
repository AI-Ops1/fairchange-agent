from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import pytest

from fairchange.user_sessions import (
    CASE_IDS,
    SessionRegister,
    SessionValidationError,
    load_session_report,
)


def _report(**overrides):
    started = datetime(2026, 9, 9, 12, 0, tzinfo=timezone.utc)
    ended = started + timedelta(minutes=8)
    report = {
        "session_code": "session-a1b2c3d4",
        "participant_role": "implementation_consultant",
        "started_at": started.isoformat().replace("+00:00", "Z"),
        "ended_at": ended.isoformat().replace("+00:00", "Z"),
        "case_order": list(CASE_IDS),
        "responses": {
            "req-defect": {"choice": "defect", "evidence_cited": True, "confidence": 5},
            "req-revision": {
                "choice": "included_revision",
                "evidence_cited": True,
                "confidence": 4,
            },
            "req-addition": {"choice": "scope_change", "evidence_cited": True, "confidence": 5},
        },
        "usability_note": "The evidence trail made the decision easy to explain.",
    }
    report.update(overrides)
    return report


def test_session_report_accepts_anonymous_three_case_walkthrough():
    report = load_session_report(_report())
    assert report.session_code == "session-a1b2c3d4"
    assert report.case_order == CASE_IDS
    assert report.responses["req-addition"].choice == "scope_change"


@pytest.mark.parametrize(
    "field,value,match",
    [
        ("session_code", "not-an-anonymous-code", "session_code"),
        ("case_order", ["req-defect", "req-defect", "req-addition"], "case_order"),
        ("responses", {"req-defect": {}}, "responses"),
        ("usability_note", "email me at person@example.com", "personal data"),
    ],
)
def test_session_report_rejects_invalid_or_identifying_input(field, value, match):
    report = _report(**{field: value})
    with pytest.raises(SessionValidationError, match=match):
        load_session_report(report)


def test_register_rejects_duplicate_session_codes_and_summarizes(tmp_path):
    path = tmp_path / "sessions.jsonl"
    register = SessionRegister(path)
    register.append(load_session_report(_report()))

    with pytest.raises(SessionValidationError, match="already exists"):
        register.append(load_session_report(_report()))

    summary = register.summary()
    assert summary == {
        "sessions": 1,
        "roles": {"implementation_consultant": 1},
        "case_completions": dict.fromkeys(CASE_IDS, 1),
        "evidence_cited_rate": 1.0,
    }
    assert json.loads(path.read_text(encoding="utf-8").splitlines()[0])["session_code"] == "session-a1b2c3d4"

