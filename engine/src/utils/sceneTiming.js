/**
 * FILE: sceneTiming.js
 * PURPOSE: Scene duration utilities.
 *
 * Provides safe defaults for scene durations and computes total video
 * length from an array of scenes. Used by Root.jsx to calculate
 * the Composition's total frame count.
 *
 * CONSTANTS:
 *   DEFAULT_SCENE_DURATION = 300 frames (10 seconds at 30fps)
 *
 * EXPORTS:
 *   normalizeSceneDuration(scene)  → Validated integer frame count
 *   computeTotalFrames(scenes)     → Sum of all scene durations
 */

/**
 * Default scene duration in frames (10 seconds at 30fps).
 */
export const DEFAULT_SCENE_DURATION = 300;

/**
 * Safely extract a positive integer duration from a scene object.
 * Returns the fallback value if the scene's duration is missing,
 * non-numeric, zero, or negative.
 */
export const normalizeSceneDuration = (scene, fallback = DEFAULT_SCENE_DURATION) => {
  const duration = Number(scene?.duration);
  return Number.isFinite(duration) && duration > 0 ? Math.round(duration) : fallback;
};

/**
 * Compute the total frame count for a video by summing all scene durations.
 * This is passed to Remotion's <Composition durationInFrames={...} />.
 */
export const computeTotalFrames = (scenes) => {
  return scenes.reduce((acc, scene) => acc + normalizeSceneDuration(scene), 0);
};
