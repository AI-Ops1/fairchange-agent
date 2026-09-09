"""Framework-independent payload handling for the AgentCore entrypoint."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .domain import Engagement, IncomingRequest


def request_from_payload(payload: dict[str, Any], engagement: Engagement) -> IncomingRequest:
    request_id = payload.get("request_id")
    if request_id:
        for request in engagement.requests:
            if request.id == request_id:
                return request
        raise ValueError(f"Unknown request_id: {request_id}")
    prompt = payload.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("payload.prompt must be a non-empty string")
    return IncomingRequest(
        id=str(payload.get("id", "runtime-request")),
        received_at=str(payload.get("received_at", "runtime")),
        text=prompt.strip(),
    )


def assessment_payload(assessment: Any) -> dict[str, Any]:
    return asdict(assessment)
