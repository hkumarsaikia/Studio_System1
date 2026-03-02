/**
 * FILE: useSceneAnimation.js
 * PURPOSE: Reusable React hook for scene entrance/exit animations.
 *
 * Provides a plug-and-play animation system that any scene component
 * can use for consistent entrance effects. Returns a `style` object
 * that can be spread directly into a component's style prop.
 *
 * THREE ENTRANCE MODES:
 *   'fade'   → Simple opacity fade (no movement)
 *   'spring' → Bouncy scale-up with Remotion's spring() physics
 *   'slide'  → Linear slide-up entrance with slide-down exit
 *
 * ALL MODES INCLUDE:
 *   - Opacity envelope (fade in → hold → fade out)
 *   - Blur envelope (blurry → clear → clear → blurry)
 *
 * USAGE:
 *   const { style } = useSceneAnimation({ entrance: 'spring', duration: 300 });
 *   return <div style={style}>My Scene Content</div>;
 *
 * @param {number}  options.duration    – Total scene frames (default 300)
 * @param {number}  options.fadeEdge    – Frames for fade transition (default 12)
 * @param {number}  options.slideAmount – Y translation pixels (default 24)
 * @param {string}  options.entrance    – Animation mode (default 'spring')
 *
 * @returns {object} { opacity, translateY, scale, blur, style }
 */
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

export const useSceneAnimation = ({
    duration = 300,
    fadeEdge = 12,
    slideAmount = 24,
    entrance = 'spring',
} = {}) => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    // ── Opacity envelope ───────────────────────────────────────────
    // Fades in over `fadeEdge` frames, holds at full opacity,
    // then fades out over the last `fadeEdge` frames.
    const opacity = interpolate(
        frame,
        [0, fadeEdge, duration - fadeEdge, duration],
        [0, 1, 1, 0],
        { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
    );

    // ── Blur envelope ──────────────────────────────────────────────
    // Adds a slight gaussian blur at scene edges for a cinematic feel.
    // Uses fadeEdge + 6 frames (slightly longer than opacity) for smoothness.
    const blur = interpolate(
        frame,
        [0, fadeEdge + 6, duration - fadeEdge - 6, duration],
        [6, 0, 0, 6],
        { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
    );

    // ── Entrance-specific transforms ───────────────────────────────
    let translateY = 0;
    let scale = 1;

    if (entrance === 'spring') {
        // Spring entrance: bouncy scale-up using Remotion's physics engine
        const springVal = spring({ frame, fps, config: { damping: 200 } });
        translateY = (1 - springVal) * slideAmount;    // Slides up as spring progresses
        scale = 0.92 + springVal * 0.08;               // Scales from 92% → 100%
    } else if (entrance === 'slide') {
        // Slide entrance: linear slide-up on enter, slide-down on exit
        translateY = interpolate(
            frame,
            [0, fadeEdge * 2, duration - fadeEdge * 2, duration],
            [slideAmount, 0, 0, -slideAmount],
            { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
        );
    }
    // 'fade' entrance: translateY and scale stay at defaults (0 and 1)

    return {
        opacity,
        translateY,
        scale,
        blur,
        // Ready-to-spread style object — apply with style={{...animation.style}}
        style: {
            opacity,
            filter: blur > 0.1 ? `blur(${blur}px)` : 'none',
            transform: `translateY(${translateY}px) scale(${scale})`,
        },
    };
};
