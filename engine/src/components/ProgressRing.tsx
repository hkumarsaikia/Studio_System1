import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate, useVideoConfig } from 'remotion';

export interface ProgressRingProps {
    rings?: Array<{ value: number; label: string; color: string }>;
}

const defaultRings = [
    { value: 85, label: 'CPU', color: '#38bdf8' },
    { value: 62, label: 'MEM', color: '#22c55e' },
    { value: 93, label: 'NET', color: '#f472b6' },
    { value: 47, label: 'DSK', color: '#EFF396' },
];

export const ProgressRing: React.FC<ProgressRingProps> = ({
    rings = defaultRings,
}) => {
    const frame = useCurrentFrame();
    const fadeIn = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' });

    const baseRadius = 180;
    const strokeWidth = 22;
    const gap = 10;

    return (
        <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', opacity: fadeIn }}>
            <div style={{ position: 'relative', width: baseRadius * 2 + 100, height: baseRadius * 2 + 100 }}>
                <svg
                    width="100%" height="100%"
                    viewBox={`0 0 ${(baseRadius + 50) * 2} ${(baseRadius + 50) * 2}`}
                    style={{ transform: 'rotate(-90deg)' }}
                >
                    {rings.map((ring, i) => {
                        const r = baseRadius - i * (strokeWidth + gap);
                        const circumference = 2 * Math.PI * r;

                        // Staggered animation: each ring starts 8 frames after the previous
                        const delay = i * 8;
                        const displayValue = interpolate(frame - delay, [0, 50], [0, ring.value], {
                            extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
                        });
                        const offset = circumference - (displayValue / 100) * circumference;
                        const cx = baseRadius + 50;
                        const cy = baseRadius + 50;

                        return (
                            <g key={i}>
                                {/* Background track */}
                                <circle
                                    cx={cx} cy={cy} r={r}
                                    fill="none" stroke="#1e293b"
                                    strokeWidth={strokeWidth}
                                />
                                {/* Animated arc */}
                                <circle
                                    cx={cx} cy={cy} r={r}
                                    fill="none" stroke={ring.color}
                                    strokeWidth={strokeWidth}
                                    strokeDasharray={circumference}
                                    strokeDashoffset={offset}
                                    strokeLinecap="round"
                                />
                            </g>
                        );
                    })}
                </svg>

                {/* Labels positioned to the right of the rings */}
                <div style={{
                    position: 'absolute',
                    top: 0, left: 0, right: 0, bottom: 0,
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center',
                    alignItems: 'center',
                    gap: 6,
                }}>
                    {rings.map((ring, i) => {
                        const delay = i * 8;
                        const displayValue = interpolate(frame - delay, [0, 50], [0, ring.value], {
                            extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
                        });
                        return (
                            <div key={i} style={{
                                display: 'flex', alignItems: 'center', gap: 10,
                                fontSize: 20, fontWeight: 700,
                                color: ring.color,
                            }}>
                                <span style={{ fontSize: 14, color: '#94a3b8', width: 40 }}>{ring.label}</span>
                                <span>{Math.round(displayValue)}%</span>
                            </div>
                        );
                    })}
                </div>
            </div>
        </AbsoluteFill>
    );
};
