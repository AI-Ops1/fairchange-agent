"""Amazon Bedrock AgentCore entrypoint for the FairChange demo."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Any

from .runtime_logic import assessment_payload, request_from_payload
from .workflow import ModelAssessor, load_engagement


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "crm-engagement.json"


def create_app():
    """Create the AgentCore app lazily so local tests need no cloud SDK."""
    from bedrock_agentcore import BedrockAgentCoreApp
    from strands.models import BedrockModel

    region = os.getenv("AWS_REGION", "eu-north-1")
    model_id = os.getenv("STRANDS_MODEL_ID", "eu.anthropic.claude-sonnet-4-6")
    model_kwargs: dict[str, Any] = {
        "model_id": model_id,
        "region_name": region,
        "max_tokens": 2000,
        "temperature": 0,
    }
    bearer_token = os.getenv("AWS_BEARER_TOKEN_BEDROCK")
    if bearer_token:
        model_kwargs["api_key"] = bearer_token
    model = BedrockModel(**model_kwargs)
    engagement = load_engagement(FIXTURE)
    assessor = ModelAssessor(model, model_id)
    app = BedrockAgentCoreApp()

    @app.entrypoint
    async def invoke(payload: dict[str, Any]) -> dict[str, Any]:
        request = request_from_payload(payload, engagement)
        assessment = await asyncio.to_thread(assessor.assess, request, engagement)
        return {"request_id": request.id, "assessment": assessment_payload(assessment)}

    return app


if __name__ == "__main__":
    create_app().run()
