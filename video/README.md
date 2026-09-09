# FairChange premium video

This Remotion project contains two 1920×1080 compositions:

- `FairChangeJudging` — the 3:15 judging cut.
- `FairChangeTrailer` — the 0:45 trailer.

The scene timing and narration handoff live in [`../docs/demo-video-script.md`](../docs/demo-video-script.md). The current render uses the branded motion system, local caption JSON, and a quiet ambient bed. The narration layer is intentionally replaceable so the founder's recorded scene takes can be dropped in later.

## Preview and render

```powershell
npm install
npm run dev
npx remotion still FairChangeJudging --frame=30 --output=out/fairchange-video-still.png --bundle-cache
npx remotion render FairChangeTrailer out/fairchange-trailer.mp4 --codec=h264 --bundle-cache --concurrency=4
npx remotion render FairChangeJudging out/fairchange-judging.mp4 --codec=h264 --bundle-cache --concurrency=4
```

The output folder is ignored by Git. Replace the caption JSON and add the recorded voiceover as a local audio asset when the narration is ready; keep credentials and private material out of the project.
