/**
 * FILE: ProtestCinematic.jsx
 * PURPOSE: Social movement / protest-themed cinematic template.
 *
 * Uses the "slate" theme for high-contrast, impactful visuals.
 * Assigned to ~2/3 of the 500 videos (those where index % 3 != 0).
 *
 * THEME: slate (blue-gray palette, high contrast)
 */
import React from 'react';
import { SceneManager } from '../core/SceneManager.jsx';

export const ProtestCinematic = ({ scenes }) => {
  return <SceneManager scenes={scenes} theme="slate" />;
};
