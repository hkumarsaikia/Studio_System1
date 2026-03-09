import React, { useMemo } from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { LayoutProfile, mergeLayoutProfile } from '@/types/layout';
import { SceneAudio } from '@/components/SceneAudio';
import { GenericScene } from './GenericScene';
import { fadeInOut, slideY, scaleIn, slideX, rotateIn, blurReveal, wipeDown } from '@/utils/sceneTransitions';

export interface SceneBlockProps {
    scene: any;
    themeName: string;
    layoutProfile?: LayoutProfile;
}

export const SceneBlock: React.FC<SceneBlockProps> = ({ scene, themeName, layoutProfile }) => {
    const frame = useCurrentFrame();
    const duration = scene.duration || 300;
    const transition = scene.transition || 'fade';

    const enrichedScene = useMemo(() => ({
        ...scene,
        themeName,
        palette: scene.palette || {
            background: '#0f172a',
            secondary: '#38bdf8',
        },
        accentColor: scene.accentColor || '#f8fafc',
        layout: mergeLayoutProfile((scene.layout ?? layoutProfile) as Record<string, unknown> | undefined),
    }), [layoutProfile, scene, themeName]);

    const style = computeTransitionStyle(transition, frame, duration);

    return (
        <AbsoluteFill style={style}>
            <GenericScene scene={enrichedScene} layoutProfile={enrichedScene.layout} />
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
        case 'wipe': {
            const progress = wipeDown(frame, duration);
            return {
                clipPath: `inset(0 0 ${(1 - progress) * 100}% 0)`,
            };
        }
        case 'fade':
        default:
            return {
                opacity: fadeInOut(frame, duration),
                transform: `translateY(${slideY(frame, duration, 22)}px)`,
            };
    }
}
