import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { TerrainGenerator } from './TerrainGenerator';
import { Canvas3D } from './3d/Canvas3D';
import { ShaderBackground } from './ShaderBackground';
import { CharacterHappy } from './generated/CharacterHappy';
import { smoothPop, swingSettle } from '@/utils/motion';
import { PrismField } from '@/components/fx/PrismField';
import { ConstellationMesh } from '@/components/fx/ConstellationMesh';

/**
 * FILE: AdvancedAnimationShowcase.tsx
 * PURPOSE: A full integration test of the procedural terrain, custom physics
 * motion curves, and auto-generated Inkscape React SVG assets.
 */
export const AdvancedAnimationShowcase: React.FC = () => {
    const frame = useCurrentFrame();

    // 1. ADVANCED MOTION: Complex physics-based entry animations

    // Character swings in from -500px to 0px overframes 10-30, overshooting slightly
    const characterX = swingSettle(frame, 10, -500, 0);

    // Title pops in with a dramatic "minimalist" punch at frame 30
    const titleScale = smoothPop(frame, 30, 20); // 20 frame duration
    const titleOpacity = smoothPop(frame, 30, 10);

    return (
        <AbsoluteFill style={{ backgroundColor: '#020617', overflow: 'hidden' }}>

            {/* 2. PROCEDURAL TERRAIN & HARDWARE ACCELERATION */}
            {/* The Canvas3D layer sits in the background rendering RTF and Shaders */}
            <Canvas3D>
                {/* A deep atmospheric nebula */}
                <ShaderBackground color1="#4c1d95" color2="#0f766e" />

                {/* The procedural simplex noise mountains zooming by */}
                <TerrainGenerator
                    width={500}
                    depth={300}
                    segments={100}
                    heightScale={40}
                    baseColor="#1e293b"
                    accentColor="#f472b6"
                    speed={0.8}
                    wireframe={false}
                />
            </Canvas3D>
            <ConstellationMesh color="#67e8f9" secondaryColor="#f472b6" />
            <PrismField color="#38bdf8" secondaryColor="#f472b6" prismCount={10} />

            {/* 3. INKSCAPE AUTO-GENERATED ASSETS & DOM OVERLAYS */}
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', position: 'relative', zIndex: 2 }}>

                <div style={{ transform: `translateX(${characterX}px)` }}>
                    <CharacterHappy size={400} />
                </div>

                <h1
                    style={{
                        fontFamily: 'Inter',
                        fontSize: '100px',
                        fontWeight: 900,
                        color: 'white',
                        marginTop: '20px',
                        transform: `scale(${titleScale})`,
                        opacity: titleOpacity,
                        textShadow: '0 0 20px rgba(0,0,0,0.5)'
                    }}
                >
                    PROCEDURAL WORLDS
                </h1>
            </div>

        </AbsoluteFill>
    );
};
