# Demo video

[`artifacts/fairchange-demo.mp4`](../artifacts/fairchange-demo.mp4) is a 42-second, captioned walkthrough of the FairChange judging path.

It shows the evidence sources, the three classifications, the human approval boundary, restart-safe cursor behavior, and the verified AgentCore runtime. The video uses the repository's synthetic fixture and makes no claim of independent customer validation.

To regenerate it locally:

```powershell
.video-venv\Scripts\python.exe scripts\build_demo_video.py
```

The render is intentionally captioned and voice-free so the workflow is reviewable without audio.
