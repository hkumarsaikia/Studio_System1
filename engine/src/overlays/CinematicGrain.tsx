import React from 'react';
import { AbsoluteFill } from 'remotion';

export interface CinematicGrainProps {
    opacity?: number;
    baseFrequency?: number;
}

export const CinematicGrain: React.FC<CinematicGrainProps> = ({ opacity = 0.05, baseFrequency = 0.6 }) => {
    return (
        <AbsoluteFill
            style={{
                width: '100%',
                height: '100%',
                pointerEvents: 'none',
                zIndex: 9999,
                opacity,
                mixBlendMode: 'overlay',
            }}
        >
            <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                <filter id="cinematic-grain" x="0" y="0" width="100%" height="100%">
                    <feTurbulence
                        type="fractalNoise"
                        baseFrequency={baseFrequency}
                        numOctaves={3}
                        stitchTiles="stitch"
                    />
                    <feColorMatrix type="saturate" values="0" />
                </filter>
                <rect width="100%" height="100%" filter="url(#cinematic-grain)" fill="none" />
            </svg>
        </AbsoluteFill>
    );
};
