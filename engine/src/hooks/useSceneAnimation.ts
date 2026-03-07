import { interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import React from 'react';
import { springPop } from '@/utils/sceneTransitions';

export interface SceneAnimationOptions {
    duration?: number;
    fadeEdge?: number;
    slideAmount?: number;
    entrance?: 'fade' | 'spring' | 'slide';
}

export interface SceneAnimationResult {
    opacity: number;
    translateY: number;
    scale: number;
    blur: number;
    style: React.CSSProperties;
}

export const useSceneAnimation = ({
    duration = 300,
    fadeEdge = 12,
    slideAmount = 24,
    entrance = 'spring',
}: SceneAnimationOptions = {}): SceneAnimationResult => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    const opacity = interpolate(
        frame,
        [0, fadeEdge, duration - fadeEdge, duration],
        [0, 1, 1, 0],
        { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
    );

    const blur = interpolate(
        frame,
        [0, fadeEdge + 6, duration - fadeEdge - 6, duration],
        [6, 0, 0, 6],
        { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
    );

    let translateY = 0;
    let scale = 1;

    if (entrance === 'spring') {
        const springVal = springPop(frame, 30);
        translateY = (1 - springVal) * slideAmount;
        scale = 0.92 + springVal * 0.08;
    } else if (entrance === 'slide') {
        translateY = interpolate(
            frame,
            [0, fadeEdge * 2, duration - fadeEdge * 2, duration],
            [slideAmount, 0, 0, -slideAmount],
            { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
        );
    }

    return {
        opacity,
        translateY,
        scale,
        blur,
        style: {
            opacity,
            filter: blur > 0.1 ? `blur(${blur}px)` : 'none',
            transform: `translateY(${translateY}px) scale(${scale})`,
        },
    };
};
