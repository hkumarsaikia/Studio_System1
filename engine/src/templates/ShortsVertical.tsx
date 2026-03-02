import React from 'react';
import { SceneManager } from '@/core/SceneManager';

export interface ShortsVerticalProps {
    scenes: any[];
}

export const ShortsVertical: React.FC<ShortsVerticalProps> = ({ scenes }) => {
    return <SceneManager scenes={scenes} theme="minimal" />;
};
