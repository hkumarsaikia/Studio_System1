import { interpolate, spring } from 'remotion';

const clamp = { extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const };

// ── Original transitions (improved) ──────────────────────────────

export const fadeInOut = (frame: number, duration: number, edge: number = 12): number => {
    return interpolate(frame, [0, edge, duration - edge, duration], [0, 1, 1, 0], clamp);
};

export const slideY = (frame: number, duration: number, amount: number = 30, edge: number = 16): number => {
    return interpolate(frame, [0, edge, duration - edge, duration], [amount, 0, 0, -amount], clamp);
};

// ── Phase 18: New transition functions ───────────────────────────

/** Scale from 85% to 100% on enter, 100% to 90% on exit */
export const scaleIn = (frame: number, duration: number, edge: number = 20): number => {
    return interpolate(frame, [0, edge, duration - edge, duration], [0.85, 1, 1, 0.9], clamp);
};

/** Horizontal slide (positive = from right, negative = from left) */
export const slideX = (frame: number, duration: number, amount: number = 60, edge: number = 18): number => {
    return interpolate(frame, [0, edge, duration - edge, duration], [amount, 0, 0, -amount], clamp);
};

/** Subtle rotation entrance from ±3 degrees */
export const rotateIn = (frame: number, duration: number, degrees: number = 3, edge: number = 20): number => {
    return interpolate(frame, [0, edge, duration - edge, duration], [degrees, 0, 0, -degrees], clamp);
};

/** Heavy blur entrance (20px → 0) without opacity change */
export const blurReveal = (frame: number, duration: number, maxBlur: number = 20, edge: number = 25): number => {
    return interpolate(frame, [0, edge, duration - edge, duration], [maxBlur, 0, 0, maxBlur], clamp);
};

/** Progressive top-to-bottom reveal for clip-path wipes. */
export const wipeDown = (frame: number, duration: number, edge: number = 20): number => {
    return interpolate(frame, [0, edge, duration], [0, 1, 1], clamp);
};

/** Pure linear bounce entrance that doesn't trigger React hooks */
export const springPop = (frame: number, duration: number = 20, delay: number = 0): number => {
    // Pure math-based spring proxy to avoid 'useCurrentFrame' hook loops inside interpolation blocks
    const t = Math.max(0, (frame - delay) / duration);
    if (t >= 1) return 1;
    return Math.min(1, Math.sin(t * Math.PI) * 1.2 + t);
};
