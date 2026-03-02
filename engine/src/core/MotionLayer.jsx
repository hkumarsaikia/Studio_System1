/**
 * FILE: MotionLayer.jsx
 * PURPOSE: Cinematic entrance/exit wrapper for scene content.
 *
 * Wraps scene content with a time-based opacity fade and blur effect:
 *   - Frames 0–12: Fade in from transparent + blurred → opaque + clear
 *   - Frames 12 to (duration-12): Full visibility
 *   - Frames (duration-12) to duration: Fade out + blur back in
 *
 * This creates a smooth, cinematic feel for scene transitions without
 * needing complex video editing. Every scene's visual content is wrapped
 * in this layer (see GenericScene.jsx).
 *
 * PROPS:
 *   @param {ReactNode} children - Scene content to wrap
 *   @param {number}    duration - Total scene duration in frames (default: 300)
 */
import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

export const MotionLayer = ({ children, duration = 300 }) => {
  const frame = useCurrentFrame();

  // Opacity envelope: 0 → 1 → 1 → 0 over the scene duration
  // The 12-frame edge creates a quick but smooth fade
  const opacity = interpolate(frame, [0, 12, duration - 12, duration], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Blur envelope: blurry → clear → clear → blurry
  // Uses an 18-frame edge (slightly longer than opacity) for extra smoothness
  const blur = interpolate(frame, [0, 18, duration - 18, duration], [8, 0, 0, 8], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{ opacity, filter: `blur(${blur}px)` }}>
      {children}
    </AbsoluteFill>
  );
};
