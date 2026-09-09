from __future__ import annotations

from fairchange.resolution import build_decision_card
from fairchange.resolution_store import JsonResolutionStore
from fairchange.session import JsonResolutionSessionStore
from fairchange.workflow import DeterministicAssessor, load_engagement


def _card():
    engagement = load_engagement("fixtures/crm-engagement.json")
    request = next(item for item in engagement.requests if item.id == "req-addition")
    assessment = DeterministicAssessor().assess(request, engagement)
    return build_decision_card(engagement, assessment, proposal_version=1)


def test_session_pauses_and_resumes_across_owner_and_client_decisions(tmp_path):
    resolution_store = JsonResolutionStore(tmp_path / "resolution.json")
    session_store = JsonResolutionSessionStore(tmp_path / "session.json")
    card = _card()
    resolution_store.save_draft(card)

    paused = session_store.start(card)
    assert paused.status == "paused"
    assert paused.waiting_for == "owner"
    assert session_store.load() == paused

    resolution_store.authorize(card.proposal_id, "owner-demo", 1, card.content_hash)
    waiting_for_client = session_store.resume(resolution_store)
    assert waiting_for_client.waiting_for == "client"
    assert waiting_for_client.status == "paused"

    resolution_store.accept(card.proposal_id, "client-demo", 1, card.content_hash)
    completed = session_store.resume(resolution_store)
    assert completed.status == "completed"
    assert completed.waiting_for is None
    assert completed.last_event == "client_accepted"


def test_session_fails_loudly_when_its_proposal_is_missing(tmp_path):
    resolution_store = JsonResolutionStore(tmp_path / "resolution.json")
    session_store = JsonResolutionSessionStore(tmp_path / "session.json")
    card = _card()
    session_store.start(card)

    try:
        session_store.resume(resolution_store)
    except ValueError as exc:
        assert "Proposal is missing" in str(exc)
    else:
        raise AssertionError("A missing proposal must not leave a continuation silently paused")
