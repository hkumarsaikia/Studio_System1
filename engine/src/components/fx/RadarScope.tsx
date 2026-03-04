import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from 'remotion';

export interface RadarScopeProps {
    color?: string;
    blipCount?: number;
}

export const RadarScope: React.FC<RadarScopeProps> = ({
    color = '#39FF14',
    blipCount = 6
}) => {
    const frame = useCurrentFrame();
    const { width, height } = useVideoConfig();
    const cx = width / 2;
    const cy = height * 0.45;
    const maxRadius = 300;

    const sweepAngle = (frame * 3) % 360;
    const fadeIn = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });

    // Deterministic blip positions
    const blips = Array.from({ length: blipCount }).map((_, i) => {
        const angle = ((i * 137.508) % 360) * (Math.PI / 180);
        const dist = 60 + (Math.sin(i * 42.42) * 0.5 + 0.5) * (maxRadius - 80);
        const blipAngle = (angle * 180 / Math.PI) % 360;

        // Blip visibility: glow brightly when the sweep passes over it
        const diff = Math.abs(((sweepAngle - blipAngle) % 360 + 360) % 360);
        const intensity = diff < 30 ? interpolate(diff, [0, 30], [1, 0.15]) : 0.15;

        return {
            x: cx + Math.cos(angle) * dist,
            y: cy + Math.sin(angle) * dist,
            intensity,
        };
    });

    return (
        <AbsoluteFill style={{ opacity: fadeIn }}>
            <svg width="100%" height="100%" viewBox={`0 0 ${width} ${height}`}>
                {/* Concentric range rings */}
                {[0.25, 0.5, 0.75, 1].map((scale, i) => (
                    <circle
                        key={i}
                        cx={cx} cy={cy} r={maxRadius * scale}
                        fill="none" stroke={color} strokeWidth={1} opacity={0.2}
                    />
                ))}

                {/* Cross axis lines */}
                <line x1={cx - maxRadius} y1={cy} x2={cx + maxRadius} y2={cy} stroke={color} strokeWidth={1} opacity={0.15} />
                <line x1={cx} y1={cy - maxRadius} x2={cx} y2={cy + maxRadius} stroke={color} strokeWidth={1} opacity={0.15} />

                {/* Sweep line */}
                <line
                    x1={cx} y1={cy}
                    x2={cx + Math.cos(sweepAngle * Math.PI / 180) * maxRadius}
                    y2={cy + Math.sin(sweepAngle * Math.PI / 180) * maxRadius}
                    stroke={color} strokeWidth={2} opacity={0.9}
                />

                {/* Sweep trail (fading arc) */}
                {Array.from({ length: 20 }).map((_, i) => {
                    const trailAngle = ((sweepAngle - i * 3) * Math.PI) / 180;
                    return (
                        <line
                            key={`trail-${i}`}
                            x1={cx} y1={cy}
                            x2={cx + Math.cos(trailAngle) * maxRadius}
                            y2={cy + Math.sin(trailAngle) * maxRadius}
                            stroke={color} strokeWidth={1}
                            opacity={0.4 * (1 - i / 20)}
                        />
                    );
                })}

                {/* Blips */}
                {blips.map((blip, i) => (
                    <g key={i}>
                        <circle cx={blip.x} cy={blip.y} r={8} fill={color} opacity={blip.intensity} />
                        <circle cx={blip.x} cy={blip.y} r={16} fill="none" stroke={color} strokeWidth={1} opacity={blip.intensity * 0.5} />
                    </g>
                ))}

                {/* Center dot */}
                <circle cx={cx} cy={cy} r={4} fill={color} />
            </svg>
        </AbsoluteFill>
    );
};
