import { useEffect } from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import gsap from 'gsap';

/**
 * FILE: useGSAPSync.ts
 * PURPOSE: Sycnchronizes a GSAP timeline or tween to Remotion's frame-by-frame rendering.
 * 
 * By default, GSAP uses `requestAnimationFrame` and plays based on real-world time.
 * For Remotion rendering (especially headless), we must freeze the timeline and 
 * mathematically force its playhead (`.progress()`) to exactly match the current video frame.
 */
export const useGSAPSync = (animation: gsap.core.Timeline | gsap.core.Tween | null) => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    useEffect(() => {
        if (!animation) return;

        // Important: Pause the animation so it doesn't run on its own clock
        animation.pause();

        // Calculate the GSAP animation total duration in frames based on video FPS
        const durationInSeconds = animation.duration();
        const totalFramesInAnim = durationInSeconds * fps;

        // Compute where the GSAP playhead should be (0.0 to 1.0)
        let progress = 0;
        if (totalFramesInAnim > 0) {
            progress = Math.max(0, Math.min(1, frame / totalFramesInAnim));
        }

        // Force GSAP to instantly render the exact state for this frame calculation
        animation.progress(progress);
    }, [frame, fps, animation]);
};
