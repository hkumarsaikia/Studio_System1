import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { PixiCanvas } from './PixiCanvas';
import { createWeatherSystem } from './WeatherSystem';
import { CharacterAngry } from '../generated/CharacterAngry';
import { BackgroundSunset } from '../generated/BackgroundSunset';
import { swingSettle } from '@/utils/motion';
import { AuroraBands } from './AuroraBands';
import { ConstellationMesh } from './ConstellationMesh';
import { ParticleExplosion } from './ParticleExplosion';

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
            <AuroraBands colors={['#fb7185', '#f59e0b', '#fbbf24']} ribbonCount={4} />
            <ConstellationMesh color="#fca5a5" secondaryColor="#fde68a" />

            {/* 2. Procedural Weather Layer (Behind Character) */}
            <PixiCanvas transparent style={{ zIndex: 1, pointerEvents: 'none' }}>
                {(app) => createWeatherSystem({ app, type: 'rain', intensity: 1.5 })}
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

            {/* 4. Foreground Explosion Layer */}
            {/* Use a deterministic SVG explosion here because PixiCanvas children are imperative-only. */}
            <AbsoluteFill style={{ zIndex: 3, pointerEvents: 'none' }}>
                <ParticleExplosion color="#ef4444" particleCount={120} />
            </AbsoluteFill>

        </AbsoluteFill>
    );
};
