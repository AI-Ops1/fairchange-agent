"""Run the local test-client owner authorization and client acceptance flow."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fairchange.resolution_store import JsonResolutionStore, decision_card_from_dict  # noqa: E402
from fairchange.test_client import AuthenticatedResolutionClient, issue_test_token  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--card", type=Path, default=ROOT / "artifacts" / "decision-card-v1.json"
    )
    parser.add_argument(
        "--store", type=Path, default=ROOT / "artifacts" / "resolution-state.json"
    )
    parser.add_argument("--owner-id", default="owner-demo")
    parser.add_argument("--client-id", default="client-demo")
    parser.add_argument(
        "--test-secret",
        default=os.getenv("FAIRCHANGE_TEST_SECRET", "local-demo-secret"),
        help="Local test-only signing secret; use FAIRCHANGE_TEST_SECRET outside the demo.",
    )
    args = parser.parse_args()

    if not args.card.exists():
        raise SystemExit(f"DECISION_CARD_MISSING: run scripts/build_decision_card.py first: {args.card}")
    card = decision_card_from_dict(json.loads(args.card.read_text(encoding="utf-8")))
    store = JsonResolutionStore(args.store)
    store.save_draft(card)
    client = AuthenticatedResolutionClient(store, args.test_secret)
    owner_token = issue_test_token(args.owner_id, "owner", args.test_secret)
    client_token = issue_test_token(args.client_id, "client", args.test_secret)

    state = store.load()
    existing = state.proposals.get(card.proposal_id)
    if existing and existing.get("owner_status") == "authorized":
        authorized = decision_card_from_dict(existing)
    else:
        authorized = client.authorize(
            card.proposal_id, owner_token, card.proposal_version, card.content_hash
        )
    record = client.accept(
        authorized.proposal_id,
        client_token,
        authorized.proposal_version,
        authorized.content_hash,
    )
    print(f"OWNER_AUTHORIZED: {authorized.owner_id}")
    print(f"CLIENT_ACCEPTED: {record.client_id}")
    print(f"SCOPE_CHANGE: {record.change_id}; version={record.accepted_scope_version}")
    print(f"DELIVERY_TASK: {record.delivery_task_id}; status=ready")
    print(f"STATE_FILE: {args.store}")
    print("TEST_ONLY_AUTH: local HMAC tokens; replace with the deployed identity provider.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
