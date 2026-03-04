import React from 'react';
import { useVideoConfig } from 'remotion';

export const SvgDefs: React.FC = () => {
    // Generate distinct glow filters and drop shadows for the Kurzgesagt style
    return (
        <svg width="0" height="0" style={{ position: 'absolute' }}>
            <defs>
                {/* 1. Global Soft Drop Shadow (Essential for 3D depth in 2D) */}
                <filter id="kurzDropShadow" x="-20%" y="-20%" width="140%" height="140%">
                    <feDropShadow dx="0" dy="8" stdDeviation="6" floodColor="#0f172a" floodOpacity="0.45" />
                </filter>

                {/* 2. Intense Drop Shadow (For prominent overlaid elements) */}
                <filter id="kurzIntenseShadow" x="-30%" y="-30%" width="160%" height="160%">
                    <feDropShadow dx="0" dy="12" stdDeviation="10" floodColor="#020617" floodOpacity="0.6" />
                </filter>

                {/* 3. Glowing Highlight Filter (For neon elements/screens) */}
                <filter id="neonGlow" x="-50%" y="-50%" width="200%" height="200%">
                    <feGaussianBlur in="SourceGraphic" stdDeviation="8" result="blur1" />
                    <feGaussianBlur in="SourceGraphic" stdDeviation="2" result="blur2" />
                    <feMerge>
                        <feMergeNode in="blur1" />
                        <feMergeNode in="blur2" />
                        <feMergeNode in="SourceGraphic" />
                    </feMerge>
                </filter>

                {/* 4. Skin Gradient (Provides spherical volume to flat faces) */}
                <radialGradient id="skinGlow" cx="30%" cy="30%" r="70%">
                    <stop offset="0%" stopColor="#ffedd5" stopOpacity="0.3" />
                    <stop offset="70%" stopColor="#ea580c" stopOpacity="0.0" />
                    <stop offset="100%" stopColor="#7c2d12" stopOpacity="0.2" />
                </radialGradient>

                {/* 5. Metallic Global Gradient */}
                <linearGradient id="metalShine" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#f1f5f9" stopOpacity="1" />
                    <stop offset="50%" stopColor="#94a3b8" stopOpacity="1" />
                    <stop offset="100%" stopColor="#334155" stopOpacity="1" />
                </linearGradient>

                {/* 6. Deep Vignette Filter for Backgrounds */}
                <radialGradient id="deepVignette" cx="50%" cy="50%" r="75%">
                    <stop offset="40%" stopColor="#000000" stopOpacity="0" />
                    <stop offset="100%" stopColor="#000000" stopOpacity="0.6" />
                </radialGradient>
            </defs>
        </svg>
    );
};
