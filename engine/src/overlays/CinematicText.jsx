/**
 * FILE: CinematicText.jsx
 * PURPOSE: Animated text overlay for scene titles and subtitles.
 *
 * This is the "text card" that appears on every scene — it shows:
 *   1. Category badge (pill-shaped label, e.g. "ECONOMICS & FINANCE")
 *   2. Title (large hero text with text shadow)
 *   3. Subtitle (smaller explanatory text, optional)
 *
 * ANIMATIONS:
 *   - Fade in over first 12 frames, hold, fade out at frame 210–240
 *   - Slide up from 22px below during entrance
 *   - Spring scale from 92% → 100% for a bouncy entrance feel
 *
 * PROPS:
 *   @param {string} title       - Main heading text
 *   @param {string} subtitle    - Secondary text (optional)
 *   @param {string} accentColor - Category pill color (default: sky blue)
 *   @param {string} category    - Category label text
 */
import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

export const CinematicText = ({ title, subtitle, accentColor = '#38bdf8', category = 'SYSTEMS EXPLAINER' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Opacity: fade in over 12 frames, hold until 210, fade out by 240
  const opacity = interpolate(frame, [0, 12, 210, 240], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Slide up: content moves from 22px below to 0 over first 20 frames
  const y = interpolate(frame, [0, 20], [22, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Spring scale: bouncy entrance from 92% to 100%
  const scale = spring({
    frame,
    fps,
    config: { damping: 200 },  // High damping = subtle, professional bounce
  });

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'center',
        alignItems: 'center',
        textAlign: 'center',
        padding: 80,
        opacity,
        transform: `translateY(${y}px) scale(${0.92 + scale * 0.08})`,
      }}
    >
      {/* Category badge — pill-shaped label at the top */}
      <div
        style={{
          marginBottom: 20,
          display: 'inline-block',
          padding: '8px 14px',
          borderRadius: 999,                              // Fully rounded pill shape
          backgroundColor: `${accentColor}33`,            // Accent color at 20% opacity
          border: `1px solid ${accentColor}`,
          fontSize: 20,
          fontWeight: 700,
          letterSpacing: 1,
        }}
      >
        {category}
      </div>

      {/* Main title */}
      <h1 style={{ fontSize: 74, lineHeight: 1.08, marginBottom: 18, textShadow: '0 8px 30px rgba(15,23,42,0.4)' }}>
        {title}
      </h1>

      {/* Optional subtitle */}
      {subtitle ? (
        <p style={{ fontSize: 32, lineHeight: 1.35, maxWidth: 920, margin: 0, color: '#e2e8f0' }}>{subtitle}</p>
      ) : null}
    </AbsoluteFill>
  );
};
