import React from 'react';
import { AbsoluteFill } from 'remotion';
import { P5Wrapper, P5Sketch } from './P5Wrapper';

/**
 * FILE: GenerativeDataLattice.tsx
 * PURPOSE: A powerful p5.js mathematical visualization.
 * It draws a complex, rotating isometric lattice of interconnected data nodes
 * that scales and morphs based on mathematical trigonometric functions sync'd
 * perfectly to the Remotion frame.
 */

// The p5 sketch logic (separated from React)
const latticeSketch: P5Sketch = (p, frame, width, height, fps, accentColor) => {
    // We use this function both for setup and draw across the P5Wrapper.
    // We determine what to do based on the context.

    // Clear the background to transparent so it overlays properly
    p.clear(0, 0, 0, 0);

    p.push();
    // Move to center of screen
    p.translate(width / 2, height / 2);

    // Calculate time in seconds based on Remotion frame and fps
    const time = frame / fps;

    // Global rotation based on time
    p.rotate(time * 0.2);

    const numCols = 15;
    const numRows = 15;
    const spacing = 60;

    // Grid offset so it's centered
    const xOff = (numCols * spacing) / 2;
    const yOff = (numRows * spacing) / 2;

    // Parse accent hex to p5 color for varying opacities
    const c = p.color(accentColor);

    p.strokeWeight(1.5);
    p.noFill();

    for (let i = 0; i < numCols; i++) {
        for (let j = 0; j < numRows; j++) {
            const x = i * spacing - xOff;
            const y = j * spacing - yOff;

            // Distance from center determines animation phase
            const d = p.dist(0, 0, x, y);

            // Calculate a morphing size offset based on distance, time, and coordinates
            // This creates a mathematical "wave" riding through the isometric lattice
            const sizeOffset = p.sin(d * 0.05 - time * 2) * p.cos(i * 0.1) * 30;

            const r = 10 + sizeOffset;

            if (r > 0) {
                // Map opacity based on size and distance, so outer nodes fade out
                const opc = p.map(d, 0, width / 2, 200, 0);
                c.setAlpha(p.max(opc, 0));
                p.stroke(c);

                // Draw the node
                p.ellipse(x, y, r, r);

                // Connect neighboring nodes conditionally to form the lattice
                if (i < numCols - 1 && j < numRows - 1) {
                    if (p.sin(x * y + time) > 0.5) {
                        const nextX = (i + 1) * spacing - xOff;
                        p.line(x, y, nextX, y);
                    }
                    if (p.cos(x * y - time) > 0.5) {
                        const nextY = (j + 1) * spacing - yOff;
                        p.line(x, y, x, nextY);
                    }
                }
            }
        }
    }

    p.pop();
};

// The React Component exported for SceneFactory
export const GenerativeDataLattice: React.FC<{ accentColor?: string }> = ({
    accentColor = '#f472b6'
}) => {
    return (
        <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
            <P5Wrapper sketch={latticeSketch} accentColor={accentColor} />
        </AbsoluteFill>
    );
};
