import React, { useMemo, useCallback } from 'react';
import { AbsoluteFill } from 'remotion';
import { LayoutProfile, mergeLayoutProfile } from '@/types/layout';
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
import { SceneAssetCluster } from '@/components/2d/SceneAssetCluster';
import { PixiCanvas } from '@/components/fx/PixiCanvas';
import { createWeatherSystem } from '@/components/fx/WeatherSystem';

export interface GenericSceneProps {
    scene: any;
    layoutProfile?: LayoutProfile;
}

export const GenericScene: React.FC<GenericSceneProps> = ({ scene, layoutProfile }) => {
    const layout = mergeLayoutProfile((scene.layout ?? layoutProfile) as Record<string, unknown> | undefined);
    const paletteBg = scene.palette?.background || '#0f172a';
    const paletteSec = scene.palette?.secondary || '#1e293b';
    const accent = scene.accentColor || '#f8fafc';
    const duration = scene.duration || 300;
    const cameraAction = scene.action || 'slow_zoom_in';
    const overlays: string[] = useMemo(() => scene.overlays || ['grain', 'vignette'], [scene.overlays]);
    const bgMode = scene.backgroundMode || 'gradient';
    const textEffect = scene.textEffect || 'default';
    const enableWeatherFx = process.env.REMOTION_ENABLE_WEATHER_FX === '1';

    const background = useMemo(() => (
        <Background
            palette={{ background: paletteBg, secondary: paletteSec }}
            motion={scene.motion || 'pan'}
            mode={bgMode}
        />
    ), [paletteBg, paletteSec, scene.motion, bgMode]);

    const renderWeather = useCallback((app: any) => {
        return createWeatherSystem({
            type: scene.weather === 'snow' ? 'snow' : 'rain',
            intensity: 0.8,
            app,
        });
    }, [scene.weather]);

    return (
        <AbsoluteFill style={{ color: '#f8fafc', overflow: 'hidden' }}>
            <SvgDefs />
            {background}

            <Camera action={cameraAction} duration={duration}>
                <MotionLayer duration={duration}>
                    <div
                        style={{
                            width: '100%',
                            height: '100%',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            transform: `scale(${layout.visualScale})`,
                            transformOrigin: 'center center',
                        }}
                    >
                        <SceneFactory scene={scene} />
                    </div>
                </MotionLayer>
            </Camera>

            {scene.visual !== 'icons' && (
                <SceneAssetCluster
                    assetTags={scene.assetTags}
                    accentColor={accent}
                    palette={scene.palette}
                />
            )}

            <CinematicText
                title={scene.text}
                subtitle={scene.subtext}
                accentColor={accent}
                category={scene.category || 'SYSTEMS EXPLAINER'}
                textEffect={textEffect}
                layoutProfile={layout}
            />

            {overlays.includes('grain') && <CinematicGrain opacity={0.06} baseFrequency={0.65} />}
            {overlays.includes('vignette') && <Vignette intensity={0.5} />}
            {overlays.includes('scanlines') && <ScanLines opacity={0.06} />}
            {overlays.includes('lightleak') && <LightLeak color={accent} />}

            {scene.weather && enableWeatherFx && (
                <AbsoluteFill style={{ zIndex: 50, pointerEvents: 'none', mixBlendMode: 'screen' }}>
                    <PixiCanvas>{renderWeather}</PixiCanvas>
                </AbsoluteFill>
            )}
        </AbsoluteFill>
    );
};
