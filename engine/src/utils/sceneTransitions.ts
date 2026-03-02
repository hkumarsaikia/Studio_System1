import { interpolate } from 'remotion';

export const fadeInOut = (frame: number, duration: number, edge: number = 12): number => {
    return interpolate(frame, [0, edge, duration - edge, duration], [0, 1, 1, 0], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
    });
};

export const slideY = (frame: number, duration: number, amount: number = 30, edge: number = 16): number => {
    return interpolate(frame, [0, edge, duration - edge, duration], [amount, 0, 0, -amount], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
    });
};
