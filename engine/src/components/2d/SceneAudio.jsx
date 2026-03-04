/**
 * FILE: SceneAudio.jsx
 * PURPOSE: Audio player component for individual scenes.
 *
 * Wraps Remotion's <Audio> component with safety checks so that
 * missing audio files don't crash the render pipeline. If no audio
 * file is provided or the file doesn't exist, the scene renders
 * in silence rather than throwing an error.
 *
 * This is critical for the 500-video pipeline because most scenes
 * won't have audio files during initial bulk renders.
 *
 * PROPS:
 *   @param {string} audioFile - Filename relative to public/audio/ (e.g. "video_001_scene_01.mp3")
 *   @param {number} volume    - Playback volume 0–1 (default: 1)
 *
 * USAGE:
 *   <SceneAudio audioFile="video_001_scene_01.mp3" volume={0.8} />
 *   <SceneAudio audioFile={null} />  // → renders nothing (silence)
 */
import React from 'react';
import { Audio, staticFile } from 'remotion';

export const SceneAudio = ({ audioFile, volume = 1 }) => {
  // Guard: if no audio file is specified, render silence
  if (!audioFile || typeof audioFile !== 'string') {
    return null;
  }

  try {
    // Resolve the audio path relative to public/audio/
    const src = staticFile(`audio/${audioFile}`);
    return <Audio src={src} volume={volume} />;
  } catch {
    // If staticFile throws (file not found), log a warning and
    // default to silence rather than crashing the entire render.
    console.warn(`[SceneAudio] Audio file not found: audio/${audioFile} – defaulting to silence`);
    return null;
  }
};