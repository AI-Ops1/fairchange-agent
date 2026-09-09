export const FPS = 30;

export type VideoScene = {
  id: string;
  label: string;
  from: number;
  duration: number;
  kind: "hook" | "records" | "promise" | "flow" | "defect" | "revision" | "scope" | "gate" | "workspace" | "session" | "close";
  eyebrow: string;
  title: string;
  body: string;
  accent: string;
};

export const FULL_SCENES: VideoScene[] = [
  { id: "hook", label: "01 · The request", from: 0, duration: 12, kind: "hook", eyebrow: "A change request arrives", title: "What happens next?", body: "Defect, included work, or new commercial commitment?", accent: "#8af0c0" },
  { id: "records", label: "02 · The hidden cost", from: 12, duration: 16, kind: "records", eyebrow: "The evidence is scattered", title: "Find the receipts before making a promise.", body: "Signed scope. Correspondence. Estimates. Delivery tasks.", accent: "#b8b1ff" },
  { id: "promise", label: "03 · The promise", from: 28, duration: 17, kind: "promise", eyebrow: "FairChange", title: "Automation handles the search.", body: "People own the commitment.", accent: "#ff9c8e" },
  { id: "flow", label: "04 · The flow", from: 45, duration: 20, kind: "flow", eyebrow: "One legible path", title: "From request to safe action.", body: "Every step leaves an inspectable trail.", accent: "#8af0c0" },
  { id: "defect", label: "05 · Defect", from: 65, duration: 19, kind: "defect", eyebrow: "Case 01 · req-defect", title: "Inactive representative routing", body: "The delivered workflow misses an agreed acceptance criterion.", accent: "#8af0c0" },
  { id: "revision", label: "06 · Included revision", from: 84, duration: 19, kind: "revision", eyebrow: "Case 02 · req-revision", title: "Move the conversion chart", body: "One dashboard revision round remains in scope.", accent: "#8af0c0" },
  { id: "scope", label: "07 · Scope change", from: 103, duration: 25, kind: "scope", eyebrow: "Case 03 · req-addition", title: "Add UK and Canada routing", body: "Regional work changes the commercial agreement.", accent: "#f5c36a" },
  { id: "gate", label: "08 · Human gate", from: 128, duration: 22, kind: "gate", eyebrow: "Commercial authority stays human", title: "The agent drafts. People decide.", body: "Owner review, then exact client acceptance.", accent: "#f5c36a" },
  { id: "workspace", label: "09 · Product walkthrough", from: 150, duration: 20, kind: "workspace", eyebrow: "Public synthetic workspace", title: "See the evidence before the answer.", body: "Select a case. Inspect the trail. Read the next safe action.", accent: "#b8b1ff" },
  { id: "session", label: "10 · Independent session", from: 170, duration: 15, kind: "session", eyebrow: "Separate usability kit", title: "Let an outside participant try it.", body: "Anonymous, local, synthetic, and independent.", accent: "#8af0c0" },
  { id: "close", label: "11 · Close", from: 185, duration: 10, kind: "close", eyebrow: "FairChange", title: "Make scope decisions explainable.", body: "Before they become commercial surprises.", accent: "#8af0c0" },
];

export const TRAILER_SCENES: VideoScene[] = [
  { ...FULL_SCENES[0], id: "trailer-hook", from: 0, duration: 8 },
  { ...FULL_SCENES[3], id: "trailer-flow", from: 8, duration: 9 },
  { ...FULL_SCENES[6], id: "trailer-scope", from: 17, duration: 10 },
  { ...FULL_SCENES[7], id: "trailer-gate", from: 27, duration: 10 },
  { ...FULL_SCENES[10], id: "trailer-close", from: 37, duration: 8 },
];
