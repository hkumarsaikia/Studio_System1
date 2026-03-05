import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig, random } from 'remotion';

export interface BackgroundProps {
    palette: { background: string; secondary: string };
    motion?: string;
    mode?: 'gradient' | 'mesh' | 'aurora' | 'vortex' | 'starfield' | 'terrain';
}

export const Background: React.FC<BackgroundProps> = ({
    palette,
    motion = 'pan',
    mode = 'gradient',
}) => {
    const globalOverlay = (
        <AbsoluteFill style={{ pointerEvents: 'none' }}>
            <AmbientParticles count={30} />
            {/* Global Deep Vignette for minimalist style */}
            <AbsoluteFill style={{
                background: 'radial-gradient(circle at center, transparent 30%, rgba(0,0,0,0.6) 100%)'
            }} />
        </AbsoluteFill>
    );

    let bgContent;
    switch (mode) {
        case 'terrain':
        case 'mesh':
            bgContent = <MeshBackground palette={palette} motion={motion} />;
            break;
        case 'aurora':
            bgContent = <AuroraBackground palette={palette} />;
            break;
        case 'vortex':
            bgContent = <VortexBackground palette={palette} />;
            break;
        case 'starfield':
            bgContent = <StarfieldBackground palette={palette} />;
            break;
        case 'gradient':
        default:
            bgContent = <GradientBackground palette={palette} motion={motion} />;
            break;
    }

    return (
        <AbsoluteFill>
            {bgContent}
            {globalOverlay}
        </AbsoluteFill>
    );
};

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// AMBIENT PARTICLES (minimalist-style floating dust)
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const AmbientParticles: React.FC<{ count: number }> = ({ count }) => {
    const frame = useCurrentFrame();
    const { width, height } = useVideoConfig();

    return (
        <svg width="100%" height="100%" style={{ position: 'absolute', opacity: 0.6, filter: 'url(#neonGlow)' }}>
            {Array.from({ length: count }).map((_, i) => {
                // Generative deterministic randomness based on index
                const seedX = random(`x-${i}`);
                const seedY = random(`y-${i}`);
                const seedSize = random(`size-${i}`);
                const seedSpeed = random(`speed-${i}`);

                const baseX = seedX * width;
                const baseY = seedY * height;

                // Slow drift upward and wobble
                const y = (baseY - frame * (0.5 + seedSpeed)) % (height + 50);
                const actualY = y < -50 ? y + height + 50 : y;

                const xOffset = Math.sin((frame * 0.01) + (i * 10)) * 20;

                const size = 1 + seedSize * 4;
                const opacity = 0.2 + (Math.sin(frame * 0.05 + i) * 0.5 + 0.5) * 0.4;

                return (
                    <circle
                        key={i}
                        cx={baseX + xOffset}
                        cy={actualY}
                        r={size}
                        fill="#ffffff"
                        opacity={opacity}
                    />
                );
            })}
        </svg>
    );
};

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Mode 1: GRADIENT (original, improved with scene-color orbs)
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const GradientBackground: React.FC<{ palette: BackgroundProps['palette']; motion: string }> = ({ palette, motion }) => {
    const frame = useCurrentFrame();
    const translateY = interpolate(frame, [0, 300], [0, -40], { extrapolateRight: 'clamp' });
    const driftX = interpolate(frame, [0, 300], [-25, 25], { extrapolateRight: 'clamp' });
    const glowA = interpolate(frame % 180, [0, 90, 180], [0.18, 0.33, 0.18]);
    const glowB = interpolate(frame % 220, [0, 110, 220], [0.12, 0.28, 0.12]);
    const gradient = `linear-gradient(160deg, ${palette.background} 0%, ${palette.secondary} 100%)`;

    return (
        <AbsoluteFill style={{ overflow: 'hidden' }}>
            <AbsoluteFill style={{ background: gradient, transform: motion === 'pan' ? `translateY(${translateY}px)` : 'none' }} />
            <AbsoluteFill style={{
                backgroundImage: 'radial-gradient(circle at 20% 25%, rgba(56,189,248,0.6) 0%, rgba(56,189,248,0) 38%), radial-gradient(circle at 78% 70%, rgba(244,114,182,0.45) 0%, rgba(244,114,182,0) 34%)',
                opacity: glowA, transform: `translateX(${driftX}px)`,
            }} />
            <AbsoluteFill style={{
                backgroundImage: 'linear-gradient(rgba(148,163,184,0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(148,163,184,0.08) 1px, transparent 1px)',
                backgroundSize: '60px 60px', opacity: glowB,
            }} />
        </AbsoluteFill>
    );
};

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Mode 2: MESH — Multi-point gradient mesh with independent motion
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const MeshBackground: React.FC<{ palette: BackgroundProps['palette']; motion: string }> = ({ palette }) => {
    const frame = useCurrentFrame();

    const orbs = [
        { cx: 20 + Math.sin(frame * 0.015) * 15, cy: 20 + Math.cos(frame * 0.02) * 10, color: palette.secondary, size: 45 },
        { cx: 75 + Math.cos(frame * 0.012) * 12, cy: 30 + Math.sin(frame * 0.018) * 15, color: '#38bdf8', size: 40 },
        { cx: 50 + Math.sin(frame * 0.02) * 20, cy: 70 + Math.cos(frame * 0.015) * 12, color: '#f472b6', size: 38 },
        { cx: 30 + Math.cos(frame * 0.025) * 10, cy: 85 + Math.sin(frame * 0.01) * 8, color: '#a78bfa', size: 35 },
        { cx: 80 + Math.sin(frame * 0.018) * 8, cy: 75 + Math.cos(frame * 0.022) * 14, color: '#14b8a6', size: 30 },
    ];

    const gradients = orbs.map((o, i) =>
        `radial-gradient(circle at ${o.cx}% ${o.cy}%, ${o.color}88 0%, transparent ${o.size}%)`
    ).join(', ');

    return (
        <AbsoluteFill style={{ overflow: 'hidden' }}>
            <AbsoluteFill style={{ background: palette.background }} />
            <AbsoluteFill style={{ backgroundImage: gradients, filter: 'blur(60px)' }} />
            <AbsoluteFill style={{
                backgroundImage: 'linear-gradient(rgba(148,163,184,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(148,163,184,0.05) 1px, transparent 1px)',
                backgroundSize: '80px 80px', opacity: 0.2,
            }} />
        </AbsoluteFill>
    );
};

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Mode 3: AURORA — Flowing wave bands with sinusoidal color shifting
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const AuroraBackground: React.FC<{ palette: BackgroundProps['palette'] }> = ({ palette }) => {
    const frame = useCurrentFrame();
    const { width, height } = useVideoConfig();

    const bands = Array.from({ length: 5 }).map((_, i) => {
        const baseY = height * 0.3 + i * (height * 0.1);
        const amplitude = 40 + i * 15;
        const frequency = 0.003 + i * 0.001;
        const speed = 0.04 + i * 0.008;
        const opacity = 0.15 + (Math.sin(frame * 0.02 + i) * 0.5 + 0.5) * 0.2;

        // Generate a wavy path
        const points: string[] = [];
        for (let x = 0; x <= width; x += 20) {
            const y = baseY + Math.sin(x * frequency + frame * speed) * amplitude + Math.cos(x * frequency * 0.7 + frame * speed * 1.3) * (amplitude * 0.4);
            points.push(`${x},${y}`);
        }
        // Close the path at the bottom
        const d = `M0,${height} L${points.join(' L')} L${width},${height} Z`;

        const colors = ['#38bdf8', '#a78bfa', '#14b8a6', '#f472b6', '#22c55e'];
        return { d, color: colors[i % colors.length], opacity };
    });

    return (
        <AbsoluteFill style={{ overflow: 'hidden' }}>
            <AbsoluteFill style={{ background: palette.background }} />
            <svg width="100%" height="100%" viewBox={`0 0 ${width} ${height}`} style={{ position: 'absolute' }}>
                <defs>
                    <filter id="aurora-blur"><feGaussianBlur stdDeviation="30" /></filter>
                </defs>
                <g filter="url(#aurora-blur)">
                    {bands.map((band, i) => (
                        <path key={i} d={band.d} fill={band.color} opacity={band.opacity} />
                    ))}
                </g>
            </svg>
        </AbsoluteFill>
    );
};

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Mode 4: VORTEX — Rotating concentric rings spiraling inward
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const VortexBackground: React.FC<{ palette: BackgroundProps['palette'] }> = ({ palette }) => {
    const frame = useCurrentFrame();
    const { width, height } = useVideoConfig();
    const cx = width / 2;
    const cy = height / 2;

    const rings = Array.from({ length: 12 }).map((_, i) => {
        const baseRadius = 50 + i * 80;
        const rotation = frame * (0.3 + i * 0.15) * (i % 2 === 0 ? 1 : -1);
        const pulseRadius = baseRadius + Math.sin(frame * 0.04 + i * 0.8) * 15;
        const opacity = interpolate(i, [0, 11], [0.3, 0.05]);
        return { radius: pulseRadius, rotation, opacity };
    });

    return (
        <AbsoluteFill style={{ overflow: 'hidden' }}>
            <AbsoluteFill style={{ background: palette.background }} />
            <svg width="100%" height="100%" viewBox={`0 0 ${width} ${height}`} style={{ position: 'absolute' }}>
                {rings.map((ring, i) => (
                    <circle
                        key={i}
                        cx={cx} cy={cy} r={ring.radius}
                        fill="none"
                        stroke={palette.secondary}
                        strokeWidth={2}
                        strokeDasharray="15 25"
                        opacity={ring.opacity}
                        transform={`rotate(${ring.rotation}, ${cx}, ${cy})`}
                    />
                ))}
            </svg>
        </AbsoluteFill>
    );
};

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Mode 5: STARFIELD — Parallax dots at 3 depth layers
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const StarfieldBackground: React.FC<{ palette: BackgroundProps['palette'] }> = ({ palette }) => {
    const frame = useCurrentFrame();
    const { width, height } = useVideoConfig();

    // Generate deterministic stars across 3 parallax layers
    const layers = [
        { count: 60, speed: 0.3, sizeRange: [1, 2], opacity: 0.3 },
        { count: 40, speed: 0.7, sizeRange: [2, 3], opacity: 0.5 },
        { count: 20, speed: 1.5, sizeRange: [3, 5], opacity: 0.8 },
    ];

    return (
        <AbsoluteFill style={{ overflow: 'hidden' }}>
            <AbsoluteFill style={{ background: palette.background }} />
            <svg width="100%" height="100%" viewBox={`0 0 ${width} ${height}`} style={{ position: 'absolute' }}>
                {layers.map((layer, li) =>
                    Array.from({ length: layer.count }).map((_, si) => {
                        const seedX = (Math.sin(si * 127.1 + li * 311.7) * 0.5 + 0.5) * width;
                        const seedY = (Math.cos(si * 269.5 + li * 183.3) * 0.5 + 0.5) * height;
                        const size = layer.sizeRange[0] + (Math.sin(si * 53.1) * 0.5 + 0.5) * (layer.sizeRange[1] - layer.sizeRange[0]);

                        // Stars drift upward and wrap
                        const y = (seedY - frame * layer.speed + height * 2) % (height + 20) - 10;
                        // Subtle twinkle
                        const twinkle = 0.5 + Math.sin(frame * 0.15 + si * 7.7) * 0.5;

                        return (
                            <circle
                                key={`${li}-${si}`}
                                cx={seedX} cy={y}
                                r={size * twinkle}
                                fill="#f8fafc"
                                opacity={layer.opacity * twinkle}
                            />
                        );
                    })
                )}
            </svg>
        </AbsoluteFill>
    );
};
