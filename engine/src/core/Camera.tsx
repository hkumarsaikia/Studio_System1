import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

export interface CameraLegacyProps {
    panX: number;
    panY: number;
    zoom: number;
}

export interface CameraProps {
    children: React.ReactNode;
    action?: 'slow_zoom_in' | 'pan_right' | 'pan_left' | 'static_focus' | 'dramatic_pull_back' | 'slow_pan_up' | 'slow_pan_down' | string;
    duration?: number;
    panX?: number;
    panY?: number;
    zoom?: number;
}

export const Camera: React.FC<CameraProps> = ({
    children,
    action = 'slow_zoom_in',
    duration = 300,
    panX = 20,
    panY = -18,
    zoom = 1.04,
}) => {
    const frame = useCurrentFrame();
    const style = computeCameraStyle(action, frame, duration, { panX, panY, zoom });

    return (
        <AbsoluteFill style={style}>
            {children}
        </AbsoluteFill>
    );
};

function computeCameraStyle(action: string, frame: number, duration: number, legacy: CameraLegacyProps): React.CSSProperties {
    const clamp: Parameters<typeof interpolate>[3] = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' };

    switch (action) {
        case 'slow_zoom_in': {
            const scale = interpolate(frame, [0, duration], [1, 1.2], clamp);
            return { transform: `scale(${scale})` };
        }
        case 'dramatic_pull_back': {
            const scale = interpolate(frame, [0, duration], [1.2, 1.0], clamp);
            return { transform: `scale(${scale})` };
        }
        case 'pan_right': {
            const tx = interpolate(frame, [0, duration], [0, 100], clamp);
            return { transform: `translateX(${tx}px)` };
        }
        case 'pan_left': {
            const tx = interpolate(frame, [0, duration], [0, -100], clamp);
            return { transform: `translateX(${tx}px)` };
        }
        case 'slow_pan_up': {
            const ty = interpolate(frame, [0, duration], [0, -60], clamp);
            return { transform: `translateY(${ty}px)` };
        }
        case 'slow_pan_down': {
            const ty = interpolate(frame, [0, duration], [0, 60], clamp);
            return { transform: `translateY(${ty}px)` };
        }
        case 'static_focus': {
            return { transform: 'none' };
        }
        default: {
            const progress = interpolate(frame, [0, duration], [0, 1], clamp);
            const tx = legacy.panX * progress;
            const ty = legacy.panY * progress;
            const scale = 1 + (legacy.zoom - 1) * progress;
            return { transform: `translate(${tx}px, ${ty}px) scale(${scale})` };
        }
    }
}
