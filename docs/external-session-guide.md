# Independent session guide

The public [external session kit](external-session.html) is a privacy-safe, no-login walkthrough for implementation consultants and delivery leads. It uses only the three fictional fixture cases and performs no network upload. A participant receives a fresh anonymous session code, makes an independent classification for each case, records confidence and whether the evidence trail was traceable, then returns the generated JSON through a channel agreed with the study owner.

## Protocol

1. Send the participant the public session-kit URL and ask them to complete it without coaching.
2. Do not provide the expected labels before the participant finishes.
3. Accept only the generated JSON report. Do not request names, email addresses, company names, customer data, credentials, or screen recordings.
4. Validate the report locally with `scripts/record_user_session.py` and keep the local register outside the repository.
5. Record a session as independent evidence only when the participant is outside the build team and completed the session themselves.

The session kit is a collection tool, not product telemetry. It intentionally does not expose the protected AgentCore runtime or accept user credentials. The three cases are synthetic, so session notes measure usability and evidence traceability rather than customer performance.

## Registering a returned report

```powershell
python scripts/record_user_session.py path\to\session-xxxxxxxx.json
python scripts/record_user_session.py --summary
```

The register is written to `artifacts/external-session-register.jsonl` by default. Keep that file local; do not commit participant reports or private feedback to GitHub. The validator rejects duplicate session codes, incomplete case responses, timestamps without timezones, and common email/phone patterns in notes.
