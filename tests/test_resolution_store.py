from __future__ import annotations

from dataclasses import asdict

from fairchange.approval import ApprovalError
from fairchange.resolution import build_decision_card
from fairchange.resolution_store import JsonResolutionStore
from fairchange.workflow import DeterministicAssessor, load_engagement


def _card():
    engagement = load_engagement("fixtures/crm-engagement.json")
    request = next(item for item in engagement.requests if item.id == "req-addition")
    assessment = DeterministicAssessor().assess(request, engagement)
    return build_decision_card(engagement, assessment, proposal_version=1)


def test_acceptance_persists_scope_change_and_delivery_task_together(tmp_path):
    store = JsonResolutionStore(tmp_path / "resolution.json")
    card = _card()
    store.save_draft(card)
    authorized = store.authorize(card.proposal_id, "owner-demo", 1, card.content_hash)
    record = store.accept(card.proposal_id, "client-demo", 1, card.content_hash)

    state = store.load()
    assert authorized.owner_status == "authorized"
    assert state.acceptances[card.proposal_id]["client_id"] == "client-demo"
    assert state.scope_changes[record.change_id]["status"] == "accepted"
    assert state.delivery_tasks[record.delivery_task_id]["status"] == "ready"
    assert state.scope_changes[record.change_id]["accepted_scope_version"] == 2


def test_acceptance_rejects_a_different_hash_after_authorization(tmp_path):
    store = JsonResolutionStore(tmp_path / "resolution.json")
    card = _card()
    store.save_draft(card)
    store.authorize(card.proposal_id, "owner-demo", 1, card.content_hash)

    try:
        store.accept(card.proposal_id, "client-demo", 1, "sha256:stale")
    except ApprovalError as exc:
        assert "hash" in str(exc)
    else:
        raise AssertionError("A stale proposal hash was accepted")
