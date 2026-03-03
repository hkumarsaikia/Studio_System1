import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { SceneAudio } from '@/components/SceneAudio';
import { GenericScene } from './GenericScene';
import { themes } from '@/styles/theme';
import { fadeInOut, slideY, scaleIn, slideX, rotateIn, blurReveal, wipeDown } from '@/utils/sceneTransitions';

export interface SceneBlockProps {
    scene: any;
    themeName: string;
}

export const SceneBlock: React.FC<SceneBlockProps> = ({ scene, themeName }) => {
    const frame = useCurrentFrame();
    const theme = themes[themeName] || themes.dark;
    const duration = scene.duration || 300;
    const transition = scene.transition || 'fade';

    const enrichedScene = {
        ...scene,
        palette: scene.palette || {
            background: theme.background,
            secondary: theme.accent,
        },
        accentColor: scene.accentColor || theme.text,
    };

    // Compute transition style based on the scene's transition prop
    const style = computeTransitionStyle(transition, frame, duration);

    return (
        <AbsoluteFill style={style}>
            <GenericScene scene={enrichedScene} />
            {scene.audio ? <SceneAudio audioFile={scene.audio} /> : null}
        </AbsoluteFill>
    );
};

function computeTransitionStyle(transition: string, frame: number, duration: number): React.CSSProperties {
    switch (transition) {
        case 'scale':
            return {
                opacity: fadeInOut(frame, duration),
                transform: `scale(${scaleIn(frame, duration)})`,
            };
        case 'slide_left':
            return {
                opacity: fadeInOut(frame, duration),
                transform: `translateX(${slideX(frame, duration, -80)}px)`,
            };
        case 'slide_right':
            return {
                opacity: fadeInOut(frame, duration),
                transform: `translateX(${slideX(frame, duration, 80)}px)`,
            };
        case 'rotate':
            return {
                opacity: fadeInOut(frame, duration),
                transform: `rotate(${rotateIn(frame, duration)}deg)`,
            };
        case 'blur':
            return {
                filter: `blur(${blurReveal(frame, duration)}px)`,
            };
        case 'wipe':
            const progress = wipeDown(frame, duration);
            return {
                clipPath: `inset(0 0 ${(1 - progress) * 100}% 0)`,
            };
        case 'fade':
        default:
            return {
                opacity: fadeInOut(frame, duration),
                transform: `translateY(${slideY(frame, duration, 22)}px)`,
            };
    }
}
