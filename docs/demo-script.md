# Judge demo script

Target length: 4–5 minutes, within the hackathon's five-minute limit. All inputs are fictional and labeled synthetic.

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
python scripts/resume_resolution.py start
python scripts/approve_resolution.py --phase owner
python scripts/resume_resolution.py resume
python scripts/approve_resolution.py --phase client
python scripts/resume_resolution.py resume
```

The continuation pauses for owner authorization, then client acceptance, then persists the accepted scope revision and linked delivery task. The local tokens are test-only. `python scripts/approve_resolution.py` remains available as a compact all-phases shortcut for the offline fixture.

## 5. Show the production identity boundary (30 seconds)

Show the protected AgentCore runtime boundary without exposing credentials: an unauthenticated request is rejected with HTTP 401, while a short-lived Cognito-authenticated request for `req-defect` returns HTTP 200 and cites S1 and S5 before proposing a non-billable corrective task. The static Pages demo remains intentionally separate and never embeds a token.

## 6. Close with the honest limits (15 seconds)

State that the fixture and evaluation set are synthetic, independent consultant sessions have not yet been collected, and the public Pages link is a read-only judging demo. Point judges to the repository's authentication, limitations, and checklist notes.

## Judge takeaway

FairChange makes the evidence and approval boundary inspectable. It does not claim autonomous commercial authority, customer data, or measured savings.
