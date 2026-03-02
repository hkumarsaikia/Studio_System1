/**
 * FILE: LandscapeBackdrop.jsx
 * PURPOSE: Nature/horizon SVG backdrop for environment-themed scenes.
 *
 * Renders a sunset landscape with:
 *   - Gradient sky (blue → orange)
 *   - Large sun ellipse
 *   - Rolling green hills (two layers for depth)
 *   - Water body in the foreground
 *
 * This is a purely decorative component with no props — it's a
 * static SVG illustration used as a backdrop for ecology/environment scenes.
 */
import React from 'react';
import { AbsoluteFill } from 'remotion';
import { WaveField } from './WaveField.jsx';

export const LandscapeBackdrop = () => {
  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
      <WaveField accentColor="#38bdf8" duration={300} />
    </AbsoluteFill>
  );
};
