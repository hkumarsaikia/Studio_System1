/**
 * FILE: dataParser.js
 * PURPOSE: Parses and normalizes raw video JSON data into a safe format.
 *
 * Takes the raw JSON loaded from data/videos/video_XXX.json and ensures
 * all required fields have valid values. This is the first stop in the
 * data pipeline — before any component sees the data, it passes through
 * this parser.
 *
 * NORMALIZATIONS:
 *   - fps    → default 30
 *   - width  → default 1080
 *   - height → default 1920
 *   - template → default 'shorts'
 *   - scenes → validated via propsValidator
 *
 * USAGE:
 *   const safeData = parseVideoData(rawJson);
 */
import { validateScenes } from './propsValidator.js';

export const parseVideoData = (videoData) => {
  // Validate all scenes first (throws if any are malformed)
  const scenes = validateScenes(videoData?.scenes ?? []);

  return {
    ...videoData,
    fps: Number(videoData?.fps) || 30,           // Default: 30 frames per second
    width: Number(videoData?.width) || 1080,     // Default: 1080px (vertical format)
    height: Number(videoData?.height) || 1920,   // Default: 1920px (9:16 aspect ratio)
    template: videoData?.template || 'shorts',   // Default: ShortsVertical template
    scenes,
  };
};
