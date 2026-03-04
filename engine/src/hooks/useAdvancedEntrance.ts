import { useCurrentFrame, interpolate } from 'remotion';
import BezierEasing from 'bezier-easing';

/**
 * FILE: useAdvancedEntrance.ts
 * PURPOSE: Wrapper hook to easily apply the cinematic cubic-bezier physical curves.
 * We replace `spring` equations with our precomputed BezierEasing objects.
 */

// We define our cinematic easing curves to recreate the "overshoot" snap feel
const easePunch = BezierEasing(0.25, 1.5, 0.4, 1);

export interface AdvancedEntranceConfig {
    delay?: number;
    duration?: number;
    popScale?: number;
}

export const useAdvancedEntrance = ({
    delay = 0,
    duration = 30, // Default duration of the pop-in
    popScale = 1.05 // How much to overshoot
}: AdvancedEntranceConfig = {}) => {
    const frame = useCurrentFrame();

    // The current frame offset relative to this animation's start time
    const localFrame = Math.max(0, frame - delay);

    // Clamp progress between 0 and 1
    const progress = Math.min(1, Math.max(0, localFrame / duration));

    // Apply the cubic bezier curve to the progress
    const easedProgress = easePunch(progress);

    // Calculate the scale value mapping [0, 1] to [0, popScale] using overshoot
    const scale = progress < 1 ? interpolate(easedProgress, [0, 1], [0, popScale]) : 1;

    // Smooth opacity fade-in
    const opacity = interpolate(progress, [0, 0.5], [0, 1], { extrapolateRight: 'clamp' });

    return { scale, opacity };
};
