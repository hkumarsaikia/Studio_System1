import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';

export interface AuroraBandsProps {
    colors?: string[];
    ribbonCount?: number;
    glowColor?: string;
}

export const AuroraBands: React.FC<AuroraBandsProps> = ({
    colors = ['#22d3ee', '#a78bfa', '#34d399'],
    ribbonCount = 5,
    glowColor = '#e0f2fe',
}) => {
    const frame = useCurrentFrame();
    const { width, height } = useVideoConfig();
    const fadeIn = interpolate(frame, [0, 18], [0, 1], {
        extrapolateRight: 'clamp',
    });
    const horizon = height * 0.22;
    const bandSpan = width / (ribbonCount + 1);

    return (
        <AbsoluteFill
            style={{
                opacity: fadeIn,
                overflow: 'hidden',
                pointerEvents: 'none',
                mixBlendMode: 'screen',
            }}
        >
            <svg width="100%" height="100%" viewBox={`0 0 ${width} ${height}`}>
                <defs>
                    <filter id="aurora-band-blur">
                        <feGaussianBlur stdDeviation="24" />
                    </filter>
                    <filter id="aurora-glow-blur">
                        <feGaussianBlur stdDeviation="60" />
                    </filter>
                    {Array.from({ length: ribbonCount }).map((_, index) => {
                        const color = colors[index % colors.length];
                        return (
                            <linearGradient
                                key={`aurora-band-grad-${index}`}
                                id={`aurora-band-grad-${index}`}
                                x1="0%"
                                y1="0%"
                                x2="0%"
                                y2="100%"
                            >
                                <stop offset="0%" stopColor={color} stopOpacity="0.08" />
                                <stop offset="35%" stopColor={color} stopOpacity="0.6" />
                                <stop offset="72%" stopColor={color} stopOpacity="0.18" />
                                <stop offset="100%" stopColor={color} stopOpacity="0" />
                            </linearGradient>
                        );
                    })}
                </defs>

                {Array.from({ length: ribbonCount }).map((_, index) => {
                    const baseX = bandSpan * (index + 1);
                    const sway = Math.sin(frame * 0.018 + index * 0.95) * 90;
                    const curl = Math.cos(frame * 0.024 + index * 1.4) * 130;
                    const drift = Math.sin(frame * 0.011 + index * 0.7) * 50;
                    const bandWidth = bandSpan * (0.75 + (index % 3) * 0.12);
                    const midY1 = horizon + Math.sin(frame * 0.017 + index) * 80;
                    const midY2 = height * 0.55 + Math.cos(frame * 0.023 + index * 1.2) * 120;
                    const bottomY = height + 160;
                    const left = baseX - bandWidth * 0.52 + sway;
                    const right = baseX + bandWidth * 0.52 + sway;
                    const bandOpacity = 0.35 + ((Math.sin(frame * 0.02 + index) + 1) / 2) * 0.2;
                    const d = [
                        `M ${left} -140`,
                        `C ${baseX - bandWidth + curl} ${midY1}, ${baseX - bandWidth * 0.15 - drift} ${midY2}, ${baseX - bandWidth * 0.35 + drift} ${bottomY}`,
                        `L ${baseX + bandWidth * 0.4 + drift} ${bottomY}`,
                        `C ${baseX + bandWidth * 0.2 + curl} ${midY2}, ${baseX + bandWidth + drift} ${midY1}, ${right} -140`,
                        'Z',
                    ].join(' ');

                    return (
                        <path
                            key={`aurora-band-${index}`}
                            d={d}
                            fill={`url(#aurora-band-grad-${index})`}
                            opacity={bandOpacity}
                            filter="url(#aurora-band-blur)"
                        />
                    );
                })}

                {Array.from({ length: 7 }).map((_, index) => {
                    const cx = (width / 8) * (index + 1) + Math.sin(frame * 0.01 + index) * 40;
                    const cy = horizon + Math.cos(frame * 0.016 + index * 0.7) * 80;
                    const radius = 80 + (index % 3) * 28;
                    const opacity = 0.08 + ((Math.sin(frame * 0.03 + index * 0.9) + 1) / 2) * 0.1;

                    return (
                        <circle
                            key={`aurora-glow-${index}`}
                            cx={cx}
                            cy={cy}
                            r={radius}
                            fill={glowColor}
                            opacity={opacity}
                            filter="url(#aurora-glow-blur)"
                        />
                    );
                })}
            </svg>
        </AbsoluteFill>
    );
};
