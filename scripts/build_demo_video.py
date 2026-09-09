"""Build a short captioned FairChange judge demo video."""
from __future__ import annotations

from pathlib import Path
from textwrap import wrap

import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "fairchange-demo.mp4"
WIDTH, HEIGHT = 1280, 720
FPS = 30

BG = (10, 18, 32)
PANEL = (20, 32, 52)
TEXT = (238, 244, 252)
MUTED = (166, 184, 207)
ACCENT = (70, 190, 165)
AMBER = (245, 178, 74)
RED = (241, 111, 111)


def font(size: int, bold: bool = False):
    path = Path("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf")
    return ImageFont.truetype(str(path), size)


def frame(title: str, subtitle: str, bullets: list[str], tag: str, color=ACCENT):
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, WIDTH, 12), fill=color)
    draw.text((70, 54), "FAIRCHANGE", font=font(24, True), fill=color)
    draw.text((70, 112), title, font=font(46, True), fill=TEXT)
    y = 190
    for paragraph in [subtitle, *bullets]:
        lines = wrap(paragraph, width=58)
        for line in lines:
            draw.text((78, y), line, font=font(28 if paragraph == subtitle else 26), fill=MUTED if paragraph == subtitle else TEXT)
            y += 40
        y += 18
    draw.rounded_rectangle((70, 620, 1210, 680), radius=16, fill=PANEL, outline=(50, 74, 103), width=2)
    draw.text((95, 636), tag, font=font(22, True), fill=color)
    draw.text((930, 636), "Synthetic walkthrough • Cognito-protected runtime", font=font(18), fill=MUTED)
    return image


def scene(title, subtitle, bullets, tag, seconds, color=ACCENT):
    image = frame(title, subtitle, bullets, tag, color)
    return [image] * int(seconds * FPS)


scenes = []
scenes += scene(
    "FairChange",
    "An evidence-backed change-resolution agent for GTM implementation teams.",
    ["A client request arrives after delivery has started.", "The consultant must decide: defect, included work, or paid change.", "FairChange makes the evidence and next safe action inspectable."],
    "01  End-to-end walkthrough", 15.0)
scenes += scene(
    "The problem and the person",
    "Implementation consultants and delivery leads lose time debating what the signed scope already covers.",
    ["Defects should be fixed without an extra charge.", "Included revisions should not be resold.", "True additions need a controlled commercial decision."],
    "02  Problem → professional audience → impact", 20.0)
scenes += scene(
    "One engagement, read-only evidence",
    "The agent retrieves facts before it classifies a request.",
    ["Signed scope clauses and scope version", "Prior correspondence and approved estimates", "Existing delivery tasks, status, and acceptance criteria"],
    "03  Evidence sources", 20.0)
scenes += scene(
    "The working flow",
    "Request → Strands retrieval → structured assessment → policy checks → next safe action.",
    ["Retrieval tools can inspect the synthetic fixture but cannot send messages.", "Every assessment must cite the incoming request and supporting records.", "Commercial work stops at a human gate."],
    "04  AgentCore + Strands + evidence validation", 22.0)
scenes += scene(
    "Case 1: defect protection",
    "`req-defect` says qualifying US leads are being assigned to an inactive representative.",
    ["Scope S1 requires assignment to an active representative.", "Scope S5 says acceptance-criteria failures are corrected without an additional fee.", "Result: defect; non-billable corrective task."],
    "05  req-defect → defect", 18.0, ACCENT)
scenes += scene(
    "Case 2: included work",
    "`req-revision` asks to move the conversion chart above the pipeline chart.",
    ["Scope S2 includes two dashboard revision rounds.", "The evidence shows one round remains unused.", "Result: included_revision; update the existing delivery task."],
    "06  req-revision → included_revision", 18.0, ACCENT)
scenes += scene(
    "Case 3: governed addition",
    "`req-addition` asks for UK and Canada routing and suggests trading unstarted training for it.",
    ["Scope S4 excludes additional countries and requires authorization and acceptance.", "The estimate and correspondence are attached as evidence.", "Result: scope_change; billable proposal and owner review required."],
    "07  req-addition → scope_change", 20.0, AMBER)
scenes += scene(
    "The commercial boundary stays human",
    "A model assessment is not permission to change the contract.",
    ["FairChange creates an exact proposal version and content hash.", "The owner authorizes that exact proposal.", "The client accepts that exact version; only then is a scope revision and delivery task persisted."],
    "08  Owner authorization → client acceptance", 25.0, AMBER)
scenes += scene(
    "The decision survives interruption",
    "The resolution continuation pauses at the human steps and can resume later.",
    ["PAUSED: waiting_for=owner", "RESUMED: waiting_for=client", "RESUMED: status=completed; event=client_accepted"],
    "09  Restart-safe human gate", 20.0)
scenes += scene(
    "The intake cursor is idempotent",
    "The same workflow can be restarted without duplicating work.",
    ["First offline run: PROCESSED_REQUESTS: 3", "Second run with the same state: PROCESSED_REQUESTS: 0", "The cursor, assessments, and tasks remain inspectable in artifacts/."],
    "10  Durable workflow", 16.0)
scenes += scene(
    "Evaluation without label leakage",
    "The repository includes a balanced synthetic evaluation set for review.",
    ["20 cases: 5 ambiguous, 5 defect, 5 included_revision, 5 scope_change", "Expected labels stay outside the agent payload.", "The set is a reproducibility check, not a claim of customer performance."],
    "11  Synthetic evaluation evidence", 20.0)
scenes += scene(
    "Production identity boundary",
    "The deployed Amazon Bedrock AgentCore runtime is protected before the application entrypoint runs.",
    ["No bearer token: HTTP 401.", "Cognito-authenticated {request_id: req-defect}: HTTP 200 with S1/S5 evidence.", "The public Pages demo never embeds AWS credentials or user tokens."],
    "12  Cognito JWT → AgentCore → FairChange", 25.0, AMBER)
scenes += scene(
    "What is public and what is not",
    "Judges can inspect the repository, architecture, synthetic fixture, evaluation set, and Pages demo.",
    ["The Pages site is a read-only synthetic judging demo.", "The live runtime requires a Cognito bearer token and is not exposed through a browser proxy.", "Independent consultant sessions have not been collected and are not claimed."],
    "13  Honest limits", 22.0, RED)
scenes += scene(
    "FairChange",
    "Make scope decisions explainable before they become commercial surprises.",
    ["Repository: github.com/AI-Ops1/fairchange-agent", "Public demo: ai-ops1.github.io/fairchange-agent/", "Track: Professional Agents · MIT licensed"],
    "14  End", 15.0)

OUT.parent.mkdir(parents=True, exist_ok=True)
with imageio.get_writer(OUT, fps=FPS, codec="libx264", quality=8, macro_block_size=1) as writer:
    for image in scenes:
        writer.append_data(np.asarray(image))
print(f"VIDEO: {OUT}")
print(f"SECONDS: {len(scenes) / FPS:.1f}")


