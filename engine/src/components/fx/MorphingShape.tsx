import React, { useMemo } from 'react';
import { interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import { interpolate as flubberInterpolate } from 'flubber';
import { springPop } from '@/utils/sceneTransitions';

/**
 * FILE: MorphingShape.tsx
 * PURPOSE: Mathematically morphs between two SVG paths over time using Flubber.
 * 
 * Flubber excels at morphing shapes with completely different point counts and topologies
 * (e.g., a circle into a star) smoothly, whereas raw SVG transitions fail or tear.
 */

export interface MorphingShapeProps {
    pathFrom: string;
    pathTo: string;
    morphStartFrame?: number;
    morphDuration?: number;
    useSpring?: boolean; // If true, bounces into the new shape
    fill?: string;
    stroke?: string;
    strokeWidth?: number;
    filter?: string; // Optional glow/shadow filter
}

export const MorphingShape: React.FC<MorphingShapeProps> = ({
    pathFrom,
    pathTo,
    morphStartFrame = 0,
    morphDuration = 30, // Default 1 second at 30fps
    useSpring = false,
    fill = '#38bdf8',
    stroke = 'none',
    strokeWidth = 0,
    filter = 'url(#kurzDropShadow)', // Applies minimalist depth by default
}) => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    // 1. Generate the Flubber interpolator ONCE (heavy computation)
    const interpolator = useMemo(() => {
        return flubberInterpolate(pathFrom, pathTo, {
            maxSegmentLength: 2 // High detail for smooth morphing
        });
    }, [pathFrom, pathTo]);

    // 2. Calculate the progress value (0 to 1) synchronously with Remotion
    let progress = 0;

    if (useSpring) {
        // Elastic/bouncy morph using pure math to avoid hook recursion in React 19
        progress = springPop(frame, morphDuration, morphStartFrame);
    } else {
        // Smooth linear/eased morph
        progress = interpolate(
            frame,
            [morphStartFrame, morphStartFrame + morphDuration],
            [0, 1],
            {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
                easing: (t) => t * t * (3 - 2 * t) // SmoothStep easing
            }
        );
    }

    // 3. Inject the progression into the mathematical solver to get the dynamic SVG path
    const currentPath = interpolator(Math.max(0, Math.min(1, progress)));

    return (
        <path
            d={currentPath}
            fill={fill}
            stroke={stroke}
            strokeWidth={strokeWidth}
            filter={filter}
        />
    );
};
