import React from 'react';
import { LayoutProfile } from '@/types/layout';
import { ShortsVertical } from '@/templates/ShortsVertical';
import { ExplainerCinematic } from '@/templates/ExplainerCinematic';
import { DataInfographic } from '@/templates/DataInfographic';
import { ProtestCinematic } from '@/templates/ProtestCinematic';

export interface TemplateLoaderProps {
    template: string;
    scenes: any[];
    layoutProfile?: LayoutProfile;
}

export const TemplateLoader: React.FC<TemplateLoaderProps> = ({ template, scenes, layoutProfile }) => {
    switch (template) {
        case 'explainer':
            return <ExplainerCinematic scenes={scenes} layoutProfile={layoutProfile} />;
        case 'infographic':
            return <DataInfographic scenes={scenes} layoutProfile={layoutProfile} />;
        case 'protest':
            return <ProtestCinematic scenes={scenes} layoutProfile={layoutProfile} />;
        case 'shorts':
        default:
            return <ShortsVertical scenes={scenes} layoutProfile={layoutProfile} />;
    }
};
