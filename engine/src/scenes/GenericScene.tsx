import React from 'react';
import { AbsoluteFill } from 'remotion';
import { CinematicText } from '@/overlays/CinematicText';
import { SceneFactory } from './SceneFactory';
import { Camera } from '@/core/Camera';
import { MotionLayer } from '@/core/MotionLayer';
import { CinematicGrain } from '@/overlays/CinematicGrain';
import { Vignette } from '@/overlays/Vignette';
import { ScanLines } from '@/overlays/ScanLines';
import { LightLeak } from '@/overlays/LightLeak';
import { SvgDefs } from '@/core/SvgDefs';
import { Background } from '@/components/2d/Background';
import { PixiCanvas } from '@/components/fx/PixiCanvas';
import { WeatherSystem } from '@/components/fx/WeatherSystem';

const defaultPalette = {
    background: '#0f172a',
    secondary: '#1e293b',
};

export interface GenericSceneProps {
    scene: any;
}

export const GenericScene: React.FC<GenericSceneProps> = ({ scene }) => {
    const palette = scene.palette || defaultPalette;
    const cameraAction = scene.action || 'slow_zoom_in';
    const overlays: string[] = scene.overlays || ['grain', 'vignette'];
    const bgMode = scene.backgroundMode || 'gradient';
    const textEffect = scene.textEffect || 'default';

    return (
        <AbsoluteFill style={{ color: '#f8fafc' }}>
            <SvgDefs />
            <Background palette={palette} motion={scene.motion || 'pan'} mode={bgMode} />

            <Camera action={cameraAction} duration={scene.duration || 300}>
                <MotionLayer duration={scene.duration || 300}>
                    <SceneFactory scene={scene} />
                </MotionLayer>
            </Camera>

            <CinematicText
                title={scene.text}
                subtitle={scene.subtext}
                accentColor={scene.accentColor}
                category={scene.category || 'SYSTEMS EXPLAINER'}
                textEffect={textEffect}
            />

            {/* Configurable overlay stack */}
            {overlays.includes('grain') && <CinematicGrain opacity={0.06} baseFrequency={0.65} />}
            {overlays.includes('vignette') && <Vignette intensity={0.5} />}
            {overlays.includes('scanlines') && <ScanLines opacity={0.06} />}
            {overlays.includes('lightleak') && <LightLeak color={scene.accentColor || '#f97316'} />}

            {/* PixiJS Procedural Weather System Layer */}
            {scene.weather && (
                <AbsoluteFill style={{ zIndex: 50, pointerEvents: 'none', mixBlendMode: 'screen' }}>
                    <PixiCanvas>
                        {(app) => (
                            <WeatherSystem
                                type={scene.weather === 'snow' ? 'snow' : 'rain'}
                                intensity={0.8}
                                app={app}
                            />
                        )}
                    </PixiCanvas>
                </AbsoluteFill>
            )}
        </AbsoluteFill>
    );
};
