import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';

export interface LightLeakProps {
    color?: string;
    direction?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';
}

export const LightLeak: React.FC<LightLeakProps> = ({
    color = '#f97316',
    direction = 'top-right',
}) => {
    const frame = useCurrentFrame();
    const { width, height } = useVideoConfig();

    // Light leak sweeps across the frame over 90 frames, peaks at 45
    const sweepProgress = interpolate(frame % 180, [0, 45, 90, 180], [0, 1, 0.3, 0], {
        extrapolateRight: 'clamp',
    });

    const positions: Record<string, { cx: string; cy: string }> = {
        'top-left': { cx: '10%', cy: '10%' },
        'top-right': { cx: '90%', cy: '10%' },
        'bottom-left': { cx: '10%', cy: '90%' },
        'bottom-right': { cx: '90%', cy: '90%' },
    };

    const pos = positions[direction] || positions['top-right'];
    const size = 30 + sweepProgress * 50;

    return (
        <AbsoluteFill
            style={{
                backgroundImage: `radial-gradient(ellipse at ${pos.cx} ${pos.cy}, ${color}80 0%, ${color}20 ${size}%, transparent ${size + 20}%)`,
                opacity: sweepProgress * 0.4,
                mixBlendMode: 'screen',
                pointerEvents: 'none',
                zIndex: 9992,
            }}
        />
    );
};
