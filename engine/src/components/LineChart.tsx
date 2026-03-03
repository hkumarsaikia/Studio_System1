import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate, useVideoConfig } from 'remotion';

export interface LineChartProps {
    values?: number[];
    color?: string;
    label?: string;
}

export const LineChart: React.FC<LineChartProps> = ({
    values = [10, 35, 28, 55, 42, 68, 60, 82, 75, 95],
    color = '#38bdf8',
    label = 'TREND ANALYSIS',
}) => {
    const frame = useCurrentFrame();
    const { width, height } = useVideoConfig();

    const chartW = width * 0.75;
    const chartH = 350;
    const chartX = (width - chartW) / 2;
    const chartY = height * 0.35;

    const maxVal = Math.max(...values);
    const fadeIn = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' });

    // How much of the line to reveal (draws left-to-right over 60 frames)
    const revealProgress = interpolate(frame, [5, 65], [0, 1], {
        extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
    });

    // Build points
    const points = values.map((v, i) => {
        const x = chartX + (i / (values.length - 1)) * chartW;
        const y = chartY + chartH - (v / maxVal) * chartH;
        return { x, y };
    });

    // Build the visible polyline (clipped by revealProgress)
    const visibleCount = Math.ceil(revealProgress * points.length);
    const visiblePoints = points.slice(0, visibleCount);

    // Polyline string
    const polylinePoints = visiblePoints.map(p => `${p.x},${p.y}`).join(' ');

    // Area fill path (close at the bottom)
    const areaPath = visiblePoints.length > 1
        ? `M${visiblePoints[0].x},${chartY + chartH} ${visiblePoints.map(p => `L${p.x},${p.y}`).join(' ')} L${visiblePoints[visiblePoints.length - 1].x},${chartY + chartH} Z`
        : '';

    return (
        <AbsoluteFill style={{ opacity: fadeIn }}>
            <svg width="100%" height="100%" viewBox={`0 0 ${width} ${height}`}>
                <defs>
                    <linearGradient id="area-fill" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor={color} stopOpacity="0.3" />
                        <stop offset="100%" stopColor={color} stopOpacity="0.02" />
                    </linearGradient>
                </defs>

                {/* Horizontal grid lines */}
                {[0, 0.25, 0.5, 0.75, 1].map((pct, i) => (
                    <line
                        key={i}
                        x1={chartX} y1={chartY + chartH * (1 - pct)}
                        x2={chartX + chartW} y2={chartY + chartH * (1 - pct)}
                        stroke="#334155" strokeWidth={1} opacity={0.4}
                    />
                ))}

                {/* Area fill */}
                {areaPath && <path d={areaPath} fill="url(#area-fill)" />}

                {/* Line */}
                {visiblePoints.length > 1 && (
                    <polyline
                        points={polylinePoints}
                        fill="none"
                        stroke={color}
                        strokeWidth={4}
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    />
                )}

                {/* Data dots */}
                {visiblePoints.map((p, i) => (
                    <g key={i}>
                        <circle cx={p.x} cy={p.y} r={7} fill={color} />
                        <circle cx={p.x} cy={p.y} r={12} fill="none" stroke={color} strokeWidth={2} opacity={0.3} />
                    </g>
                ))}

                {/* Label */}
                <text
                    x={width / 2} y={chartY - 30}
                    textAnchor="middle"
                    fontSize={24} fontWeight={700}
                    fill="#cbd5e1" letterSpacing={2}
                    fontFamily="'Montserrat', sans-serif"
                >
                    {label}
                </text>
            </svg>
        </AbsoluteFill>
    );
};
