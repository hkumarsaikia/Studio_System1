import React from 'react';
import { SceneManager } from '@/core/SceneManager';

export interface ProtestCinematicProps {
    scenes: any[];
}

export const ProtestCinematic: React.FC<ProtestCinematicProps> = ({ scenes }) => {
    return <SceneManager scenes={scenes} theme="slate" />;
};
