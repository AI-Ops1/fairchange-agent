# Limitations and next work

- The CRM engagement is synthetic; no customer data is included.
- The local HMAC token signer is a test boundary, not a production identity provider.
- The persisted JSON store is a demo adapter; a production deployment should use a durable shared store.
- The AgentCore runtime is IAM-protected and does not expose a public browser URL.
- The three-case workflow and 20-case labeled evaluation set are synthetic checks. Independent consultant sessions have not yet been collected.
- Model quality, latency, and cost should be measured with fresh cases before production use.
