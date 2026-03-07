import React, { useMemo, useCallback } from 'react';
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
import { createWeatherSystem } from '@/components/fx/WeatherSystem';
export interface GenericSceneProps {
    scene: any;
}

export const GenericScene: React.FC<GenericSceneProps> = ({ scene }) => {
    const paletteBg = scene.palette?.background || '#0f172a';
    const paletteSec = scene.palette?.secondary || '#1e293b';
    const accent = scene.accentColor || '#f8fafc';

    // Convert to memoized flat styles instead of spreading scene objects
    const duration = scene.duration || 300;
    const cameraAction = scene.action || 'slow_zoom_in';
    const overlays: string[] = useMemo(() => scene.overlays || ['grain', 'vignette'], [scene.overlays]);
    const bgMode = scene.backgroundMode || 'gradient';
    const textEffect = scene.textEffect || 'default';

    // Memoize the background to prevent unnecessary re-renders during frame updates
    const background = useMemo(() => (
        <Background
            palette={{ background: paletteBg, secondary: paletteSec }}
            motion={scene.motion || 'pan'}
            mode={bgMode}
        />
    ), [paletteBg, paletteSec, scene.motion, bgMode]);

    // Use a stable render function for PixiCanvas to avoids recursion triggers
    // Use a stable render function for PixiCanvas to avoids recursion triggers.
    // In the new PixiCanvas, this function returns a cleanup function, not JSX.
    const renderWeather = useCallback((app: any) => {
        return createWeatherSystem({
            type: scene.weather === 'snow' ? 'snow' : 'rain',
            intensity: 0.8,
            app: app
        });
    }, [scene.weather]);

    return (
        <AbsoluteFill style={{ color: '#f8fafc' }}>
            <SvgDefs />
            {background}

            <Camera action={cameraAction} duration={duration}>
                <MotionLayer duration={duration}>
                    <SceneFactory scene={scene} />
                </MotionLayer>
            </Camera>

            <CinematicText
                title={scene.text}
                subtitle={scene.subtext}
                accentColor={accent}
                category={scene.category || 'SYSTEMS EXPLAINER'}
                textEffect={textEffect}
            />

            {/* Configurable overlay stack */}
            {overlays.includes('grain') && <CinematicGrain opacity={0.06} baseFrequency={0.65} />}
            {overlays.includes('vignette') && <Vignette intensity={0.5} />}
            {overlays.includes('scanlines') && <ScanLines opacity={0.06} />}
            {overlays.includes('lightleak') && <LightLeak color={accent} />}

            {/* PixiJS Procedural Weather System Layer */}
            {scene.weather && (
                <AbsoluteFill style={{ zIndex: 50, pointerEvents: 'none', mixBlendMode: 'screen' }}>
                    <PixiCanvas>
                        {renderWeather}
                    </PixiCanvas>
                </AbsoluteFill>
            )}
        </AbsoluteFill>
    );
};
