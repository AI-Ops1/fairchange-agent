"""Privacy-safe validation and local registration for independent user sessions.

The public session kit exports only anonymous, synthetic-case observations. This
module deliberately has no network client and rejects common identifying fields
or content before a report is written to the local JSONL register.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping


CASE_IDS = ("req-defect", "req-revision", "req-addition")
DECISIONS = ("defect", "included_revision", "scope_change", "ambiguous")
ROLES = ("implementation_consultant", "delivery_lead", "other")
_SESSION_CODE = re.compile(r"^session-[a-z0-9]{8,32}$")
_EMAIL = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
_PHONE = re.compile(r"(?<!\w)\+?[\d][\d\s().-]{7,}[\d](?!\w)")


class SessionValidationError(ValueError):
    """Raised when an external-session report is unsafe or incomplete."""


@dataclass(frozen=True)
class SessionResponse:
    choice: str
    evidence_cited: bool
    confidence: int


@dataclass(frozen=True)
class SessionRecord:
    session_code: str
    participant_role: str
    started_at: str
    ended_at: str
    case_order: tuple[str, ...]
    responses: dict[str, SessionResponse]
    usability_note: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["case_order"] = list(self.case_order)
        payload["responses"] = {
            case_id: asdict(response) for case_id, response in self.responses.items()
        }
        return payload


def load_session_report(payload: Mapping[str, Any]) -> SessionRecord:
    """Validate and parse one anonymous report exported by the session kit."""

    if not isinstance(payload, Mapping):
        raise SessionValidationError("report must be an object")
    required = {
        "session_code",
        "participant_role",
        "started_at",
        "ended_at",
        "case_order",
        "responses",
        "usability_note",
    }
    unknown = set(payload) - required
    missing = required - set(payload)
    if missing:
        raise SessionValidationError(f"missing report fields: {sorted(missing)}")
    if unknown:
        raise SessionValidationError(f"unsupported report fields: {sorted(unknown)}")

    session_code = payload["session_code"]
    if not isinstance(session_code, str) or not _SESSION_CODE.fullmatch(session_code):
        raise SessionValidationError("session_code must be an anonymous session-<8..32 lowercase alphanumeric> value")

    role = payload["participant_role"]
    if role not in ROLES:
        raise SessionValidationError(f"participant_role must be one of {ROLES}")

    started_at = _validated_timestamp(payload["started_at"], "started_at")
    ended_at = _validated_timestamp(payload["ended_at"], "ended_at")
    if _parse_timestamp(ended_at) < _parse_timestamp(started_at):
        raise SessionValidationError("ended_at must be after started_at")

    case_order = payload["case_order"]
    if not isinstance(case_order, list) or tuple(case_order) != CASE_IDS:
        raise SessionValidationError("case_order must contain req-defect, req-revision, and req-addition exactly once")

    responses_payload = payload["responses"]
    if not isinstance(responses_payload, Mapping) or set(responses_payload) != set(CASE_IDS):
        raise SessionValidationError("responses must contain one response for every case")
    responses: dict[str, SessionResponse] = {}
    for case_id in CASE_IDS:
        item = responses_payload[case_id]
        if not isinstance(item, Mapping) or set(item) != {"choice", "evidence_cited", "confidence"}:
            raise SessionValidationError(f"responses[{case_id}] has an invalid shape")
        choice = item["choice"]
        if choice not in DECISIONS:
            raise SessionValidationError(f"responses[{case_id}].choice is invalid")
        evidence_cited = item["evidence_cited"]
        confidence = item["confidence"]
        if not isinstance(evidence_cited, bool):
            raise SessionValidationError(f"responses[{case_id}].evidence_cited must be boolean")
        if isinstance(confidence, bool) or not isinstance(confidence, int) or not 1 <= confidence <= 5:
            raise SessionValidationError(f"responses[{case_id}].confidence must be an integer from 1 to 5")
        responses[case_id] = SessionResponse(choice, evidence_cited, confidence)

    note = payload["usability_note"]
    if not isinstance(note, str) or len(note.strip()) < 3 or len(note) > 500:
        raise SessionValidationError("usability_note must be between 3 and 500 characters")
    if _EMAIL.search(note) or _PHONE.search(note):
        raise SessionValidationError("usability_note contains personal data")

    return SessionRecord(
        session_code=session_code,
        participant_role=role,
        started_at=started_at,
        ended_at=ended_at,
        case_order=CASE_IDS,
        responses=responses,
        usability_note=note.strip(),
    )


class SessionRegister:
    """Append-only local register for anonymized reports received from testers."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def append(self, report: SessionRecord) -> None:
        existing = self._read()
        if any(item.session_code == report.session_code for item in existing):
            raise SessionValidationError(f"session_code already exists: {report.session_code}")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(report.to_dict(), sort_keys=True) + "\n")

    def summary(self) -> dict[str, Any]:
        records = self._read()
        completions = {case_id: 0 for case_id in CASE_IDS}
        roles = {role: 0 for role in ROLES}
        cited = 0
        total_responses = 0
        for record in records:
            roles[record.participant_role] += 1
            for case_id, response in record.responses.items():
                completions[case_id] += 1
                cited += int(response.evidence_cited)
                total_responses += 1
        return {
            "sessions": len(records),
            "roles": {key: value for key, value in roles.items() if value},
            "case_completions": completions,
            "evidence_cited_rate": round(cited / total_responses, 4) if total_responses else 0.0,
        }

    def _read(self) -> list[SessionRecord]:
        if not self.path.exists():
            return []
        records: list[SessionRecord] = []
        for line_number, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                records.append(load_session_report(json.loads(line)))
            except (json.JSONDecodeError, SessionValidationError) as exc:
                raise SessionValidationError(f"invalid register record on line {line_number}: {exc}") from exc
        return records


def _parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _validated_timestamp(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise SessionValidationError(f"{field} must be an ISO-8601 timestamp")
    try:
        parsed = _parse_timestamp(value)
    except ValueError as exc:
        raise SessionValidationError(f"{field} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise SessionValidationError(f"{field} must include a timezone")
    return value
