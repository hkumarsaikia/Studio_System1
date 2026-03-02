/**
 * FILE: FlowDiagram.jsx
 * PURPOSE: Parametric flow diagram showing a chain of 2–6 connected nodes.
 *
 * Used in scenes that explain cause-and-effect chains, process flows,
 * or system pipelines (e.g. "Input → System → Output").
 *
 * PROPS:
 *   @param {string[]} labels    - Text labels for each node (2–6 items)
 *   @param {string}   direction - 'horizontal' (default) or 'vertical'
 *   @param {string}   accent    - Stroke/arrow color (defaults to primarySystem)
 *
 * INTERNALS:
 *   - Node: Rounded rectangle with centered label text
 *   - Arrow: Line with directional arrowhead (auto-computed from dx/dy)
 *   - Layout auto-adjusts spacing based on node count
 *
 * USAGE:
 *   <FlowDiagram
 *     labels={['Trigger', 'Mechanism', 'Outcome']}
 *     direction="horizontal"
 *     accent="#22c55e"
 *   />
 */
import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import { colors } from '../styles/theme.js';

// ── Node ── Single box in the flow, with rounded corners and centered label
const Node = ({ x, y, label, accent = colors.primarySystem }) => (
  <g transform={`translate(${x}, ${y})`}>
    <rect width="180" height="70" rx="14" fill="#1e293b" stroke={accent} strokeWidth="2" />
    <text x="90" y="42" fill="#e2e8f0" fontSize="20" textAnchor="middle"
      style={{ fontFamily: "'Montserrat', sans-serif", fontWeight: 600 }}>
      {label}
    </text>
  </g>
);

// ── Arrow ── Connects two nodes with a line and directional triangle head.
// The arrowhead is computed from the direction vector (dx, dy) so it
// works correctly for both horizontal and vertical layouts.
const Arrow = ({ x1, y1, x2, y2, accent = colors.primarySystem, delayStart = 0 }) => {
  const frame = useCurrentFrame();
  const dx = x2 - x1;
  const dy = y2 - y1;
  const len = Math.sqrt(dx * dx + dy * dy);
  // Unit vector pointing from start to end
  const ux = dx / len;
  const uy = dy / len;
  // Arrowhead tip is at (x2, y2); the two base points sit 18px back
  // and 10px perpendicular to the line direction.
  const tipX = x2;
  const tipY = y2;
  const base1X = tipX - ux * 18 - uy * 10;
  const base1Y = tipY - uy * 18 + ux * 10;
  const base2X = tipX - ux * 18 + uy * 10;
  const base2Y = tipY - uy * 18 - ux * 10;

  // Animate the line drawing over 30 frames, starting after 'delayStart'
  const offset = interpolate(frame, [delayStart, delayStart + 30], [len, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Make the arrowhead fade in exactly when the line finishes drawing
  const headOpacity = interpolate(frame, [delayStart + 25, delayStart + 30], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <>
      <line
        x1={x1} y1={y1} x2={x2} y2={y2}
        stroke={accent} strokeWidth="4"
        strokeDasharray={len}
        strokeDashoffset={offset}
      />
      <polygon
        points={`${tipX},${tipY} ${base1X},${base1Y} ${base2X},${base2Y}`}
        fill={accent}
        opacity={headOpacity}
      />
    </>
  );
};

/**
 * FlowDiagram – the main exported component.
 * Renders nodes and arrows in either horizontal or vertical layout.
 */
export const FlowDiagram = ({
  labels = ['Input', 'System', 'Output'],
  direction = 'horizontal',
  accent = colors.primarySystem,
}) => {
  // Clamp to 6 nodes max to keep the diagram readable at video resolution
  const count = Math.min(labels.length, 6);
  const safeLabels = labels.slice(0, count);

  // ── Vertical layout ──
  if (direction === 'vertical') {
    const nodeX = 360;                         // Center horizontally
    const startY = 30;
    const gap = 90;                            // Vertical space between nodes
    const viewH = startY + count * (70 + gap); // Dynamic viewBox height

    return (
      <svg viewBox={`0 0 900 ${viewH}`} style={{ width: '100%', height: '100%' }}>
        {safeLabels.map((label, idx) => {
          const ny = startY + idx * (70 + gap);
          return (
            <React.Fragment key={idx}>
              <Node x={nodeX} y={ny} label={label} accent={accent} />
              {/* Draw arrow between consecutive nodes (not after the last) */}
              {idx < count - 1 && (
                <Arrow
                  x1={nodeX + 90} y1={ny + 70}
                  x2={nodeX + 90} y2={ny + 70 + gap}
                  accent={accent}
                  delayStart={15 + idx * 25} // Staggered drawing
                />
              )}
            </React.Fragment>
          );
        })}
      </svg>
    );
  }

  // ── Horizontal layout (default) ──
  const nodeWidth = 180;
  // Even spacing: distribute remaining width among gaps
  const gap = Math.max(40, (900 - count * nodeWidth) / (count + 1));
  const startX = gap;

  return (
    <svg viewBox="0 0 900 420" style={{ width: '100%', height: '100%' }}>
      {safeLabels.map((label, idx) => {
        const nx = startX + idx * (nodeWidth + gap);
        return (
          <React.Fragment key={idx}>
            <Node x={nx} y={160} label={label} accent={accent} />
            {/* Arrow connects right edge of this node to left edge of next */}
            {idx < count - 1 && (
              <Arrow
                x1={nx + nodeWidth} y1={195}
                x2={nx + nodeWidth + gap} y2={195}
                accent={accent}
                delayStart={15 + idx * 25} // Staggered horizontal drawing
              />
            )}
          </React.Fragment>
        );
      })}
    </svg>
  );
};
