# Deployment notes

The deployed runtime is an Amazon Bedrock AgentCore Runtime in `eu-north-1`. The public repository intentionally does not contain the account-specific runtime ARN or any credentials.

Set the ARN at invocation time:

```powershell
$env:FAIRCHANGE_RUNTIME_ARN = "<runtime-arn>"
```

Use an AWS-authenticated server-side principal with permission to invoke the runtime. The CloudShell deployment used a dedicated runtime role with a service trust condition and scoped model, logging, tracing, and code-bucket permissions. Replace the bootstrap credentials and root-account workflow with a dedicated deployment identity before production use.

The runtime was verified with:

```json
{"request_id":"req-defect"}
```

It returned status code 200 and a structured defect assessment. The public judging page is available at `https://ai-ops1.github.io/fairchange-agent/`; it presents synthetic fixture results and does not proxy AWS credentials or invoke the protected runtime from the browser. A live public invocation endpoint remains a separate production integration step.
