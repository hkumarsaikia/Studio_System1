import bezier from 'bezier-easing';
import { interpolate } from 'remotion';

/**
 * FILE: motion.ts
 * PURPOSE: A central utility library exporting advanced animation capabilities
 * like physics-based springs, custom easing curves, and specialized interpolations
 * missing from Remotion's baseline.
 */

// ============================================================================
// 1. BEZIER EASING CURVES (Cinematic / minimalist feel)
// ============================================================================
// Standardized industry curves used in after effects
export const easings = {
    // Very swift in, slow out. Good for UI sliding in.
    swiftOut: bezier(0.55, 0, 0.1, 1),

    // Gradual acceleration, sudden stop. Good for impacts.
    impact: bezier(1, 0, 1, 1),

    // Smooth cinematic pan (slow start, fast middle, slow end)
    cinematic: bezier(0.85, 0.0, 0.15, 1.0),

    // Bouncy or rubber-banding (goes past 1 slightly and comes back)
    overshoot: bezier(0.175, 0.885, 0.32, 1.275),

    // A complex, extremely punchy curve often used in minimalist explainer pop-ups
    kurzPunch: bezier(0.17, 0.89, 0.0, 1.3),
};

// ============================================================================
// 2. ADVANCED INTERPOLATION WRAPPERS
// ============================================================================

/**
 * Interpolate a value smoothly along a cinematic bezier curve.
 */
export const smoothPop = (frame: number, startFrame: number, duration: number = 30): number => {
    return interpolate(frame, [startFrame, startFrame + duration], [0, 1], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
        easing: easings.kurzPunch
    });
};

/**
 * A specialized interpolator that swings from A, overshoots to B, settles back to C.
 * Example of a complex chained animation logic inside a single hook.
 */
export const swingSettle = (frame: number, startFrame: number, valA: number, valB: number): number => {
    return interpolate(frame, [startFrame, startFrame + 20], [valA, valB], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
        easing: easings.overshoot
    });
};

// ============================================================================
// 3. ANIME.JS / GSAP MATH HELPERS
// ============================================================================
// When working with paths, svg-path-commander or animejs timelines often need 
// normalized time fractions.
// Here we expose a pure fraction of completion [0 -> 1] for external orchestrators.
export const getProgress = (frame: number, startFrame: number, durationInFrames: number): number => {
    const progress = (frame - startFrame) / durationInFrames;
    return Math.max(0, Math.min(1, progress));
};
