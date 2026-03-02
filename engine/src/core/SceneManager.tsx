import React from 'react';
import { Series } from 'remotion';
import { SceneBlock } from '@/scenes/SceneBlock';
import { validateScenes } from '@/utils/propsValidator';

export interface SceneManagerProps {
    scenes: any[];
    theme: string;
}

export const SceneManager: React.FC<SceneManagerProps> = ({ scenes, theme }) => {
    const safeScenes = validateScenes(scenes);

    return (
        <Series>
            {safeScenes.map((scene, index) => (
                <Series.Sequence key={index} durationInFrames={scene.duration}>
                    <SceneBlock scene={scene} themeName={theme} />
                </Series.Sequence>
            ))}
        </Series>
    );
};
