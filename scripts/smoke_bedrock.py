"""Small, explicit Bedrock smoke test for action 3.

The script intentionally reads credentials through the normal AWS credential
chain. It never accepts or prints secret keys. Run it only after installing
requirements and enabling model access in the AWS account.
"""

from __future__ import annotations

import os
import sys
import getpass


def main() -> int:
    try:
        import boto3
        from strands import Agent
        from strands.models import BedrockModel
    except ImportError as exc:
        print(f"DEPENDENCY_MISSING: {exc}")
        print("Install requirements.txt inside the project .venv first.")
        return 2

    region = os.getenv("AWS_REGION", "eu-north-1")
    model_id = os.getenv("STRANDS_MODEL_ID", "eu.anthropic.claude-sonnet-4-6")
    credentials = boto3.Session(region_name=region).get_credentials()
    bearer_token = os.getenv("AWS_BEARER_TOKEN_BEDROCK")
    if credentials is None and not bearer_token and sys.stdin.isatty():
        bearer_token = getpass.getpass("Temporary Amazon Bedrock API key (hidden): ")
        if bearer_token:
            os.environ["AWS_BEARER_TOKEN_BEDROCK"] = bearer_token
    if credentials is None and not bearer_token:
        print("AWS_CREDENTIALS_MISSING: configure an approved AWS credential source locally.")
        return 3

    print(f"Invoking Strands model {model_id} in {region} ...")
    # Keep this connectivity probe deliberately tiny; new AWS accounts can
    # have very small daily token quotas while access is being established.
    bedrock_model = BedrockModel(
        model_id=model_id,
        region_name=region,
        max_tokens=64,
        temperature=0,
    )
    agent = Agent(model=bedrock_model)
    try:
        result = agent(
            "Reply with exactly the word READY. This is a connectivity smoke test; do not use tools."
        )
    except Exception as exc:
        print(f"MODEL_CALL_FAILED: {type(exc).__name__}: {exc}")
        response = getattr(exc, "response", None)
        if isinstance(response, dict):
            error = response.get("Error", {})
            if error.get("Code"):
                print(f"AWS_ERROR_CODE: {error['Code']}")
            if error.get("Message"):
                print(f"AWS_ERROR_MESSAGE: {error['Message']}")
        return 4
    print(f"MODEL_RESPONSE: {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
