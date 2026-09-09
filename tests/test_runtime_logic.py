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
