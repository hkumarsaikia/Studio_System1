import React, { useEffect, useMemo, useRef } from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import chroma from 'chroma-js';
import gsap from 'gsap';
import { useSceneStore } from '@/store/sceneStore';
import { useGSAPSync } from '@/hooks/useGSAPSync';
import { ShaderBackground } from '@/components/ShaderBackground';
import { MorphingShape } from '@/components/MorphingShape';

export interface AdvancedShowcaseProps {
    accentColor?: string;
}

const STAR_PATH = "M 50 10 L 61 39 L 92 39 L 66 57 L 76 86 L 50 68 L 24 86 L 34 57 L 8 39 L 39 39 Z";
const CIRCLE_PATH = "M 50 5 C 25 5 5 25 5 50 C 5 75 25 95 50 95 C 75 95 95 75 95 50 C 95 25 75 5 50 5 Z";

/**
 * FILE: AdvancedShowcase.tsx
 * PURPOSE: The ultimate demonstration of the new graphics architecture.
 * Combines 3D Shaders, Zustand global state, Chroma.js color algebra,
 * Flubber math scaling, and GSAP timeline animation all completely synced to Remotion.
 */
export const AdvancedShowcase: React.FC<AdvancedShowcaseProps> = ({ accentColor = '#a78bfa' }) => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    // 1. ZUSTAND: Drive global state deterministically
    const setGlobalIntensity = useSceneStore((state) => state.setGlobalIntensity);
    const globalIntensity = useSceneStore((state) => state.globalIntensity);

    useEffect(() => {
        // Build up intensity from frame 0 to 60
        const intensity = interpolate(frame, [0, 60], [0, 1], { extrapolateRight: 'clamp' });
        setGlobalIntensity(intensity);
    }, [frame, setGlobalIntensity]);

    // 2. CHROMA-JS: Dynamic Color Algebra
    // Generate an automatic split-complementary color palette, brightened for neon effect
    const palette = useMemo(() => {
        return chroma.scale([
            chroma(accentColor).darken(3).hex(),
            accentColor,
            chroma(accentColor).brighten(2).hex()
        ]).mode('lch').colors(5);
    }, [accentColor]);

    // 3. GSAP: Complex timeline orchestration (synced via useGSAPSync)
    const tlRef = useRef<gsap.core.Timeline | null>(null);
    const containerRef = useRef<HTMLDivElement>(null);
    const titleRef = useRef<HTMLHeadingElement>(null);

    useEffect(() => {
        if (!containerRef.current || !titleRef.current) return;

        // Construct the immutable timeline once
        const tl = gsap.timeline({ paused: true });

        tl.fromTo(titleRef.current,
            { y: 100, opacity: 0, scale: 0.8 },
            { y: 0, opacity: 1, scale: 1, duration: 1.5, ease: "elastic.out(1, 0.5)" }
        );

        tlRef.current = tl;
        return () => { tl.kill(); };
    }, []);

    // Sync the GSAP timeline to the current frame!
    useGSAPSync(tlRef.current);

    return (
        <AbsoluteFill style={{ overflow: 'hidden' }}>
            {/* 4. THREE.JS & GLSL: Hardware-accelerated fluid background */}
            <ShaderBackground color1={palette[0]} color2={palette[2]} />

            {/* Main 2D DOM Layer */}
            <div ref={containerRef} style={{
                flex: 1,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                // Zustand global intensity driving CSS scale!
                transform: `scale(${1 + (globalIntensity * 0.05)})`
            }}>

                {/* 5. FLUBBER: Mathematical SVG path morphing */}
                <svg viewBox="0 0 100 100" style={{ width: 400, height: 400, overflow: 'visible' }}>
                    <MorphingShape
                        pathFrom={CIRCLE_PATH}
                        pathTo={STAR_PATH}
                        morphStartFrame={30}
                        morphDuration={45} // 1.5 seconds morphology
                        useSpring={true}
                        fill={palette[3]}
                    />
                </svg>

                <h1
                    ref={titleRef}
                    style={{
                        fontFamily: 'Inter',
                        fontSize: '120px',
                        fontWeight: 900,
                        color: palette[4],
                        textShadow: `0 0 40px ${chroma(palette[4]).alpha(0.5).css()}`
                    }}
                >
                    CINEMATIC CORE
                </h1>
            </div>
        </AbsoluteFill>
    );
};
