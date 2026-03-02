/**
 * FILE: Crowd.jsx
 * PURPOSE: Renders a group of Person figures arranged in rows.
 *
 * Used for opening and closing scenes to show "the public" or "society."
 * Figures are laid out in a 4-column grid with slight scale variation
 * by row to create a sense of depth. Each person gets a different shirt
 * color for visual variety.
 *
 * PROPS:
 *   @param {number} count  - Number of people to render (default: 8)
 *   @param {number} width  - SVG viewBox width (default: 900)
 *   @param {number} height - SVG viewBox height (default: 600)
 */
import React from 'react';
import { useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { Person } from './Person.jsx';

export const Crowd = ({ count = 8, width = 900, height = 600 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Generate person positions in a 4-column grid
  const people = Array.from({ length: count }).map((_, i) => {
    const row = Math.floor(i / 4);       // Which row (0, 1, 2, ...)
    const col = i % 4;                    // Column within the row
    const delay = i * 4; // Stagger each person by 4 frames

    // Physics-based spring pop-in
    const pop = spring({
      frame: frame - delay,
      fps,
      config: {
        damping: 12,
        stiffness: 150,
      },
    });

    return {
      key: i,
      x: width * 0.2 + col * 170,
      y: height * 0.72 + row * 18,
      scale: (0.8 + row * 0.08) * pop, // Base scale * bounce physics
      shirt: ['#2563eb', '#14b8a6', '#f97316', '#8b5cf6'][i % 4],
    };
  });

  return (
    <svg viewBox={`0 0 ${width} ${height}`} style={{ width: '100%', height: '100%' }}>
      {people.map((person) => (
        <Person
          key={person.key}
          x={person.x}
          y={person.y}
          scale={person.scale}
          shirt={person.shirt}
        />
      ))}
    </svg>
  );
};
