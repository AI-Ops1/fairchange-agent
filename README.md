# FairChange

FairChange is an evidence-backed change-resolution agent for GTM implementation consultants. It checks a client request against signed scope, correspondence, and delivery tasks, then classifies the request as a defect, included revision, or scope change and prepares the next safe action.

The workflow keeps commercial judgment behind a human gate: owners review proposed commercial changes and clients accept the exact proposal before a scope revision is persisted. Routine internal work can proceed under a standing policy.

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
- [Judging evidence](docs/judging-evidence.md) — capability-to-file and verification map.
- [Evaluation cases](evaluation/README.md) — 20 balanced synthetic cases with isolated labels.
- [Deployment notes](docs/deployment.md) and [limitations](docs/limitations.md).
- [User-session notes](docs/user-sessions.md) — current evidence and open validation work.
- [Captioned demo video](artifacts/fairchange-demo.mp4) and [video notes](docs/demo-video.md).
- [Submission copy](docs/submission-copy.md) and [final checklist](docs/submission-checklist.md).

The static public demo page is served from [`docs/index.html`](docs/index.html) when GitHub Pages is enabled for the `main` branch. It presents synthetic judging fixtures; the AgentCore runtime itself remains IAM-authenticated.

## Deployment status

The AgentCore runtime is deployed in `eu-north-1` and has been verified with the `req-defect` fixture. The invocation returned HTTP 200 and produced an evidence-backed defect assessment citing scope clauses S1 and S5 with a non-billable corrective task.

The runtime is IAM-authenticated. Do not put AWS credentials in a browser or commit them to this repository. The local HMAC token flow is test-only and must be replaced by the production identity provider before handling real client work.

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

Set the runtime ARN in your shell and use an AWS-authenticated principal with permission to invoke AgentCore:

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

The runtime also accepts a `prompt` payload for exploratory testing, but the fixture `request_id` path is the reproducible judging path.

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
