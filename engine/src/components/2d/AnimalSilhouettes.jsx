/**
 * FILE: AnimalSilhouettes.jsx
 * PURPOSE: Emoji-based wildlife display for ecology/nature scenes.
 *
 * Renders animal emojis inside dark circular badges with labels.
 * Used for "Environment & Nature" category scenes to illustrate
 * wildlife concepts when scene.visual === 'animals'.
 *
 * SUPPORTED ANIMALS:
 *   bird, fish, deer, cow, bee, turtle
 *   Unknown animals fall back to the paw print emoji (🐾).
 *
 * PROPS:
 *   @param {string[]} animals - Array of animal name strings
 */
import React from 'react';

export const AnimalSilhouettes = ({ animals = ['bird', 'fish', 'deer'] }) => {
  // Emoji lookup table — maps animal names to display emojis
  const symbols = {
    bird: '🕊️',
    fish: '🐟',
    deer: '🦌',
    cow: '🐄',
    bee: '🐝',
    turtle: '🐢',
  };

  return (
    <svg viewBox="0 0 900 520" style={{ width: '100%', height: '100%' }}>
      {animals.map((a, idx) => (
        // Each animal is positioned in a horizontal row with slight zigzag
        <g key={`${a}-${idx}`} transform={`translate(${120 + idx * 220}, ${210 + (idx % 2) * 60})`}>
          {/* Dark circular badge behind the emoji */}
          <circle r="74" fill="#0f172a" opacity="0.75" />
          {/* Animal emoji */}
          <text textAnchor="middle" y="18" fontSize="56">
            {symbols[a] || '🐾'}
          </text>
          {/* Label below the badge */}
          <text textAnchor="middle" y="112" fill="#cbd5e1" fontSize="20" style={{ textTransform: 'uppercase' }}>
            {a}
          </text>
        </g>
      ))}
    </svg>
  );
};
