from __future__ import annotations

import pytest

from fairchange.runtime_logic import request_from_payload
from fairchange.workflow import load_engagement


def test_runtime_payload_can_select_a_fixture_request():
    engagement = load_engagement("fixtures/crm-engagement.json")
    request = request_from_payload({"request_id": "req-addition"}, engagement)
    assert request.id == "req-addition"
    assert "UK and Canada" in request.text


def test_runtime_payload_requires_a_known_request_or_prompt():
    engagement = load_engagement("fixtures/crm-engagement.json")
    with pytest.raises(ValueError, match="prompt"):
        request_from_payload({}, engagement)
    with pytest.raises(ValueError, match="Unknown request_id"):
        request_from_payload({"request_id": "missing"}, engagement)


def test_runtime_payload_creates_a_bounded_ephemeral_request_for_prompt():
    engagement = load_engagement("fixtures/crm-engagement.json")
    request = request_from_payload(
        {"id": "runtime-001", "prompt": "Please review this change request."}, engagement
    )
    assert request.id == "runtime-001"
    assert request.text == "Please review this change request."


def test_runtime_payload_rejects_fixture_id_reuse_and_oversized_prompt():
    engagement = load_engagement("fixtures/crm-engagement.json")
    with pytest.raises(ValueError, match="must not reuse"):
        request_from_payload({"id": "req-defect", "prompt": "x"}, engagement)
    with pytest.raises(ValueError, match="at most"):
        request_from_payload({"prompt": "x" * 4001}, engagement)
