import { Audio } from "@remotion/media";
import { AbsoluteFill, Composition, Sequence, staticFile } from "remotion";
import { CaptionOverlay } from "./CaptionOverlay";
import { FULL_SCENES, TRAILER_SCENES, FPS, type VideoScene } from "./sceneData";
import { SceneRenderer } from "./scenes";

const Video: React.FC<{ scenes: VideoScene[]; captions: string }> = ({ scenes, captions }) => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0e1b" }}>
      {scenes.map((scene) => (
        <Sequence key={scene.id} from={scene.from * FPS} durationInFrames={scene.duration * FPS} name={scene.label}>
          <SceneRenderer scene={scene} />
        </Sequence>
      ))}
      <Audio src={staticFile("ambient-bed.wav")} loop volume={0.12} />
      <CaptionOverlay source={captions} />
    </AbsoluteFill>
  );
};

export const MyComposition = () => (
  <>
    <Composition id="FairChangeJudging" component={() => <Video scenes={FULL_SCENES} captions="judging-captions.json" />} durationInFrames={195 * FPS} fps={FPS} width={1920} height={1080} />
    <Composition id="FairChangeTrailer" component={() => <Video scenes={TRAILER_SCENES} captions="trailer-captions.json" />} durationInFrames={45 * FPS} fps={FPS} width={1920} height={1080} />
  </>
);
