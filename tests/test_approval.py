from __future__ import annotations

from fairchange.resolution import build_decision_card
from fairchange.approval import ApprovalError, accept_card, authorize_card
from fairchange.workflow import DeterministicAssessor, load_engagement


def _card():
    engagement = load_engagement("fixtures/crm-engagement.json")
    request = next(item for item in engagement.requests if item.id == "req-addition")
    assessment = DeterministicAssessor().assess(request, engagement)
    return build_decision_card(engagement, assessment, proposal_version=1)


def test_authorization_and_acceptance_bind_to_exact_version_and_hash():
    card = _card()
    authorized = authorize_card(card, owner_id="owner-demo", proposal_version=1, content_hash=card.content_hash)
    record = accept_card(
        authorized,
        client_id="client-demo",
        proposal_version=1,
        content_hash=card.content_hash,
    )

    assert authorized.owner_status == "authorized"
    assert authorized.owner_id == "owner-demo"
    assert record.proposal_id == card.proposal_id
    assert record.owner_id == "owner-demo"
    assert record.client_id == "client-demo"
    assert record.accepted_scope_version == 2


def test_stale_or_unapproved_acceptance_is_rejected():
    card = _card()
    try:
        accept_card(card, "client-demo", proposal_version=1, content_hash=card.content_hash)
    except ApprovalError as exc:
        assert "owner authorization" in str(exc)
    else:
        raise AssertionError("Unapproved proposal was accepted")

    authorized = authorize_card(card, "owner-demo", proposal_version=1, content_hash=card.content_hash)
    try:
        accept_card(authorized, "client-demo", proposal_version=2, content_hash=card.content_hash)
    except ApprovalError as exc:
        assert "version" in str(exc)
    else:
        raise AssertionError("Stale proposal version was accepted")
