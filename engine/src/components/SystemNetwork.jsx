/**
 * FILE: SystemNetwork.jsx
 * PURPOSE: Pentagon-shaped node graph for system relationship scenes.
 *
 * Renders 5 labeled nodes arranged in a pentagon with connecting edges.
 * Used for "System boundary" and "Cause layer 3" scenes to show how
 * different actors/forces in a system are interconnected.
 *
 * The layout is a fixed pentagon (5 nodes at predefined coordinates)
 * with 7 edges connecting them (5 perimeter + 2 cross links).
 *
 * PROPS:
 *   @param {string[]} nodes - Labels for each of the 5 nodes
 */
import React, { useEffect, useState } from 'react';
import { AbsoluteFill } from 'remotion';
import Particles, { initParticlesEngine } from "@tsparticles/react";
import { loadSlim } from "@tsparticles/slim";

export const SystemNetwork = ({ nodes = ['State', 'Market', 'Labor', 'Capital', 'Public'] }) => {
  const [init, setInit] = useState(false);

  useEffect(() => {
    initParticlesEngine(async (engine) => {
      await loadSlim(engine);
    }).then(() => {
      setInit(true);
    });
  }, []);
  // Fixed pentagon positions (hand-tuned for 900×480 viewBox)
  const points = [
    { x: 200, y: 180 },   // Top-left
    { x: 460, y: 90 },    // Top-center
    { x: 700, y: 180 },   // Top-right
    { x: 610, y: 340 },   // Bottom-right
    { x: 290, y: 340 },   // Bottom-left
  ];

  // Edge definitions: pairs of node indices to connect
  // First 5 = perimeter edges, last 2 = cross-links for complexity
  const links = [
    [0, 1], [1, 2], [2, 3], [3, 4], [4, 0],  // Pentagon perimeter
    [0, 2], [1, 3],                             // Cross-links
  ];

  return (
    <AbsoluteFill style={{ position: 'relative' }}>
      {init && (
        <Particles
          id="tsparticles-network"
          options={{
            fpsLimit: 30, // Remotion standard
            particles: {
              color: { value: '#38bdf8' },
              links: {
                color: '#38bdf8',
                distance: 150,
                enable: true,
                opacity: 0.15,
                width: 1,
              },
              move: {
                enable: true,
                speed: 0.5,
                direction: 'none',
              },
              number: { density: { enable: true, area: 800 }, value: 30 },
              opacity: { value: 0.2 },
              shape: { type: 'circle' },
              size: { value: { min: 1, max: 2 } },
            },
            detectRetina: true,
          }}
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            zIndex: -1,
          }}
        />
      )}
      <svg viewBox="0 0 900 480" style={{ width: '100%', height: '100%' }}>
        {/* Draw edges first (behind nodes) */}
        {links.map(([a, b], idx) => (
          <line
            key={`l-${idx}`}
            x1={points[a].x} y1={points[a].y}
            x2={points[b].x} y2={points[b].y}
            stroke="#38bdf8" strokeOpacity="0.45" strokeWidth="3"
          />
        ))}

        {/* Draw nodes on top of edges */}
        {points.map((p, idx) => (
          <g key={`n-${idx}`} transform={`translate(${p.x}, ${p.y})`}>
            <circle r="46" fill="#0f172a" stroke="#38bdf8" strokeWidth="3" />
            <text x="0" y="7" fill="#e2e8f0" textAnchor="middle" fontSize="18" fontWeight="700">
              {nodes[idx] || `N${idx + 1}`}
            </text>
          </g>
        ))}
      </svg>
    </AbsoluteFill>
  );
};
