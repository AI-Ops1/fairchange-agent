"""Start or resume the persisted human-decision continuation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fairchange.resolution_store import JsonResolutionStore, decision_card_from_dict  # noqa: E402
from fairchange.session import JsonResolutionSessionStore  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("start", "resume"))
    parser.add_argument(
        "--card", type=Path, default=ROOT / "artifacts" / "decision-card-v1.json"
    )
    parser.add_argument(
        "--resolution-state",
        type=Path,
        default=ROOT / "artifacts" / "resolution-state.json",
    )
    parser.add_argument(
        "--session-state",
        type=Path,
        default=ROOT / "artifacts" / "resolution-session.json",
    )
    args = parser.parse_args()

    session_store = JsonResolutionSessionStore(args.session_state)
    resolution_store = JsonResolutionStore(args.resolution_state)
    if args.phase == "start":
        if not args.card.exists():
            raise SystemExit(f"DECISION_CARD_MISSING: {args.card}")
        card = decision_card_from_dict(json.loads(args.card.read_text(encoding="utf-8")))
        session = session_store.start(card)
        print(f"PAUSED: {session.continuation_id}; waiting_for={session.waiting_for}")
    else:
        session = session_store.resume(resolution_store)
        print(
            f"RESUMED: {session.continuation_id}; status={session.status}; "
            f"waiting_for={session.waiting_for}; event={session.last_event}"
        )
    print(f"SESSION_FILE: {args.session_state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
