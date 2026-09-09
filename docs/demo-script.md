# Judge demo script

Target length: 3–4 minutes. All inputs are fictional and labeled synthetic.

## 1. Show the problem (30 seconds)

FairChange reviews a change request against the signed scope and delivery record. The goal is to avoid charging for defects or included work while routing true additions through owner review and client acceptance.

## 2. Run the three-case local workflow (60 seconds)

```powershell
python scripts/run_demo.py --offline --state artifacts/judge-demo-state.json
```

Expected output:

```text
PROCESSED_REQUESTS: 3
- req-defect: defect; evidence=3
- req-revision: included_revision; evidence=3
- req-addition: scope_change; evidence=5
```

Run the same command again with the same state file. It should report zero new requests, demonstrating the persisted cursor.

## 3. Show the decision boundary (45 seconds)

Open `artifacts/decision-card-v1.json`. The extra routing request produces an owner-review proposal. It is not silently marked non-billable, and no external message is sent automatically.

## 4. Show the human gate (45 seconds)

```powershell
python scripts/approve_resolution.py
python scripts/resume_resolution.py start
python scripts/resume_resolution.py resume
python scripts/resume_resolution.py resume
```

The continuation pauses for owner authorization, then client acceptance, then persists the accepted scope revision and linked delivery task. The local tokens are test-only.

## 5. Show the deployed runtime (30 seconds)

Invoke the AgentCore runtime with the `req-defect` payload from the README. The verified response returned HTTP 200 and cited S1 and S5 before proposing a non-billable corrective task.

## Judge takeaway

FairChange makes the evidence and approval boundary inspectable. It does not claim autonomous commercial authority, customer data, or measured savings.
