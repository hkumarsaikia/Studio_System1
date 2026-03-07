import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';

export interface PrismFieldProps {
    color?: string;
    secondaryColor?: string;
    prismCount?: number;
}

export const PrismField: React.FC<PrismFieldProps> = ({
    color = '#38bdf8',
    secondaryColor = '#a78bfa',
    prismCount = 14,
}) => {
    const frame = useCurrentFrame();
    const { width, height } = useVideoConfig();
    const fadeIn = interpolate(frame, [0, 20], [0, 1], {
        extrapolateRight: 'clamp',
    });
    const columns = 4;

    return (
        <AbsoluteFill style={{ opacity: fadeIn, overflow: 'hidden', pointerEvents: 'none' }}>
            <svg width="100%" height="100%" viewBox={`0 0 ${width} ${height}`}>
                <defs>
                    <linearGradient id="prism-field-grad-0" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#ffffff" stopOpacity="0.92" />
                        <stop offset="35%" stopColor={color} stopOpacity="0.38" />
                        <stop offset="100%" stopColor={color} stopOpacity="0.05" />
                    </linearGradient>
                    <linearGradient id="prism-field-grad-1" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#ffffff" stopOpacity="0.92" />
                        <stop offset="35%" stopColor={secondaryColor} stopOpacity="0.34" />
                        <stop offset="100%" stopColor={secondaryColor} stopOpacity="0.05" />
                    </linearGradient>
                    <filter id="prism-field-blur">
                        <feGaussianBlur stdDeviation="18" />
                    </filter>
                </defs>

                {Array.from({ length: 6 }).map((_, index) => {
                    const y = 180 + index * 260 + Math.sin(frame * 0.01 + index) * 18;
                    return (
                        <line
                            key={`prism-guide-${index}`}
                            x1={-120}
                            y1={y}
                            x2={width + 120}
                            y2={y - 90}
                            stroke={index % 2 === 0 ? color : secondaryColor}
                            strokeWidth={1}
                            opacity={0.08}
                        />
                    );
                })}

                {Array.from({ length: prismCount }).map((_, index) => {
                    const lane = index % columns;
                    const depth = Math.floor(index / columns);
                    const size = 48 + (index % 5) * 16;
                    const baseX = ((lane + 0.5) / columns) * width + (depth % 2 === 0 ? -40 : 40);
                    const baseY = 220 + depth * 205;
                    const x = baseX + Math.sin(frame * 0.02 + index * 0.7) * 90;
                    const y = baseY + Math.cos(frame * 0.025 + index * 0.9) * 75;
                    const rotation = frame * (index % 2 === 0 ? 0.7 : -0.9) + index * 17;
                    const scale = 0.85 + ((Math.sin(frame * 0.05 + index) + 1) / 2) * 0.18;
                    const fillId = index % 2 === 0 ? 'prism-field-grad-0' : 'prism-field-grad-1';
                    const stroke = index % 2 === 0 ? color : secondaryColor;

                    return (
                        <g
                            key={`prism-shard-${index}`}
                            transform={`translate(${x} ${y}) rotate(${rotation}) scale(${scale})`}
                        >
                            <polygon
                                points={`0,-${size} ${size * 0.85},0 0,${size} -${size * 0.85},0`}
                                fill={`url(#${fillId})`}
                                opacity={0.55}
                            />
                            <polygon
                                points={`0,-${size * 1.4} ${size * 0.22},-${size * 0.2} 0,${size * 1.1} -${size * 0.22},-${size * 0.2}`}
                                fill={stroke}
                                opacity={0.12}
                                filter="url(#prism-field-blur)"
                            />
                            <polyline
                                points={`0,-${size} ${size * 0.85},0 0,${size} -${size * 0.85},0 0,-${size}`}
                                fill="none"
                                stroke={stroke}
                                strokeWidth={2.2}
                                opacity={0.6}
                            />
                            <line
                                x1={0}
                                y1={-size}
                                x2={0}
                                y2={size}
                                stroke="#f8fafc"
                                strokeWidth={1.5}
                                opacity={0.42}
                            />
                            <line
                                x1={-size * 0.55}
                                y1={0}
                                x2={size * 0.55}
                                y2={0}
                                stroke="#f8fafc"
                                strokeWidth={1}
                                opacity={0.16}
                            />
                        </g>
                    );
                })}
            </svg>
        </AbsoluteFill>
    );
};
