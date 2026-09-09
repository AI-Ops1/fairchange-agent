"""Framework-independent payload handling for the AgentCore entrypoint."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .domain import Engagement, IncomingRequest

MAX_PROMPT_LENGTH = 4_000


def request_from_payload(payload: dict[str, Any], engagement: Engagement) -> IncomingRequest:
    if not isinstance(payload, dict):
        raise ValueError("payload must be a JSON object")
    request_id = payload.get("request_id")
    if request_id is not None:
        if not isinstance(request_id, str) or not request_id.strip():
            raise ValueError("payload.request_id must be a non-empty string")
        for request in engagement.requests:
            if request.id == request_id:
                return request
        raise ValueError(f"Unknown request_id: {request_id}")
    prompt = payload.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("payload.prompt must be a non-empty string")
    prompt = prompt.strip()
    if len(prompt) > MAX_PROMPT_LENGTH:
        raise ValueError(f"payload.prompt must be at most {MAX_PROMPT_LENGTH} characters")
    request_key = payload.get("id", "runtime-request")
    if not isinstance(request_key, str) or not request_key.strip():
        raise ValueError("payload.id must be a non-empty string when supplied")
    request_key = request_key.strip()
    if len(request_key) > 80 or any(char.isspace() for char in request_key):
        raise ValueError("payload.id must be at most 80 characters and contain no whitespace")
    if any(request.id == request_key for request in engagement.requests):
        raise ValueError("payload.id must not reuse a fixture request_id")
    return IncomingRequest(
        id=request_key,
        received_at=str(payload.get("received_at", "runtime")),
        text=prompt,
    )


def assessment_payload(assessment: Any) -> dict[str, Any]:
    return asdict(assessment)
