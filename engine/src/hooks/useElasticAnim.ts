import { spring, useCurrentFrame, useVideoConfig } from 'remotion';

/**
 * FILE: useElasticAnim.ts
 * PURPOSE: A unified hook to generate "Kurzgesagt-style" bouncy spring entrances.
 * 
 * Instead of linear fades or stiff movements, this uses Remotion's spring() 
 * physics engine to map a frame range [0 -> duration] to an elastic [0 -> 1] scale value.
 */

export interface ElasticAnimConfig {
    delay?: number;
    duration?: number;
    stiffness?: number;
    damping?: number;
    mass?: number;
}

export const useElasticAnim = ({
    delay = 0,
    duration = 30, // Default duration of the pop-in
    stiffness = 150, // Higher = faster snap
    damping = 12,    // Lower = more bouncy/elastic wobble
    mass = 0.8,
}: ElasticAnimConfig = {}) => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    // The current frame offset relative to this animation's start time
    const localFrame = Math.max(0, frame - delay);

    // Calculate the spring value (0 to 1)
    const scale = spring({
        fps,
        frame: localFrame,
        config: {
            stiffness,
            damping,
            mass,
            overshootClamping: false, // Essential for the bounce effect
        },
        durationInFrames: duration,
    });

    // Also calculate a smooth opacity fade-in that happens concurrently
    // but without the bounce (opacity = 1.2 would be invalid in CSS)
    const opacity = Math.min(1, spring({
        fps,
        frame: localFrame,
        config: {
            stiffness: stiffness * 0.8,
            damping: 20, // High damping so opacity doesn't overshoot
            overshootClamping: true
        },
        durationInFrames: duration * 0.8,
    }));

    return { scale, opacity };
};
