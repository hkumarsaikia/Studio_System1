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

    // Combine initialization and drawing into one highly deterministic frame lock.
    // Remotion runs frames in parallel across threads, so a persistent p5 canvas breaks.
    // Instead, we construct and destroy the instance perfectly per frame.
    useEffect(() => {
        if (!containerRef.current) return;

        // Create a new strict instance precisely for THIS frame
        p5InstanceRef.current = new p5((p: p5) => {
            p.setup = () => {
                p.createCanvas(width, height);
                p.noLoop(); // Disable internal clock completely
            };

            p.draw = () => {
                // Execute the raw drawing commands once
                sketch(p, frame, width, height, fps, accentColor);
            };
        }, containerRef.current);

        // Instantly force the frame draw
        p5InstanceRef.current.redraw();

        // When Remotion moves to the next frame (or thread exits), utterly annihilate the canvas memory
        return () => {
            if (p5InstanceRef.current) {
                p5InstanceRef.current.remove();
                p5InstanceRef.current = null;
            }
        };
    }, [frame, sketch, width, height, fps, accentColor]); // Triggers rigorously on EVERY frame update

    return <div ref={containerRef} style={{ width: '100%', height: '100%' }} />;
};
