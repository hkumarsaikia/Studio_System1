import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { SceneAudio } from '@/components/SceneAudio';
import { GenericScene } from './GenericScene';
import { themes } from '@/styles/theme';
import { fadeInOut, slideY } from '@/utils/sceneTransitions';

export interface SceneBlockProps {
    scene: any;
    themeName: string;
}

export const SceneBlock: React.FC<SceneBlockProps> = ({ scene, themeName }) => {
    const frame = useCurrentFrame();
    const theme = themes[themeName] || themes.dark;
    const duration = scene.duration || 300;

    const opacity = fadeInOut(frame, duration);
    const y = slideY(frame, duration, 22);

    const enrichedScene = {
        ...scene,
        palette: scene.palette || {
            background: theme.background,
            secondary: theme.accent,
        },
        accentColor: scene.accentColor || theme.text,
    };

    return (
        <AbsoluteFill style={{ opacity, transform: `translateY(${y}px)` }}>
            <GenericScene scene={enrichedScene} />
            {scene.audio ? <SceneAudio audioFile={scene.audio} /> : null}
        </AbsoluteFill>
    );
};
