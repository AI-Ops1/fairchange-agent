# Judging evidence checklist

| Capability | Evidence in repository | Verification |
|---|---|---|
| Evidence-backed classification | `fairchange/workflow.py`, `fairchange/retrieval.py` | Every assessment validates cited source IDs |
| Defect protection | `tests/test_workflow.py`, `artifacts/demo-state.json` | `req-defect` is non-billable |
| Included revision handling | `artifacts/demo-state.json` | `req-revision` consumes the remaining revision |
| Scope-change governance | `fairchange/domain.py`, `fairchange/approval.py` | Billable tasks require owner review; scope changes cannot be silently non-billable |
| Restart safety | `fairchange/store.py`, `scripts/run_demo.py` | Re-running the same state processes zero events |
| Exact human authorization | `fairchange/resolution_store.py`, `tests/test_resolution_store.py` | Version and content-hash mismatches are rejected |
| Client acceptance | `fairchange/test_client.py`, `tests/test_test_client.py` | Owner and client roles are distinct in the test boundary |
| Agent runtime | `main.py`, `fairchange/runtime.py` | Audited AgentCore runtime version 4 is READY in `eu-north-1`; the pre-redeploy fixture and bounded-prompt calls returned HTTP 200 |
| Production identity boundary | `docs/authentication.md`, `docs/deployment.md` | Cognito JWT authorizer is configured on AgentCore version 4; unauthenticated requests return 401 and IAM-signed invocation is rejected by the OAuth boundary |
| Safety disclosure | `README.md`, `docs/architecture.md`, `docs/limitations.md` | Synthetic data, bounded prompt handling, and test-only local HMAC approval tokens are explicit |
| Product clarity | `docs/index.html`, `docs/assets/fairchange-mark.svg` | Public interactive workspace shows the three-case flow, evidence trail, next safe action, and human gate without exposing the runtime |
| Independent usability | `docs/external-session.html`, `docs/external-session-guide.md` | Separate no-login kit creates a local anonymous report and keeps the participant's classification independent |

The automated suite covers workflow, runtime payload validation, evidence policy, continuation, approval boundaries, and the public product contract. Independent consultant sessions remain open and are not represented as completed evidence. The public page is a synthetic fixture workspace, not an unauthenticated production endpoint.
