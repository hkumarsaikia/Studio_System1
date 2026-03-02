/**
 * FILE: DataBars.jsx
 * PURPOSE: Simple bar chart component for data visualization scenes.
 *
 * Renders a horizontal row of vertical bars with value labels above each.
 * Used for "Data lens" scenes that show quantitative comparisons.
 * Bar heights are proportional to values (value × 3 = pixel height).
 *
 * PROPS:
 *   @param {number[]} values - Array of numeric values to display (default: 5 bars)
 */
import React from 'react';

export const DataBars = ({ values = [20, 35, 52, 68, 84] }) => {
  const barWidth = 110;  // Width of each bar in pixels
  const gap = 30;        // Space between bars

  return (
    <svg viewBox="0 0 760 480" style={{ width: '100%', height: '100%' }}>
      {/* Baseline axis */}
      <line x1="50" y1="420" x2="700" y2="420" stroke="#94a3b8" strokeWidth="4" />

      {values.map((value, index) => {
        const x = 70 + index * (barWidth + gap);  // Horizontal position
        const h = value * 3;                       // Height scaled by 3x
        const y = 420 - h;                         // Y position (grows upward from baseline)
        return (
          <g key={index}>
            {/* The bar itself */}
            <rect x={x} y={y} width={barWidth} height={h} rx="10" fill="#38bdf8" opacity={0.85} />
            {/* Value label above the bar */}
            <text x={x + barWidth / 2} y={y - 12} fill="#e2e8f0" fontSize="22" textAnchor="middle">
              {value}
            </text>
          </g>
        );
      })}
    </svg>
  );
};
