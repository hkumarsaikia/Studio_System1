import React from 'react';
import { LayoutProfile } from '@/types/layout';
import { SceneManager } from '@/core/SceneManager';

export interface DataInfographicProps {
    scenes: any[];
    layoutProfile?: LayoutProfile;
}

export const DataInfographic: React.FC<DataInfographicProps> = ({ scenes, layoutProfile }) => {
    return <SceneManager scenes={scenes} theme="minimal" layoutProfile={layoutProfile} />;
};
