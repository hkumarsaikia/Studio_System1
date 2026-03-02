/**
 * FILE: propsValidator.js
 * PURPOSE: Validates scene objects before rendering.
 *
 * Acts as a safety net — if a video JSON has malformed scenes (missing
 * text, invalid duration), this throws a clear error message instead of
 * letting the render fail with unhelpful React/Remotion errors.
 *
 * Also normalizes durations using sceneTiming.js to ensure every scene
 * has a valid positive integer frame count.
 *
 * EXPORTS:
 *   validateScene(scene, index)  → Single scene validation + normalization
 *   validateScenes(scenes)       → Validates the full array (throws if empty)
 */
import { normalizeSceneDuration } from './sceneTiming.js';

/**
 * Validate a single scene object.
 * Throws descriptive errors if the scene is missing required fields.
 * Returns the scene with a normalized duration.
 */
export const validateScene = (scene, index) => {
  if (!scene || typeof scene !== 'object') {
    throw new Error(`Scene at index ${index} is invalid.`);
  }

  // Every scene MUST have a text string (the title displayed on screen)
  if (!scene.text || typeof scene.text !== 'string') {
    throw new Error(`Scene at index ${index} must include a text string.`);
  }

  return {
    ...scene,
    duration: normalizeSceneDuration(scene),  // Safe integer, defaults to 300 if bad
  };
};

/**
 * Validate the full scenes array.
 * A video must have at least one scene to render.
 */
export const validateScenes = (scenes = []) => {
  if (!Array.isArray(scenes) || scenes.length === 0) {
    throw new Error('Video must include at least one scene.');
  }

  return scenes.map((scene, index) => validateScene(scene, index));
};
