# Judge walkthrough

Use the [public FairChange workspace](https://ai-ops1.github.io/fairchange-agent/) for a two-minute product tour. It is a synthetic fixture workspace, so no login or customer data is required.

1. Start with **Try the synthetic workspace**. The selected request asks for UK and Canada routing while suggesting that an unstarted training deliverable be dropped to stay within budget.
2. Read the **Evidence trail** before the answer. S4 excludes additional countries and regional routing; S3 shows that training is unstarted; the delivery task records the dependency.
3. Read **FairChange decision** and **Next safe action**. The result is **Scope change**, with an owner-review proposal required before work starts.
4. Look at the **human gate**: owner review comes first, followed by exact client acceptance. FairChange prepares the evidence-backed proposal; people retain commercial authority.
5. Select the other two cases to see the policy boundary: the inactive-representative routing issue is a no-fee defect, while the chart reorder uses the remaining included revision.

For independent usability evidence, use the [session kit](https://ai-ops1.github.io/fairchange-agent/external-session.html). It is a separate no-login page with three fictional cases. The participant's anonymous JSON report is created locally and is never uploaded by the page.

## What to evaluate

- **Clarity:** Can a first-time user tell what the request is, what evidence supports it, and what happens next?
- **Governance:** Is it obvious that the agent cannot approve a commercial change by itself?
- **Traceability:** Can each outcome be explained with a scope clause, correspondence item, or delivery task?
- **Boundary:** Is the distinction between the public synthetic demo and the protected Cognito-authenticated AgentCore runtime clear?

The standalone FairChange workspace is designed as a future ScopeLedger capability for surfacing scope risk and preparing governed proposals. It does not claim a current ScopeLedger integration.
