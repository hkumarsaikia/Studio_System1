/**
 * FILE: WaveField.jsx
 * PURPOSE: A generative, morphing terrain background using simplex noise.
 *
 * This calculates overlapping paths ("waves") using `simplex-noise`. The 
 * noise function uses the current Remotion frame as the Z-axis (time),
 * causing the terrain to organically shift, morph, and flow over the duration
 * of the scene without requiring heavy video assets.
 *
 * PROPS:
 *   @param {string} accentColor - The primary brand line color
 *   @param {number} duration    - Total frames to animate over
 */
import React, { useMemo } from 'react';
import { AbsoluteFill, useVideoConfig, useCurrentFrame, interpolate } from 'remotion';
import { createNoise3D } from 'simplex-noise';

export const WaveField = ({ accentColor = '#38bdf8', duration = 300 }) => {
    const frame = useCurrentFrame();
    const { width, height } = useVideoConfig();

    // We initialize the noise generator once per render
    const noise3D = useMemo(() => createNoise3D(), []);

    // Compute the waves for the current frame
    // We offset the 'time' parameter extremely slowly so it flows gently
    const timeOffset = frame * 0.005;

    const lines = 12;      // Number of stacked horizontal waves
    const points = 40;     // Resolution of each wave curve
    const ySpacing = 60;   // Distance between each wave
    const amplitude = 180; // How tall the waves can get

    const paths = [];

    for (let i = 0; i < lines; i++) {
        // Determine the base Y position of this line (centered vertically)
        const baseY = height / 2 + (i - lines / 2) * ySpacing;
        let d = '';

        for (let j = 0; j <= points; j++) {
            // Map j [0, points] to x coordinate [0, width]
            const x = (j / points) * width;

            // The noise coordinates.
            // x-axis: spatial spread (so it looks wavy left-to-right)
            // y-axis: line index spread (so each line is similar but offset from the one above)
            // z-axis: time flow (so it animates)
            const nx = x * 0.002;
            const ny = i * 0.15;
            const nz = timeOffset;

            // Generate a noise value between -1 and 1
            let noiseVal = noise3D(nx, ny, nz);

            // Dampen the noise at the left/right edges so it ties nicely to the screen bounds
            // Multiplier goes 0 -> 1 -> 0 across the width
            const edgeDampening = Math.sin((j / points) * Math.PI);
            noiseVal *= edgeDampening;

            const y = baseY + noiseVal * amplitude;

            if (j === 0) {
                d += `M ${x} ${y} `;
            } else {
                d += `L ${x} ${y} `;
            }
        }
        paths.push(d);
    }

    // Fade in the waves
    const opacity = interpolate(frame, [0, 30], [0, 0.4], {
        extrapolateRight: 'clamp',
    });

    return (
        <AbsoluteFill style={{ opacity }}>
            <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
                {paths.map((d, i) => (
                    <path
                        key={i}
                        d={d}
                        fill="none"
                        stroke={accentColor}
                        strokeWidth="3"
                        strokeLinecap="round"
                        style={{
                            // Add a slight glowing effect to the lines
                            filter: `drop-shadow(0 0 10px ${accentColor})`,
                        }}
                    />
                ))}
            </svg>
        </AbsoluteFill>
    );
};
