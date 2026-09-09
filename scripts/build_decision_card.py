"""Build the owner-review card from the persisted real model assessment."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fairchange.resolution import assessment_from_dict, build_decision_card  # noqa: E402
from fairchange.workflow import load_engagement  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", type=Path, default=ROOT / "artifacts" / "demo-state.json")
    parser.add_argument(
        "--output", type=Path, default=ROOT / "artifacts" / "decision-card-v1.json"
    )
    args = parser.parse_args()

    if not args.state.exists():
        raise SystemExit(f"STATE_FILE_MISSING: run scripts/run_demo.py first: {args.state}")
    state = json.loads(args.state.read_text(encoding="utf-8"))
    raw_assessment = state.get("assessments", {}).get("req-addition")
    if raw_assessment is None:
        raise SystemExit("ASSESSMENT_MISSING: req-addition has not been processed yet")

    engagement = load_engagement(ROOT / "fixtures" / "crm-engagement.json")
    assessment = assessment_from_dict(raw_assessment)
    card = build_decision_card(engagement, assessment, proposal_version=1)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(card.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    print(f"DECISION_CARD: {card.proposal_id}")
    print(f"CONTENT_HASH: {card.content_hash}")
    print(f"LIST_PRICE_USD: {card.list_price_usd:.2f}")
    print(f"TRAINING_CREDIT_USD: {card.training_credit_usd:.2f}")
    print(f"NET_PRICE_USD: {card.net_price_usd:.2f}")
    print(f"OUTPUT_FILE: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
