# Final submission checklist

- [x] Public GitHub repository on `main`: `https://github.com/AI-Ops1/fairchange-agent`
- [x] Updated README with setup, architecture, deployment status, and limitations
- [x] MIT license included
- [x] Deterministic offline demo and automated tests passing in the source environment
- [x] Twenty synthetic evaluation cases with balanced labels and label-isolation checks
- [ ] Final captioned walkthrough video regenerated after the audit and uploaded publicly to YouTube or Vimeo (maximum 5 minutes)
- [x] Public static demo: `https://ai-ops1.github.io/fairchange-agent/`
- [x] Judge-facing architecture, demo, evidence, deployment, limitations, and user-session notes
- [x] Audited Bedrock AgentCore runtime version 3 deployed; unauthenticated 401, Cognito access-token `req-defect` 200, and bounded-prompt 200 smoke checks recorded
- [x] Production identity provider configured: Amazon Cognito JWT authorizer preserved on AgentCore runtime version 3
- [ ] Independent user sessions with external consultants
- [ ] Live public invocation endpoint; the current runtime requires a Cognito bearer token and is not proxied by the static demo
- [ ] Final Devpost submission and any track-specific form submission

The unchecked items are stated explicitly because this repository should not imply external validation, a completed public video submission, or an unauthenticated production endpoint that has not been built.
