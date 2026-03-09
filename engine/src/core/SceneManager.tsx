import React from 'react';
import { Series } from 'remotion';
import { LayoutProfile } from '@/types/layout';
import { SceneBlock } from '@/scenes/SceneBlock';
import { validateScenes } from '@/utils/propsValidator';

export interface SceneManagerProps {
    scenes: any[];
    theme: string;
    layoutProfile?: LayoutProfile;
}

export const SceneManager: React.FC<SceneManagerProps> = ({ scenes, theme, layoutProfile }) => {
    const safeScenes = validateScenes(scenes);

    return (
        <Series>
            {safeScenes.map((scene, index) => (
                <Series.Sequence key={index} durationInFrames={scene.duration}>
                    <SceneBlock scene={scene} themeName={theme} layoutProfile={layoutProfile} />
                </Series.Sequence>
            ))}
        </Series>
    );
};
