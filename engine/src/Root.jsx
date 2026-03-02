/**
 * FILE: Root.jsx
 * PURPOSE: Remotion entry point — loads video data and creates the Composition.
 *
 * This is the top-level React component that Remotion uses to discover
 * and render video compositions. It does three things:
 *
 *   1. READ the video ID from the REMOTION_VIDEO_ID environment variable
 *   2. LOAD the corresponding JSON data from data/videos/video_XXX.json
 *   3. CREATE a Remotion <Composition> with the correct dimensions, fps,
 *      duration, and template
 *
 * The render pipeline sets REMOTION_VIDEO_ID before calling `npx remotion render`,
 * so each render produces a different video based on the ID.
 *
 * DATA FLOW:
 *   env(REMOTION_VIDEO_ID) → getVideoData() → parseVideoData() → <Composition>
 *                                                                    ↓
 *                                                             <TemplateLoader>
 *                                                                    ↓
 *                                                             <SceneManager>
 */
import React, { useEffect, useMemo, useState } from 'react';
import { Composition, cancelRender, continueRender, delayRender } from 'remotion';
import { loadFont } from '@remotion/google-fonts/Outfit';
import { TemplateLoader } from './core/TemplateLoader.jsx';
import { getVideoData } from './generated/videoManifest.js';
import { parseVideoData } from './utils/dataParser.js';
import { computeTotalFrames } from './utils/sceneTiming.js';

// Load the premium typography for the entire engine
loadFont();

/**
 * Read the video ID from environment.
 * Falls back to 'video_001' for local development / Remotion Studio.
 */
const getVideoIdFromEnv = () => {
  const envId = process.env.REMOTION_VIDEO_ID;
  return envId && typeof envId === 'string' ? envId : 'video_001';
};

export const RemotionRoot = () => {
  const [videoData, setVideoData] = useState(null);
  // delayRender() pauses Remotion until we call continueRender()
  // This gives us time to load the video JSON asynchronously
  const [handle] = useState(() => delayRender('Loading selected video data'));
  const videoId = useMemo(() => getVideoIdFromEnv(), []);

  useEffect(() => {
    let active = true;  // Prevents state updates after unmount

    getVideoData(videoId)
      .then((data) => {
        if (!active) {
          return;
        }
        // Parse and normalize the raw JSON data
        setVideoData(parseVideoData(data));
        // Signal Remotion that data is ready — rendering can begin
        continueRender(handle);
      })
      .catch((error) => {
        // Cancel the render with a descriptive error
        cancelRender(error);
      });

    // Cleanup: prevent state updates if component unmounts during fetch
    return () => {
      active = false;
    };
  }, [handle, videoId]);

  // Don't render anything until video data is loaded
  if (!videoData) {
    return null;
  }

  // Calculate total duration by summing all scene durations
  const totalDuration = computeTotalFrames(videoData.scenes);

  return (
    <Composition
      id="MainComposition"
      component={TemplateLoader}
      durationInFrames={totalDuration}
      fps={videoData.fps}
      width={videoData.width}
      height={videoData.height}
      defaultProps={{
        template: videoData.template,
        scenes: videoData.scenes,
      }}
    />
  );
};
