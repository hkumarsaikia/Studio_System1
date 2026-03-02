/**
 * FILE: DataInfographic.jsx
 * PURPOSE: Data-heavy infographic template for statistics-focused videos.
 *
 * Uses the "minimal" theme — clean and uncluttered to let the data
 * visualizations (bars, charts, networks) take center stage.
 *
 * THEME: minimal (dark, clean, data-focused)
 */
import React from 'react';
import { SceneManager } from '../core/SceneManager.jsx';

export const DataInfographic = ({ scenes }) => {
  return <SceneManager scenes={scenes} theme="minimal" />;
};
