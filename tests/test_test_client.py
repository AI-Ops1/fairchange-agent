from __future__ import annotations

import pytest

from fairchange.approval import ApprovalError
from fairchange.resolution import build_decision_card
from fairchange.resolution_store import JsonResolutionStore
from fairchange.test_client import (
    AuthenticatedResolutionClient,
    AuthenticationError,
    issue_test_token,
)
from fairchange.workflow import DeterministicAssessor, load_engagement


def _card():
    engagement = load_engagement("fixtures/crm-engagement.json")
    request = next(item for item in engagement.requests if item.id == "req-addition")
    assessment = DeterministicAssessor().assess(request, engagement)
    return build_decision_card(engagement, assessment, proposal_version=1)


def test_test_client_requires_signed_owner_and_client_tokens(tmp_path):
    store = JsonResolutionStore(tmp_path / "resolution.json")
    card = _card()
    store.save_draft(card)
    client = AuthenticatedResolutionClient(store, "local-demo-secret")

    owner_token = issue_test_token("owner-demo", "owner", "local-demo-secret")
    client_token = issue_test_token("client-demo", "client", "local-demo-secret")
    authorized = client.authorize(card.proposal_id, owner_token, 1, card.content_hash)
    record = client.accept(card.proposal_id, client_token, 1, card.content_hash)

    assert authorized.owner_id == "owner-demo"
    assert record.client_id == "client-demo"
    assert store.load().delivery_tasks[record.delivery_task_id]["status"] == "ready"


def test_test_client_rejects_tampered_or_wrong_role_tokens(tmp_path):
    store = JsonResolutionStore(tmp_path / "resolution.json")
    card = _card()
    store.save_draft(card)
    client = AuthenticatedResolutionClient(store, "local-demo-secret")
    wrong_role = issue_test_token("client-demo", "client", "local-demo-secret")
    tampered = wrong_role[:-1] + ("A" if wrong_role[-1] != "A" else "B")

    with pytest.raises(AuthenticationError):
        client.authorize(card.proposal_id, wrong_role, 1, card.content_hash)
    with pytest.raises(AuthenticationError):
        client.accept(card.proposal_id, tampered, 1, card.content_hash)
