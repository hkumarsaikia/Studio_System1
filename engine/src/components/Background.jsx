/**
 * FILE: Background.jsx
 * PURPOSE: Animated gradient background for every scene.
 *
 * Creates a three-layer visual:
 *   1. Base gradient (palette.background → palette.secondary)
 *   2. Floating color orbs (sky blue + pink) that pulse and drift
 *   3. Subtle grid overlay for a "tech dashboard" feel
 *
 * The background is always behind all scene content (z-order: bottom).
 *
 * PROPS:
 *   @param {object} palette           - { background, secondary } hex colors
 *   @param {string} motion            - 'pan' enables slow vertical drift
 */
import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

export const Background = ({ palette, motion = 'pan' }) => {
  const frame = useCurrentFrame();

  // Slow vertical drift when motion='pan' (moves background slightly upward)
  const translateY = interpolate(frame, [0, 300], [0, -40], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Horizontal drift for the floating orbs layer
  const driftX = interpolate(frame, [0, 300], [-25, 25], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Pulsing opacity for the two glow layers (creates a breathing effect)
  const glowA = interpolate(frame % 180, [0, 90, 180], [0.18, 0.33, 0.18]);
  const glowB = interpolate(frame % 220, [0, 110, 220], [0.12, 0.28, 0.12]);

  // Build the base gradient from palette colors
  const gradient = `linear-gradient(160deg, ${palette.background} 0%, ${palette.secondary} 100%)`;

  return (
    <AbsoluteFill style={{ overflow: 'hidden' }}>
      {/* Layer 1: Base color gradient */}
      <AbsoluteFill
        style={{
          background: gradient,
          transform: motion === 'pan' ? `translateY(${translateY}px)` : 'none',
        }}
      />

      {/* Layer 2: Floating color orbs (radial gradients) that drift sideways */}
      <AbsoluteFill
        style={{
          backgroundImage:
            'radial-gradient(circle at 20% 25%, rgba(56,189,248,0.6) 0%, rgba(56,189,248,0.0) 38%), radial-gradient(circle at 78% 70%, rgba(244,114,182,0.45) 0%, rgba(244,114,182,0.0) 34%)',
          opacity: glowA,
          transform: `translateX(${driftX}px)`,
        }}
      />

      {/* Layer 3: Subtle grid lines for a "tech dashboard" feel */}
      <AbsoluteFill
        style={{
          backgroundImage:
            'linear-gradient(rgba(148,163,184,0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(148,163,184,0.08) 1px, transparent 1px)',
          backgroundSize: '60px 60px',
          opacity: glowB,
        }}
      />
    </AbsoluteFill>
  );
};
