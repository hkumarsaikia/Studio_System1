import React from 'react';
import { AbsoluteFill } from 'remotion';

export interface VignetteProps {
    intensity?: number;
    color?: string;
}

export const Vignette: React.FC<VignetteProps> = ({
    intensity = 0.6,
    color = '#000000',
}) => {
    return (
        <AbsoluteFill
            style={{
                background: `radial-gradient(ellipse at center, transparent 45%, ${color} 100%)`,
                opacity: intensity,
                pointerEvents: 'none',
                zIndex: 9990,
            }}
        />
    );
};
