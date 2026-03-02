import React from 'react';
import { ShortsVertical } from '@/templates/ShortsVertical';
import { ExplainerCinematic } from '@/templates/ExplainerCinematic';
import { DataInfographic } from '@/templates/DataInfographic';
import { ProtestCinematic } from '@/templates/ProtestCinematic';

export interface TemplateLoaderProps {
    template: string;
    scenes: any[];
}

export const TemplateLoader: React.FC<TemplateLoaderProps> = ({ template, scenes }) => {
    switch (template) {
        case 'explainer':
            return <ExplainerCinematic scenes={scenes} />;
        case 'infographic':
            return <DataInfographic scenes={scenes} />;
        case 'protest':
            return <ProtestCinematic scenes={scenes} />;
        case 'shorts':
        default:
            return <ShortsVertical scenes={scenes} />;
    }
};
