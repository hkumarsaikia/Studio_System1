import React from 'react';
import { interpolate, useCurrentFrame, spring, useVideoConfig } from 'remotion';
import { darken } from 'polished';

export interface PersonProps {
    x?: number;
    y?: number;
    skin?: string;
    shirt?: string;
    mood?: 'neutral' | 'stressed' | 'happy' | 'thinking';
    size?: number;
}

export const Person: React.FC<PersonProps> = ({
    x = 0,
    y = 0,
    skin = '#c9a676',
    shirt = '#38bdf8',
    mood = 'neutral',
    size = 1.0
}) => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    // ── Continuous Breathing/Floating Animation ──
    // Uses harmonic oscillation for a gentle, natural breathe effect
    const breatheCycle = (frame % (fps * 2)) / (fps * 2);
    const breatheOffset = Math.sin(breatheCycle * Math.PI * 2) * 3;

    // Gentle arm swinging
    const armSwing = Math.sin(breatheCycle * Math.PI * 2) * 2;

    const shadowSkin = darken(0.15, skin);
    const shadowShirt = darken(0.2, shirt);
    const baseShirt = shirt;

    // ── Mood-specific facial/body config ──
    const moodConfig = {
        neutral: {
            browY: 0,
            mouthCurve: 0,
            armAngle: 0,
            innerBrowAngle: 0,
        },
        stressed: {
            browY: -4,
            mouthCurve: 4,
            armAngle: -30,
            innerBrowAngle: -15, // Furrowed
        },
        happy: {
            browY: -3,
            mouthCurve: -6,
            armAngle: 45,
            innerBrowAngle: 10,
        },
        thinking: {
            browY: -2,
            mouthCurve: 2,
            armAngle: -15,
            innerBrowAngle: 0,
        },
    };

    const config = moodConfig[mood] || moodConfig.neutral;

    return (
        <g transform={`translate(${x}, ${y}) scale(${size})`} filter="url(#kurzDropShadow)">

            {/* ── Floor Drop Shadow ── */}
            <ellipse cx="0" cy="5" rx="30" ry="8" fill="#0f172a" opacity="0.3" filter="url(#neonGlow)" />

            <g transform={`translate(0, ${breatheOffset})`}>

                {/* ── Legs ── */}
                {/* Back leg */}
                <rect x="2" y="-25" width="12" height="30" rx="6" fill="#1e293b" />
                {/* Front leg */}
                <rect x="-14" y="-25" width="12" height="30" rx="6" fill="#334155" />

                {/* ── Body / Torso ── */}
                {/* Shadow layer for volume */}
                <rect x="-18" y="-65" width="36" height="42" rx="10" fill={shadowShirt} transform="translate(2, 2)" />
                {/* Base layer */}
                <rect x="-18" y="-65" width="36" height="42" rx="10" fill={baseShirt} />
                {/* Highlight layer */}
                <path d="M-18 -55 Q0 -65 18 -55 L18 -65 Q0 -75 -18 -65 Z" fill="#ffffff" opacity="0.2" />

                {/* ── Arms ── */}
                {/* Back Arm */}
                <rect x="14" y="-62" width="10" height="32" rx="5" fill={shadowSkin}
                    transform={`rotate(${-config.armAngle - armSwing}, 18, -62)`} />

                {/* ── Head ── */}
                <g transform="translate(0, -90)">
                    {/* Shadow base for the head */}
                    <circle cx="2" cy="2" r="22" fill={shadowSkin} />
                    {/* Main Head (Uses global SvgDefs skinGlow to make it spherical) */}
                    <circle cx="0" cy="0" r="22" fill={skin} />
                    <circle cx="0" cy="0" r="22" fill="url(#skinGlow)" />

                    {/* Hair / Character accents could go here */}

                    {/* ── Face ── */}
                    {/* Eyebrows */}
                    <line x1="-10" y1={-10 + config.browY} x2="-4" y2={-10 + config.browY + (config.innerBrowAngle * -0.1)}
                        stroke="#0f172a" strokeWidth="3" strokeLinecap="round" />
                    <line x1="4" y1={-10 + config.browY + (config.innerBrowAngle * -0.1)} x2="10" y2={-10 + config.browY}
                        stroke="#0f172a" strokeWidth="3" strokeLinecap="round" />

                    {/* Eyes */}
                    <circle cx="-7" cy="-2" r="2.5" fill="#0f172a" />
                    <circle cx="7" cy="-2" r="2.5" fill="#0f172a" />

                    {/* Mouth */}
                    <path d={`M -6 6 Q 0 ${6 + config.mouthCurve} 6 6`}
                        stroke="#0f172a" strokeWidth="2.5" fill="none" strokeLinecap="round" />

                    {/* Cheeks */}
                    <circle cx="-12" cy="4" r="3" fill="#ef4444" opacity="0.2" filter="url(#neonGlow)" />
                    <circle cx="12" cy="4" r="3" fill="#ef4444" opacity="0.2" filter="url(#neonGlow)" />
                </g>

                {/* Front Arm */}
                <rect x="-24" y="-62" width="10" height="32" rx="5" fill={skin}
                    transform={`rotate(${config.armAngle + armSwing}, -18, -62)`} />

                {/* Arm Shadow/Gradient overlay */}
                <rect x="-24" y="-62" width="10" height="32" rx="5" fill="url(#skinGlow)" opacity="0.5"
                    transform={`rotate(${config.armAngle + armSwing}, -18, -62)`} />

            </g>

            {/* ── Mood VFX (Floating emojis/particles) ── */}
            <g transform={`translate(0, ${breatheOffset})`}>
                {mood === 'stressed' && (
                    <g filter="url(#neonGlow)">
                        <path d="M-20 -130 Q-15 -120 -20 -115 Q-25 -120 -20 -130" fill="#38bdf8" />
                        <path d="M15 -135 Q20 -125 15 -120 Q10 -125 15 -135" fill="#38bdf8" />
                    </g>
                )}

                {mood === 'happy' && (
                    <g filter="url(#neonGlow)">
                        <polygon points="-25,-120 -20,-115 -15,-120 -20,-125" fill="#fbbf24" opacity="0.9" />
                        <polygon points="20,-125 25,-120 30,-125 25,-130" fill="#fbbf24" opacity="0.9" />
                        <polygon points="0,-135 4,-130 8,-135 4,-140" fill="#fbbf24" opacity="0.9" />
                    </g>
                )}

                {mood === 'thinking' && (
                    <g fill="#94a3b8" filter="url(#neonGlow)" opacity="0.7">
                        <circle cx="20" cy="-115" r="3" />
                        <circle cx="28" cy="-125" r="4.5" />

                        {/* Cloud bubble */}
                        <path d="M35 -140 A8 8 0 0 1 45 -145 A10 10 0 0 1 60 -140 A8 8 0 0 1 60 -125 A8 8 0 0 1 45 -125 A10 10 0 0 1 35 -140" />
                        {/* Inner glowing question mark */}
                        <text x="49" y="-130" textAnchor="middle" fontSize="14" fill="#0f172a" fontWeight="bold">?</text>
                    </g>
                )}
            </g>

        </g>
    );
};
