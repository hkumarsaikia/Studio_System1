import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate, useVideoConfig } from 'remotion';

export interface PulseGridProps {
    color?: string;
    columns?: number;
    rows?: number;
}

export const PulseGrid: React.FC<PulseGridProps> = ({
    color = '#6C5CE7',
    columns = 12,
    rows = 8
}) => {
    const frame = useCurrentFrame();
    const { width, height } = useVideoConfig();
    const fadeIn = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' });

    const cellW = width / columns;
    const cellH = height / rows;

    return (
        <AbsoluteFill style={{ opacity: fadeIn }}>
            <svg width="100%" height="100%" viewBox={`0 0 ${width} ${height}`}>
                {Array.from({ length: rows }).map((_, row) =>
                    Array.from({ length: columns }).map((_, col) => {
                        const cx = col * cellW + cellW / 2;
                        const cy = row * cellH + cellH / 2;

                        // Ripple wave expanding outward from center
                        const distFromCenter = Math.sqrt(
                            Math.pow(cx - width / 2, 2) + Math.pow(cy - height / 2, 2)
                        );
                        const wave = Math.sin((frame * 0.12) - distFromCenter * 0.008);
                        const dotSize = 3 + wave * 3;
                        const dotOpacity = 0.2 + wave * 0.4;

                        return (
                            <circle
                                key={`${row}-${col}`}
                                cx={cx} cy={cy}
                                r={Math.max(1, dotSize)}
                                fill={color}
                                opacity={Math.max(0.05, dotOpacity)}
                            />
                        );
                    })
                )}
            </svg>
        </AbsoluteFill>
    );
};
