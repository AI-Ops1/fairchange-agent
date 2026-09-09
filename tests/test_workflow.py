from __future__ import annotations

import json

from fairchange.store import JsonWorkflowStore
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
