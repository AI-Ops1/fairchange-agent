# FairChange product experience redesign

## Outcome

Turn the current read-only synthetic judging page into a clear, branded product walkthrough that lets a first-time visitor understand the problem, inspect the evidence, see the classification, and understand where human approval remains required. The secure AgentCore runtime and its Cognito boundary remain unchanged; the public experience uses only the existing synthetic fixture data.

## Product promise

FairChange turns a client change request into an evidence-backed next action. It automates the repetitive work of finding the relevant scope, correspondence, and delivery records while leaving commercial authorization and final acceptance with people.

The public experience must make this sentence visible in the first viewport. It must also state that the demo is synthetic and that the public page does not invoke the protected runtime.

## Recommended architecture

Use a single static GitHub Pages experience in `docs/index.html` with local HTML, CSS, and JavaScript. Keep all interaction client-side and fixture-backed:

```text
visitor
  -> FairChange product shell
  -> case selector (req-defect / req-revision / req-addition)
  -> evidence view
  -> classification and next-action view
  -> human approval boundary
```

No AWS credentials, Cognito tokens, analytics, third-party scripts, or customer data may enter the public bundle. The static page is a product walkthrough, not a proxy to AgentCore.

## Information architecture

### Header

- FairChange decision-path mark and wordmark.
- Small descriptor: `scope decisions, made legible`.
- Links: `How it works`, `Try a case`, `Repository`.
- A compact `Synthetic workspace` status chip.

### Hero

- Headline: a clear outcome rather than an implementation description.
- Supporting copy explains the repetitive task and the human decision boundary.
- Primary action scrolls to the interactive workspace.
- Secondary action opens the repository.
- A small four-stage flow previews `Intake → Evidence → Decision → Human gate`.

### Interactive workspace

- Three case buttons with human-readable titles and outcome labels.
- A prominent request card showing what the client asked for.
- An evidence panel split into `Signed scope`, `Correspondence`, and `Delivery task`.
- Each evidence item shows the plain-language meaning first and the clause/task ID second.
- A decision panel with one of `Defect`, `Included revision`, or `Scope change`.
- A `Next safe action` card that states exactly what the team should do.
- For scope changes, an approval timeline shows `Owner review` and `Client acceptance` as required before work begins.
- A “why this decision?” disclosure exposes the evidence references without forcing visitors to read raw JSON.

### Trust and extension section

- “Human-supervised by design” explains that retrieval, classification, and drafting are automated but commercial authority is not.
- A “Built to extend ScopeLedger” paragraph describes a future integration without claiming the hackathon project currently shares code or data with ScopeLedger.
- Links to the public session kit and repository.

### Footer

- Synthetic-data disclosure.
- AgentCore/Cognito trust-boundary disclosure.
- MIT license and repository link.

## Case content

The UI will preserve the current fixture truth:

| Case | Plain-language title | Decision | Next safe action |
| --- | --- | --- | --- |
| `req-defect` | Qualifying leads are going to an inactive representative | Defect | Create a non-billable corrective task |
| `req-revision` | Move the conversion chart above the pipeline chart | Included revision | Update the existing delivery task using the remaining revision |
| `req-addition` | Add UK and Canada routing | Scope change | Prepare an owner-review proposal; wait for owner and client approval |

The S1–S5 labels remain available as secondary references, but the primary labels are:

- S1: active-representative routing
- S2: dashboard revision allowance
- S3: administrator training deliverable
- S4: additional countries excluded
- S5: acceptance failures corrected without an extra fee

## Brand direction

- Mark: a branching decision path contained in a rounded square, communicating evidence, choice, and controlled progress.
- Palette: ink navy base with soft mint, coral, lavender, and warm gold gradients; avoid large solid saturated blocks.
- Surface: layered translucent cards, subtle borders, low-noise radial gradients, and deliberate whitespace.
- Type: high-contrast display treatment for the promise and compact uppercase metadata for system state.
- Tone: calm, precise, and commercially aware; avoid “AI magic” language.

## Session kit relationship

The session kit remains a separate usability-study surface. It receives the same mark, palette, and plain-language glossary, but it must not be presented as the product workspace. Its purpose is to collect independent judgments about whether the evidence and decisions are understandable. It continues to avoid network upload, credentials, customer data, and third-party tracking.

## README changes

Rewrite the opening around:

1. The repetitive scope-decision problem.
2. FairChange’s evidence-backed workflow.
3. The human supervision boundary.
4. The current synthetic/public demo experience.
5. The future ScopeLedger extension point, clearly labelled as future integration.
6. Judge assets, deployment/authentication truth, and limitations.

## Verification

- Preserve and run the complete Python test suite.
- Parse-check the page JavaScript.
- Check every public link and asset path.
- Verify the page renders at desktop and narrow viewport widths.
- Confirm no secret, token, analytics script, or third-party data sink is introduced.
- Confirm the three displayed decisions match the deterministic fixture and existing judging evidence.

## Non-goals

- No unauthenticated proxy to AgentCore.
- No replacement of Cognito or runtime authorization.
- No real customer data.
- No claim of current ScopeLedger integration.
- No external analytics or participant tracking.
