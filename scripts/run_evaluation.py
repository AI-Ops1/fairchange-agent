"""Validate the synthetic evaluation set without sending labels to an agent."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

EXPECTED = {"defect", "included_revision", "scope_change", "ambiguous"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=Path(__file__).resolve().parents[1] / "evaluation" / "cases.json")
    args = parser.parse_args()
    payload = json.loads(args.cases.read_text(encoding="utf-8"))
    cases = payload["cases"]
    ids = [case["id"] for case in cases]
    assert len(ids) == len(set(ids)), "duplicate evaluation IDs"
    assert len(cases) == 20, f"expected 20 cases, found {len(cases)}"
    counts = {category: 0 for category in EXPECTED}
    for case in cases:
        assert set(case) == {"id", "category", "expected_decision", "request"}
        assert case["category"] in EXPECTED
        assert case["expected_decision"] in EXPECTED
        assert case["category"] == case["expected_decision"]
        assert case["request"].strip()
        # The agent payload contains only the request text; evaluation labels stay here.
        agent_payload = {"id": case["id"], "prompt": case["request"]}
        assert "expected_decision" not in agent_payload
        assert "category" not in agent_payload
        counts[case["category"]] += 1
    print(f"EVALUATION_CASES: {len(cases)}")
    for category in sorted(counts):
        print(f"- {category}: {counts[category]}")
    print("LABELS_OUTSIDE_AGENT_INPUT: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
