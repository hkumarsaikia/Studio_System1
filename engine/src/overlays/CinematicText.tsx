import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

export interface CinematicTextProps {
    title: string;
    subtitle?: string | null;
    accentColor?: string;
    category?: string;
}

export const CinematicText: React.FC<CinematicTextProps> = ({
    title,
    subtitle,
    accentColor = '#38bdf8',
    category = 'SYSTEMS EXPLAINER'
}) => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    const opacity = interpolate(frame, [0, 12, 210, 240], [0, 1, 1, 0], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
    });

    const y = interpolate(frame, [0, 20], [22, 0], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
    });

    const scale = spring({
        frame,
        fps,
        config: { damping: 200 },
    });

    return (
        <AbsoluteFill
            style={{
                justifyContent: 'center',
                alignItems: 'center',
                textAlign: 'center',
                padding: 80,
                opacity,
                transform: `translateY(${y}px) scale(${0.92 + scale * 0.08})`,
            }}
        >
            <div
                style={{
                    marginBottom: 20,
                    display: 'inline-block',
                    padding: '8px 14px',
                    borderRadius: 999,
                    backgroundColor: `${accentColor}33`,
                    border: `1px solid ${accentColor}`,
                    fontSize: 20,
                    fontWeight: 700,
                    letterSpacing: 1,
                }}
            >
                {category}
            </div>

            <h1 style={{ fontSize: 74, lineHeight: 1.08, marginBottom: 18, textShadow: '0 8px 30px rgba(15,23,42,0.4)' }}>
                {title}
            </h1>

            {subtitle ? (
                <p style={{ fontSize: 32, lineHeight: 1.35, maxWidth: 920, margin: 0, color: '#e2e8f0' }}>{subtitle}</p>
            ) : null}
        </AbsoluteFill>
    );
};
