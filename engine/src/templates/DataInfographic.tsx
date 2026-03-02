import React from 'react';
import { SceneManager } from '@/core/SceneManager';

export interface DataInfographicProps {
    scenes: any[];
}

export const DataInfographic: React.FC<DataInfographicProps> = ({ scenes }) => {
    return <SceneManager scenes={scenes} theme="minimal" />;
};
