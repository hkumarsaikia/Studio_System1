/**
 * FILE: ShortsVertical.jsx
 * PURPOSE: 9:16 vertical video template — the default layout for most videos.
 *
 * This is the primary template used by the Studio System. It renders all
 * scenes through the SceneManager with the "minimal" theme, which uses
 * dark backgrounds with subtle accents — optimized for mobile viewing.
 *
 * DIMENSIONS: 1080 × 1920 (vertical, 9:16 aspect ratio)
 * THEME: minimal (dark, clean, mobile-first)
 */
import React from 'react';
import { SceneManager } from '../core/SceneManager.jsx';

export const ShortsVertical = ({ scenes }) => {
  return (
    <SceneManager
      scenes={scenes}
      theme="minimal"
    />
  );
};