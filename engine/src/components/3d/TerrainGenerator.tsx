import React, { useMemo, useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { createNoise2D } from 'simplex-noise';
import chroma from 'chroma-js';
import * as THREE from 'three';

/**
 * FILE: TerrainGenerator.tsx
 * PURPOSE: A declarative, procedural low-poly terrain generator (mountains, landscapes)
 * using Simplex Noise to displace a PlaneGeometry.
 * 
 * Fits perfectly into the Kurzgesagt aesthetic when rendered with wireframes or flat colors.
 */

export interface TerrainGeneratorProps {
    width?: number;
    depth?: number;
    segments?: number;
    heightScale?: number;
    baseColor?: string;
    accentColor?: string;
    speed?: number;
    wireframe?: boolean;
}

export const TerrainGenerator: React.FC<TerrainGeneratorProps> = ({
    width = 200,
    depth = 200,
    segments = 60,
    heightScale = 25,
    baseColor = '#1e293b',
    accentColor = '#38bdf8',
    speed = 0.5,
    wireframe = false
}) => {
    const meshRef = useRef<THREE.Mesh>(null);
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    // 1. Initialize deterministic 2D Simplex Noise
    const noise2D = useMemo(() => createNoise2D(), []);

    // 2. Pre-calculate default geometry positions
    const { geometry, colors } = useMemo(() => {
        const geo = new THREE.PlaneGeometry(width, depth, segments, segments);

        // Let's generate vertex colors based on height
        const colorsArr = [];
        const scale = chroma.scale([baseColor, accentColor]).mode('lch');

        const posAttribute = geo.getAttribute('position');
        for (let i = 0; i < posAttribute.count; i++) {
            // Give an initial color (will be updated)
            const color = scale(0.5).gl();
            colorsArr.push(color[0], color[1], color[2]);
        }

        geo.setAttribute('color', new THREE.Float32BufferAttribute(colorsArr, 3));
        return { geometry: geo, colors: colorsArr };
    }, [width, depth, segments, baseColor, accentColor]);

    // 3. Animate vertices deterministically every frame (Remotion sync)
    // We hook into R3F useFrame just for execution context, but we use Remotion's frame for time.
    useFrame(() => {
        if (!meshRef.current) return;

        const geo = meshRef.current.geometry as THREE.PlaneGeometry;
        const posAttribute = geo.getAttribute('position');
        const colorAttribute = geo.getAttribute('color');

        const colorScale = chroma.scale([baseColor, accentColor]).mode('lch');

        // Time offset based on deterministic Remotion frame
        const timeOffset = (frame / fps) * speed;

        for (let i = 0; i < posAttribute.count; i++) {
            const x = posAttribute.getX(i);
            const y = posAttribute.getY(i);

            // Simplex Noise calculation mapping X/Y terrain to Z elevation over Time
            // Multiply by a small frequency scaler
            const noiseVal = noise2D(x * 0.03, y * 0.03 + timeOffset);

            // Displace Z-coordinate
            const z = noiseVal * heightScale;
            posAttribute.setZ(i, z);

            // Re-color dynamically based on elevation (-1 to 1 normalized)
            const normalizedHeight = (noiseVal + 1) / 2;
            const c = colorScale(normalizedHeight).gl();
            colorAttribute.setXYZ(i, c[0], c[1], c[2]);
        }

        posAttribute.needsUpdate = true;
        colorAttribute.needsUpdate = true;
        // Compute normals for light interaction if using MeshStandardMaterial
        geo.computeVertexNormals();
    });

    return (
        <mesh
            ref={meshRef}
            geometry={geometry}
            rotation={[-Math.PI / 2.2, 0, 0]}
            position={[0, -20, -50]}
        >
            <meshStandardMaterial
                vertexColors={true}
                wireframe={wireframe}
                flatShading={true} // Low poly Kurzgesagt style
                roughness={0.8}
            />
        </mesh>
    );
};
