# Final submission checklist

- [x] Public GitHub repository on `main`: `https://github.com/AI-Ops1/fairchange-agent`
- [x] Updated README with setup, architecture, deployment status, and limitations
- [x] MIT license included
- [x] Deterministic offline demo and 13 automated tests passing in the source environment
- [x] Twenty synthetic evaluation cases with balanced labels and label-isolation checks
- [x] Captioned demo video: [`fairchange-demo.mp4`](../artifacts/fairchange-demo.mp4)
- [x] Public static demo: `https://ai-ops1.github.io/fairchange-agent/`
- [x] Judge-facing architecture, demo, evidence, deployment, limitations, and user-session notes
- [x] Bedrock AgentCore runtime smoke test verified HTTP 200 for `req-defect`
- [x] Production identity provider configured: Amazon Cognito JWT authorizer on AgentCore runtime version 2; unauthenticated 401 and authenticated 200 smoke checks recorded
- [ ] Independent user sessions with external consultants
- [ ] Live public invocation endpoint; the current runtime requires a Cognito bearer token and is not proxied by the static demo
- [ ] Final Devpost submission and any track-specific form submission

The unchecked items are stated explicitly because this repository should not imply external validation or an unauthenticated production endpoint that has not been built.
