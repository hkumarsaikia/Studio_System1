import React, { useMemo, useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { Canvas3D } from './Canvas3D';

/**
 * FILE: ShaderBackground.tsx
 * PURPOSE: A hardware-accelerated WebGL procedural fluid/nebula background.
 * Uses custom GLSL Fragment and Vertex shaders mixed with React Three Fiber.
 * Runs deterministically in Remotion via the Canvas3D wrapper.
 */

const vertexShader = `
varying vec2 vUv;
void main() {
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
`;

const fragmentShader = `
uniform float uTime;
uniform vec3 uColor1;
uniform vec3 uColor2;
varying vec2 vUv;

// Classic Perlin 2D Noise function
// by Stefan Gustavson
vec4 permute(vec4 x){return mod(((x*34.0)+1.0)*x, 289.0);}
vec2 fade(vec2 t) {return t*t*t*(t*(t*6.0-15.0)+10.0);}

float cnoise(vec2 P){
  vec4 Pi = floor(P.xyxy) + vec4(0.0, 0.0, 1.0, 1.0);
  vec4 Pf = fract(P.xyxy) - vec4(0.0, 0.0, 1.0, 1.0);
  Pi = mod(Pi, 289.0);
  vec4 ix = Pi.xzxz;
  vec4 iy = Pi.yyww;
  vec4 fx = Pf.xzxz;
  vec4 fy = Pf.yyww;
  vec4 i = permute(permute(ix) + iy);
  vec4 gx = 2.0 * fract(i * 0.0243902439) - 1.0;
  vec4 gy = abs(gx) - 0.5;
  vec4 tx = floor(gx + 0.5);
  gx = gx - tx;
  vec2 g00 = vec2(gx.x,gy.x);
  vec2 g10 = vec2(gx.y,gy.y);
  vec2 g01 = vec2(gx.z,gy.z);
  vec2 g11 = vec2(gx.w,gy.w);
  vec4 norm = 1.79284291400159 - 0.85373472095314 * 
    vec4(dot(g00, g00), dot(g01, g01), dot(g10, g10), dot(g11, g11));
  g00 *= norm.x;
  g01 *= norm.y;
  g10 *= norm.z;
  g11 *= norm.w;
  float n00 = dot(g00, vec2(fx.x, fy.x));
  float n10 = dot(g10, vec2(fx.y, fy.y));
  float n01 = dot(g01, vec2(fx.z, fy.z));
  float n11 = dot(g11, vec2(fx.w, fy.w));
  vec2 fade_xy = fade(Pf.xy);
  vec2 n_x = mix(vec2(n00, n01), vec2(n10, n11), fade_xy.x);
  float n_xy = mix(n_x.x, n_x.y, fade_xy.y);
  return 2.3 * n_xy;
}

void main() {
    // Layer 1: Slow massive waves
    float noise1 = cnoise(vUv * 2.0 + uTime * 0.15);
    // Layer 2: Fast detail ripples
    float noise2 = cnoise(vUv * 5.0 - uTime * 0.05);
    
    float combinedNoise = (noise1 + noise2) * 0.5;
    
    // Create a fluid swirl algorithm
    float swirl = sin(vUv.x * 6.0 + combinedNoise * 4.0) * cos(vUv.y * 6.0 + combinedNoise * 4.0);
    
    // Mix the two theme colors based on the swirl math
    vec3 finalColor = mix(uColor1, uColor2, swirl + 0.5);
    
    // Add cinematic soft vignette baked directly into the shader
    float dist = distance(vUv, vec2(0.5));
    finalColor *= smoothstep(0.9, 0.2, dist);

    gl_FragColor = vec4(finalColor, 1.0);
}
`;

const ShaderPlane = ({ color1, color2 }: { color1: string; color2: string }) => {
    const materialRef = useRef<THREE.ShaderMaterial>(null);

    const uniforms = useMemo(
        () => ({
            uTime: { value: 0 },
            uColor1: { value: new THREE.Color(color1) },
            uColor2: { value: new THREE.Color(color2) },
        }),
        [color1, color2]
    );

    useFrame((state) => {
        if (materialRef.current) {
            // Because Canvas3D intercepts the clock, state.clock.elapsedTime
            // is perfectly synced to Remotion's frame!
            materialRef.current.uniforms.uTime.value = state.clock.elapsedTime;
        }
    });

    return (
        <mesh>
            {/* 16:9 ratio plane scaled up to cover the default camera FOV */}
            <planeGeometry args={[16 * 1.5, 9 * 1.5]} />
            <shaderMaterial
                ref={materialRef}
                vertexShader={vertexShader}
                fragmentShader={fragmentShader}
                uniforms={uniforms}
                transparent
                depthWrite={false}
            />
        </mesh>
    );
};

export interface ShaderBackgroundProps {
    color1?: string;
    color2?: string;
}

export const ShaderBackground: React.FC<ShaderBackgroundProps> = ({
    color1 = '#0f172a',
    color2 = '#38bdf8'
}) => {
    return (
        // Render behind absolutely everything else
        <div style={{ position: 'absolute', width: '100%', height: '100%', zIndex: -10 }}>
            <Canvas3D cameraPos={[0, 0, 8]} fov={75}>
                <ShaderPlane color1={color1} color2={color2} />
            </Canvas3D>
        </div>
    );
};
