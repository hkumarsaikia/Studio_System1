/**
 * FILE: ExplainerCinematic.jsx
 * PURPOSE: Widescreen cinematic explainer template.
 *
 * Uses the "slate" theme for a professional, documentary-style look.
 * Designed for longer-form explainer content with more visual depth.
 *
 * THEME: slate (blue-gray palette, professional feel)
 */
import React from 'react';
import { SceneManager } from '../core/SceneManager.jsx';

export const ExplainerCinematic = ({ scenes }) => {
  return (
    <SceneManager
      scenes={scenes}
      theme="slate"
    />
  );
};