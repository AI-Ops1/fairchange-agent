# Production authentication

FairChange's AgentCore Runtime version 4 is protected at the service boundary by an Amazon Cognito custom JWT authorizer in `eu-north-1`. The authorizer uses the Cognito discovery document for the `fairchange-prod-users` pool and allows the `fairchange-public` app client. The public client identifier is not a secret; no client secret or AWS credential is stored in this repository.

The request path is:

```text
user signs in with Cognito
  -> Cognito access token
  -> Authorization: Bearer <token>
  -> AgentCore JWT validation
  -> FairChange entrypoint (main.py)
```

Verification was performed against the deployed runtime on 2026-09-09:

- A request without `Authorization` returned HTTP 401.
- The runtime reported `READY` on version 4 with `customJWTAuthorizer` configured and the Cognito discovery URL.
- Immediately before the policy-only version 4 redeploy, a Cognito access token for a synthetic smoke user invoked `{"request_id":"req-defect"}` and a bounded free-form prompt returned HTTP 200.
- An IAM-signed invocation against version 4 was rejected with `Authorization method mismatch`, confirming the OAuth boundary is enforced instead of accepting the deployment credential path.

The static GitHub Pages demo remains intentionally separate. It shows synthetic judging fixtures and never embeds AWS credentials, Cognito passwords, or bearer tokens. A browser-facing proxy would be a separate deployment with its own rate limits, abuse controls, and token handling.

For a new client, provision a user through the Cognito user-pool workflow and issue a short-lived access token through the normal Cognito sign-in flow. Do not copy the synthetic smoke credentials into a product or a submission.
