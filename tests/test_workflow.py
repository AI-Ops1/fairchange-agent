from __future__ import annotations

import json

import pytest

from fairchange.store import JsonWorkflowStore
from fairchange.domain import Assessment, EvidenceRef, ProposedTask, utc_now
from fairchange.workflow import DeterministicAssessor, load_engagement, process_pending_requests


def test_fixture_processes_all_requests_and_survives_restart(tmp_path):
    fixture = load_engagement("fixtures/crm-engagement.json")
    state_path = tmp_path / "state.json"
    store = JsonWorkflowStore(state_path)

    first_run = process_pending_requests(fixture, store, DeterministicAssessor())
    second_run = process_pending_requests(fixture, store, DeterministicAssessor())

    assert [item.request_id for item in first_run] == [
        "req-defect",
        "req-revision",
        "req-addition",
    ]
    assert second_run == []
    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state["cursor"] == "request:req-addition"
    assert len(state["assessments"]) == 3
    assert len(state["internal_tasks"]) == 3


def test_scope_change_requires_review_and_stays_billable(tmp_path):
    fixture = load_engagement("fixtures/crm-engagement.json")
    results = process_pending_requests(
        fixture, JsonWorkflowStore(tmp_path / "state.json"), DeterministicAssessor()
    )
    addition = next(item for item in results if item.request_id == "req-addition")
    assert addition.decision == "scope_change"
    assert addition.proposed_task is not None
    assert addition.proposed_task.billable is True
    assert addition.proposed_task.requires_owner_review is True


def test_deterministic_assessor_rejects_unknown_request_ids():
    fixture = load_engagement("fixtures/crm-engagement.json")
    unknown = fixture.requests[0].__class__("unexpected", "2026-09-09T09:00:00Z", "unknown")
    try:
        DeterministicAssessor().assess(unknown, fixture)
    except ValueError as exc:
        assert "Unsupported deterministic request" in str(exc)
    else:
        raise AssertionError("Unknown deterministic requests must not become scope changes")


def test_assessment_validation_rejects_billable_defect():
    fixture = load_engagement("fixtures/crm-engagement.json")
    request = fixture.requests[0]
    assessment = Assessment(
        request_id=request.id,
        decision="defect",
        summary="A defect with an invalid commercial task.",
        ambiguity=None,
        evidence=(EvidenceRef("request", request.id, request.text),),
        proposed_task=ProposedTask("Bad task", "Should be internal", True, False),
        scope_version=fixture.scope.version,
        assessed_at=utc_now(),
        model_id="test",
    )
    try:
        assessment.validate(fixture)
    except ValueError as exc:
        assert "non-billable" in str(exc)
    else:
        raise AssertionError("A defect must not produce a billable task")


def test_assessment_validation_requires_owner_review_for_billable_tasks():
    fixture = load_engagement("fixtures/crm-engagement.json")
    request = fixture.requests[0]
    assessment = Assessment(
        request_id=request.id,
        decision="ambiguous",
        summary="The request needs human review before classification.",
        ambiguity="The evidence is not sufficient to classify it safely.",
        evidence=(EvidenceRef("request", request.id, request.text),),
        proposed_task=ProposedTask("Review request", "Resolve ambiguity", True, False),
        scope_version=fixture.scope.version,
        assessed_at=utc_now(),
        model_id="test",
    )
    with pytest.raises(ValueError, match="require owner review"):
        assessment.validate(fixture)
