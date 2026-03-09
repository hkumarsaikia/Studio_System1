import React from 'react';
import { LayoutProfile } from '@/types/layout';
import { SceneManager } from '@/core/SceneManager';

export interface ShortsVerticalProps {
    scenes: any[];
    layoutProfile?: LayoutProfile;
}

export const ShortsVertical: React.FC<ShortsVerticalProps> = ({ scenes, layoutProfile }) => {
    return <SceneManager scenes={scenes} theme="minimal" layoutProfile={layoutProfile} />;
};
