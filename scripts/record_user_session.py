"""Validate and register one anonymized external-session report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fairchange.user_sessions import SessionRegister, load_session_report


DEFAULT_REGISTER = ROOT / "artifacts" / "external-session-register.jsonl"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", nargs="?", type=Path, help="JSON report exported by docs/external-session.html")
    parser.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    register = SessionRegister(args.register)
    if args.summary:
        print(json.dumps(register.summary(), indent=2, sort_keys=True))
        return 0
    if args.report is None:
        parser.error("provide a report path or use --summary")
    report = load_session_report(json.loads(args.report.read_text(encoding="utf-8")))
    register.append(report)
    print(f"REGISTERED_SESSION: {report.session_code}")
    print(json.dumps(register.summary(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
