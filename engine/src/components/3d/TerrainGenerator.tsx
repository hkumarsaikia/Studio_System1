import React, { useMemo, useRef, useEffect } from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { createNoise2D } from 'simplex-noise';
import chroma from 'chroma-js';
import * as THREE from 'three';

/**
 * FILE: TerrainGenerator.tsx
 * PURPOSE: A stable, memory-efficient procedural low-poly terrain generator.
 * Updates vertex attributes in-place to avoid GC pressure in Remotion.
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

    const noise2D = useMemo(() => createNoise2D(), []);

    // 1. Static base geometry with initial colors
    const geometry = useMemo(() => {
        const geo = new THREE.PlaneGeometry(width, depth, segments, segments);
        const colorsArr = new Float32Array(geo.getAttribute('position').count * 3);
        geo.setAttribute('color', new THREE.BufferAttribute(colorsArr, 3));
        return geo;
    }, [width, depth, segments]);

    // 2. Stable color scale
    const colorScale = useMemo(() => {
        return chroma.scale([baseColor, accentColor]).mode('lch');
    }, [baseColor, accentColor]);

    // 3. Update attributes imperatively inside useEffect/useLayoutEffect to be safe and efficient
    // This happens every frame as frame changes.
    useEffect(() => {
        if (!meshRef.current) return;

        const geo = meshRef.current.geometry as THREE.PlaneGeometry;
        const posAttribute = geo.getAttribute('position');
        const colorAttribute = geo.getAttribute('color');

        const timeOffset = (frame / fps) * speed;

        for (let i = 0; i < posAttribute.count; i++) {
            const x = posAttribute.getX(i);
            const y = posAttribute.getY(i);

            const noiseVal = noise2D(x * 0.03, y * 0.03 + timeOffset);
            const z = noiseVal * heightScale;
            posAttribute.setZ(i, z);

            const normalizedHeight = (noiseVal + 1) / 2;
            const c = colorScale(normalizedHeight).gl();
            colorAttribute.setXYZ(i, c[0], c[1], c[2]);
        }

        posAttribute.needsUpdate = true;
        colorAttribute.needsUpdate = true;
        geo.computeVertexNormals();
    }, [frame, fps, speed, noise2D, heightScale, colorScale]);

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
                flatShading={true}
                roughness={0.8}
            />
        </mesh>
    );
};
