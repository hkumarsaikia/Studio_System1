import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

export interface GradientOrbProps {
    color1?: string;
    color2?: string;
    color3?: string;
}

export const GradientOrb: React.FC<GradientOrbProps> = ({
    color1 = '#FF10F0',
    color2 = '#00FFFF',
    color3 = '#6C5CE7'
}) => {
    const frame = useCurrentFrame();

    const scale = interpolate(frame, [0, 60, 120], [0.6, 1.1, 0.9], {
        extrapolateRight: 'clamp',
    });
    const rotation = frame * 0.8;
    const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });

    // Floating orb positions
    const orb1X = Math.sin(frame * 0.03) * 80;
    const orb1Y = Math.cos(frame * 0.02) * 60;
    const orb2X = Math.cos(frame * 0.025) * 100;
    const orb2Y = Math.sin(frame * 0.035) * 70;
    const orb3X = Math.sin(frame * 0.04) * 60;
    const orb3Y = Math.cos(frame * 0.03) * 90;

    return (
        <AbsoluteFill style={{ opacity, justifyContent: 'center', alignItems: 'center', overflow: 'hidden' }}>
            <svg width="100%" height="100%" viewBox="0 0 1080 1920">
                <defs>
                    <radialGradient id="orb1-grad" cx="50%" cy="50%" r="50%">
                        <stop offset="0%" stopColor={color1} stopOpacity="0.8" />
                        <stop offset="100%" stopColor={color1} stopOpacity="0" />
                    </radialGradient>
                    <radialGradient id="orb2-grad" cx="50%" cy="50%" r="50%">
                        <stop offset="0%" stopColor={color2} stopOpacity="0.7" />
                        <stop offset="100%" stopColor={color2} stopOpacity="0" />
                    </radialGradient>
                    <radialGradient id="orb3-grad" cx="50%" cy="50%" r="50%">
                        <stop offset="0%" stopColor={color3} stopOpacity="0.6" />
                        <stop offset="100%" stopColor={color3} stopOpacity="0" />
                    </radialGradient>
                    <filter id="orb-blur">
                        <feGaussianBlur stdDeviation="40" />
                    </filter>
                </defs>

                <g filter="url(#orb-blur)" transform={`rotate(${rotation}, 540, 960)`}>
                    <circle cx={540 + orb1X} cy={800 + orb1Y} r={350 * scale} fill="url(#orb1-grad)" />
                    <circle cx={440 + orb2X} cy={1050 + orb2Y} r={300 * scale} fill="url(#orb2-grad)" />
                    <circle cx={650 + orb3X} cy={920 + orb3Y} r={280 * scale} fill="url(#orb3-grad)" />
                </g>
            </svg>
        </AbsoluteFill>
    );
};
