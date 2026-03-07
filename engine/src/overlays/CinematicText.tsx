import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import { springPop } from '@/utils/sceneTransitions';

export interface CinematicTextProps {
    title: string;
    subtitle?: string | null;
    accentColor?: string;
    category?: string;
    textEffect?: 'default' | 'word_stagger' | 'typewriter' | 'gradient_fill' | 'glow';
}

export const CinematicText: React.FC<CinematicTextProps> = ({
    title,
    subtitle,
    accentColor = '#38bdf8',
    category = 'SYSTEMS EXPLAINER',
    textEffect = 'default',
}) => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    const globalOpacity = interpolate(frame, [0, 12, 210, 240], [0, 1, 1, 0], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
    });

    return (
        <AbsoluteFill
            style={{
                justifyContent: 'center',
                alignItems: 'center',
                textAlign: 'center',
                padding: 80,
                opacity: globalOpacity,
            }}
        >
            {/* Category Badge */}
            <CategoryBadge category={category} accentColor={accentColor} frame={frame} fps={fps} />

            {/* Title — rendered with selected effect */}
            <TitleRenderer title={title} effect={textEffect} accentColor={accentColor} frame={frame} fps={fps} />

            {/* Subtitle */}
            {subtitle ? (
                <SubtitleRenderer subtitle={subtitle} frame={frame} />
            ) : null}
        </AbsoluteFill>
    );
};

// ── Category Badge ────────────────────────────────────────────────
const CategoryBadge: React.FC<{ category: string; accentColor: string; frame: number; fps: number }> = ({
    category, accentColor, frame,
}) => {
    const pop = springPop(frame, 30);

    return (
        <div style={{
            marginBottom: 20,
            display: 'inline-block',
            padding: '8px 14px',
            borderRadius: 999,
            backgroundColor: `${accentColor}33`,
            border: `1px solid ${accentColor}`,
            fontSize: 20,
            fontWeight: 700,
            letterSpacing: 1,
            transform: `scale(${0.8 + pop * 0.2})`,
            opacity: pop,
        }}>
            {category}
        </div>
    );
};

// ── Title Renderer (selects animation effect) ─────────────────────
const TitleRenderer: React.FC<{
    title: string; effect: string; accentColor: string; frame: number; fps: number;
}> = ({ title, effect, accentColor, frame, fps }) => {
    switch (effect) {
        case 'word_stagger':
            return <WordStaggerTitle title={title} frame={frame} fps={fps} />;
        case 'typewriter':
            return <TypewriterTitle title={title} frame={frame} />;
        case 'gradient_fill':
            return <GradientTitle title={title} accentColor={accentColor} frame={frame} />;
        case 'glow':
            return <GlowTitle title={title} accentColor={accentColor} frame={frame} fps={fps} />;
        case 'default':
        default:
            return <DefaultTitle title={title} frame={frame} fps={fps} />;
    }
};

// ── Effect: Default (spring pop) ──────────────────────────────────
const DefaultTitle: React.FC<{ title: string; frame: number; fps: number }> = ({ title, frame }) => {
    const scale = springPop(frame, 35);
    const y = interpolate(frame, [0, 20], [22, 0], { extrapolateRight: 'clamp' });

    return (
        <h1 style={{
            fontSize: 74, lineHeight: 1.08, marginBottom: 18,
            textShadow: '0 8px 30px rgba(15,23,42,0.4)',
            transform: `translateY(${y}px) scale(${0.92 + scale * 0.08})`,
        }}>
            {title}
        </h1>
    );
};

// ── Effect: Word Stagger ──────────────────────────────────────────
const WordStaggerTitle: React.FC<{ title: string; frame: number; fps: number }> = ({ title, frame }) => {
    const words = title.split(' ');

    return (
        <h1 style={{ fontSize: 74, lineHeight: 1.08, marginBottom: 18 }}>
            {words.map((word, i) => {
                const delay = i * 4;
                const pop = springPop(frame, 25, delay);
                const y = interpolate(Math.max(0, frame - delay), [0, 12], [30, 0], { extrapolateRight: 'clamp' });

                return (
                    <span key={i} style={{
                        display: 'inline-block',
                        opacity: pop,
                        transform: `translateY(${y}px)`,
                        marginRight: 14,
                    }}>
                        {word}
                    </span>
                );
            })}
        </h1>
    );
};

// ── Effect: Typewriter ────────────────────────────────────────────
const TypewriterTitle: React.FC<{ title: string; frame: number }> = ({ title, frame }) => {
    const charsVisible = Math.min(title.length, Math.floor(frame * 0.8));
    const displayText = title.substring(0, charsVisible);
    const showCursor = frame % 16 < 10;

    return (
        <h1 style={{
            fontSize: 74, lineHeight: 1.08, marginBottom: 18,
            fontFamily: "'JetBrains Mono', monospace",
            textShadow: '0 4px 20px rgba(15,23,42,0.4)',
        }}>
            {displayText}
            <span style={{ opacity: showCursor ? 1 : 0, color: '#38bdf8' }}>▎</span>
        </h1>
    );
};

// ── Effect: Gradient Fill ─────────────────────────────────────────
const GradientTitle: React.FC<{ title: string; accentColor: string; frame: number }> = ({ title, accentColor, frame }) => {
    const y = interpolate(frame, [0, 20], [22, 0], { extrapolateRight: 'clamp' });
    const gradientShift = frame * 2;

    return (
        <h1 style={{
            fontSize: 74, lineHeight: 1.08, marginBottom: 18,
            background: `linear-gradient(${90 + gradientShift}deg, ${accentColor}, #f472b6, #EFF396, ${accentColor})`,
            backgroundSize: '300% 100%',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            transform: `translateY(${y}px)`,
        }}>
            {title}
        </h1>
    );
};

// ── Effect: Neon Glow ─────────────────────────────────────────────
const GlowTitle: React.FC<{ title: string; accentColor: string; frame: number; fps: number }> = ({ title, accentColor, frame }) => {
    const scale = springPop(frame, 40);
    const glowPulse = 10 + Math.sin(frame * 0.12) * 8;

    return (
        <h1 style={{
            fontSize: 74, lineHeight: 1.08, marginBottom: 18,
            color: accentColor,
            textShadow: `0 0 ${glowPulse}px ${accentColor}, 0 0 ${glowPulse * 2}px ${accentColor}66, 0 0 ${glowPulse * 4}px ${accentColor}33`,
            transform: `scale(${0.92 + scale * 0.08})`,
        }}>
            {title}
        </h1>
    );
};

// ── Subtitle ──────────────────────────────────────────────────────
const SubtitleRenderer: React.FC<{ subtitle: string; frame: number }> = ({ subtitle, frame }) => {
    const opacity = interpolate(frame, [15, 30], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
    const y = interpolate(frame, [15, 30], [12, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

    return (
        <p style={{
            fontSize: 32, lineHeight: 1.35, maxWidth: 920, margin: 0,
            color: '#e2e8f0', opacity,
            transform: `translateY(${y}px)`,
        }}>
            {subtitle}
        </p>
    );
};
