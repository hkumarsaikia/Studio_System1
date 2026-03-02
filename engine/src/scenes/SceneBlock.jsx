/**
 * FILE: SceneBlock.jsx
 * PURPOSE: Wrapper that enriches a scene with theme defaults and transitions.
 *
 * Each scene in the <Series> (from SceneManager) is rendered through this
 * component. It does three things:
 *
 *   1. ENRICHMENT – Fills in missing palette/accent colors from the theme
 *   2. TRANSITIONS – Applies fadeInOut opacity + slideY vertical motion
 *   3. DELEGATION – Passes the enriched scene to GenericScene for rendering
 *
 * Also conditionally attaches <SceneAudio> if the scene has an audio file.
 *
 * PROPS:
 *   @param {object} scene     - Raw scene object from video JSON
 *   @param {string} themeName - Theme key (resolves via themes in theme.js)
 */
import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { SceneAudio } from '../components/SceneAudio.jsx';
import { GenericScene } from './GenericScene.jsx';
import { themes } from '../styles/theme.js';
import { fadeInOut, slideY } from '../utils/sceneTransitions.js';

export const SceneBlock = ({ scene, themeName }) => {
  const frame = useCurrentFrame();
  // Resolve the theme; fall back to 'dark' if not found
  const theme = themes[themeName] || themes.dark;
  const duration = scene.duration || 300;

  // Compute transition values for this frame
  const opacity = fadeInOut(frame, duration);      // 0 → 1 → 1 → 0
  const y = slideY(frame, duration, 22);           // 22px → 0 → 0 → -22px

  // Enrich the scene with theme-derived defaults for any missing fields
  const enrichedScene = {
    ...scene,
    palette: scene.palette || {
      background: theme.background,
      secondary: theme.accent,
    },
    accentColor: scene.accentColor || theme.text,
  };

  return (
    <AbsoluteFill style={{ opacity, transform: `translateY(${y}px)` }}>
      <GenericScene scene={enrichedScene} />
      {/* Only attach audio if the scene specifies an audio file */}
      {scene.audio ? <SceneAudio audioFile={scene.audio} /> : null}
    </AbsoluteFill>
  );
};
