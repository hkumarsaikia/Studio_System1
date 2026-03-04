import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate, useVideoConfig } from 'remotion';

export interface ParticleExplosionProps {
    color?: string;
    particleCount?: number;
}

export const ParticleExplosion: React.FC<ParticleExplosionProps> = ({
    color = '#FFB347',
    particleCount = 80
}) => {
    const frame = useCurrentFrame();
    const { width, height } = useVideoConfig();
    const cx = width / 2;
    const cy = height * 0.45;

    const globalOpacity = interpolate(frame, [0, 10, 60, 90], [0, 1, 1, 0], {
        extrapolateRight: 'clamp',
    });

    // Generate deterministic particles
    const particles = Array.from({ length: particleCount }).map((_, i) => {
        const angle = (i / particleCount) * Math.PI * 2 + Math.sin(i * 7.77) * 0.5;
        const speed = 3 + (Math.sin(i * 13.37) * 0.5 + 0.5) * 8;
        const size = 3 + (Math.cos(i * 29.31) * 0.5 + 0.5) * 6;
        const delay = Math.floor((Math.sin(i * 5.55) * 0.5 + 0.5) * 8);

        const t = Math.max(0, frame - delay);
        const distance = t * speed;
        const fadeOut = interpolate(t, [0, 30, 60], [1, 0.8, 0], { extrapolateRight: 'clamp' });

        return {
            x: cx + Math.cos(angle) * distance,
            y: cy + Math.sin(angle) * distance + t * 0.8, // slight gravity
            r: size * fadeOut,
            opacity: fadeOut,
        };
    });

    return (
        <AbsoluteFill style={{ opacity: globalOpacity }}>
            <svg width="100%" height="100%" viewBox={`0 0 ${width} ${height}`}>
                {/* Central flash */}
                {frame < 15 && (
                    <circle
                        cx={cx} cy={cy}
                        r={interpolate(frame, [0, 15], [10, 200], { extrapolateRight: 'clamp' })}
                        fill={color}
                        opacity={interpolate(frame, [0, 15], [1, 0], { extrapolateRight: 'clamp' })}
                    />
                )}
                {/* Particle trails */}
                {particles.map((p, i) => (
                    <circle
                        key={i}
                        cx={p.x} cy={p.y}
                        r={p.r}
                        fill={color}
                        opacity={p.opacity}
                    />
                ))}
            </svg>
        </AbsoluteFill>
    );
};
