import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

export interface GradientOverlayProps {
    gradient?: string;
    opacity?: number;
    direction?: number; // degrees
}

export const GradientOverlay: React.FC<GradientOverlayProps> = ({
    gradient,
    opacity = 0.4,
    direction = 135
}) => {
    const frame = useCurrentFrame();
    const fadeIn = interpolate(frame, [0, 20], [0, opacity], { extrapolateRight: 'clamp' });

    const defaultGradient = `linear-gradient(${direction}deg, #FF10F0 0%, #00FFFF 50%, #6C5CE7 100%)`;

    return (
        <AbsoluteFill
            style={{
                background: gradient || defaultGradient,
                opacity: fadeIn,
                mixBlendMode: 'overlay',
                pointerEvents: 'none',
                zIndex: 9998,
            }}
        />
    );
};
