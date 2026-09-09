# Judging evidence checklist

| Capability | Evidence in repository | Verification |
|---|---|---|
| Evidence-backed classification | `fairchange/workflow.py`, `fairchange/retrieval.py` | Every assessment validates cited source IDs |
| Defect protection | `tests/test_workflow.py`, `artifacts/demo-state.json` | `req-defect` is non-billable |
| Included revision handling | `artifacts/demo-state.json` | `req-revision` consumes the remaining revision |
| Scope-change governance | `fairchange/domain.py`, `fairchange/approval.py` | Scope changes require owner review and cannot be silently non-billable |
| Restart safety | `fairchange/store.py`, `scripts/run_demo.py` | Re-running the same state processes zero events |
| Exact human authorization | `fairchange/resolution_store.py`, `tests/test_resolution_store.py` | Version and content-hash mismatches are rejected |
| Client acceptance | `fairchange/test_client.py`, `tests/test_test_client.py` | Owner and client roles are distinct in the test boundary |
| Agent runtime | `main.py`, `fairchange/runtime.py` | AgentCore runtime verified in `eu-north-1` with HTTP 200 |
| Safety disclosure | `README.md`, `docs/architecture.md` | Synthetic data and test-only authentication are explicit |

The project has 13 passing automated tests. Independent consultant sessions and production identity-provider integration remain open limitations and are not represented as completed evidence.
