/**
 * FILE: Person.jsx
 * PURPOSE: Parametric SVG human figure for crowd scenes and character
 *          illustrations across all 500 explainer videos.
 *
 * This component draws a gender-neutral person in SVG. The key feature
 * is the `mood` prop, which alters the figure's facial expression and
 * body language to match the emotional tone of each scene.
 *
 * PROPS:
 *   @param {number} x         - Horizontal position of the figure
 *   @param {number} y         - Vertical position (feet ground level)
 *   @param {string} skin      - Skin fill color (hex)
 *   @param {string} shirt     - Shirt fill color (hex)
 *   @param {string} mood      - 'neutral' | 'stressed' | 'happy' | 'thinking'
 *
 * MOOD EFFECTS:
 *   neutral  → Flat eyebrows, straight mouth, arms at sides
 *   stressed → Angled brows, frown, hands-on-head gesture, sweat drops
 *   happy    → Raised brows, smile, arms wide, sparkle effects
 *   thinking → One brow raised, diagonal mouth, hand-on-chin, thought bubble
 *
 * USAGE:
 *   <Person x={100} y={300} skin="#b07d62" shirt="#38bdf8" mood="stressed" />
 */
import React from 'react';

export const Person = ({ x = 0, y = 0, skin = '#c9a676', shirt = '#38bdf8', mood = 'neutral' }) => {
  // ── Mood-specific facial features ── ── ── ── ── ── ── ── ── ──
  // Each mood adjusts brow angle, mouth shape, and arm position
  // to convey emotion without complex animation.
  const moodConfig = {
    neutral: {
      browY: 0,            // Flat brows
      mouthCurve: 0,       // Straight mouth
      armAngle: 0,         // Arms at sides
    },
    stressed: {
      browY: -4,           // Furrowed brows (angled inward)
      mouthCurve: 4,       // Downturned frown
      armAngle: -30,       // Hands raised toward head
    },
    happy: {
      browY: -3,           // Slightly raised brows
      mouthCurve: -6,      // Upward smile curve
      armAngle: 45,        // Arms spread wide (celebratory)
    },
    thinking: {
      browY: -2,           // One brow slightly raised
      mouthCurve: 2,       // Diagonal/uncertain mouth
      armAngle: -15,       // Hand toward chin
    },
  };

  const config = moodConfig[mood] || moodConfig.neutral;

  return (
    <g transform={`translate(${x}, ${y})`}>
      {/* ── Head ── */}
      <circle cx="0" cy="-85" r="20" fill={skin} />

      {/* ── Eyebrows ── adjust Y position based on mood */}
      <line x1="-8" y1={-95 + config.browY} x2="-3" y2={-96 + config.browY}
        stroke="#1e293b" strokeWidth="2.5" strokeLinecap="round" />
      <line x1="3" y1={-96 + config.browY} x2="8" y2={-95 + config.browY}
        stroke="#1e293b" strokeWidth="2.5" strokeLinecap="round" />

      {/* ── Eyes ── simple dots */}
      <circle cx="-6" cy="-88" r="2" fill="#1e293b" />
      <circle cx="6" cy="-88" r="2" fill="#1e293b" />

      {/* ── Mouth ── curve direction controlled by mouthCurve value */}
      {/* Negative = smile, Positive = frown, Zero = straight */}
      <path d={`M -6 -78 Q 0 ${-78 + config.mouthCurve} 6 -78`}
        stroke="#1e293b" strokeWidth="2" fill="none" strokeLinecap="round" />

      {/* ── Body / Torso ── */}
      <rect x="-15" y="-65" width="30" height="40" rx="6" fill={shirt} />

      {/* ── Legs ── */}
      <rect x="-12" y="-25" width="10" height="30" rx="4" fill="#334155" />
      <rect x="2" y="-25" width="10" height="30" rx="4" fill="#334155" />

      {/* ── Arms ── rotation angle changes per mood for body language */}
      <rect x="-22" y="-62" width="8" height="28" rx="4" fill={skin}
        transform={`rotate(${config.armAngle}, -18, -62)`} />
      <rect x="14" y="-62" width="8" height="28" rx="4" fill={skin}
        transform={`rotate(${-config.armAngle}, 18, -62)`} />

      {/* ── Mood-specific visual indicators ── */}
      {/* These extra SVG elements reinforce the emotion beyond just facial features */}

      {/* Stressed: sweat droplets floating above the head */}
      {mood === 'stressed' && (
        <>
          <circle cx="-12" cy="-115" r="3" fill="#38bdf8" opacity={0.6} />
          <circle cx="10" cy="-120" r="2.5" fill="#38bdf8" opacity={0.5} />
        </>
      )}

      {/* Happy: sparkle/star burst effects */}
      {mood === 'happy' && (
        <>
          <circle cx="-18" cy="-110" r="3" fill="#fbbf24" opacity={0.8} />
          <circle cx="16" cy="-115" r="2" fill="#fbbf24" opacity={0.7} />
          <circle cx="0" cy="-120" r="2.5" fill="#fbbf24" opacity={0.6} />
        </>
      )}

      {/* Thinking: thought bubble (three ascending dots + cloud) */}
      {mood === 'thinking' && (
        <>
          <circle cx="18" cy="-105" r="3" fill="#94a3b8" opacity={0.5} />
          <circle cx="24" cy="-115" r="4" fill="#94a3b8" opacity={0.4} />
          <circle cx="30" cy="-128" r="6" fill="#94a3b8" opacity={0.3} />
        </>
      )}
    </g>
  );
};
