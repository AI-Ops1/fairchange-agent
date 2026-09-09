"""Exact-version owner authorization and client acceptance primitives."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone

from .resolution import DecisionCard


class ApprovalError(ValueError):
    """Raised when a proposal approval does not match the draft being approved."""


@dataclass(frozen=True)
class AcceptanceRecord:
    proposal_id: str
    proposal_version: int
    content_hash: str
    owner_id: str
    client_id: str
    owner_authorized_at: str
    client_accepted_at: str
    accepted_scope_version: int
    change_id: str
    delivery_task_id: str


def authorize_card(
    card: DecisionCard,
    owner_id: str,
    proposal_version: int,
    content_hash: str,
    authorized_at: str | None = None,
) -> DecisionCard:
    _check_identity(card, proposal_version, content_hash)
    if card.owner_status != "draft":
        raise ApprovalError(f"Proposal is already {card.owner_status}")
    owner_id = owner_id.strip()
    if not owner_id:
        raise ApprovalError("Owner identity is required")
    return replace(
        card,
        owner_status="authorized",
        owner_id=owner_id,
        owner_authorized_at=authorized_at or utc_now(),
    )


def accept_card(
    card: DecisionCard,
    client_id: str,
    proposal_version: int,
    content_hash: str,
    accepted_at: str | None = None,
) -> AcceptanceRecord:
    _check_identity(card, proposal_version, content_hash)
    if card.owner_status != "authorized" or not card.owner_id or not card.owner_authorized_at:
        raise ApprovalError("Client acceptance requires owner authorization")
    client_id = client_id.strip()
    if not client_id:
        raise ApprovalError("Client identity is required")
    client_accepted_at = accepted_at or utc_now()
    return AcceptanceRecord(
        proposal_id=card.proposal_id,
        proposal_version=card.proposal_version,
        content_hash=card.content_hash,
        owner_id=card.owner_id,
        client_id=client_id,
        owner_authorized_at=card.owner_authorized_at,
        client_accepted_at=client_accepted_at,
        accepted_scope_version=card.scope_version + 1,
        change_id=f"change:{card.proposal_id}:accepted",
        delivery_task_id=f"task:{card.request_id}:delivery:v{card.proposal_version}",
    )


def _check_identity(card: DecisionCard, proposal_version: int, content_hash: str) -> None:
    if proposal_version != card.proposal_version:
        raise ApprovalError(
            f"Proposal version mismatch: expected {card.proposal_version}, received {proposal_version}"
        )
    if content_hash != card.content_hash:
        raise ApprovalError("Proposal content hash mismatch")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
