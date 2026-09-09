"""Typed domain objects for the FairChange demonstration workflow."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal

DecisionKind = Literal["defect", "included_revision", "scope_change", "ambiguous"]
TaskStatus = Literal["open", "review", "done"]


@dataclass(frozen=True)
class EvidenceRef:
    """A verifiable reference used to support an assessment."""

    source_type: Literal["request", "scope", "correspondence", "task", "estimate"]
    source_id: str
    excerpt: str

    def key(self) -> str:
        return f"{self.source_type}:{self.source_id}"


@dataclass(frozen=True)
class ScopeClause:
    id: str
    text: str


@dataclass(frozen=True)
class ScopeSnapshot:
    version: int
    signed_at: str
    source_id: str
    clauses: tuple[ScopeClause, ...]


@dataclass(frozen=True)
class StandingPolicy:
    allow_internal_defect_tasks: bool
    allow_included_revision_task_updates: bool
    allow_external_messages_without_owner_approval: bool
    require_client_acceptance_for_scope_change: bool
    conflicting_promises_require_owner_review: bool


@dataclass(frozen=True)
class ApprovedEstimate:
    work_id: str
    hours: float
    rate_usd_per_hour: float
    approved_by: str
    note: str


@dataclass(frozen=True)
class Correspondence:
    id: str
    sent_at: str
    text: str


@dataclass(frozen=True)
class ExistingTask:
    id: str
    work_id: str
    status: str
    scope_clause: str | None


@dataclass(frozen=True)
class IncomingRequest:
    id: str
    received_at: str
    text: str


@dataclass(frozen=True)
class Engagement:
    synthetic: bool
    project_id: str
    client: str
    consultancy: str
    currency: str
    scope: ScopeSnapshot
    standing_policy: StandingPolicy
    approved_estimates: tuple[ApprovedEstimate, ...]
    correspondence: tuple[Correspondence, ...]
    tasks: tuple[ExistingTask, ...]
    requests: tuple[IncomingRequest, ...]

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Engagement":
        scope_raw = raw["scope"]
        scope = ScopeSnapshot(
            version=int(scope_raw["version"]),
            signed_at=str(scope_raw["signed_at"]),
            source_id=str(scope_raw["source_id"]),
            clauses=tuple(
                ScopeClause(id=str(item["id"]), text=str(item["text"]))
                for item in scope_raw["clauses"]
            ),
        )
        policy = StandingPolicy(**raw["standing_policy"])
        return cls(
            synthetic=bool(raw.get("synthetic", False)),
            project_id=str(raw["project_id"]),
            client=str(raw["client"]),
            consultancy=str(raw["consultancy"]),
            currency=str(raw["currency"]),
            scope=scope,
            standing_policy=policy,
            approved_estimates=tuple(
                ApprovedEstimate(**item) for item in raw.get("approved_estimates", [])
            ),
            correspondence=tuple(
                Correspondence(**item) for item in raw.get("correspondence", [])
            ),
            tasks=tuple(ExistingTask(**item) for item in raw.get("tasks", [])),
            requests=tuple(IncomingRequest(**item) for item in raw.get("requests", [])),
        )

    def evidence_keys(self) -> set[str]:
        return {
            *(f"scope:{item.id}" for item in self.scope.clauses),
            *(f"correspondence:{item.id}" for item in self.correspondence),
            *(f"task:{item.id}" for item in self.tasks),
            *(f"estimate:{item.work_id}" for item in self.approved_estimates),
            *(f"request:{item.id}" for item in self.requests),
        }


@dataclass(frozen=True)
class ProposedTask:
    title: str
    reason: str
    billable: bool
    requires_owner_review: bool
    status: TaskStatus = "open"


@dataclass(frozen=True)
class Assessment:
    request_id: str
    decision: DecisionKind
    summary: str
    ambiguity: str | None
    evidence: tuple[EvidenceRef, ...]
    proposed_task: ProposedTask | None
    scope_version: int
    assessed_at: str
    model_id: str

    def validate(self, engagement: Engagement) -> None:
        valid_decisions = {"defect", "included_revision", "scope_change", "ambiguous"}
        if not isinstance(self.decision, str) or self.decision not in valid_decisions:
            raise ValueError(f"Assessment {self.request_id} has invalid decision: {self.decision}")
        request_ids = {item.id for item in engagement.requests}
        if not isinstance(self.request_id, str) or self.request_id not in request_ids:
            raise ValueError(f"Assessment {self.request_id} does not match an engagement request")
        if not isinstance(self.summary, str) or not self.summary.strip():
            raise ValueError(f"Assessment {self.request_id} has no summary")
        if not self.evidence:
            raise ValueError(f"Assessment {self.request_id} has no evidence references")
        if any(
            not isinstance(item.source_id, str)
            or not item.source_id.strip()
            or not isinstance(item.excerpt, str)
            or not item.excerpt.strip()
            for item in self.evidence
        ):
            raise ValueError(f"Assessment {self.request_id} contains incomplete evidence")
        valid_keys = engagement.evidence_keys()
        invalid = [item.key() for item in self.evidence if item.key() not in valid_keys]
        if invalid:
            raise ValueError(f"Assessment {self.request_id} has unsupported evidence: {invalid}")
        if self.scope_version != engagement.scope.version:
            raise ValueError(
                f"Assessment {self.request_id} uses scope version {self.scope_version}; "
                f"current version is {engagement.scope.version}"
            )
        if self.proposed_task is not None:
            task = self.proposed_task
            if (
                not isinstance(task.title, str)
                or not task.title.strip()
                or not isinstance(task.reason, str)
                or not task.reason.strip()
            ):
                raise ValueError(f"Assessment {self.request_id} has an incomplete proposed task")
            if not isinstance(task.billable, bool) or not isinstance(task.requires_owner_review, bool):
                raise ValueError(f"Assessment {self.request_id} has invalid task policy flags")
            if not isinstance(task.status, str) or task.status not in {"open", "review", "done"}:
                raise ValueError(f"Assessment {self.request_id} has invalid task status: {task.status}")
        if self.decision == "defect" and self.proposed_task is not None:
            if self.proposed_task.billable:
                raise ValueError("Defect tasks must be non-billable")
        if self.decision == "included_revision" and self.proposed_task is not None:
            if self.proposed_task.billable:
                raise ValueError("Included revisions must be non-billable")
        if self.decision == "scope_change":
            if self.proposed_task is None or not self.proposed_task.requires_owner_review:
                raise ValueError("Scope changes must create an owner-review task")
            if self.proposed_task.billable is False:
                raise ValueError("Scope changes cannot be silently marked non-billable")


@dataclass(frozen=True)
class InternalTask:
    id: str
    request_id: str
    title: str
    reason: str
    status: TaskStatus
    billable: bool
    requires_owner_review: bool
    evidence: tuple[EvidenceRef, ...]
    created_at: str


@dataclass
class WorkflowState:
    cursor: str | None = None
    processed_event_ids: list[str] = field(default_factory=list)
    assessments: dict[str, dict[str, Any]] = field(default_factory=dict)
    internal_tasks: dict[str, dict[str, Any]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "WorkflowState":
        return cls(
            cursor=raw.get("cursor"),
            processed_event_ids=list(raw.get("processed_event_ids", [])),
            assessments=dict(raw.get("assessments", {})),
            internal_tasks=dict(raw.get("internal_tasks", {})),
        )


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
