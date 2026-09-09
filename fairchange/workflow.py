"""Fixture intake, model assessment, policy checks and task persistence."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Protocol

from .domain import (
    Assessment,
    Engagement,
    EvidenceRef,
    IncomingRequest,
    InternalTask,
    ProposedTask,
    WorkflowState,
    utc_now,
)
from .retrieval import build_retrieval_tools
from .store import JsonWorkflowStore


class Assessor(Protocol):
    def assess(self, request: IncomingRequest, engagement: Engagement) -> Assessment: ...


class ModelAssessor:
    """Use Strands plus read-only retrieval tools to assess one request."""

    def __init__(self, model: Any, model_id: str):
        from strands import Agent

        self.agent_cls = Agent
        self.model = model
        self.model_id = model_id

    def assess(self, request: IncomingRequest, engagement: Engagement) -> Assessment:
        agent = self.agent_cls(model=self.model, tools=build_retrieval_tools(engagement))
        prompt = f"""
You are FairChange, a scope-governance agent for a consulting engagement.
Use retrieval tools before deciding. Never invent evidence IDs or claim that a
client accepted a change. Classify this request as exactly one of:
defect, included_revision, scope_change, ambiguous.

The signed scope version is {engagement.scope.version}.
Incoming request ID: {request.id}
Received at: {request.received_at}
Request text: {request.text}

        Call the tools as needed, but do not show your rationale, tool commentary,
        Markdown fences, or any prose in the final response. Return only valid JSON
        with this exact shape:
{{
  "decision": "defect|included_revision|scope_change|ambiguous",
  "summary": "short factual explanation",
  "ambiguity": "null or a short explanation",
  "evidence": [{{"source_type":"request|scope|correspondence|task|estimate", "source_id":"known ID", "excerpt":"short exact or faithful excerpt"}}],
  "proposed_task": {{"title":"...", "reason":"...", "billable":true, "requires_owner_review":true, "status":"open|review|done"}} or null
}}

Rules: defects against agreed acceptance criteria are non-billable internal work;
included revisions can update internal delivery tasks; extra work must be marked
billable and require owner review plus client acceptance; never send external
messages automatically. Every assessment must cite the request and supporting
  scope, correspondence, task, or estimate evidence. For scope evidence,
  source_id must be the clause ID only, such as `S1` or `S5`; do not combine it
  with the scope bundle ID `sow-v1`.
""".strip()
        raw = str(agent(prompt)).strip()
        payload = _parse_json(raw)
        evidence = tuple(
            EvidenceRef(
                source_type=item["source_type"],
                source_id=_canonical_source_id(item["source_type"], item["source_id"], engagement),
                excerpt=item["excerpt"],
            )
            for item in payload["evidence"]
        )
        task_payload = payload.get("proposed_task")
        proposed_task = ProposedTask(**task_payload) if task_payload else None
        assessment = Assessment(
            request_id=request.id,
            decision=payload["decision"],
            summary=payload["summary"],
            ambiguity=payload.get("ambiguity"),
            evidence=evidence,
            proposed_task=proposed_task,
            scope_version=engagement.scope.version,
            assessed_at=utc_now(),
            model_id=self.model_id,
        )
        assessment.validate(engagement)
        return assessment


class DeterministicAssessor:
    """Offline assessor used for tests and deterministic local demonstrations."""

    def assess(self, request: IncomingRequest, engagement: Engagement) -> Assessment:
        if request.id == "req-defect":
            decision = "defect"
            summary = "The request describes a failure against the agreed US routing behavior."
            ambiguity = None
            evidence = (
                EvidenceRef("request", request.id, request.text),
                EvidenceRef("scope", "S1", engagement.scope.clauses[0].text),
                EvidenceRef("scope", "S5", engagement.scope.clauses[4].text),
            )
            task = ProposedTask(
                title="Fix inactive-representative routing defect",
                reason="Restore the agreed US lead-routing behavior.",
                billable=False,
                requires_owner_review=False,
            )
        elif request.id == "req-revision":
            decision = "included_revision"
            summary = "The request uses the remaining included dashboard revision."
            ambiguity = None
            evidence = (
                EvidenceRef("request", request.id, request.text),
                EvidenceRef("scope", "S2", engagement.scope.clauses[1].text),
                EvidenceRef("task", "task-dashboard", "Existing dashboard task is in review."),
            )
            task = ProposedTask(
                title="Apply remaining dashboard revision",
                reason="Use the one unused revision round in the signed scope.",
                billable=False,
                requires_owner_review=False,
            )
        else:
            decision = "scope_change"
            summary = "UK and Canada routing are excluded regional work and require a governed proposal."
            ambiguity = "The request suggests substituting unstarted training; client acceptance is not yet recorded."
            evidence = (
                EvidenceRef("request", request.id, request.text),
                EvidenceRef("scope", "S4", engagement.scope.clauses[3].text),
                EvidenceRef("scope", "S3", engagement.scope.clauses[2].text),
                EvidenceRef("estimate", "regional-routing-extension", "Approved four-hour estimate."),
                EvidenceRef("correspondence", "email-001", engagement.correspondence[0].text),
            )
            task = ProposedTask(
                title="Prepare owner-review proposal for UK and Canada routing",
                reason="Assess excluded regional work and possible training substitution.",
                billable=True,
                requires_owner_review=True,
                status="review",
            )
        assessment = Assessment(
            request_id=request.id,
            decision=decision,
            summary=summary,
            ambiguity=ambiguity,
            evidence=evidence,
            proposed_task=task,
            scope_version=engagement.scope.version,
            assessed_at=utc_now(),
            model_id="deterministic-test-assessor",
        )
        assessment.validate(engagement)
        return assessment


def load_engagement(path: str | Path) -> Engagement:
    return Engagement.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))


def event_id(request: IncomingRequest) -> str:
    return f"request:{request.id}"


def process_pending_requests(
    engagement: Engagement, store: JsonWorkflowStore, assessor: Assessor
) -> list[Assessment]:
    state = store.load()
    pending = sorted(engagement.requests, key=lambda item: (item.received_at, item.id))
    results: list[Assessment] = []
    for request in pending:
        current_event_id = event_id(request)
        if current_event_id in state.processed_event_ids:
            continue
        assessment = assessor.assess(request, engagement)
        task = _task_from_assessment(assessment)
        state.assessments[request.id] = _assessment_dict(assessment)
        if task:
            state.internal_tasks[task.id] = _task_dict(task)
        state.processed_event_ids.append(current_event_id)
        state.cursor = current_event_id
        store.save(state)
        results.append(assessment)
    return results


def _task_from_assessment(assessment: Assessment) -> InternalTask | None:
    if assessment.proposed_task is None:
        return None
    return InternalTask(
        id=f"task:fairchange:{assessment.request_id}",
        request_id=assessment.request_id,
        title=assessment.proposed_task.title,
        reason=assessment.proposed_task.reason,
        status=assessment.proposed_task.status,
        billable=assessment.proposed_task.billable,
        requires_owner_review=assessment.proposed_task.requires_owner_review,
        evidence=assessment.evidence,
        created_at=assessment.assessed_at,
    )


def _assessment_dict(assessment: Assessment) -> dict[str, Any]:
    return {
        "request_id": assessment.request_id,
        "decision": assessment.decision,
        "summary": assessment.summary,
        "ambiguity": assessment.ambiguity,
        "evidence": [item.__dict__ for item in assessment.evidence],
        "proposed_task": assessment.proposed_task.__dict__ if assessment.proposed_task else None,
        "scope_version": assessment.scope_version,
        "assessed_at": assessment.assessed_at,
        "model_id": assessment.model_id,
    }


def _task_dict(task: InternalTask) -> dict[str, Any]:
    return {
        "id": task.id,
        "request_id": task.request_id,
        "title": task.title,
        "reason": task.reason,
        "status": task.status,
        "billable": task.billable,
        "requires_owner_review": task.requires_owner_review,
        "evidence": [item.__dict__ for item in task.evidence],
        "created_at": task.created_at,
    }


def _parse_json(raw: str) -> dict[str, Any]:
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
    candidate = fenced.group(1) if fenced else raw
    start, end = candidate.find("{"), candidate.rfind("}")
    if start < 0 or end < start:
        raise ValueError(f"Model did not return a JSON object: {raw[:400]}")
    return json.loads(candidate[start : end + 1])


def _canonical_source_id(source_type: str, source_id: str, engagement: Engagement) -> str:
    """Accept a known ID, with one safe normalization for scope bundle labels."""
    value = str(source_id).strip()
    if source_type == "scope":
        known = {item.id for item in engagement.scope.clauses}
        if value not in known:
            for clause_id in known:
                if re.search(rf"(?:^|[/|: ]){re.escape(clause_id)}$", value):
                    return clause_id
    return value
