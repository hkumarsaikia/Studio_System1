import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';

export interface OrbitalAssemblyProps {
    color?: string;
    secondaryColor?: string;
    satelliteCount?: number;
}

export const OrbitalAssembly: React.FC<OrbitalAssemblyProps> = ({
    color = '#38bdf8',
    secondaryColor = '#a78bfa',
    satelliteCount = 8,
}) => {
    const frame = useCurrentFrame();
    const { width, height } = useVideoConfig();
    const fadeIn = interpolate(frame, [0, 15], [0, 1], {
        extrapolateRight: 'clamp',
    });
    const centerX = width / 2;
    const centerY = height * 0.52;
    const pulse = 1 + Math.sin(frame * 0.08) * 0.06;

    return (
        <AbsoluteFill style={{ opacity: fadeIn, pointerEvents: 'none' }}>
            <svg width="100%" height="100%" viewBox={`0 0 ${width} ${height}`}>
                <defs>
                    <radialGradient id="orbital-core-fill" cx="50%" cy="50%" r="50%">
                        <stop offset="0%" stopColor="#ffffff" stopOpacity="0.95" />
                        <stop offset="24%" stopColor={color} stopOpacity="0.9" />
                        <stop offset="72%" stopColor={secondaryColor} stopOpacity="0.24" />
                        <stop offset="100%" stopColor={secondaryColor} stopOpacity="0" />
                    </radialGradient>
                    <filter id="orbital-glow">
                        <feGaussianBlur stdDeviation="16" />
                    </filter>
                </defs>

                <g transform={`translate(${centerX} ${centerY})`}>
                    <circle r={180} fill="url(#orbital-core-fill)" opacity={0.35} filter="url(#orbital-glow)" />
                    <circle r={76 * pulse} fill={color} opacity={0.14} />
                    <circle r={48} fill="#f8fafc" opacity={0.95} />
                    <circle r={20 + ((Math.sin(frame * 0.12) + 1) / 2) * 10} fill={secondaryColor} opacity={0.4} />

                    {Array.from({ length: 4 }).map((_, ringIndex) => {
                        const rotation = frame * (ringIndex % 2 === 0 ? 0.75 : -0.6) + ringIndex * 18;
                        const rx = 160 + ringIndex * 65;
                        const ry = 58 + ringIndex * 34;
                        const ringOpacity = 0.22 + ringIndex * 0.06;

                        return (
                            <g key={`orbit-ring-${ringIndex}`} transform={`rotate(${rotation})`}>
                                <ellipse
                                    rx={rx}
                                    ry={ry}
                                    fill="none"
                                    stroke={ringIndex % 2 === 0 ? color : secondaryColor}
                                    strokeWidth={ringIndex === 0 ? 4 : 2}
                                    opacity={ringOpacity}
                                />
                                <ellipse
                                    rx={rx}
                                    ry={ry}
                                    fill="none"
                                    stroke="#f8fafc"
                                    strokeWidth={1}
                                    strokeDasharray="18 14"
                                    opacity={0.14}
                                />
                            </g>
                        );
                    })}

                    {Array.from({ length: 12 }).map((_, index) => {
                        const angle = (index / 12) * Math.PI * 2 + frame * 0.01;
                        const inner = 96;
                        const outer = 138;
                        const x1 = Math.cos(angle) * inner;
                        const y1 = Math.sin(angle) * inner;
                        const x2 = Math.cos(angle) * outer;
                        const y2 = Math.sin(angle) * outer;

                        return (
                            <line
                                key={`orbital-spoke-${index}`}
                                x1={x1}
                                y1={y1}
                                x2={x2}
                                y2={y2}
                                stroke={secondaryColor}
                                strokeWidth={2}
                                opacity={0.18}
                            />
                        );
                    })}

                    {Array.from({ length: satelliteCount }).map((_, index) => {
                        const orbit = index % 4;
                        const direction = index % 2 === 0 ? 1 : -1;
                        const angle =
                            frame * 0.025 * (orbit + 1) * direction +
                            index * ((Math.PI * 2) / satelliteCount);
                        const rx = 190 + orbit * 58;
                        const ry = 80 + orbit * 36;
                        const x = Math.cos(angle) * rx;
                        const y = Math.sin(angle) * ry;
                        const size = 12 + orbit * 3;
                        const glow = 0.25 + ((Math.sin(frame * 0.09 + index) + 1) / 2) * 0.35;

                        return (
                            <g key={`orbital-satellite-${index}`}>
                                <line
                                    x1={0}
                                    y1={0}
                                    x2={x}
                                    y2={y}
                                    stroke={color}
                                    strokeWidth={1.5}
                                    opacity={0.1 + orbit * 0.05}
                                />
                                <g transform={`translate(${x} ${y})`}>
                                    <circle r={size + 10} fill={secondaryColor} opacity={0.12} filter="url(#orbital-glow)" />
                                    <circle r={size} fill="#f8fafc" opacity={0.95} />
                                    <polygon
                                        points={`0,-${size + 6} ${size + 6},0 0,${size + 6} -${size + 6},0`}
                                        fill="none"
                                        stroke={orbit % 2 === 0 ? color : secondaryColor}
                                        strokeWidth={2}
                                        opacity={glow}
                                    />
                                </g>
                            </g>
                        );
                    })}
                </g>
            </svg>
        </AbsoluteFill>
    );
};
