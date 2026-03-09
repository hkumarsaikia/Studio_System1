import React from 'react';
import { LayoutProfile } from '@/types/layout';
import { SceneManager } from '@/core/SceneManager';

export interface ExplainerCinematicProps {
    scenes: any[];
    layoutProfile?: LayoutProfile;
}

export const ExplainerCinematic: React.FC<ExplainerCinematicProps> = ({ scenes, layoutProfile }) => {
    return <SceneManager scenes={scenes} theme="slate" layoutProfile={layoutProfile} />;
};
