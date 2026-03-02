import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, Easing } from 'remotion';

/**
 * FILE: ChalkboardEquation.tsx
 * PURPOSE: A native Remotion recreation of Manim's iconic math drawing style.
 * It takes complex SVG paths (like integrals or algorithms) and uses
 * `strokeDasharray` math to slowly "chalk" them onto the screen.
 */

// A complex mathematical integral equation represented as an SVG path
const MATH_PATH = "M30 150 C 30 50, 80 50, 80 150 C 80 250, 130 250, 130 150 M140 180 Q 150 150 170 150 T 200 180 M220 120 L 220 180 M210 150 L 250 150 M280 180 C 270 130 330 130 320 180 Z";

export const ChalkboardEquation: React.FC<{ accentColor?: string }> = ({ accentColor = '#ffffff' }) => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    // The estimated length of our complex SVG math path
    const pathLength = 1200;

    // Animate the path drawing over exactly 3 seconds (fps * 3)
    const drawProgress = interpolate(
        frame,
        [0, fps * 3],
        [pathLength, 0],
        {
            extrapolateRight: 'clamp',
            easing: Easing.inOut(Easing.cubic) // Smooth ease in and out like a hand drawing
        }
    );

    // A slight "chalk dust" glow
    const filter = `drop-shadow(0 0 10px ${accentColor}80)`;

    return (
        <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
            <svg
                width="800"
                height="400"
                viewBox="0 0 400 300"
                style={{ filter, transform: 'scale(2.5)' }} // Scaled up massively to fill the vertical frame
            >
                {/* The Manim-style drawing trace */}
                <path
                    d={MATH_PATH}
                    fill="none"
                    stroke={accentColor}
                    strokeWidth="4"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeDasharray={pathLength}
                    strokeDashoffset={drawProgress}
                />
            </svg>
        </AbsoluteFill>
    );
};
