import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

export interface CameraProps {
    children: React.ReactNode;
    action?: string;
    duration?: number;
}

export const Camera: React.FC<CameraProps> = ({
    children,
    action = 'slow_zoom_in',
    duration = 300,
}) => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();
    const style = computeCameraStyle(action, frame, duration, fps);

    return (
        <AbsoluteFill style={style}>
            {children}
        </AbsoluteFill>
    );
};

function ease(t: number): number {
    // Smooth ease-in-out cubic
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

function computeCameraStyle(action: string, frame: number, duration: number, fps: number): React.CSSProperties {
    const clamp = { extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const };
    const progress = interpolate(frame, [0, duration], [0, 1], clamp);
    const eased = ease(progress);

    switch (action) {
        // ── Original moves (now with easing) ────────────────────
        case 'slow_zoom_in': {
            const scale = 1 + eased * 0.2;
            return { transform: `scale(${scale})` };
        }
        case 'dramatic_pull_back': {
            const scale = 1.2 - eased * 0.2;
            return { transform: `scale(${scale})` };
        }
        case 'pan_right': {
            const tx = eased * 100;
            return { transform: `translateX(${tx}px)` };
        }
        case 'pan_left': {
            const tx = eased * -100;
            return { transform: `translateX(${tx}px)` };
        }
        case 'slow_pan_up': {
            const ty = eased * -60;
            return { transform: `translateY(${ty}px)` };
        }
        case 'slow_pan_down': {
            const ty = eased * 60;
            return { transform: `translateY(${ty}px)` };
        }
        case 'static_focus': {
            return { transform: 'none' };
        }

        // ── Phase 18: New cinematic moves ────────────────────────

        // Combined zoom + horizontal pan
        case 'zoom_pan_right': {
            const scale = 1 + eased * 0.15;
            const tx = eased * 80;
            return { transform: `scale(${scale}) translateX(${tx}px)` };
        }
        case 'zoom_pan_left': {
            const scale = 1 + eased * 0.15;
            const tx = eased * -80;
            return { transform: `scale(${scale}) translateX(${tx}px)` };
        }

        // Ken Burns: slow zoom from a corner
        case 'ken_burns_tl': {
            const scale = 1 + eased * 0.3;
            return { transform: `scale(${scale})`, transformOrigin: '20% 20%' };
        }
        case 'ken_burns_br': {
            const scale = 1 + eased * 0.3;
            return { transform: `scale(${scale})`, transformOrigin: '80% 80%' };
        }
        case 'ken_burns_center': {
            const scale = 1 + eased * 0.25;
            return { transform: `scale(${scale})`, transformOrigin: '50% 40%' };
        }

        // Orbit: zoom + pan + slight rotation
        case 'orbit_left': {
            const scale = 1 + eased * 0.1;
            const tx = eased * -60;
            const rot = eased * -2;
            return { transform: `scale(${scale}) translateX(${tx}px) rotate(${rot}deg)` };
        }
        case 'orbit_right': {
            const scale = 1 + eased * 0.1;
            const tx = eased * 60;
            const rot = eased * 2;
            return { transform: `scale(${scale}) translateX(${tx}px) rotate(${rot}deg)` };
        }

        // Shake: subtle high-frequency jitter (for impacts)
        case 'shake': {
            const intensity = interpolate(frame, [0, 15, 60], [0, 6, 0], clamp);
            const shakeX = Math.sin(frame * 1.7) * intensity;
            const shakeY = Math.cos(frame * 2.3) * intensity;
            return { transform: `translate(${shakeX}px, ${shakeY}px)` };
        }

        // 3D perspective tilt (parallax depth illusion)
        case 'tilt_3d': {
            const rotY = interpolate(frame, [0, duration], [-3, 3], clamp);
            return {
                transform: `perspective(1200px) rotateY(${rotY}deg)`,
                transformOrigin: '50% 50%',
            };
        }

        // Breathe: gentle in-out scale pulse
        case 'breathe': {
            const breathe = 1 + Math.sin(frame * 0.04) * 0.03;
            return { transform: `scale(${breathe})` };
        }

        // Drift: slow diagonal float
        case 'drift': {
            const tx = eased * 40;
            const ty = eased * -30;
            const scale = 1 + eased * 0.08;
            return { transform: `translate(${tx}px, ${ty}px) scale(${scale})` };
        }

        default: {
            const scale = 1 + eased * 0.04;
            return { transform: `scale(${scale})` };
        }
    }
}
