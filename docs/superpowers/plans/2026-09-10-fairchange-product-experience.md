# FairChange Product Experience Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the vague static FairChange page with a branded, interactive, judge-facing product walkthrough that explains the evidence-backed workflow and human approval boundary in under one minute.

**Architecture:** Keep the secure Python/AgentCore backend unchanged. Build a self-contained static GitHub Pages experience in `docs/index.html` backed by the existing three synthetic cases, add a code-native SVG mark, align the session kit to the same brand, and rewrite the README around the product problem, human supervision, and future ScopeLedger extension.

**Tech Stack:** HTML, CSS, vanilla JavaScript, inline fixture data, SVG, Python `pytest` content checks, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-09-10-fairchange-product-experience-design.md`

## Global Constraints

- Use only synthetic fixture data in the public bundle.
- Do not add AWS credentials, Cognito tokens, analytics, third-party scripts, or customer data to the public pages.
- Preserve the exact fixture truth for `req-defect`, `req-revision`, and `req-addition`.
- Keep the AgentCore runtime and Cognito authorization boundary unchanged.
- Clearly label ScopeLedger integration as a future extension; do not claim current integration.
- Keep the session kit separate from the product workspace and explain its usability-study purpose.
- Preserve a clear disclosure that the public page does not invoke the protected runtime.

---

### Task 1: Add the FairChange brand mark and public-asset tests

**Files:**
- Create: `docs/assets/fairchange-mark.svg`
- Create: `tests/test_public_demo.py`

**Interfaces:**
- Produces the stable browser asset path `assets/fairchange-mark.svg` for both public HTML pages.
- Produces Python tests that subsequent HTML edits must continue to satisfy.

- [ ] **Step 1: Write the failing asset/content tests**

```python
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def test_public_demo_contains_brand_and_three_case_flow():
    html = (DOCS / "index.html").read_text(encoding="utf-8")
    assert 'assets/fairchange-mark.svg' in html
    assert "req-defect" in html
    assert "req-revision" in html
    assert "req-addition" in html
    assert "Owner review" in html
    assert "Client acceptance" in html


def test_public_pages_disclose_synthetic_data_and_avoid_runtime_secrets():
    for path in (DOCS / "index.html", DOCS / "external-session.html"):
        html = path.read_text(encoding="utf-8").lower()
        assert "synthetic" in html
        assert "cognito" in html or "no network" in html
        assert "access_key_id" not in html
        assert "secret_access_key" not in html
        assert "authorization: bearer" not in html


def test_brand_mark_is_local_svg():
    svg = (DOCS / "assets" / "fairchange-mark.svg").read_text(encoding="utf-8")
    assert "<svg" in svg
    assert "<title>FairChange mark</title>" in svg
    assert "linearGradient" in svg
```

- [ ] **Step 2: Run the focused tests to confirm the current page fails the new contract**

Run: `& '.video-venv\Scripts\python.exe' -m pytest -q tests/test_public_demo.py -p no:cacheprovider --basetemp .pytest-tmp-public-red`

Expected: FAIL because the current page has no local SVG mark or interactive approval-flow labels.

- [ ] **Step 3: Create the code-native gradient decision-path mark**

Create a rounded-square SVG with a dark translucent base, a mint-to-coral gradient path, three decision nodes, and the exact accessible title `FairChange mark`. Do not include raster data, external fonts, or brand text inside the mark.

- [ ] **Step 4: Run the focused tests again**

Run: `& '.video-venv\Scripts\python.exe' -m pytest -q tests/test_public_demo.py -p no:cacheprovider --basetemp .pytest-tmp-public-green`

Expected: the local SVG test passes while the page-content assertions remain red until Task 2.

- [ ] **Step 5: Commit the mark and tests**

```powershell
git add docs/assets/fairchange-mark.svg tests/test_public_demo.py
git commit -m "Add FairChange brand mark and public page contract tests"
```

### Task 2: Build the branded interactive judge-facing workspace

**Files:**
- Modify: `docs/index.html`
- Test: `tests/test_public_demo.py`

**Interfaces:**
- Consumes the local mark at `assets/fairchange-mark.svg`.
- Produces a static product workspace with case buttons, evidence panels, decision cards, approval timeline, and a session-kit link.
- Keeps all state in browser memory; no network calls or persisted user data.

- [ ] **Step 1: Replace the current static page with the approved information architecture**

Implement these sections in order: header, hero promise, four-stage flow, interactive case workspace, human-supervision section, ScopeLedger extension note, judge-resource links, and footer disclosures.

- [ ] **Step 2: Add the fixture-backed case model and render function**

Use a local JavaScript object with the three exact cases and render the selected case into request, evidence, decision, next-action, and approval-state regions. The default case should be `req-addition` because it makes the human gate visible immediately.

- [ ] **Step 3: Add plain-language evidence and secondary clause IDs**

Show S1–S5 as readable labels first, with the raw IDs as metadata. Use the approved mappings from the spec and do not introduce claims outside the fixture.

- [ ] **Step 4: Add responsive interaction and accessibility behavior**

Use semantic buttons for case selection, visible focus states, `aria-pressed` on the active case, a live region for decision changes, and a single-column layout below 820px. Respect `prefers-reduced-motion` by disabling decorative transitions.

- [ ] **Step 5: Run the public-page tests and JavaScript parse check**

Run:

```powershell
& '.video-venv\Scripts\python.exe' -m pytest -q tests/test_public_demo.py -p no:cacheprovider --basetemp .pytest-tmp-public-ui
node -e "const fs=require('fs'); const html=fs.readFileSync('docs/index.html','utf8'); const start=html.indexOf('<script>')+8; const end=html.indexOf('</script>',start); if(start<8||end<0) throw new Error('script missing'); new Function(html.slice(start,end)); console.log('public demo JavaScript syntax OK');"
```

Expected: all public-page tests pass and the JavaScript parse check prints success.

- [ ] **Step 6: Commit the interactive workspace**

```powershell
git add docs/index.html tests/test_public_demo.py
git commit -m "Build branded interactive FairChange workspace"
```

### Task 3: Align the external session kit with the product brand

**Files:**
- Modify: `docs/external-session.html`
- Modify: `docs/external-session-guide.md`

**Interfaces:**
- Keeps the existing anonymous report schema and local-only behavior unchanged.
- Produces a visibly related but clearly separate usability-study surface.

- [ ] **Step 1: Add the shared mark, product link, and study framing**

Place the mark and wordmark above the purpose section, link back to the product demo, and state that the page evaluates clarity rather than serving as the product runtime.

- [ ] **Step 2: Improve the case cards without revealing expected answers before completion**

Keep the participant choices independent. Replace unexplained IDs with plain-language evidence labels and retain the glossary. Preserve the existing no-PII notice and no-network behavior.

- [ ] **Step 3: Parse-check the session-kit JavaScript**

Run the same `node -e` script against `docs/external-session.html` and run the existing session tests.

- [ ] **Step 4: Commit the session-kit alignment**

```powershell
git add docs/external-session.html docs/external-session-guide.md
git commit -m "Align independent session kit with FairChange brand"
```

### Task 4: Rewrite the product story and judge-facing README

**Files:**
- Modify: `README.md`
- Modify: `docs/submission-copy.md`
- Modify: `docs/judging-evidence.md`

**Interfaces:**
- Produces a consistent narrative across GitHub and the public demo.
- Does not alter deployment/authentication claims or the existing limitations.

- [ ] **Step 1: Rewrite the README opening around the user problem**

Lead with the repetitive work of checking change requests against signed scope and delivery evidence. Explain the three outcomes and the human supervision boundary before listing implementation details.

- [ ] **Step 2: Add the ScopeLedger extension story with an explicit boundary**

State that FairChange is standalone hackathon code today and could become a ScopeLedger capability for governed change control in the future. Do not claim shared code, current integration, or customer data.

- [ ] **Step 3: Update submission copy and judging evidence**

Describe the new interactive demo as a synthetic, fixture-backed product walkthrough. Point judges to the evidence panel, approval timeline, architecture, and authentication notes.

- [ ] **Step 4: Run content checks and commit the narrative**

Run: `rg -n -i "human|scopeledger|synthetic|cognito|scope change|included revision|defect" README.md docs/submission-copy.md docs/judging-evidence.md`

Then:

```powershell
git add README.md docs/submission-copy.md docs/judging-evidence.md
git commit -m "Rewrite FairChange product and ScopeLedger story"
```

### Task 5: Verify, publish, and record the design result

**Files:**
- Modify: none unless verification finds a concrete defect.
- Test: `tests/test_public_demo.py`, full existing suite.

**Interfaces:**
- Produces a pushed `main` branch and publicly reachable GitHub Pages assets.

- [ ] **Step 1: Run the complete regression suite**

Run: `& '.video-venv\Scripts\python.exe' -m pytest -q -p no:cacheprovider --basetemp .pytest-tmp-product-experience`

Expected: all existing and new tests pass.

- [ ] **Step 2: Check static links and assets locally**

Verify `docs/index.html`, `docs/external-session.html`, and `docs/assets/fairchange-mark.svg` exist; verify every relative link target exists; run `git diff --check`.

- [ ] **Step 3: Push the completed public experience**

```powershell
git push origin main
```

- [ ] **Step 4: Verify GitHub Pages responses**

Check the public root, session-kit URL, and mark URL with `Invoke-WebRequest`. Confirm HTTP 200 and search the returned HTML for the product promise, purpose section, and case labels.

- [ ] **Step 5: Record the final commit and public links**

Update `docs/submission-checklist.md` only for assets that are actually complete. Keep the independent-user, public-runtime, video, and Devpost gates honest if they remain open. Commit any checklist change separately.
