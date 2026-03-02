import React from 'react';
import { SceneManager } from '@/core/SceneManager';

export interface ExplainerCinematicProps {
    scenes: any[];
}

export const ExplainerCinematic: React.FC<ExplainerCinematicProps> = ({ scenes }) => {
    return <SceneManager scenes={scenes} theme="slate" />;
};
