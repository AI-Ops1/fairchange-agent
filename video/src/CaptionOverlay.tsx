import type { Caption } from "@remotion/captions";
import { useEffect, useState } from "react";
import { AbsoluteFill, staticFile, useCurrentFrame, useDelayRender, useVideoConfig } from "remotion";

export const CaptionOverlay: React.FC<{ source: string }> = ({ source }) => {
  const [captions, setCaptions] = useState<Caption[] | null>(null);
  const { delayRender, continueRender, cancelRender } = useDelayRender();
  const [handle] = useState(() => delayRender(`Load ${source}`));
  useEffect(() => {
    fetch(staticFile(source))
      .then((response) => response.json())
      .then((data: Caption[]) => { setCaptions(data); continueRender(handle); })
      .catch((error) => cancelRender(error));
  }, [cancelRender, continueRender, handle, source]);

  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!captions) return null;
  const timeMs = (frame / fps) * 1000;
  const active = captions.find((caption) => caption.startMs <= timeMs && caption.endMs > timeMs);
  if (!active) return null;

  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", pointerEvents: "none", paddingBottom: 62 }}>
      <div style={{ maxWidth: 1350, padding: "14px 26px", borderRadius: 18, background: "rgba(5,8,17,.82)", border: "1px solid rgba(255,255,255,.18)", color: "#f5f7ff", fontSize: 32, fontWeight: 650, letterSpacing: "-0.02em", textAlign: "center", boxShadow: "0 14px 50px rgba(0,0,0,.25)" }}>{active.text}</div>
    </AbsoluteFill>
  );
};
