import React from 'react';
import { LayoutProfile } from '@/types/layout';
import { SceneManager } from '@/core/SceneManager';

export interface ProtestCinematicProps {
    scenes: any[];
    layoutProfile?: LayoutProfile;
}

export const ProtestCinematic: React.FC<ProtestCinematicProps> = ({ scenes, layoutProfile }) => {
    return <SceneManager scenes={scenes} theme="slate" layoutProfile={layoutProfile} />;
};
