# Founder walkthrough record

**Status:** The public, privacy-safe session kit is published; no independent consultant sessions are claimed until anonymized reports are received and validated.

- **Participant:** founder/operator, internal validation only.
- **Data:** fictional CRM engagement from `fixtures/crm-engagement.json`.
- **Cases reviewed:** `req-defect`, `req-revision`, and `req-addition`.
- **Baseline:** manually inspect the scope, correspondence, estimate, and task records.
- **Assisted path:** run `scripts/run_demo.py --offline`, inspect `artifacts/demo-state.json`, then run the approval-bound resolution scripts.
- **Observed result:** all three cases were classified with cited evidence; the extra request required owner review; the resolution flow paused until owner and client test approvals were present.
- **Consent and attribution:** this is an internal walkthrough, not an external testimonial.

No outreach was sent without a recipient and channel explicitly approved by the founder. The kit is available at [`docs/external-session.html`](external-session.html), with the protocol in [`docs/external-session-guide.md`](external-session-guide.md).

## Ready-to-run session kit

Each external session uses a fresh anonymous session code and the same three synthetic cases (`req-defect`, `req-revision`, `req-addition`). The kit records only start/end timestamps, case order, role category, confidence, whether the participant could trace the evidence, and one short usability note. It performs no network upload. Do not collect customer data, credentials, or identifying information. The repository's evaluation cases remain offline evidence; they are not substitutes for independent human sessions.
