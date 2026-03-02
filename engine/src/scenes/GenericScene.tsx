import React from 'react';
import { AbsoluteFill } from 'remotion';
import { Background } from '@/components/Background';
import { CinematicText } from '@/overlays/CinematicText';
import { SceneFactory } from './SceneFactory';
import { Camera } from '@/core/Camera';
import { MotionLayer } from '@/core/MotionLayer';
import { CinematicGrain } from '@/overlays/CinematicGrain';

const defaultPalette = {
    background: '#0f172a',
    secondary: '#1e293b',
};

export interface GenericSceneProps {
    scene: any;
}

export const GenericScene: React.FC<GenericSceneProps> = ({ scene }) => {
    const palette = scene.palette || defaultPalette;
    const cameraAction = scene.action || 'slow_zoom_in';

    return (
        <AbsoluteFill style={{ color: '#f8fafc' }}>
            <Background palette={palette} motion={scene.motion || 'pan'} />

            <Camera action={cameraAction} duration={scene.duration || 300}>
                <MotionLayer duration={scene.duration || 300}>
                    <SceneFactory scene={scene} />
                </MotionLayer>
            </Camera>

            <CinematicText
                title={scene.text}
                subtitle={scene.subtext}
                accentColor={scene.accentColor}
                category={scene.category || 'SYSTEMS EXPLAINER'}
            />

            <CinematicGrain opacity={0.06} baseFrequency={0.65} />
        </AbsoluteFill>
    );
};
