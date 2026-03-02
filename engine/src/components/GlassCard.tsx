import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

export interface GlassCardProps {
    title?: string;
    subtitle?: string;
    color?: string;
    icon?: string;
}

export const GlassCard: React.FC<GlassCardProps> = ({
    title = 'System Status',
    subtitle = 'All systems operational',
    color = '#59B4C3',
    icon = '◆'
}) => {
    const frame = useCurrentFrame();
    const slideY = interpolate(frame, [0, 25], [60, 0], { extrapolateRight: 'clamp' });
    const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
    const glowPulse = 0.3 + Math.sin(frame * 0.08) * 0.15;

    return (
        <AbsoluteFill style={{
            justifyContent: 'center',
            alignItems: 'center',
            opacity,
            transform: `translateY(${slideY}px)`,
        }}>
            <div style={{
                width: 700,
                padding: '60px 50px',
                background: 'rgba(255,255,255,0.06)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: `1px solid rgba(255,255,255,0.12)`,
                borderRadius: 28,
                boxShadow: `0 0 60px ${color}${Math.round(glowPulse * 255).toString(16).padStart(2, '0')}, 0 20px 60px rgba(0,0,0,0.5)`,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: 20,
            }}>
                {/* Icon Circle */}
                <div style={{
                    width: 80, height: 80,
                    borderRadius: '50%',
                    background: `${color}22`,
                    border: `2px solid ${color}`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: 36,
                    color,
                }}>
                    {icon}
                </div>

                <h2 style={{
                    fontSize: 42,
                    fontWeight: 700,
                    color: '#f8fafc',
                    textAlign: 'center',
                    letterSpacing: -0.5,
                }}>
                    {title}
                </h2>

                <p style={{
                    fontSize: 24,
                    color: '#94a3b8',
                    textAlign: 'center',
                    maxWidth: 500,
                    lineHeight: 1.5,
                }}>
                    {subtitle}
                </p>

                {/* Bottom accent bar */}
                <div style={{
                    width: 120,
                    height: 4,
                    borderRadius: 999,
                    background: `linear-gradient(90deg, transparent, ${color}, transparent)`,
                    marginTop: 10,
                }} />
            </div>
        </AbsoluteFill>
    );
};
