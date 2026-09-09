# FairChange

FairChange is an evidence-backed change-resolution agent for implementation teams. It automates the repetitive work of finding the relevant scope clause, correspondence, and delivery task, then explains whether a client request is a defect, included revision, or scope change. The final commercial decision stays with accountable humans.

The workflow keeps commercial judgment behind a human gate: owners review proposed commercial changes and clients accept the exact proposal before a scope revision is persisted. Routine internal work can proceed under a standing policy.

## Product experience

The [public FairChange workspace](https://ai-ops1.github.io/fairchange-agent/) is the fastest way to understand the product. It uses three synthetic cases to show the complete path: retrieve evidence, classify the request, explain the decision, and place commercial work behind an owner-review and client-acceptance gate. Each case has a plain-language next action so a judge or first-time user can understand the system without knowing the internal S1–S5 labels first.

The [independent session kit](https://ai-ops1.github.io/fairchange-agent/external-session.html) is a separate, no-login usability walkthrough. It creates a local anonymous report and never calls the protected runtime. FairChange is standalone for this hackathon; the evidence-backed flow is designed as a future ScopeLedger capability for surfacing scope risk and preparing governed proposals, not as a current ScopeLedger integration.

### The FairChange mark

![FairChange mark](docs/assets/fairchange-mark.svg)

The logo is a stylized **F** built as a routed decision path. Its three nodes represent the product's core movement: retrieve the evidence, classify what changed, and govern the next action. The mint-to-lavender-to-coral gradient moves from a safe, evidence-backed starting point through analysis to a human-controlled commercial decision. The rounded dark tile gives the mark a calm, dependable workspace feel; it is intentionally softer than a warning or billing icon because FairChange helps teams explain change before anyone commits to it.

## What is implemented

- Typed requests, scope clauses, evidence references, decisions, and tasks.
- Stable event IDs and a persisted cursor for restart-safe intake.
- Strands retrieval tools for scope, correspondence, and task evidence.
- Evidence validation that rejects unsupported citations.
- Defect and included-revision handling without silently converting work into a billable change.
- Owner authorization and client acceptance bound to the exact proposal version and content hash.
- Persisted scope revisions and linked delivery tasks with recoverable state.
- An Amazon Bedrock AgentCore Runtime entrypoint in `main.py`.

The fixture is fictional and contains three cases: a routing defect, an included dashboard revision, and an out-of-scope regional-routing request. Names, correspondence, amounts, and tasks are synthetic; the illustrative hours are human-authored fixture values.

## Judge assets

- [Architecture](docs/architecture.md) — evidence flow, state boundaries, and human gate.
- [Demo script](docs/demo-script.md) — reproducible three-case walkthrough.
- [Judge walkthrough](docs/judge-walkthrough.md) — a two-minute product tour and evaluation prompts.
- [Judging evidence](docs/judging-evidence.md) — capability-to-file and verification map.
- [Evaluation cases](evaluation/README.md) — 20 balanced synthetic cases with isolated labels.
- [Deployment notes](docs/deployment.md) and [limitations](docs/limitations.md).
- [User-session notes](docs/user-sessions.md) — current evidence and open validation work.
- [Independent session kit](docs/external-session.html) and [session protocol](docs/external-session-guide.md) — anonymous, no-login usability session for outside consultants.
- [Captioned demo video](artifacts/fairchange-demo.mp4) and [video notes](docs/demo-video.md).
- [Submission copy](docs/submission-copy.md) and [final checklist](docs/submission-checklist.md).
- [Audit report](docs/audit-2026-09-09.md) — code, runtime, and submission-gate review.

Public demo: [ai-ops1.github.io/fairchange-agent](https://ai-ops1.github.io/fairchange-agent/). It presents synthetic judging fixtures; the [independent session kit](https://ai-ops1.github.io/fairchange-agent/external-session.html) collects no network data; the AgentCore runtime is protected by a Cognito JWT authorizer and is not proxied through the browser demo.

## Deployment status

The AgentCore runtime is deployed in `eu-north-1` and has been verified with the `req-defect` fixture. The invocation returned HTTP 200 and produced an evidence-backed defect assessment citing scope clauses S1 and S5 with a non-billable corrective task.

The runtime uses an Amazon Cognito user pool as its production identity provider. AgentCore validates the bearer JWT at the runtime boundary before the FairChange entrypoint runs; IAM remains the AWS deployment and administration path. Do not put AWS credentials or bearer tokens in a browser bundle or commit them to this repository. The local HMAC token flow is test-only.

## Run locally

Use Python 3.12 or later in a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run the deterministic workflow and its tests:

```powershell
python scripts/run_demo.py --offline
python -m pytest -q
python scripts/run_evaluation.py
```

The workflow writes demo state under `artifacts/`. A second run should process zero new events because the cursor is persisted.

Run the approval-bound resolution demonstration:

```powershell
python scripts/build_decision_card.py
python scripts/approve_resolution.py
python scripts/resume_resolution.py start
python scripts/resume_resolution.py resume
python scripts/resume_resolution.py resume
```

These commands use synthetic data and local test identities only.

## Invoke the deployed runtime

Set the runtime ARN in your shell and use an AWS-authenticated principal with permission to invoke AgentCore for the administrative smoke path:

```powershell
$env:FAIRCHANGE_RUNTIME_ARN = "<your-agent-runtime-arn>"
@'{"request_id":"req-defect"}'@ | Set-Content payload.json
aws bedrock-agentcore invoke-agent-runtime response.json `
  --agent-runtime-arn $env:FAIRCHANGE_RUNTIME_ARN `
  --qualifier DEFAULT `
  --runtime-session-id fairchange-demo-session-000000000000000000000000 `
  --content-type application/json `
  --accept application/json `
  --payload fileb://payload.json `
  --region eu-north-1
Get-Content response.json
```

The runtime accepts either a known fixture `request_id` or a bounded ephemeral `prompt` payload. Fixture IDs are the reproducible judging path; prompt requests are evaluated against the same synthetic engagement and are never persisted as customer records.

For the production user path, obtain a Cognito access token from the configured user pool and send it as `Authorization: Bearer <token>` to the AgentCore runtime endpoint. The deployed configuration and verification evidence are documented in [authentication](docs/authentication.md).

## Repository layout

```text
fairchange/       domain, retrieval, workflow, runtime, and resolution logic
fixtures/         synthetic CRM engagement and evidence
scripts/          demo, approval, and smoke-test entrypoints
tests/            behavioral tests for workflow and authorization boundaries
artifacts/        inspectable synthetic demo outputs
main.py           AgentCore Runtime entrypoint
```

## Hackathon disclosure

This is an independent hackathon project. It does not integrate with ScopeLedger and does not reuse ScopeLedger source code. Any user-validation notes are planning material; no external endorsement or production customer data is claimed.

## License

MIT. See [LICENSE](LICENSE).
