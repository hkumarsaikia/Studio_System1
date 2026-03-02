/**
 * FILE: audioSync.js
 * PURPOSE: Audio file resolution and timing utilities.
 *
 * Provides a hardened audio pipeline that:
 *   1. Looks for an explicit `audio` field on the scene JSON first
 *   2. Falls back to convention-based paths (video_XXX_scene_YY.mp3)
 *   3. Returns null (silence) if no audio is available
 *
 * This prevents render crashes from missing audio files — silence is
 * always a valid fallback. The render will succeed even if no audio
 * files exist on disk.
 *
 * CONVENTION-BASED PATH FORMAT:
 *   public/audio/{videoId}_scene_{sceneNumber}.mp3
 *   Example: public/audio/video_001_scene_03.mp3
 *
 * EXPORTS:
 *   buildAudioPath(videoId, sceneIndex) → Convention-based filename
 *   resolveAudioSource(scene, videoId, sceneIndex) → Final audio path or null
 *   getSceneStartFrame(scenes, sceneIndex) → Start frame for a scene
 *   mapAudioOffsets(scenes, videoId) → Array of { audio, startFrame, duration }
 */

/**
 * Build the expected audio file name using the naming convention.
 * Scene indices are 0-based internally but 1-based in filenames.
 *
 * @param {string} videoId    - e.g. "video_001"
 * @param {number} sceneIndex - 0-based scene index
 * @returns {string}          - e.g. "video_001_scene_03.mp3"
 */
export const buildAudioPath = (videoId, sceneIndex) => {
  const paddedScene = String(sceneIndex + 1).padStart(2, '0');
  return `${videoId}_scene_${paddedScene}.mp3`;
};

/**
 * Resolve the final audio source for a scene.
 * Priority order:
 *   1. Explicit scene.audio field (highest priority)
 *   2. Convention-based path (if scene.hasAudio is true)
 *   3. null (silence — default, safest)
 */
export const resolveAudioSource = (scene, videoId, sceneIndex) => {
  // Explicit audio field takes priority
  if (scene.audio && typeof scene.audio === 'string') {
    return scene.audio;
  }

  // Convention-based path: only return if the scene opts into audio
  if (scene.hasAudio) {
    return buildAudioPath(videoId, sceneIndex);
  }

  // Default: silence (no audio for this scene)
  return null;
};

/**
 * Calculate the start frame for a given scene by summing all
 * previous scene durations.
 */
export const getSceneStartFrame = (scenes, sceneIndex) => {
  return scenes.slice(0, sceneIndex).reduce((acc, scene) => acc + scene.duration, 0);
};

/**
 * Build a complete audio offset map for the entire video.
 * Used to synchronize audio playback with scene timing.
 * Only includes scenes that have audio (filters out nulls).
 */
export const mapAudioOffsets = (scenes, videoId) => {
  return scenes
    .map((scene, index) => {
      const audioFile = resolveAudioSource(scene, videoId, index);
      return {
        audio: audioFile,
        startFrame: getSceneStartFrame(scenes, index),
        duration: scene.duration,
      };
    })
    .filter((item) => Boolean(item.audio));  // Remove scenes with no audio
};
