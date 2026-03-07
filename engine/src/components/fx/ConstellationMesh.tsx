import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';

const MESH_POINTS = [
    { x: 0.12, y: 0.14 },
    { x: 0.24, y: 0.2 },
    { x: 0.38, y: 0.11 },
    { x: 0.52, y: 0.22 },
    { x: 0.7, y: 0.15 },
    { x: 0.84, y: 0.28 },
    { x: 0.15, y: 0.44 },
    { x: 0.31, y: 0.52 },
    { x: 0.49, y: 0.46 },
    { x: 0.65, y: 0.58 },
    { x: 0.82, y: 0.47 },
    { x: 0.2, y: 0.76 },
    { x: 0.43, y: 0.73 },
    { x: 0.61, y: 0.82 },
    { x: 0.79, y: 0.74 },
];

export interface ConstellationMeshProps {
    color?: string;
    secondaryColor?: string;
}

export const ConstellationMesh: React.FC<ConstellationMeshProps> = ({
    color = '#22d3ee',
    secondaryColor = '#a78bfa',
}) => {
    const frame = useCurrentFrame();
    const { width, height } = useVideoConfig();
    const fadeIn = interpolate(frame, [0, 15], [0, 1], {
        extrapolateRight: 'clamp',
    });
    const scanX = ((frame * 18) % (width + 320)) - 160;
    const points = MESH_POINTS.map((point) => ({
        x: point.x * width,
        y: point.y * height,
    }));
    const connections: { key: string; ax: number; ay: number; bx: number; by: number; midpoint: number }[] = [];

    for (let i = 0; i < points.length; i++) {
        for (let j = i + 1; j < points.length; j++) {
            const dx = points[i].x - points[j].x;
            const dy = points[i].y - points[j].y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < 290) {
                connections.push({
                    key: `${i}-${j}`,
                    ax: points[i].x,
                    ay: points[i].y,
                    bx: points[j].x,
                    by: points[j].y,
                    midpoint: (points[i].x + points[j].x) / 2,
                });
            }
        }
    }

    return (
        <AbsoluteFill style={{ opacity: fadeIn, pointerEvents: 'none' }}>
            <svg width="100%" height="100%" viewBox={`0 0 ${width} ${height}`}>
                <defs>
                    <filter id="constellation-glow">
                        <feGaussianBlur stdDeviation="8" />
                    </filter>
                    <linearGradient id="constellation-scan" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor="#ffffff" stopOpacity="0" />
                        <stop offset="50%" stopColor="#ffffff" stopOpacity="0.35" />
                        <stop offset="100%" stopColor="#ffffff" stopOpacity="0" />
                    </linearGradient>
                </defs>

                {connections.map((connection) => {
                    const distanceToScan = Math.abs(connection.midpoint - scanX);
                    const scanBoost = Math.max(0, 1 - distanceToScan / 240);
                    const opacity = 0.08 + scanBoost * 0.38;

                    return (
                        <line
                            key={connection.key}
                            x1={connection.ax}
                            y1={connection.ay}
                            x2={connection.bx}
                            y2={connection.by}
                            stroke={connection.midpoint % 2 === 0 ? color : secondaryColor}
                            strokeWidth={1.8}
                            opacity={opacity}
                        />
                    );
                })}

                {points.map((point, index) => {
                    const twinkle = 0.35 + ((Math.sin(frame * 0.08 + index * 0.9) + 1) / 2) * 0.65;
                    const radius = 2.5 + twinkle * 4.2;
                    const fill = index % 2 === 0 ? color : secondaryColor;

                    return (
                        <g key={`constellation-point-${index}`}>
                            <circle
                                cx={point.x}
                                cy={point.y}
                                r={radius * 2.8}
                                fill={fill}
                                opacity={0.14}
                                filter="url(#constellation-glow)"
                            />
                            <circle cx={point.x} cy={point.y} r={radius} fill="#f8fafc" opacity={0.96} />
                            <circle
                                cx={point.x}
                                cy={point.y}
                                r={radius * 1.6}
                                fill="none"
                                stroke={fill}
                                strokeWidth={1.4}
                                opacity={0.42}
                            />
                        </g>
                    );
                })}

                <rect
                    x={scanX - 90}
                    y={0}
                    width={180}
                    height={height}
                    fill="url(#constellation-scan)"
                    opacity={0.18}
                />
            </svg>
        </AbsoluteFill>
    );
};
