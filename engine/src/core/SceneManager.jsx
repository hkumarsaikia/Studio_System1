/**
 * FILE: SceneManager.jsx
 * PURPOSE: Orchestrates the sequence of all 12 scenes in a video.
 *
 * This is the "conductor" of the video — it takes the array of scene
 * objects from the video JSON and lays them out in time using Remotion's
 * <Series> component. Each scene plays for exactly its `duration` frames,
 * then the next scene starts immediately (frame-exact transitions).
 *
 * WHY <Series> INSTEAD OF <Sequence>?
 *   - <Sequence> requires manually computing startFrame offsets
 *   - <Series> handles this automatically — Scene 2 starts the frame
 *     after Scene 1 ends. No offset math, no off-by-one bugs.
 *
 * PROPS:
 *   @param {object[]} scenes - Array of scene objects from video JSON
 *   @param {string}   theme  - Theme name (resolves via theme.js)
 *
 * USAGE:
 *   <SceneManager scenes={videoData.scenes} theme="slate" />
 */
import React from 'react';
import { Series } from 'remotion';
import { SceneBlock } from '../scenes/SceneBlock.jsx';
import { validateScenes } from '../utils/propsValidator.js';

export const SceneManager = ({ scenes, theme }) => {
  // Validate all scenes before rendering — throws if any scene is
  // malformed (missing text, invalid duration, etc.)
  const safeScenes = validateScenes(scenes);

  return (
    <Series>
      {safeScenes.map((scene, index) => (
        // Each Series.Sequence auto-starts after the previous one ends
        <Series.Sequence key={index} durationInFrames={scene.duration}>
          <SceneBlock scene={scene} themeName={theme} />
        </Series.Sequence>
      ))}
    </Series>
  );
};
