import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate, useVideoConfig } from 'remotion';

export interface TimelineBarProps {
    events?: Array<{ label: string; progress: number }>;
    color?: string;
}

const defaultEvents = [
    { label: 'Phase 1', progress: 0.2 },
    { label: 'Phase 2', progress: 0.45 },
    { label: 'Phase 3', progress: 0.7 },
    { label: 'Phase 4', progress: 0.95 },
];

export const TimelineBar: React.FC<TimelineBarProps> = ({
    events = defaultEvents,
    color = '#EFF396'
}) => {
    const frame = useCurrentFrame();
    const { width } = useVideoConfig();
    const fadeIn = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' });

    // Timeline fills left-to-right over 90 frames
    const fillProgress = interpolate(frame, [10, 90], [0, 1], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
    });

    const barWidth = width * 0.75;
    const barX = (width - barWidth) / 2;
    const barY = 480;

    return (
        <AbsoluteFill style={{ opacity: fadeIn }}>
            <svg width="100%" height="100%" viewBox={`0 0 ${width} 960`}>
                {/* Track */}
                <rect x={barX} y={barY} width={barWidth} height={8} rx={4} fill="#1e293b" />

                {/* Fill Bar */}
                <rect x={barX} y={barY} width={barWidth * fillProgress} height={8} rx={4} fill={color} />

                {/* Event markers */}
                {events.map((event, i) => {
                    const eventX = barX + barWidth * event.progress;
                    const isReached = fillProgress >= event.progress;
                    const dotScale = isReached
                        ? interpolate(
                            fillProgress,
                            [event.progress, Math.min(event.progress + 0.05, 1)],
                            [0.5, 1],
                            { extrapolateRight: 'clamp' }
                        )
                        : 0.5;

                    return (
                        <g key={i}>
                            {/* Connector */}
                            <line
                                x1={eventX} y1={barY - 10}
                                x2={eventX} y2={barY - 50}
                                stroke={isReached ? color : '#475569'}
                                strokeWidth={2}
                                opacity={isReached ? 1 : 0.4}
                            />
                            {/* Dot */}
                            <circle
                                cx={eventX} cy={barY + 4}
                                r={10 * dotScale}
                                fill={isReached ? color : '#475569'}
                                stroke={isReached ? '#fff' : 'none'}
                                strokeWidth={2}
                            />
                            {/* Label */}
                            <text
                                x={eventX} y={barY - 60}
                                textAnchor="middle"
                                fontSize={20}
                                fontWeight={isReached ? 700 : 400}
                                fill={isReached ? '#f8fafc' : '#64748b'}
                                fontFamily="'Montserrat', sans-serif"
                            >
                                {event.label}
                            </text>
                        </g>
                    );
                })}
            </svg>
        </AbsoluteFill>
    );
};
