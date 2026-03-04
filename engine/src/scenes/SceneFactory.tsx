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
import { PropServer } from '@/components/generated/PropServer';
import { PropDeclarativeRobot } from '@/components/generated/PropDeclarativeRobot';
import { PropDeclarativeSaturn } from '@/components/generated/PropDeclarativeSaturn';

import { DonutChart } from '@/components/DonutChart';
import { MatrixRain } from '@/components/MatrixRain';
import { CyberHUD } from '@/components/CyberHUD';
import { GradientOrb } from '@/components/GradientOrb';
import { ParticleExplosion } from '@/components/ParticleExplosion';
import { RadarScope } from '@/components/RadarScope';
import { GlassCard } from '@/components/GlassCard';
import { PulseGrid } from '@/components/PulseGrid';
import { TimelineBar } from '@/components/TimelineBar';
import { LineChart } from '@/components/LineChart';
import { ProgressRing } from '@/components/ProgressRing';

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

        case 'gradient_orb':
            return <GradientOrb color1={scene.color1 || '#FF10F0'} color2={scene.color2 || '#00FFFF'} color3={scene.color3 || '#6C5CE7'} />;

        case 'explosion':
            return <ParticleExplosion color={scene.accentColor || '#FFB347'} particleCount={scene.particleCount || 80} />;

        case 'radar':
            return <RadarScope color={scene.accentColor || '#39FF14'} blipCount={scene.blipCount || 6} />;

        case 'glass_card':
            return (
                <GlassCard
                    title={scene.cardTitle || 'System Status'}
                    subtitle={scene.cardSubtitle || 'All systems operational'}
                    color={scene.accentColor || '#59B4C3'}
                    icon={scene.cardIcon || '◆'}
                />
            );

        case 'pulse_grid':
            return <PulseGrid color={scene.accentColor || '#6C5CE7'} />;

        case 'timeline':
            return (
                <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
                    <TimelineBar events={scene.events} color={scene.accentColor || '#EFF396'} />
                </AbsoluteFill>
            );

        case 'line_chart':
            return (
                <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
                    <LineChart values={scene.chartValues} color={scene.accentColor || '#38bdf8'} label={scene.label || 'TREND ANALYSIS'} />
                </AbsoluteFill>
            );

        case 'progress_ring':
            return <ProgressRing rings={scene.rings} />;

        case 'PropServer':
            return (
                <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
                    <PropServer />
                </AbsoluteFill>
            );

        case 'PropDeclarativeRobot':
            return (
                <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
                    <PropDeclarativeRobot />
                </AbsoluteFill>
            );

        case 'PropDeclarativeSaturn':
            return (
                <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
                    <PropDeclarativeSaturn />
                </AbsoluteFill>
            );

        case 'none':
        default:
            return null;
    }
};
