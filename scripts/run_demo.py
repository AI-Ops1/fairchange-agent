"""Run FairChange's first persisted intake-to-internal-task workflow."""

from __future__ import annotations

import argparse
import getpass
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fairchange.workflow import (  # noqa: E402
    DeterministicAssessor,
    ModelAssessor,
    JsonWorkflowStore,
    load_engagement,
    process_pending_requests,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true", help="Use deterministic assessor; no AWS call")
    parser.add_argument("--fixture", type=Path, default=ROOT / "fixtures" / "crm-engagement.json")
    parser.add_argument("--state", type=Path, default=ROOT / "artifacts" / "demo-state.json")
    args = parser.parse_args()

    engagement = load_engagement(args.fixture)
    if args.offline:
        assessor = DeterministicAssessor()
    else:
        import boto3
        from strands.models import BedrockModel

        region = os.getenv("AWS_REGION", "eu-north-1")
        model_id = os.getenv("STRANDS_MODEL_ID", "eu.anthropic.claude-sonnet-4-6")
        # Resolve credentials before constructing the model so a prompted
        # bearer token is available to Strands at client initialization.
        bearer_token = os.getenv("AWS_BEARER_TOKEN_BEDROCK")
        if (
            boto3.Session(region_name=region).get_credentials() is None
            and not bearer_token
            and sys.stdin.isatty()
        ):
            token = getpass.getpass("Temporary Amazon Bedrock API key (hidden): ")
            if token:
                bearer_token = token
        if boto3.Session(region_name=region).get_credentials() is None and not bearer_token:
            raise SystemExit("AWS_CREDENTIALS_MISSING: run the smoke test credential flow first.")
        model_kwargs = {
            "model_id": model_id,
            "region_name": region,
            "max_tokens": 2000,
            "temperature": 0,
        }
        if bearer_token:
            model_kwargs["api_key"] = bearer_token
        model = BedrockModel(**model_kwargs)
        assessor = ModelAssessor(model, model_id)

    assessments = process_pending_requests(engagement, JsonWorkflowStore(args.state), assessor)
    print(f"PROCESSED_REQUESTS: {len(assessments)}")
    for item in assessments:
        print(f"- {item.request_id}: {item.decision}; evidence={len(item.evidence)}")
    print(f"STATE_FILE: {args.state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
