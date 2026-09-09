# Demo video

[`artifacts/fairchange-demo.mp4`](../artifacts/fairchange-demo.mp4) is a 42-second, captioned walkthrough of the FairChange judging path.

The public demo page serves the same video from the GitHub Pages origin at [`fairchange-demo.mp4`](fairchange-demo.mp4), so viewers do not depend on the separate raw-file host.

It shows the evidence sources, the three classifications, the human approval boundary, restart-safe cursor behavior, and the verified AgentCore runtime. The video uses the repository's synthetic fixture and makes no claim of independent customer validation.

To regenerate it locally:

```powershell
.video-venv\Scripts\python.exe scripts\build_demo_video.py
```

The render is intentionally captioned and voice-free so the workflow is reviewable without audio.
