/**
 * FILE: GenericScene.jsx
 * PURPOSE: Default scene renderer — the visual assembly pipeline for each scene.
 *
 * Every scene in a video passes through this component. It layers four
 * elements in depth order (back to front):
 *
 *   1. Background   → Gradient + ambient glow + grid overlay
 *   2. Camera       → Applies the camera movement (zoom, pan, etc.)
 *   3. MotionLayer  → Fade-in/out + blur envelope around content
 *   4. SceneFactory → The actual visual component (crowd, bars, flow, etc.)
 *   5. CinematicText → Title + subtitle + category badge overlay
 *
 * PROPS:
 *   @param {object} scene - A single scene object from the video JSON
 *     scene.palette     → Background colors (from category)
 *     scene.action      → Camera move name (e.g. "pan_right")
 *     scene.duration    → Frame count (usually 300 = 10 seconds)
 *     scene.visual      → Visual type for SceneFactory
 *     scene.text        → Title text
 *     scene.subtext     → Subtitle text
 *     scene.accentColor → Category accent color
 *     scene.category    → Category label string
 */
import React from 'react';
import { AbsoluteFill } from 'remotion';
import { Background } from '../components/Background.jsx';
import { CinematicText } from '../overlays/CinematicText.jsx';
import { SceneFactory } from './SceneFactory.jsx';
import { Camera } from '../core/Camera.jsx';
import { MotionLayer } from '../core/MotionLayer.jsx';
import { CinematicGrain } from '../overlays/CinematicGrain.jsx';

// Fallback palette if scene doesn't specify one (shouldn't happen with
// the current build_topic_library.py, but safety first)
const defaultPalette = {
  background: '#0f172a',
  secondary: '#1e293b',
};

export const GenericScene = ({ scene }) => {
  const palette = scene.palette || defaultPalette;
  // Read camera action from scene JSON; default to slow zoom if missing
  const cameraAction = scene.action || 'slow_zoom_in';

  return (
    <AbsoluteFill style={{ color: '#f8fafc' }}>
      {/* Layer 1: Animated gradient background */}
      <Background palette={palette} motion={scene.motion || 'pan'} />

      {/* Layer 2-3: Camera wraps MotionLayer wraps visual content */}
      <Camera action={cameraAction} duration={scene.duration || 300}>
        <MotionLayer duration={scene.duration || 300}>
          {/* Layer 4: The actual visual component (crowd, bars, flow, etc.) */}
          <SceneFactory scene={scene} />
        </MotionLayer>
      </Camera>

      {/* Layer 5: Text overlay on top of everything */}
      <CinematicText
        title={scene.text}
        subtitle={scene.subtext}
        accentColor={scene.accentColor}
        category={scene.category || 'SYSTEMS EXPLAINER'}
      />

      {/* Layer 6: Film Grain Texture Overlay */}
      <CinematicGrain opacity={0.06} baseFrequency={0.65} />
    </AbsoluteFill>
  );
};
