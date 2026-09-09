# FairChange architecture

```mermaid
flowchart LR
    U[Consultant or owner] -->|request_id or prompt| C[AWS-authenticated caller]
    C --> R[Amazon Bedrock AgentCore Runtime]
    R --> A[Strands assessment agent]
    A --> T[Read-only retrieval tools]
    T --> F[(Synthetic CRM fixture)]
    A --> D[Evidence-backed decision]
    D --> G{Human gate}
    G -->|defect or included revision| I[Internal task]
    G -->|scope change| O[Owner authorization]
    O --> K[Exact proposal version and hash]
    K --> V[Client acceptance]
    V --> S[Persisted scope revision and delivery task]
```

The deployed runtime receives JSON and returns a structured assessment. Retrieval is read-only: the model can inspect the fixture's scope clauses, correspondence, estimates, and existing tasks but cannot send messages or change scope directly.

The local workflow persists a cursor, assessments, and internal tasks in replace-based JSON state. The resolution workflow persists the proposal, owner authorization, client acceptance, scope revision, and delivery task as one recoverable state update. The local HMAC client is explicitly a test boundary; production identity should be supplied by the host application's identity provider.

The runtime is IAM-authenticated. A production caller should use a least-privilege role with `bedrock-agentcore:InvokeAgentRuntime` and model permissions only where required. AWS credentials belong on the server side, never in a browser.
