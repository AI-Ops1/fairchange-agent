"""Owner-review decision cards for proposed scope changes."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, replace
from typing import Any, Literal

from .domain import Assessment, Engagement, EvidenceRef
from .domain import ProposedTask


@dataclass(frozen=True)
class PriceBasis:
    source_id: str
    work_id: str
    label: str
    hours: float
    rate_usd_per_hour: float
    amount_usd: float
    note: str


@dataclass(frozen=True)
class DecisionCard:
    proposal_id: str
    proposal_version: int
    project_id: str
    request_id: str
    scope_version: int
    title: str
    summary: str
    evidence: tuple[EvidenceRef, ...]
    price_basis: tuple[PriceBasis, ...]
    list_price_usd: float
    training_credit_usd: float
    net_price_usd: float
    recommended_option: Literal["substitute-training"]
    proposed_message: str
    owner_status: Literal["draft", "authorized", "rejected"] = "draft"
    owner_id: str | None = None
    owner_authorized_at: str | None = None
    content_hash: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def assessment_from_dict(raw: dict[str, Any]) -> Assessment:
    """Rehydrate one persisted model assessment for resolution work."""
    task_raw = raw.get("proposed_task")
    return Assessment(
        request_id=raw["request_id"],
        decision=raw["decision"],
        summary=raw["summary"],
        ambiguity=raw.get("ambiguity"),
        evidence=tuple(EvidenceRef(**item) for item in raw["evidence"]),
        proposed_task=ProposedTask(**task_raw) if task_raw else None,
        scope_version=int(raw["scope_version"]),
        assessed_at=raw["assessed_at"],
        model_id=raw["model_id"],
    )


def build_decision_card(
    engagement: Engagement, assessment: Assessment, proposal_version: int
) -> DecisionCard:
    if assessment.decision != "scope_change":
        raise ValueError("Decision cards require a scope_change assessment")
    if assessment.proposed_task is None or not assessment.proposed_task.requires_owner_review:
        raise ValueError("Scope-change decision cards require owner review")
    if not assessment.proposed_task.billable:
        raise ValueError("Scope-change decision cards must preserve billable work")
    if assessment.scope_version != engagement.scope.version:
        raise ValueError("Assessment scope version does not match the current engagement")
    if proposal_version < 1:
        raise ValueError("Proposal version must be positive")

    routing_estimate = _find_estimate(engagement, "regional-routing-extension")
    training_estimate = _find_estimate(engagement, "administrator-training")
    training_task = _find_task(engagement, "administrator-training")
    routing_amount = _amount(routing_estimate.hours, routing_estimate.rate_usd_per_hour)
    training_amount = _amount(training_estimate.hours, training_estimate.rate_usd_per_hour)
    proposal_id = f"proposal:{engagement.project_id}:{assessment.request_id}:v{proposal_version}"

    evidence = list(assessment.evidence)
    _append_evidence(
        evidence,
        EvidenceRef(
            "estimate",
            routing_estimate.work_id,
            f"Approved estimate: {routing_estimate.hours:g} hours at "
            f"{engagement.currency} {routing_estimate.rate_usd_per_hour:,.2f}/hour.",
        ),
    )
    _append_evidence(
        evidence,
        EvidenceRef(
            "task",
            training_task.id,
            f"Existing task: work_id {training_task.work_id}, status {training_task.status}, "
            f"scope clause {training_task.scope_clause}.",
        ),
    )
    _append_evidence(
        evidence,
        EvidenceRef(
            "estimate",
            training_estimate.work_id,
            f"Training estimate: {training_estimate.hours:g} hours at "
            f"{engagement.currency} {training_estimate.rate_usd_per_hour:,.2f}/hour; "
            "deliverable is unstarted and proposed as a possible substitution.",
        ),
    )
    title = "UK and Canada routing in place of administrator training"
    summary = (
        "The requested UK and Canada routing is excluded by S4. This draft offers "
        "a budget-neutral substitution of the unstarted administrator training "
        "deliverable, subject to owner authorization and client acceptance."
    )
    message = (
        f"Hi {engagement.client} team,\n\n"
        "We reviewed your request for UK and Canada routing. Those regional rules "
        f"are outside the signed scope under S4. We propose replacing the unstarted "
        f"administrator training deliverable with the requested routing work. The "
        f"routing price basis is {engagement.currency} {routing_amount:,.2f} "
        f"({routing_estimate.hours:g} hours × {engagement.currency} "
        f"{routing_estimate.rate_usd_per_hour:,.2f}/hour), with a "
        f"{engagement.currency} {training_amount:,.2f} credit for the training "
        f"deliverable, making the proposed net change {engagement.currency} "
        f"{routing_amount - training_amount:,.2f}.\n\n"
        "This is a proposal to revise the deliverables. It requires owner "
        "authorization and your explicit acceptance. No work will begin until "
        "both approvals are recorded."
    )
    card = DecisionCard(
        proposal_id=proposal_id,
        proposal_version=proposal_version,
        project_id=engagement.project_id,
        request_id=assessment.request_id,
        scope_version=assessment.scope_version,
        title=title,
        summary=summary,
        evidence=tuple(evidence),
        price_basis=(
            PriceBasis(
                source_id=routing_estimate.work_id,
                work_id=routing_estimate.work_id,
                label="UK and Canada regional routing",
                hours=routing_estimate.hours,
                rate_usd_per_hour=routing_estimate.rate_usd_per_hour,
                amount_usd=routing_amount,
                note=routing_estimate.note,
            ),
            PriceBasis(
                source_id=training_estimate.work_id,
                work_id=training_estimate.work_id,
                label="Administrator training credit",
                hours=training_estimate.hours,
                rate_usd_per_hour=training_estimate.rate_usd_per_hour,
                amount_usd=training_amount,
                note=training_estimate.note,
            ),
        ),
        list_price_usd=routing_amount,
        training_credit_usd=training_amount,
        net_price_usd=routing_amount - training_amount,
        recommended_option="substitute-training",
        proposed_message=message,
    )
    return _with_hash(card)


def _with_hash(card: DecisionCard) -> DecisionCard:
    payload = card.to_dict()
    payload["content_hash"] = ""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return replace(card, content_hash=f"sha256:{hashlib.sha256(encoded).hexdigest()}")


def _find_estimate(engagement: Engagement, work_id: str):
    for estimate in engagement.approved_estimates:
        if estimate.work_id == work_id:
            return estimate
    raise ValueError(f"Missing approved estimate: {work_id}")


def _find_task(engagement: Engagement, work_id: str):
    for task in engagement.tasks:
        if task.work_id == work_id:
            return task
    raise ValueError(f"Missing existing task: {work_id}")


def _amount(hours: float, rate: float) -> float:
    return round(hours * rate, 2)


def _append_evidence(evidence: list[EvidenceRef], item: EvidenceRef) -> None:
    if not any(existing.source_type == item.source_type and existing.source_id == item.source_id for existing in evidence):
        evidence.append(item)
