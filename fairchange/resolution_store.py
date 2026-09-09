"""Durable, atomic persistence for owner-review resolution decisions."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .approval import AcceptanceRecord, ApprovalError, accept_card, authorize_card
from .domain import EvidenceRef
from .resolution import DecisionCard, PriceBasis


@dataclass
class ResolutionState:
    """Persisted proposal, approval, and delivery records."""

    proposals: dict[str, dict[str, Any]] = field(default_factory=dict)
    acceptances: dict[str, dict[str, Any]] = field(default_factory=dict)
    scope_changes: dict[str, dict[str, Any]] = field(default_factory=dict)
    delivery_tasks: dict[str, dict[str, Any]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "ResolutionState":
        return cls(
            proposals=dict(raw.get("proposals", {})),
            acceptances=dict(raw.get("acceptances", {})),
            scope_changes=dict(raw.get("scope_changes", {})),
            delivery_tasks=dict(raw.get("delivery_tasks", {})),
        )


class JsonResolutionStore:
    """Store resolution records with replace-based atomic writes."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> ResolutionState:
        if not self.path.exists():
            return ResolutionState()
        return ResolutionState.from_dict(json.loads(self.path.read_text(encoding="utf-8")))

    def save_draft(self, card: DecisionCard) -> None:
        state = self.load()
        existing = state.proposals.get(card.proposal_id)
        if existing is not None:
            existing_card = decision_card_from_dict(existing)
            if existing_card.content_hash != card.content_hash:
                raise ApprovalError("A different proposal already uses this proposal ID")
            return
        state.proposals[card.proposal_id] = card.to_dict()
        self._save(state)

    def authorize(
        self,
        proposal_id: str,
        owner_id: str,
        proposal_version: int,
        content_hash: str,
    ) -> DecisionCard:
        state = self.load()
        card = self._proposal(state, proposal_id)
        authorized = authorize_card(card, owner_id, proposal_version, content_hash)
        state.proposals[proposal_id] = authorized.to_dict()
        self._save(state)
        return authorized

    def accept(
        self,
        proposal_id: str,
        client_id: str,
        proposal_version: int,
        content_hash: str,
    ) -> AcceptanceRecord:
        state = self.load()
        card = self._proposal(state, proposal_id)
        existing = state.acceptances.get(proposal_id)
        if existing is not None:
            if (
                existing.get("proposal_version") == proposal_version
                and existing.get("content_hash") == content_hash
                and existing.get("client_id") == client_id.strip()
            ):
                return AcceptanceRecord(**existing)
            raise ApprovalError("Proposal has already been accepted with different details")

        record = accept_card(card, client_id, proposal_version, content_hash)
        state.acceptances[proposal_id] = asdict(record)
        state.scope_changes[record.change_id] = {
            "change_id": record.change_id,
            "proposal_id": record.proposal_id,
            "request_id": card.request_id,
            "status": "accepted",
            "accepted_scope_version": record.accepted_scope_version,
            "content_hash": record.content_hash,
            "owner_id": record.owner_id,
            "client_id": record.client_id,
            "accepted_at": record.client_accepted_at,
        }
        state.delivery_tasks[record.delivery_task_id] = {
            "id": record.delivery_task_id,
            "request_id": card.request_id,
            "proposal_id": record.proposal_id,
            "status": "ready",
            "billable": True,
            "requires_owner_review": False,
            "content_hash": record.content_hash,
            "created_at": record.client_accepted_at,
        }
        self._save(state)
        return record

    def _proposal(self, state: ResolutionState, proposal_id: str) -> DecisionCard:
        raw = state.proposals.get(proposal_id)
        if raw is None:
            raise ApprovalError(f"Unknown proposal: {proposal_id}")
        return decision_card_from_dict(raw)

    def _save(self, state: ResolutionState) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(state.to_dict(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        os.replace(temporary, self.path)


def decision_card_from_dict(raw: dict[str, Any]) -> DecisionCard:
    return DecisionCard(
        proposal_id=raw["proposal_id"],
        proposal_version=int(raw["proposal_version"]),
        project_id=raw["project_id"],
        request_id=raw["request_id"],
        scope_version=int(raw["scope_version"]),
        title=raw["title"],
        summary=raw["summary"],
        evidence=tuple(EvidenceRef(**item) for item in raw["evidence"]),
        price_basis=tuple(PriceBasis(**item) for item in raw["price_basis"]),
        list_price_usd=float(raw["list_price_usd"]),
        training_credit_usd=float(raw["training_credit_usd"]),
        net_price_usd=float(raw["net_price_usd"]),
        recommended_option=raw["recommended_option"],
        proposed_message=raw["proposed_message"],
        owner_status=raw.get("owner_status", "draft"),
        owner_id=raw.get("owner_id"),
        owner_authorized_at=raw.get("owner_authorized_at"),
        content_hash=raw["content_hash"],
    )
