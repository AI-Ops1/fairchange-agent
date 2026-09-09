"""Persisted pause/resume state around the human resolution gate."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

from .resolution import DecisionCard
from .resolution_store import JsonResolutionStore


class ContinuationError(ValueError):
    """Raised when a continuation no longer matches its proposal."""


@dataclass(frozen=True)
class ResolutionSession:
    continuation_id: str
    proposal_id: str
    proposal_version: int
    content_hash: str
    status: Literal["paused", "completed"]
    waiting_for: Literal["owner", "client"] | None
    last_event: str
    paused_at: str
    resumed_at: str | None = None
    completed_at: str | None = None


class JsonResolutionSessionStore:
    """Durable continuation store for a model-to-human-to-delivery run."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> ResolutionSession | None:
        if not self.path.exists():
            return None
        return ResolutionSession(**json.loads(self.path.read_text(encoding="utf-8")))

    def start(self, card: DecisionCard) -> ResolutionSession:
        existing = self.load()
        if existing is not None:
            self._check_match(existing, card.proposal_id, card.proposal_version, card.content_hash)
            return existing
        session = ResolutionSession(
            continuation_id=f"continuation:{card.proposal_id}",
            proposal_id=card.proposal_id,
            proposal_version=card.proposal_version,
            content_hash=card.content_hash,
            status="paused",
            waiting_for="owner",
            last_event="model_assessment_complete",
            paused_at=_now(),
        )
        self._save(session)
        return session

    def resume(self, resolution_store: JsonResolutionStore) -> ResolutionSession:
        session = self.load()
        if session is None:
            raise ContinuationError("No paused resolution session exists")
        if session.status == "completed":
            return session

        state = resolution_store.load()
        proposal = state.proposals.get(session.proposal_id)
        if proposal is None:
            raise ContinuationError(
                f"Proposal is missing for continuation: {session.proposal_id}"
            )
        self._check_match(
            session,
            proposal["proposal_id"],
            int(proposal["proposal_version"]),
            proposal["content_hash"],
        )
        if session.waiting_for == "owner" and proposal.get("owner_status") == "authorized":
            session = ResolutionSession(
                **{
                    **asdict(session),
                    "waiting_for": "client",
                    "last_event": "owner_authorized",
                    "resumed_at": _now(),
                }
            )
            self._save(session)
            return session
        if session.waiting_for == "client" and session.proposal_id in state.acceptances:
            acceptance = state.acceptances[session.proposal_id]
            if (
                int(acceptance["proposal_version"]) != session.proposal_version
                or acceptance["content_hash"] != session.content_hash
            ):
                raise ContinuationError("Acceptance does not match the paused proposal")
            session = ResolutionSession(
                **{
                    **asdict(session),
                    "status": "completed",
                    "waiting_for": None,
                    "last_event": "client_accepted",
                    "completed_at": _now(),
                }
            )
            self._save(session)
        return session

    def _check_match(
        self, session: ResolutionSession, proposal_id: str, proposal_version: int, content_hash: str
    ) -> None:
        if (
            proposal_id != session.proposal_id
            or proposal_version != session.proposal_version
            or content_hash != session.content_hash
        ):
            raise ContinuationError("Continuation does not match the proposal version or content hash")

    def _save(self, session: ResolutionSession) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(json.dumps(asdict(session), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(temporary, self.path)


def _now() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
