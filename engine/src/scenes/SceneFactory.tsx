import React from 'react';
import { AbsoluteFill } from 'remotion';
import { Crowd } from '@/components/Crowd';
import { DataBars } from '@/components/DataBars';
import { FlowDiagram } from '@/components/FlowDiagram';
import { SystemNetwork } from '@/components/SystemNetwork';
import { SystemIconGrid } from '@/components/SystemIcons';
import { LandscapeBackdrop } from '@/components/LandscapeBackdrop';
import { CityStreetBackdrop } from '@/components/CityStreetBackdrop';
import { AnimalSilhouettes } from '@/components/AnimalSilhouettes';
import { GeoEarth } from '@/components/GeoEarth';
import { GenerativeDataLattice } from '@/components/p5/GenerativeDataLattice';
import { NeuralCore } from '@/components/intelligence/NeuralCore';
import { ChalkboardEquation } from '@/components/manim/ChalkboardEquation';

import { DonutChart } from '@/components/DonutChart';
import { MatrixRain } from '@/components/MatrixRain';
import { CyberHUD } from '@/components/CyberHUD';

export interface SceneFactoryProps {
    scene: any;
}

export const SceneFactory: React.FC<SceneFactoryProps> = ({ scene }) => {
    const visual = scene.visual || 'none';

    switch (visual) {
        case 'crowd':
            return (
                <AbsoluteFill style={{ justifyContent: 'flex-end' }}>
                    <Crowd count={scene.crowdCount || 8} />
                </AbsoluteFill>
            );

        case 'bars':
            return (
                <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', padding: 80 }}>
                    <DataBars values={scene.barValues || [20, 35, 52, 68, 84]} />
                </AbsoluteFill>
            );

        case 'flow':
            return (
                <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', padding: 80 }}>
                    <FlowDiagram
                        labels={scene.flowLabels || ['Input', 'System', 'Output']}
                        direction={scene.flowDirection || 'horizontal'}
                        accent={scene.accentColor}
                    />
                </AbsoluteFill>
            );

        case 'network':
            return (
                <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', padding: 80 }}>
                    <SystemNetwork nodes={scene.networkNodes || ['State', 'Market', 'Labor', 'Capital', 'Public']} />
                </AbsoluteFill>
            );

        case 'icons':
            return (
                <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', padding: 70 }}>
                    <SystemIconGrid
                        icons={scene.icons || ['bank', 'factory', 'home', 'cart', 'law', 'media']}
                        color={scene.accentColor || '#38bdf8'}
                    />
                </AbsoluteFill>
            );

        case 'landscape':
            return (
                <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
                    <LandscapeBackdrop />
                </AbsoluteFill>
            );

        case 'city':
            return (
                <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
                    <CityStreetBackdrop />
                </AbsoluteFill>
            );

        case 'animals':
            return (
                <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', padding: 70 }}>
                    <AnimalSilhouettes animals={scene.animals || ['bird', 'fish', 'deer']} />
                </AbsoluteFill>
            );

        case 'lattice':
            return <GenerativeDataLattice accentColor={scene.accentColor || '#f472b6'} />;

        case 'neural_core':
            return <NeuralCore accentColor={scene.accentColor || '#a78bfa'} />;

        case 'math_equation':
            return <ChalkboardEquation accentColor={scene.accentColor || '#ffffff'} />;

        case 'earth':
            return (
                <GeoEarth
                    accentColor={scene.accentColor || '#38bdf8'}
                    palette={scene.palette || { secondary: '#1e293b' }}
                />
            );

        case 'matrix':
            return <MatrixRain color={scene.accentColor || '#22c55e'} />;

        case 'hud':
            return <CyberHUD color={scene.accentColor || '#06b6d4'} />;

        case 'donut':
            return (
                <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
                    <DonutChart
                        color={scene.accentColor || '#38bdf8'}
                        value={scene.value || 75}
                        label={scene.label || 'SYSTEM DATA'}
                    />
                </AbsoluteFill>
            );

        case 'none':
        default:
            return null;
    }
};
