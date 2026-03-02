import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

export interface MotionLayerProps {
    children: React.ReactNode;
    duration?: number;
}

export const MotionLayer: React.FC<MotionLayerProps> = ({ children, duration = 300 }) => {
    const frame = useCurrentFrame();

    const opacity = interpolate(frame, [0, 12, duration - 12, duration], [0, 1, 1, 0], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
    });

    const blur = interpolate(frame, [0, 18, duration - 18, duration], [8, 0, 0, 8], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
    });

    return (
        <AbsoluteFill style={{ opacity, filter: `blur(${blur}px)` }}>
            {children}
        </AbsoluteFill>
    );
};
