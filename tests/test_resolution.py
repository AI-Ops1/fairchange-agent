from __future__ import annotations

from fairchange.workflow import DeterministicAssessor, load_engagement
from fairchange.resolution import build_decision_card


def test_scope_change_decision_card_binds_evidence_price_and_message():
    engagement = load_engagement("fixtures/crm-engagement.json")
    request = next(item for item in engagement.requests if item.id == "req-addition")
    assessment = DeterministicAssessor().assess(request, engagement)

    card = build_decision_card(engagement, assessment, proposal_version=1)

    assert card.proposal_id == "proposal:demo-crm-001:req-addition:v1"
    assert card.content_hash.startswith("sha256:")
    assert {item.source_id for item in card.evidence} >= {
        "req-addition",
        "S3",
        "S4",
        "task-training",
        "regional-routing-extension",
    }
    assert card.list_price_usd == 600.0
    assert card.training_credit_usd == 600.0
    assert card.recommended_option == "substitute-training"
    assert card.net_price_usd == 0.0
    assert "owner authorization" in card.proposed_message
    assert "explicit acceptance" in card.proposed_message


def test_decision_card_rejects_non_scope_change():
    engagement = load_engagement("fixtures/crm-engagement.json")
    request = next(item for item in engagement.requests if item.id == "req-defect")
    assessment = DeterministicAssessor().assess(request, engagement)

    try:
        build_decision_card(engagement, assessment, proposal_version=1)
    except ValueError as exc:
        assert "scope_change" in str(exc)
    else:
        raise AssertionError("A decision card must not be created for a defect")
