# Limitations and next work

- The CRM engagement is synthetic; no customer data is included.
- The local HMAC token signer is a test boundary; production runtime access now uses Amazon Cognito JWT validation at AgentCore.
- The persisted JSON store is a demo adapter; a production deployment should use a durable shared store.
- The AgentCore runtime requires a Cognito bearer token for user invocations and does not expose an unauthenticated public browser URL.
- The three-case workflow and 20-case labeled evaluation set are synthetic checks. Independent consultant sessions have not yet been collected.
- Model quality, latency, and cost should be measured with fresh cases before production use.
