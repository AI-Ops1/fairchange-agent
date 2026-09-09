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
| Agent runtime | `main.py`, `fairchange/runtime.py` | Audited AgentCore runtime version 3 is deployed in `eu-north-1`; fixture and bounded-prompt calls returned HTTP 200 |
| Production identity boundary | `docs/authentication.md`, `docs/deployment.md` | Cognito JWT authorizer is configured on AgentCore version 3; unauthenticated requests return 401 and a Cognito access-token fixture invocation returns 200 |
| Safety disclosure | `README.md`, `docs/architecture.md`, `docs/limitations.md` | Synthetic data, bounded prompt handling, and test-only local HMAC approval tokens are explicit |

The automated suite covers workflow, runtime payload validation, evidence policy, continuation, and approval boundaries. Independent consultant sessions remain open and are not represented as completed evidence. The static page is a public fixture demo, not an unauthenticated production endpoint.
