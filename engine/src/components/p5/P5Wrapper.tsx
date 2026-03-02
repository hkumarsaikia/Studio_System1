import React, { useEffect, useRef } from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import p5 from 'p5';

// Define the type for our custom sketch function
export type P5Sketch = (p: p5, frame: number, width: number, height: number, fps: number, accentColor: string) => void;

interface P5WrapperProps {
    sketch: P5Sketch;
    accentColor?: string;
    width?: number;
    height?: number;
}

/**
 * P5Wrapper
 * Safely bridges p5.js instance mode with Remotion's strict frame timeline.
 * It disables p5's internal `requestAnimationFrame` loop, and forces a
 * `redraw()` only when Remotion's `useCurrentFrame()` advances.
 */
export const P5Wrapper: React.FC<P5WrapperProps> = ({
    sketch,
    accentColor = '#38bdf8',
    width = 1080,
    height = 1920
}) => {
    const containerRef = useRef<HTMLDivElement>(null);
    const p5InstanceRef = useRef<p5 | null>(null);

    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    // 1. Initialize the p5 Canvas exactly once
    useEffect(() => {
        if (!containerRef.current) return;

        // Create a new p5 instance using instance mode
        p5InstanceRef.current = new p5((p: p5) => {
            p.setup = () => {
                p.createCanvas(width, height);
                // CRITICAL FOR REMOTION: Turn off p5's internal clock
                p.noLoop();
                // Give the sketch function initial access to define custom setup logic
                // We pass frame=0 just for initialization
                sketch(p, 0, width, height, fps, accentColor);
            };

            p.draw = () => {
                // We use an empty draw loop here because we manually trigger drawing 
                // down below in the frame-change useEffect instead.
            };
        }, containerRef.current);

        // Cleanup when unmounting
        return () => {
            if (p5InstanceRef.current) {
                p5InstanceRef.current.remove();
                p5InstanceRef.current = null;
            }
        };
    }, [width, height, fps, accentColor]); // Re-init only if structural props change

    // 2. Force p5 to redraw every time Remotion's frame advances
    useEffect(() => {
        if (p5InstanceRef.current) {
            const p = p5InstanceRef.current;
            // Execute the custom sketch logic with the CURRENT Remotion frame
            sketch(p, frame, width, height, fps, accentColor);
            // Force p5 canvas to render that exact frame
            p.redraw();
        }
    }, [frame, sketch, width, height, fps, accentColor]);

    return <div ref={containerRef} style={{ width: '100%', height: '100%' }} />;
};
