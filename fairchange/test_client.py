"""Test-only authenticated client for the local human-approval demo.

The token signer here is deliberately small and local. It demonstrates the
approval boundary without pretending to be a production identity provider.
Production deployment should replace it with the host application's identity
and authorization service.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
from dataclasses import dataclass

from .approval import AcceptanceRecord
from .resolution import DecisionCard
from .resolution_store import JsonResolutionStore


class AuthenticationError(ValueError):
    """Raised when a test token cannot be verified for the requested role."""


def issue_test_token(identity: str, role: str, secret: str) -> str:
    """Issue a signed local token for the test client."""
    identity = identity.strip()
    role = role.strip()
    if not identity or not role or not secret:
        raise AuthenticationError("Test token identity, role, and secret are required")
    payload = _encode({"sub": identity, "role": role})
    return f"fc1.{payload}.{_sign(payload, secret)}"


@dataclass(frozen=True)
class AuthenticatedResolutionClient:
    store: JsonResolutionStore
    secret: str

    def authorize(
        self,
        proposal_id: str,
        owner_token: str,
        proposal_version: int,
        content_hash: str,
    ) -> DecisionCard:
        identity = _verify(owner_token, self.secret, expected_role="owner")
        return self.store.authorize(proposal_id, identity, proposal_version, content_hash)

    def accept(
        self,
        proposal_id: str,
        client_token: str,
        proposal_version: int,
        content_hash: str,
    ) -> AcceptanceRecord:
        identity = _verify(client_token, self.secret, expected_role="client")
        return self.store.accept(proposal_id, identity, proposal_version, content_hash)


def _verify(token: str, secret: str, expected_role: str) -> str:
    if not secret:
        raise AuthenticationError("Test client secret is required")
    try:
        scheme, payload, signature = token.split(".", 2)
        if scheme != "fc1":
            raise ValueError
        expected_signature = _sign(payload, secret)
        if not hmac.compare_digest(signature, expected_signature):
            raise ValueError
        claims = json.loads(_decode(payload))
        if claims.get("role") != expected_role or not str(claims.get("sub", "")).strip():
            raise ValueError
        return str(claims["sub"]).strip()
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise AuthenticationError("Invalid test authentication token") from exc


def _sign(payload: str, secret: str) -> str:
    return hmac.new(secret.encode("utf-8"), payload.encode("ascii"), hashlib.sha256).hexdigest()


def _encode(value: dict[str, str]) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _decode(value: str) -> str:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4)).decode("utf-8")
