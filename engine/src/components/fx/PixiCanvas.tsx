import React, { useEffect, useRef, useState } from 'react';
import { useCurrentFrame, useVideoConfig, delayRender, continueRender } from 'remotion';
import * as PIXI from 'pixi.js';

/**
 * FILE: PixiCanvas.tsx
 * PURPOSE: A custom wrapper for Pixi.js that forces the WebGL 2D engine
 * to run deterministically aligned with Remotion's frame clock.
 * Essential for generating complex procedural particle effects like rain/explosions
 * that won't jitter during headless mp4 rendering.
 */

// We disable Pixi's default shared ticker globally so it doesn't run away from Remotion
PIXI.Ticker.shared.autoStart = false;
PIXI.Ticker.shared.stop();
PIXI.Ticker.system.autoStart = false;
PIXI.Ticker.system.stop();

export interface PixiCanvasProps {
    children?: (app: PIXI.Application) => React.ReactNode | (() => void);
    width?: number;
    height?: number;
    backgroundColor?: string;
    transparent?: boolean;
    style?: React.CSSProperties;
}

export const PixiCanvas: React.FC<PixiCanvasProps> = ({
    children,
    width = 1920,
    height = 1080,
    backgroundColor = '#000000',
    transparent = true,
    style
}) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const appRef = useRef<PIXI.Application | null>(null);
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    const [handle] = useState(() => delayRender('PixiCanvas Init'));

    // 1. One-time Setup and Cleanup
    useEffect(() => {
        if (!canvasRef.current) return;

        let active = true;
        let pixiCleanup: (() => void) | null = null;

        const setup = async () => {
            let pixiApp: PIXI.Application | null = new PIXI.Application();
            await pixiApp.init({
                canvas: canvasRef.current!,
                width,
                height,
                backgroundColor: backgroundColor,
                backgroundAlpha: transparent ? 0 : 1,
                autoStart: false,
                resolution: window.devicePixelRatio || 1,
                antialias: true,
            });

            if (!active) {
                pixiApp.destroy(false, { children: true });
                return;
            }

            appRef.current = pixiApp;

            // Allow children to initialize if they need the app instance immediately
            // and capture any returned cleanup function
            if (children) {
                const result = children(pixiApp);
                if (typeof result === 'function') {
                    pixiCleanup = result;
                }
            }

            continueRender(handle);
        };

        setup();

        return () => {
            active = false;
            if (pixiCleanup) {
                pixiCleanup();
            }
            if (appRef.current) {
                // Remove ticker listeners first to stop any pending updates
                appRef.current.ticker.stop();
                appRef.current.destroy(false, { children: true });
                appRef.current = null;
            }
        };
    }, [width, height, backgroundColor, transparent]); // Stable config dependencies

    // 2. Deterministic Synchronization Loop
    // We use a separate effect for frame updates to keep them isolated from mount/unmount logic
    useEffect(() => {
        const app = appRef.current;
        if (!app) return;

        const renderedFrame = () => {
            // Calculate the exact elapsed time based on the specific Remotion frame
            const elapsedMS = (frame / fps) * 1000;
            app.ticker.update(elapsedMS);
            app.render();
        };

        // We use requestAnimationFrame as a secondary guard to ensure we don't block
        // during high-frequency React updates, though Remotion should handle this.
        renderedFrame();

    }, [frame, fps]);

    return (
        <div style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, ...style }}>
            <canvas
                ref={canvasRef}
                style={{ width: '100%', height: '100%', display: 'block' }}
            />
            {/* Note: In this version, children are handled imperative via the setup callback */}
        </div>
    );
};
