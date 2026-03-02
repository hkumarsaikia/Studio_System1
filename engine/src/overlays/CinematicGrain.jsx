/**
 * FILE: CinematicGrain.jsx
 * PURPOSE: Renders an SVG <feTurbulence> filter to create a film grain overlay.
 *
 * This injects a subtle but powerful visual texture uniformly across the whole
 * video composition, elevating it from flat digital colors to a premium,
 * "cinematic" aesthetic.
 *
 * PROPS:
 *   @param {number} opacity     - Strength of the grain (default: 0.05)
 *   @param {number} baseFrequency - Size/density of the noise (default: 0.6)
 */
import React from 'react';
import { AbsoluteFill } from 'remotion';

export const CinematicGrain = ({ opacity = 0.05, baseFrequency = 0.6 }) => {
    return (
        <AbsoluteFill
            style={{
                width: '100%',
                height: '100%',
                pointerEvents: 'none', // Ensure it doesn't block other layers
                zIndex: 9999,          // Always sit on top of everything
                opacity,
                mixBlendMode: 'overlay', // Blend organically into the colors beneath
            }}
        >
            <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                <filter id="cinematic-grain" x="0" y="0" width="100%" height="100%">
                    <feTurbulence
                        type="fractalNoise"
                        baseFrequency={baseFrequency}
                        numOctaves="3"
                        stitchTiles="stitch"
                    />
                    {/* Convert the noise to black/white for the grain effect */}
                    <feColorMatrix type="saturate" values="0" />
                </filter>
                <rect width="100%" height="100%" filter="url(#cinematic-grain)" fill="none" />
            </svg>
        </AbsoluteFill>
    );
};
