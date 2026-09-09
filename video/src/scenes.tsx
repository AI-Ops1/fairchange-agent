import { Img, AbsoluteFill, Easing, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import type { ReactNode } from "react";
import type { VideoScene } from "./sceneData";

const INK = "#090d19";
const TEXT = "#f5f7ff";
const MUTED = "#a7b1c9";
const LINE = "rgba(177,194,231,.2)";
const PANEL = "rgba(20,27,48,.76)";

const ease = Easing.bezier(0.16, 1, 0.3, 1);

const motion = (frame: number, fps: number, delay = 0, stiffness = 110) => spring({
  frame: Math.max(0, frame - delay),
  fps,
  config: { damping: 18, mass: 0.72, stiffness },
});

const reveal = (value: number) => interpolate(value, [0, 1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

const Brand: React.FC<{ compact?: boolean }> = ({ compact = false }) => (
  <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
    <Img src={staticFile("fairchange-mark.svg")} style={{ width: compact ? 42 : 56, height: compact ? 42 : 56 }} />
    <div style={{ display: "grid", gap: 2 }}>
      <span style={{ fontSize: compact ? 22 : 28, fontWeight: 800, letterSpacing: "-0.04em", color: TEXT }}>FairChange</span>
      {!compact && <span style={{ color: MUTED, fontSize: 13, letterSpacing: "0.12em", textTransform: "uppercase" }}>scope decisions, made legible</span>}
    </div>
  </div>
);

const SceneShell: React.FC<{ scene: VideoScene; children: ReactNode }> = ({ scene, children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const appear = interpolate(frame, [0, 13], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const lift = interpolate(frame, [0, 16], [30, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const pulse = spring({ frame, fps, config: { damping: 200, mass: 0.7, stiffness: 90 } });
  return (
    <AbsoluteFill style={{ background: `radial-gradient(circle at 83% 14%, ${scene.accent}24, transparent 32%), radial-gradient(circle at 12% 88%, #3b5d8a22, transparent 38%), ${INK}`, color: TEXT, opacity: appear }}>
      <div style={{ position: "absolute", inset: 0, opacity: 0.16, backgroundImage: "radial-gradient(rgba(255,255,255,.32) .7px, transparent .7px)", backgroundSize: "7px 7px", maskImage: "linear-gradient(to bottom, black, transparent 90%)" }} />
      <div style={{ position: "absolute", top: 52, left: 72, right: 72, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <Brand compact />
        <div style={{ color: MUTED, fontSize: 14, letterSpacing: "0.12em", textTransform: "uppercase" }}>Professional Agents · synthetic walkthrough</div>
      </div>
      <div style={{ position: "absolute", inset: 0, translate: `0px ${lift}px`, scale: 0.985 + pulse * 0.015 }}>{children}</div>
      <div style={{ position: "absolute", bottom: 38, left: 72, right: 72, display: "flex", justifyContent: "space-between", alignItems: "center", color: MUTED, fontSize: 13 }}>
        <span>{scene.label}</span><span style={{ color: scene.accent }}>FAIRCHANGE / {String(scene.from).padStart(3, "0")}s</span>
      </div>
    </AbsoluteFill>
  );
};

const Eyebrow: React.FC<{ children: ReactNode; color: string }> = ({ children, color }) => <div style={{ color, fontSize: 16, fontWeight: 800, letterSpacing: "0.17em", textTransform: "uppercase" }}>{children}</div>;

const BigTitle: React.FC<{ children: ReactNode; size?: number }> = ({ children, size = 78 }) => <h1 style={{ margin: "18px 0 0", maxWidth: 1000, color: TEXT, fontSize: size, lineHeight: 1.02, letterSpacing: "-0.065em", fontWeight: 760 }}>{children}</h1>;

const Pill: React.FC<{ children: ReactNode; color: string }> = ({ children, color }) => <span style={{ display: "inline-flex", alignItems: "center", gap: 8, border: `1px solid ${color}55`, background: `${color}12`, color, borderRadius: 999, padding: "9px 14px", fontSize: 14, fontWeight: 750, letterSpacing: "0.05em", textTransform: "uppercase" }}>{children}</span>;

const Panel: React.FC<{ children: ReactNode; style?: React.CSSProperties; accent?: string }> = ({ children, style, accent }) => <div style={{ border: `1px solid ${accent ? `${accent}45` : LINE}`, borderRadius: 22, background: PANEL, boxShadow: "0 28px 90px rgba(0,0,0,.26)", ...style }}>{children}</div>;

const Dot: React.FC<{ color: string; size?: number }> = ({ color, size = 14 }) => <span style={{ display: "inline-block", width: size, height: size, borderRadius: "50%", background: color, boxShadow: `0 0 0 ${size / 2}px ${color}18` }} />;

const RequestCard: React.FC<{ label: string; quote: string; accent: string }> = ({ label, quote, accent }) => <Panel accent={accent} style={{ width: 900, padding: 34, background: `linear-gradient(135deg, ${accent}14, rgba(255,255,255,.035))` }}><div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}><Pill color={accent}>{label}</Pill><span style={{ color: MUTED, fontSize: 14 }}>client request / synthetic</span></div><div style={{ marginTop: 32, fontSize: 42, lineHeight: 1.15, letterSpacing: "-0.04em", fontWeight: 680 }}>“{quote}”</div></Panel>;

const Step: React.FC<{ n: string; title: string; text: string; color: string; active?: boolean }> = ({ n, title, text, color, active = false }) => <div style={{ display: "flex", gap: 18, alignItems: "flex-start", flex: 1, minWidth: 0 }}><div style={{ width: 52, height: 52, display: "grid", placeItems: "center", borderRadius: 16, border: `1px solid ${active ? color : LINE}`, background: active ? `${color}18` : "rgba(255,255,255,.03)", color: active ? color : MUTED, fontWeight: 850, fontSize: 17 }}>{n}</div><div><div style={{ color: TEXT, fontSize: 21, fontWeight: 750 }}>{title}</div><div style={{ marginTop: 8, color: MUTED, fontSize: 15, lineHeight: 1.4 }}>{text}</div></div></div>;

const Record: React.FC<{ title: string; meta: string; color: string; top: number; left: number; enterX: number; enterY: number; delay: number }> = ({ title, meta, color, top, left, enterX, enterY, delay }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = spring({ frame: Math.max(0, frame - delay), fps, config: { damping: 18, mass: 0.72, stiffness: 110 } });
  const x = interpolate(progress, [0, 1], [enterX, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const y = interpolate(progress, [0, 1], [enterY, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const opacity = interpolate(progress, [0, 0.18, 1], [0, 0.85, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const scale = interpolate(progress, [0, 1], [0.92, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return <Panel accent={color} style={{ position: "absolute", width: 490, padding: 22, top, left, opacity, transform: `translate3d(${x}px, ${y}px, 0) scale(${scale})`, transformOrigin: "center left", background: "rgba(20,27,48,.92)" }}><div style={{ display: "flex", gap: 13, alignItems: "center" }}><Dot color={color} /><div><div style={{ color: TEXT, fontSize: 18, fontWeight: 740 }}>{title}</div><div style={{ color: MUTED, fontSize: 13, marginTop: 3 }}>{meta}</div></div></div></Panel>;
};

const EvidenceCard: React.FC<{ id: string; title: string; text: string; color: string }> = ({ id, title, text, color }) => <Panel accent={color} style={{ padding: 19, flex: 1, minWidth: 0 }}><div style={{ display: "flex", justifyContent: "space-between", color, fontSize: 12, fontWeight: 800, letterSpacing: "0.12em", textTransform: "uppercase" }}><span>signed scope</span><span>{id}</span></div><div style={{ color: TEXT, fontSize: 18, fontWeight: 750, marginTop: 14 }}>{title}</div><div style={{ color: MUTED, fontSize: 14, lineHeight: 1.4, marginTop: 8 }}>{text}</div></Panel>;

const OutcomeScene: React.FC<{ scene: VideoScene; outcome: string; next: string; evidence: Array<{ id: string; title: string; text: string }>; color: string }> = ({ scene, outcome, next, evidence, color }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const heading = motion(frame, fps, 7);
  const cards = evidence.map((_, index) => motion(frame, fps, 24 + index * 16));
  const result = motion(frame, fps, 52, 95);
  const action = motion(frame, fps, 70, 95);
  return <SceneShell scene={scene}><div style={{ position: "absolute", top: 187, left: 160, right: 160 }}><div style={{ opacity: reveal(heading), transform: `translate3d(0, ${interpolate(heading, [0, 1], [22, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}px, 0)` }}><Eyebrow color={color}>{scene.eyebrow}</Eyebrow><div style={{ display: "flex", justifyContent: "space-between", gap: 40, alignItems: "end" }}><div><BigTitle size={64}>{scene.title}</BigTitle><p style={{ maxWidth: 760, margin: "22px 0 0", color: MUTED, fontSize: 23 }}>{scene.body}</p></div><div style={{ opacity: reveal(result), transform: `scale(${interpolate(result, [0, 1], [0.78, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })})` }}><Pill color={color}>{outcome}</Pill></div></div></div><div style={{ display: "flex", gap: 18, marginTop: 56 }}>{evidence.map((item, index) => <div key={item.id} style={{ flex: 1, minWidth: 0, opacity: reveal(cards[index]), transform: `translate3d(0, ${interpolate(cards[index], [0, 1], [28, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}px, 0)`, boxShadow: frame >= 38 + index * 16 ? `0 0 0 1px ${color}25, 0 18px 55px ${color}12` : "none", borderRadius: 22 }}><EvidenceCard {...item} color={color} /></div>)}</div><div style={{ opacity: reveal(action), transform: `translate3d(0, ${interpolate(action, [0, 1], [24, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}px, 0)` }}><Panel accent={color} style={{ display: "flex", justifyContent: "space-between", gap: 30, alignItems: "center", marginTop: 22, padding: "18px 24px", background: `${color}0e` }}><div style={{ color: MUTED, fontSize: 14, letterSpacing: "0.1em", textTransform: "uppercase" }}>next safe action</div><div style={{ color: TEXT, fontSize: 20, fontWeight: 700 }}>{next}</div></Panel></div></div></SceneShell>;
};

const HookScene: React.FC<{ scene: VideoScene }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const request = motion(frame, fps, 4);
  const outcomes = [motion(frame, fps, 28), motion(frame, fps, 39), motion(frame, fps, 50)];
  return <SceneShell scene={scene}><div style={{ position: "absolute", top: 250, left: 170, right: 170, display: "flex", alignItems: "center", justifyContent: "space-between", gap: 70 }}><div style={{ maxWidth: 700 }}><Eyebrow color={scene.accent}>{scene.eyebrow}</Eyebrow><BigTitle>{scene.title}</BigTitle><p style={{ margin: "26px 0 0", color: MUTED, fontSize: 27, lineHeight: 1.4 }}>{scene.body}</p></div><div style={{ position: "relative", opacity: reveal(request), transform: `translate3d(${interpolate(request, [0, 1], [70, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}px, 0, 0) scale(${interpolate(request, [0, 1], [0.94, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })})` }}><RequestCard label="REQ-ADDITION" quote="Could you add routing for our UK and Canada teams?" accent={scene.accent} /><div style={{ display: "flex", justifyContent: "center", gap: 16, marginTop: 22 }}><div style={{ opacity: reveal(outcomes[0]), transform: `translateY(${interpolate(outcomes[0], [0, 1], [18, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}px)` }}><Pill color="#8af0c0">Defect</Pill></div><div style={{ opacity: reveal(outcomes[1]), transform: `translateY(${interpolate(outcomes[1], [0, 1], [18, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}px)` }}><Pill color="#b8b1ff">Included work</Pill></div><div style={{ opacity: reveal(outcomes[2]), transform: `translateY(${interpolate(outcomes[2], [0, 1], [18, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}px)` }}><Pill color="#f5c36a">Scope change</Pill></div></div></div></div></SceneShell>;
};

const RecordsScene: React.FC<{ scene: VideoScene }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const trailProgress = spring({ frame: Math.max(0, frame - 45), fps, config: { damping: 200, mass: 0.7, stiffness: 90 } });
  return <SceneShell scene={scene}><div style={{ position: "absolute", top: 190, left: 170, right: 170 }}><Eyebrow color={scene.accent}>{scene.eyebrow}</Eyebrow><BigTitle size={64}>{scene.title}</BigTitle><p style={{ margin: "22px 0 0", color: MUTED, fontSize: 23 }}>{scene.body}</p><div style={{ display: "flex", gap: 100, marginTop: 70, alignItems: "center" }}><div style={{ position: "relative", width: 530, height: 300 }}><Record title="Signed scope" meta="S1 · S3 · S4 · S5" color="#8af0c0" top={0} left={0} enterX={-420} enterY={-34} delay={2} /><Record title="Correspondence" meta="approved request thread" color="#b8b1ff" top={104} left={48} enterX={420} enterY={0} delay={14} /><Record title="Delivery tasks" meta="status · acceptance · dependencies" color="#ff9c8e" top={208} left={96} enterX={-340} enterY={34} delay={27} /></div><div style={{ width: 220, height: 2, opacity: interpolate(trailProgress, [0, 1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }), transform: `scaleX(${interpolate(trailProgress, [0, 1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })})`, transformOrigin: "left center", background: `linear-gradient(90deg, ${scene.accent}, transparent)` }} /><Panel accent={scene.accent} style={{ flex: 1, padding: 28, opacity: interpolate(trailProgress, [0, 1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }), transform: `translate3d(${interpolate(trailProgress, [0, 1], [30, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}px, 0, 0)` }}><div style={{ color: scene.accent, fontSize: 13, fontWeight: 800, letterSpacing: "0.12em", textTransform: "uppercase" }}>evidence trail</div><div style={{ marginTop: 18, color: TEXT, fontSize: 28, fontWeight: 750, letterSpacing: "-0.03em" }}>One request.<br />One defensible answer.</div><div style={{ marginTop: 25, color: MUTED, fontSize: 16 }}>Every assessment must cite the records it used.</div></Panel></div></div></SceneShell>;
};

const PromiseScene: React.FC<{ scene: VideoScene }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const copy = motion(frame, fps, 8);
  const mark = motion(frame, fps, 22, 85);
  return <SceneShell scene={scene}><div style={{ position: "absolute", top: 245, left: 260, right: 260, display: "flex", justifyContent: "space-between", alignItems: "center", gap: 90 }}><div style={{ opacity: reveal(copy), transform: `translate3d(${interpolate(copy, [0, 1], [-36, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}px, 0, 0)` }}><Eyebrow color={scene.accent}>{scene.eyebrow}</Eyebrow><BigTitle size={76}>{scene.title}</BigTitle><p style={{ margin: "25px 0 0", color: scene.accent, fontSize: 37, fontWeight: 700, letterSpacing: "-0.04em" }}>{scene.body}</p></div><div style={{ display: "grid", placeItems: "center", gap: 20, opacity: reveal(mark), transform: `translate3d(0, ${interpolate(mark, [0, 1], [40, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}px, 0) scale(${interpolate(mark, [0, 1], [0.74, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })}) rotate(${interpolate(mark, [0, 1], [-12, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}deg)` }}><Img src={staticFile("fairchange-mark.svg")} style={{ width: 230, height: 230, filter: "drop-shadow(0 20px 40px rgba(138,240,192,.22))" }} /><span style={{ color: MUTED, fontSize: 15, letterSpacing: "0.1em", textTransform: "uppercase" }}>evidence → decision → gate</span></div></div></SceneShell>;
};

const FlowScene: React.FC<{ scene: VideoScene }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const steps = [motion(frame, fps, 8), motion(frame, fps, 20), motion(frame, fps, 32), motion(frame, fps, 44)];
  const traveller = interpolate(frame, [18, 112], [2, 98], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  return <SceneShell scene={scene}><div style={{ position: "absolute", top: 195, left: 150, right: 150 }}><Eyebrow color={scene.accent}>{scene.eyebrow}</Eyebrow><BigTitle size={67}>{scene.title}</BigTitle><p style={{ margin: "22px 0 0", color: MUTED, fontSize: 23 }}>{scene.body}</p><div style={{ position: "relative", display: "flex", gap: 34, marginTop: 75, alignItems: "center" }}><div style={{ position: "absolute", top: -34, left: `${traveller}%`, width: 32, height: 32, transform: "translateX(-50%)", opacity: interpolate(frame, [18, 30], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }), filter: "drop-shadow(0 0 18px rgba(138,240,192,.55))" }}><Img src={staticFile("fairchange-mark.svg")} style={{ width: 32, height: 32 }} /></div><div style={{ flex: 1, opacity: reveal(steps[0]), transform: `translateY(${interpolate(steps[0], [0, 1], [24, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}px)` }}><Step n="01" title="Intake" text="Capture the request" color="#8af0c0" active /></div><div style={{ flex: 0.2, height: 2, background: "linear-gradient(90deg,#8af0c0,#b8b1ff)" }} /><div style={{ flex: 1, opacity: reveal(steps[1]), transform: `translateY(${interpolate(steps[1], [0, 1], [24, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}px)` }}><Step n="02" title="Evidence" text="Retrieve the receipts" color="#b8b1ff" active /></div><div style={{ flex: 0.2, height: 2, background: "linear-gradient(90deg,#b8b1ff,#ff9c8e)" }} /><div style={{ flex: 1, opacity: reveal(steps[2]), transform: `translateY(${interpolate(steps[2], [0, 1], [24, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}px)` }}><Step n="03" title="Decision" text="Name what changed" color="#ff9c8e" active /></div><div style={{ flex: 0.2, height: 2, background: "linear-gradient(90deg,#ff9c8e,#f5c36a)" }} /><div style={{ flex: 1, opacity: reveal(steps[3]), transform: `translateY(${interpolate(steps[3], [0, 1], [24, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}px)` }}><Step n="04" title="Human gate" text="Protect the commitment" color="#f5c36a" active /></div></div></div></SceneShell>;
};

const GateScene: React.FC<{ scene: VideoScene }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const copy = motion(frame, fps, 7);
  const owner = motion(frame, fps, 24, 95);
  const client = motion(frame, fps, 56, 95);
  const line = motion(frame, fps, 42, 90);
  return <SceneShell scene={scene}><div style={{ position: "absolute", top: 220, left: 180, right: 180, display: "flex", gap: 90, alignItems: "center" }}><div style={{ width: 730, opacity: reveal(copy), transform: `translate3d(${interpolate(copy, [0, 1], [-28, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}px, 0, 0)` }}><Eyebrow color={scene.accent}>{scene.eyebrow}</Eyebrow><BigTitle size={70}>{scene.title}</BigTitle><p style={{ margin: "24px 0 0", color: MUTED, fontSize: 25, lineHeight: 1.45 }}>{scene.body}</p><div style={{ display: "flex", gap: 12, marginTop: 38 }}><Pill color="#8af0c0">No silent scope revision</Pill><Pill color="#f5c36a">Exact version</Pill></div></div><Panel accent={scene.accent} style={{ width: 620, padding: 30, background: `linear-gradient(145deg, ${scene.accent}15, rgba(255,255,255,.03))` }}><div style={{ color: MUTED, fontSize: 13, fontWeight: 800, letterSpacing: "0.13em", textTransform: "uppercase" }}>commercial gate</div><div style={{ display: "flex", alignItems: "center", gap: 18, marginTop: 32 }}><div style={{ display: "grid", placeItems: "center", gap: 10, width: 160, color: TEXT, fontWeight: 750, opacity: reveal(owner), transform: `translateY(${interpolate(owner, [0, 1], [24, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}px)` }}><div style={{ width: 62, height: 62, display: "grid", placeItems: "center", borderRadius: "50%", color: "#091018", background: "#8af0c0", fontSize: 26 }}>1</div>Owner review</div><div style={{ flex: 1, height: 2, transform: `scaleX(${reveal(line)})`, transformOrigin: "left center", background: `linear-gradient(90deg,#8af0c0,${scene.accent})` }} /><div style={{ display: "grid", placeItems: "center", gap: 10, width: 160, color: TEXT, opacity: reveal(client), transform: `translateY(${interpolate(client, [0, 1], [24, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}px)` }}><div style={{ width: 62, height: 62, display: "grid", placeItems: "center", borderRadius: "50%", color: "#15101a", background: "#f5c36a", fontSize: 26 }}>2</div>Client acceptance</div></div><div style={{ marginTop: 28, paddingTop: 20, borderTop: `1px solid ${LINE}`, color: MUTED, fontSize: 15 }}>The agent can prepare the proposal. It cannot authorize the commitment.</div></Panel></div></SceneShell>;
};

const WORKSPACE_CASES = [
  { label: "Inactive rep assignment", requestId: "req-defect", title: "Qualifying US leads need active reps", evidence: [{ id: "S1", title: "Active representative", text: "Every qualifying lead must reach an active representative." }, { id: "S5", title: "No-fee correction", text: "Acceptance failures are corrected without an extra fee." }], action: "Create a non-billable corrective task.", color: "#8af0c0" },
  { label: "Chart layout revision", requestId: "req-revision", title: "Move the conversion chart above the pipeline", evidence: [{ id: "S2", title: "Two revision rounds", text: "One dashboard revision round remains unused." }, { id: "TASK", title: "Layout change", text: "The request changes chart order, not the feature set." }], action: "Update the existing delivery task.", color: "#b8b1ff" },
  { label: "UK + Canada routing", requestId: "req-addition", title: "Add UK and Canada routing for the regional teams", evidence: [{ id: "S4", title: "Additional countries excluded", text: "Regional routing is outside the signed scope." }, { id: "S3", title: "Training is unstarted", text: "A proposed substitution needs review." }], action: "Prepare an owner-review proposal.", color: "#f5c36a" },
] as const;

const WorkspaceScene: React.FC<{ scene: VideoScene }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const activeIndex = Math.min(WORKSPACE_CASES.length - 1, Math.floor(frame / 180));
  const activeCase = WORKSPACE_CASES[activeIndex];
  const panel = motion(frame, fps, 8);
  const cursorY = interpolate(frame, [0, 180, 360], [85, 152, 219], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  return <SceneShell scene={scene}><div style={{ position: "absolute", top: 170, left: 130, right: 130, opacity: reveal(panel), transform: `translateY(${interpolate(panel, [0, 1], [24, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}px)` }}><Eyebrow color={scene.accent}>{scene.eyebrow}</Eyebrow><div style={{ display: "flex", justifyContent: "space-between", alignItems: "end" }}><div><BigTitle size={60}>{scene.title}</BigTitle><p style={{ margin: "18px 0 0", color: MUTED, fontSize: 21 }}>{scene.body}</p></div><Pill color="#8af0c0">synthetic workspace</Pill></div><Panel accent={scene.accent} style={{ marginTop: 40, overflow: "hidden", background: "#10182a" }}><div style={{ height: 52, display: "flex", alignItems: "center", gap: 10, padding: "0 20px", borderBottom: `1px solid ${LINE}`, color: MUTED, fontSize: 13 }}><Dot color="#ff7d8b" size={9} /><Dot color="#f5c36a" size={9} /><Dot color="#8af0c0" size={9} /><span style={{ marginLeft: 12 }}>FairChange / decision workspace</span></div><div style={{ display: "grid", gridTemplateColumns: "230px 1fr", minHeight: 370 }}><div style={{ position: "relative", padding: 20, borderRight: `1px solid ${LINE}`, background: "rgba(255,255,255,.025)" }}><div style={{ color: MUTED, fontSize: 12, letterSpacing: "0.13em", textTransform: "uppercase" }}>case library · 3</div>{WORKSPACE_CASES.map((item, i) => <div key={item.label} style={{ position: "relative", marginTop: 17, padding: 12, borderRadius: 11, border: `1px solid ${i === activeIndex ? `${item.color}88` : LINE}`, background: i === activeIndex ? `${item.color}15` : "transparent", color: i === activeIndex ? TEXT : MUTED, fontSize: 14, boxShadow: i === activeIndex ? `0 0 0 2px ${item.color}15` : "none" }}>{String(i + 1).padStart(2, "0")} · {item.label}</div>)}<div style={{ position: "absolute", right: -10, top: cursorY, color: activeCase.color, fontSize: 24, filter: `drop-shadow(0 0 8px ${activeCase.color})` }}>◀</div></div><div style={{ padding: 25 }}><div style={{ color: MUTED, fontSize: 12, letterSpacing: "0.12em", textTransform: "uppercase" }}>request · {activeCase.requestId}</div><div style={{ color: TEXT, fontSize: 27, fontWeight: 750, marginTop: 10 }}>{activeCase.title}</div><div style={{ display: "flex", gap: 14, marginTop: 24 }}>{activeCase.evidence.map((item) => <EvidenceCard key={item.id} id={item.id} title={item.title} text={item.text} color={activeCase.color} />)}</div><div style={{ marginTop: 20, color: activeCase.color, fontSize: 16, fontWeight: 750 }}>Next safe action · {activeCase.action}</div></div></div></Panel></div></SceneShell>;
};

const SessionScene: React.FC<{ scene: VideoScene }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const copy = motion(frame, fps, 7);
  const cards = [motion(frame, fps, 20), motion(frame, fps, 32), motion(frame, fps, 44)];
  const report = motion(frame, fps, 66, 95);
  return <SceneShell scene={scene}><div style={{ position: "absolute", top: 220, left: 165, right: 165, display: "flex", gap: 80, alignItems: "center" }}><div style={{ flex: 1, opacity: reveal(copy), transform: `translate3d(${interpolate(copy, [0, 1], [-28, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}px, 0, 0)` }}><Eyebrow color={scene.accent}>{scene.eyebrow}</Eyebrow><BigTitle size={64}>{scene.title}</BigTitle><p style={{ margin: "23px 0 0", color: MUTED, fontSize: 24, lineHeight: 1.4 }}>{scene.body}</p><div style={{ marginTop: 30, color: scene.accent, fontWeight: 700, fontSize: 16 }}>No login · no upload · fictional cases only</div><div style={{ marginTop: 24, color: MUTED, fontSize: 14, lineHeight: 1.5 }}>Defect = broken promise · Included work = within allowance · Scope change = new commitment</div></div><Panel accent={scene.accent} style={{ width: 700, padding: 24, opacity: reveal(report), transform: `translate3d(${interpolate(report, [0, 1], [36, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}px, 0, 0)` }}><div style={{ display: "flex", justifyContent: "space-between", color: MUTED, fontSize: 13 }}><span>FairChange / independent session kit</span><span>session-f49698ac</span></div><div style={{ display: "flex", gap: 14, marginTop: 23 }}>{["Qualifying US leads", "Dashboard layout", "UK + Canada routing"].map((x, i) => <div key={x} style={{ flex: 1, minHeight: 160, padding: 16, opacity: reveal(cards[i]), transform: `translateY(${interpolate(cards[i], [0, 1], [22, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}px)`, border: `1px solid ${i === 2 ? "#f5c36a66" : LINE}`, borderRadius: 14, background: i === 2 ? "#f5c36a10" : "rgba(255,255,255,.025)" }}><div style={{ color: i === 2 ? "#f5c36a" : scene.accent, fontSize: 12, fontWeight: 800 }}>CASE {i + 1}</div><div style={{ color: TEXT, fontSize: 16, fontWeight: 720, marginTop: 20 }}>{x}</div><div style={{ marginTop: 25, height: 9, borderRadius: 9, background: "rgba(255,255,255,.12)" }} /><div style={{ marginTop: 11, height: 9, width: "70%", borderRadius: 9, background: "rgba(255,255,255,.08)" }} /></div>)}</div><div style={{ marginTop: 20, padding: 14, borderRadius: 12, background: "rgba(138,240,192,.08)", color: "#8af0c0", fontWeight: 700, opacity: reveal(report) }}>Anonymous report ready · created locally</div></Panel></div></SceneShell>;
};

const CloseScene: React.FC<{ scene: VideoScene }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const mark = motion(frame, fps, 5, 85);
  const copy = motion(frame, fps, 24);
  const links = motion(frame, fps, 48);
  return <SceneShell scene={scene}><div style={{ position: "absolute", inset: 0, display: "grid", placeItems: "center", textAlign: "center" }}><div><div style={{ opacity: reveal(mark), transform: `scale(${interpolate(mark, [0, 1], [0.72, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })}) rotate(${interpolate(mark, [0, 1], [-10, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}deg)` }}><Img src={staticFile("fairchange-mark.svg")} style={{ width: 150, height: 150, filter: "drop-shadow(0 25px 50px rgba(138,240,192,.2))" }} /></div><div style={{ marginTop: 26, opacity: reveal(copy), transform: `translateY(${interpolate(copy, [0, 1], [24, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}px)` }}><Eyebrow color={scene.accent}>{scene.eyebrow}</Eyebrow><BigTitle size={70}>{scene.title}</BigTitle><p style={{ margin: "20px 0 0", color: scene.accent, fontSize: 28, fontWeight: 700 }}>{scene.body}</p></div><div style={{ display: "flex", justifyContent: "center", gap: 16, marginTop: 36, opacity: reveal(links), transform: `translateY(${interpolate(links, [0, 1], [20, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })}px)` }}><Pill color="#8af0c0">ai-ops1.github.io/fairchange-agent</Pill><Pill color="#b8b1ff">github.com/AI-Ops1/fairchange-agent</Pill></div></div></div></SceneShell>;
};

export const SceneRenderer: React.FC<{ scene: VideoScene }> = ({ scene }) => {
  switch (scene.kind) {
    case "hook": return <HookScene scene={scene} />;
    case "records": return <RecordsScene scene={scene} />;
    case "promise": return <PromiseScene scene={scene} />;
    case "flow": return <FlowScene scene={scene} />;
    case "defect": return <OutcomeScene scene={scene} outcome="Defect" next="Create a non-billable corrective task." color={scene.accent} evidence={[{ id: "S1", title: "Active representative", text: "Every qualifying lead must reach an active representative." }, { id: "S5", title: "No-fee correction", text: "Acceptance failures are corrected without an extra fee." }]} />;
    case "revision": return <OutcomeScene scene={scene} outcome="Included work" next="Update the existing delivery task." color={scene.accent} evidence={[{ id: "S2", title: "Two revision rounds", text: "One dashboard revision round remains unused." }, { id: "TASK", title: "Layout change", text: "The request changes chart order, not the feature set." }]} />;
    case "scope": return <OutcomeScene scene={scene} outcome="Scope change" next="Prepare an owner-review proposal." color={scene.accent} evidence={[{ id: "S4", title: "Countries excluded", text: "Additional countries and regional routing are excluded." }, { id: "S3", title: "Training unstarted", text: "A substitution still needs authorization and acceptance." }]} />;
    case "gate": return <GateScene scene={scene} />;
    case "workspace": return <WorkspaceScene scene={scene} />;
    case "session": return <SessionScene scene={scene} />;
    case "close": return <CloseScene scene={scene} />;
    default: return null;
  }
};
