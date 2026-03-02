/**
 * FILE: CityStreetBackdrop.jsx
 * PURPOSE: Urban skyline SVG backdrop for society/infrastructure scenes.
 *
 * Renders a stylized city street scene with:
 *   - Light sky background
 *   - Building silhouettes (varying heights)
 *   - Road surface with lane markings
 *   - Crosswalk
 *   - Two trees for visual balance
 *
 * Used for cityscape/urban scenes (scene.visual === 'city').
 * No props — this is a static decorative backdrop.
 */
import React from 'react';

export const CityStreetBackdrop = () => {
  return (
    <svg viewBox="0 0 1200 900" style={{ width: '100%', height: '100%' }}>
      {/* Sky */}
      <rect width="1200" height="900" fill="#d8f2f1" />
      {/* Road surface */}
      <rect x="0" y="590" width="1200" height="310" fill="#8b7a86" />

      {/* Building silhouettes */}
      <rect x="40" y="120" width="250" height="470" fill="#b3d1e6" />
      <rect x="930" y="160" width="230" height="430" fill="#b8d5e8" />
      <rect x="420" y="300" width="150" height="290" fill="#9cb7cf" />
      <rect x="630" y="260" width="170" height="330" fill="#93afc6" />

      {/* Lane markings (dashed center line) */}
      {Array.from({ length: 10 }).map((_, i) => (
        <rect key={i} x={490 + i * 65} y="710" width="34" height="16" fill="#eadfbf" />
      ))}

      {/* Crosswalk */}
      <rect x="360" y="680" width="480" height="36" fill="#efe4c8" />

      {/* Decorative trees on sidewalks */}
      <circle cx="250" cy="470" r="52" fill="#9ccf5a" />
      <circle cx="970" cy="470" r="58" fill="#9ccf5a" />
    </svg>
  );
};
