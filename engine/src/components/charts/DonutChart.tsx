import React from 'react';
import { interpolate, useCurrentFrame, useVideoConfig } from 'remotion';

export interface DonutChartProps {
    value?: number; // Target percentage (0-100)
    label?: string; // Text to display below the chart
    color?: string; // Main chart color
}

export const DonutChart: React.FC<DonutChartProps> = ({
    value = 75,
    label = 'SYSTEM EFFICIENCY',
    color = '#38bdf8'
}) => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    // Chart dimensions
    const radius = 160;
    const stroke = 32;
    const circumference = 2 * Math.PI * radius;

    // Animate the chart filling up over the first 45 frames
    const displayValue = interpolate(frame, [0, 45], [0, value], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
    });

    // Calculate the strokeDashoffset to reveal the arc
    const strokeDashoffset = circumference - (displayValue / 100) * circumference;

    // Fade the whole chart in quickly
    const opacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' });

    // Pop the label in
    const labelY = interpolate(frame, [10, 30], [20, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
    const labelOpacity = interpolate(frame, [10, 30], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

    return (
        <div style={{ opacity, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', width: '100%', height: '100%' }}>
            <div style={{ position: 'relative', width: radius * 2 + stroke, height: radius * 2 + stroke }}>
                {/* SVG Container for the donut arcs */}
                <svg
                    width="100%"
                    height="100%"
                    viewBox={`0 0 ${radius * 2 + stroke} ${radius * 2 + stroke}`}
                    style={{ transform: 'rotate(-90deg)' }} // Rotate so 0% starts at the top
                >
                    {/* Background Track Arc */}
                    <circle
                        cx={(radius * 2 + stroke) / 2}
                        cy={(radius * 2 + stroke) / 2}
                        r={radius}
                        fill="none"
                        stroke="#1e293b" // Soft dark track
                        strokeWidth={stroke}
                    />

                    {/* Animated Value Arc */}
                    <circle
                        cx={(radius * 2 + stroke) / 2}
                        cy={(radius * 2 + stroke) / 2}
                        r={radius}
                        fill="none"
                        stroke={color}
                        strokeWidth={stroke}
                        strokeDasharray={circumference}
                        strokeDashoffset={strokeDashoffset}
                        strokeLinecap="round" // Rounded ends for a premium feel
                        style={{ transition: 'stroke-dashoffset 0.1s linear' }}
                    />
                </svg>

                {/* Counter readout exactly in the center of the ring */}
                <div style={{
                    position: 'absolute',
                    top: 0, left: 0, right: 0, bottom: 0,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: 72,
                    fontWeight: 800,
                    color: '#f8fafc',
                    textShadow: `0 0 20px ${color}40`
                }}>
                    {Math.round(displayValue)}%
                </div>
            </div>

            {/* Label Text below the chart */}
            <h2 style={{
                marginTop: 40,
                fontSize: 32,
                fontWeight: 600,
                color: '#cbd5e1',
                letterSpacing: 2,
                opacity: labelOpacity,
                transform: `translateY(${labelY}px)`,
                textTransform: 'uppercase'
            }}>
                {label}
            </h2>
        </div>
    );
};
