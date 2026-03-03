import React from 'react';
import { AbsoluteFill } from 'remotion';

export interface ScanLinesProps {
    opacity?: number;
    lineWidth?: number;
    gap?: number;
}

export const ScanLines: React.FC<ScanLinesProps> = ({
    opacity = 0.08,
    lineWidth = 2,
    gap = 4,
}) => {
    return (
        <AbsoluteFill
            style={{
                backgroundImage: `repeating-linear-gradient(
                    0deg,
                    transparent,
                    transparent ${gap}px,
                    rgba(0, 0, 0, ${opacity}) ${gap}px,
                    rgba(0, 0, 0, ${opacity}) ${gap + lineWidth}px
                )`,
                pointerEvents: 'none',
                zIndex: 9991,
            }}
        />
    );
};
