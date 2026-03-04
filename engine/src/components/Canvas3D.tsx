import React, { Suspense } from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { Environment } from '@react-three/drei';

/**
 * FILE: Canvas3D.tsx
 * PURPOSE: A robust Foundation wrapper for running Three.js / WebGL inside Remotion.
 * 
 * Mixed 2D/3D architectures require the internal physics/time clock of 
 * the 3D engine to be hijacked and driven strictly by Remotion's frame state.
 * If we don't do this, 3D animations will drop frames during final MP4 rendering.
 */

// Intercepts the R3F loop and overrides standard progression with deterministic frame calculation
const RemotionTimeSync: React.FC = () => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();
    const { clock } = useThree();

    useFrame(() => {
        // Override elapsed time exactly 
        clock.elapsedTime = frame / fps;
    }, 1); // Run this at priority 1 to execute before any other useFrame logic

    return null;
};

export interface Canvas3DProps {
    children: React.ReactNode;
    cameraPos?: [number, number, number];
    fov?: number;
    envPreset?: 'sunset' | 'dawn' | 'night' | 'warehouse' | 'forest' | 'apartment' | 'studio' | 'city' | 'park' | 'lobby';
}

export const Canvas3D: React.FC<Canvas3DProps> = ({
    children,
    cameraPos = [0, 0, 5],
    fov = 50,
    envPreset = 'studio'
}) => {
    return (
        <AbsoluteFill style={{ pointerEvents: 'none' }}>
            <Canvas
                shadows
                camera={{ position: cameraPos, fov }}
                gl={{
                    antialias: true,
                    alpha: true,
                    // CRITICAL FOR REMOTION:
                    preserveDrawingBuffer: true
                }}
            >
                <RemotionTimeSync />

                {/* Default cinematic lighting via Environment map */}
                <Suspense fallback={null}>
                    <Environment preset={envPreset} />
                    {children}
                </Suspense>
            </Canvas>
        </AbsoluteFill>
    );
};
