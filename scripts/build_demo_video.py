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
    draw.text((980, 636), "Synthetic demo • IAM-protected runtime", font=font(18), fill=MUTED)
    return image


def scene(title, subtitle, bullets, tag, seconds, color=ACCENT):
    image = frame(title, subtitle, bullets, tag, color)
    return [image] * int(seconds * FPS)


scenes = []
scenes += scene(
    "FairChange",
    "Evidence-backed change resolution for GTM implementation work.",
    ["Check the request against signed scope.", "Protect defects and included work from accidental billing.", "Route true additions through human authorization."],
    "01  Problem → governed resolution", 4.5)
scenes += scene(
    "One request, three evidence sources",
    "FairChange reads the synthetic engagement before deciding.",
    ["Signed scope clauses", "Prior correspondence and approved estimates", "Existing delivery tasks and statuses"],
    "02  Retrieval is read-only", 4.5)
scenes += scene(
    "Three decisions from one workflow",
    "The deterministic demo processes the complete fixture.",
    ["req-defect → defect; non-billable corrective task", "req-revision → included_revision; use remaining round", "req-addition → scope_change; owner review required"],
    "03  PROCESSED_REQUESTS: 3", 7.0)
scenes += scene(
    "The commercial boundary stays human",
    "A scope change cannot silently become a free or paid commitment.",
    ["Owner authorizes the exact proposal version.", "Client accepts the exact proposal content hash.", "Only then does FairChange persist a scope revision and delivery task."],
    "04  Owner review → client acceptance", 6.5, AMBER)
scenes += scene(
    "Restart-safe by construction",
    "The persisted cursor prevents duplicate work after a restart.",
    ["First run: three new events", "Second run: zero new events", "State remains inspectable in artifacts/"],
    "05  Durable workflow boundary", 4.5)
scenes += scene(
    "Verified on Amazon Bedrock AgentCore",
    "The deployed runtime accepts an IAM-authenticated JSON request.",
    ["Region: eu-north-1", "Payload: {request_id: req-defect}", "Response: HTTP 200 with S1/S5 evidence and a non-billable fix"],
    "06  Runtime verified", 6.0)
scenes += scene(
    "What this demo claims",
    "The evidence is reproducible and the limits are explicit.",
    ["Synthetic CRM data only", "Local HMAC tokens are test-only", "Independent consultant sessions and a public HTTPS facade remain next work"],
    "07  Honest limitations", 5.0, RED)
scenes += scene(
    "FairChange",
    "Make scope decisions explainable before they become commercial surprises.",
    ["Source: github.com/AI-Ops1/fairchange-agent", "Run: python scripts/run_demo.py --offline", "Track: Professional Agents"],
    "08  End", 4.0)

OUT.parent.mkdir(parents=True, exist_ok=True)
with imageio.get_writer(OUT, fps=FPS, codec="libx264", quality=8, macro_block_size=1) as writer:
    for image in scenes:
        writer.append_data(np.asarray(image))
print(f"VIDEO: {OUT}")
print(f"SECONDS: {len(scenes) / FPS:.1f}")


