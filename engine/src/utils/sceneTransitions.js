/**
 * FILE: sceneTransitions.js
 * PURPOSE: Reusable transition functions for scene entrance/exit effects.
 *
 * These are pure functions that take the current frame and return a
 * numeric value for CSS properties (opacity, translateY). Used by
 * SceneBlock.jsx for consistent transitions across all scenes.
 *
 * EXPORTS:
 *   fadeInOut(frame, duration, edge)    → Opacity value (0 → 1 → 1 → 0)
 *   slideY(frame, duration, amount, edge) → Y offset (amount → 0 → 0 → -amount)
 */
import { interpolate } from 'remotion';

/**
 * Compute opacity for a fade-in / fade-out envelope.
 *
 * @param {number} frame    - Current frame
 * @param {number} duration - Total scene duration
 * @param {number} edge     - Frames for the fade transition (default: 12)
 * @returns {number}        - Opacity value between 0 and 1
 */
export const fadeInOut = (frame, duration, edge = 12) => {
  return interpolate(frame, [0, edge, duration - edge, duration], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
};

/**
 * Compute vertical slide offset for entrance/exit.
 * Content slides up on entrance (amount → 0) and down on exit (0 → -amount).
 *
 * @param {number} frame    - Current frame
 * @param {number} duration - Total scene duration
 * @param {number} amount   - Slide distance in pixels (default: 30)
 * @param {number} edge     - Frames for the transition (default: 16)
 * @returns {number}        - Y offset in pixels
 */
export const slideY = (frame, duration, amount = 30, edge = 16) => {
  return interpolate(frame, [0, edge, duration - edge, duration], [amount, 0, 0, -amount], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
};
