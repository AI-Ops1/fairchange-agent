# Demo video status

The replacement premium cut is being built in [`video/`](../video/) with 1920×1080 Remotion compositions. The narration handoff, scene timings, and trailer copy are in [`demo-video-script.md`](demo-video-script.md). The full judging cut is designed for 3:15 and the trailer for 0:45; both include captions and a replaceable narration layer.

[`artifacts/fairchange-demo.mp4`](../artifacts/fairchange-demo.mp4) is the current 4-minute-36-second, captioned synthetic walkthrough rendered after the audit. The Pages copy is [`fairchange-demo.mp4`](fairchange-demo.mp4).

The public demo page serves the same video from the GitHub Pages origin at [`fairchange-demo.mp4`](fairchange-demo.mp4), so viewers do not depend on the separate raw-file host.

It shows, in one coherent path, the problem and audience, the three classifications, evidence traceability, restart-safe behavior, the owner/client approval gate, and the production authentication boundary without exposing credentials. It makes clear that the public Pages site is a synthetic fixture demo, that independent consultant sessions have not been collected, and that the live AgentCore endpoint is protected. The hackathon's final video must still be public on YouTube or Vimeo; this repository asset alone does not close that submission gate.

To regenerate it locally:

```powershell
.video-venv\Scripts\python.exe scripts\build_demo_video.py
```

The existing audit render is intentionally captioned and voice-free so the workflow is reviewable without audio. It remains available while the new premium Remotion cut is assembled and recorded. Uploading the final narrated cut to a public YouTube or Vimeo URL is a separate final-submission action.
