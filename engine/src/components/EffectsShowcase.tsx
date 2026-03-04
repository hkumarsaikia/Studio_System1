import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { PixiCanvas } from './PixiCanvas';
import { WeatherSystem } from './WeatherSystem';
import { ExplosionEffect } from './ExplosionEffect';
import { CharacterAngry } from './generated/CharacterAngry';
import { BackgroundSunset } from './generated/BackgroundSunset';
import { swingSettle } from '@/utils/motion';

/**
 * FILE: EffectsShowcase.tsx
 * PURPOSE: A demonstration of WebGL Pixi.js 2D procedural effects (rain, explosions)
 * layered tightly with auto-generated React SVG components.
 */
export const EffectsShowcase: React.FC = () => {
    const frame = useCurrentFrame();

    // The character shakes aggressively upon the explosion frame
    let xOffset = 0;
    if (frame >= 30 && frame < 45) {
        xOffset = Math.sin(frame * 2) * 20; // Camera shake effect
    }

    // Enter screen via swing
    const charY = swingSettle(frame, 0, 500, 0);

    return (
        <AbsoluteFill>
            {/* 1. Underlying Pre-rendered Background */}
            <BackgroundSunset />

            {/* 2. Procedural Weather Layer (Behind Character) */}
            <PixiCanvas transparent style={{ zIndex: 1, pointerEvents: 'none' }}>
                {(app) => <WeatherSystem app={app} type="rain" intensity={1.5} />}
            </PixiCanvas>

            {/* 3. Character DOM Overlay */}
            <div style={{
                position: 'absolute',
                top: '50%',
                left: '50%',
                transform: `translate(-50%, ${-50 + charY}%) translateX(${xOffset}px)`,
                zIndex: 2
            }}>
                <CharacterAngry size={600} />
            </div>

            {/* 4. Foreground Procedural Explosion Layer */}
            {/* Layered above the character for dramatic burst impacts */}
            <PixiCanvas transparent style={{ zIndex: 3, pointerEvents: 'none' }}>
                {(app) => (
                    <ExplosionEffect
                        app={app}
                        x={1920 / 2}
                        y={1080 / 2 + 200} // Explode near their feet
                        triggerFrame={30}
                        color="#ef4444" // Deep red/orange burst
                    />
                )}
            </PixiCanvas>

        </AbsoluteFill>
    );
};
