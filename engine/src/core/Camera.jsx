/**
 * FILE: Camera.jsx
 * PURPOSE: Programmatic camera movement system for the Remotion engine.
 *
 * Instead of physically moving a camera (this is 2D), we apply CSS
 * transforms (scale, translateX/Y) to the entire scene content to
 * simulate cinematic camera movements.
 *
 * The `action` prop selects one of 7 named camera moves. Each video
 * scene's JSON includes an `action` field (e.g. "pan_right") that
 * GenericScene passes to this component.
 *
 * AVAILABLE ACTIONS:
 *   slow_zoom_in       → Scale 1.0 → 1.2 (most common, used for emphasis)
 *   pan_right           → Slide content left by 100px (reveals new info)
 *   pan_left            → Slide content right by 100px
 *   static_focus        → No movement (for text-heavy scenes)
 *   dramatic_pull_back  → Scale 1.2 → 1.0 (reverse zoom, closing shots)
 *   slow_pan_up         → Slide content down by 60px (data reveals)
 *   slow_pan_down       → Slide content up by 60px (macro trends)
 *
 * PROPS:
 *   @param {ReactNode} children  – Scene content to wrap
 *   @param {string}    action    – One of the 7 action names above
 *   @param {number}    duration  – Total scene frames (used for interpolation)
 *   @param {number}    panX      – Legacy: manual X drift (fallback mode only)
 *   @param {number}    panY      – Legacy: manual Y drift (fallback mode only)
 *   @param {number}    zoom      – Legacy: manual zoom factor (fallback mode only)
 *
 * USAGE:
 *   <Camera action="pan_right" duration={300}>
 *     <SceneContent />
 *   </Camera>
 */
import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

export const Camera = ({
  children,
  action = 'slow_zoom_in',
  duration = 300,
  // Legacy props — used only when `action` doesn't match any named move.
  // This maintains backward compatibility with older scene JSONs.
  panX = 20,
  panY = -18,
  zoom = 1.04,
}) => {
  const frame = useCurrentFrame();

  // Compute the CSS transform for this frame based on the action type
  const style = computeCameraStyle(action, frame, duration, { panX, panY, zoom });

  return (
    <AbsoluteFill style={style}>
      {children}
    </AbsoluteFill>
  );
};

/**
 * computeCameraStyle – Pure function that maps (action, frame) → CSS transform.
 *
 * Uses Remotion's `interpolate()` to smoothly transition values over the
 * scene duration. The `clamp` config prevents overshoot at start/end.
 */
function computeCameraStyle(action, frame, duration, legacy) {
  // Clamp prevents values from extrapolating beyond the defined range
  const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' };

  switch (action) {
    // ── Zoom moves ──
    case 'slow_zoom_in': {
      // Gradually scale from 1.0 to 1.2 over the full scene duration
      const scale = interpolate(frame, [0, duration], [1, 1.2], clamp);
      return { transform: `scale(${scale})` };
    }

    case 'dramatic_pull_back': {
      // Reverse of zoom in — starts close, pulls back to normal
      const scale = interpolate(frame, [0, duration], [1.2, 1.0], clamp);
      return { transform: `scale(${scale})` };
    }

    // ── Horizontal pan moves ──
    case 'pan_right': {
      const tx = interpolate(frame, [0, duration], [0, 100], clamp);
      return { transform: `translateX(${tx}px)` };
    }

    case 'pan_left': {
      const tx = interpolate(frame, [0, duration], [0, -100], clamp);
      return { transform: `translateX(${tx}px)` };
    }

    // ── Vertical pan moves ──
    case 'slow_pan_up': {
      const ty = interpolate(frame, [0, duration], [0, -60], clamp);
      return { transform: `translateY(${ty}px)` };
    }

    case 'slow_pan_down': {
      const ty = interpolate(frame, [0, duration], [0, 60], clamp);
      return { transform: `translateY(${ty}px)` };
    }

    // ── No movement ──
    case 'static_focus': {
      return { transform: 'none' };
    }

    // ── Legacy fallback ──
    // If action doesn't match any named move, use the legacy panX/panY/zoom
    // props for a gentle drift effect. This keeps old scene JSONs working.
    default: {
      const progress = interpolate(frame, [0, duration], [0, 1], clamp);
      const tx = legacy.panX * progress;
      const ty = legacy.panY * progress;
      const scale = 1 + (legacy.zoom - 1) * progress;
      return { transform: `translate(${tx}px, ${ty}px) scale(${scale})` };
    }
  }
}
