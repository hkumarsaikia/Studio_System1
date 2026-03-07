import { useCurrentFrame, useVideoConfig } from 'remotion';
import { springPop } from '@/utils/sceneTransitions';

/**
 * FILE: useElasticAnim.ts
 * PURPOSE: A unified hook to generate "minimalist-style" bouncy spring entrances.
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

    // Calculate the spring value (0 to 1) using pure mathematical proxy
    const scale = springPop(frame, duration, delay);

    // Smooth opacity fade-in
    const opacity = Math.min(1, springPop(frame, duration * 0.8, delay));

    return { scale, opacity };
};
