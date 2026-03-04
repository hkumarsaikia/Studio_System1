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
    children?: (app: PIXI.Application) => React.ReactNode;
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
    const [app, setApp] = useState<PIXI.Application | null>(null);
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    const [handle] = useState(() => delayRender('PixiCanvas Init'));

    useEffect(() => {
        if (!canvasRef.current) return;

        let active = true;
        const pixiApp = new PIXI.Application();

        // 1. Initialize Pixi Application Asynchronously (v8 requirement)
        pixiApp.init({
            canvas: canvasRef.current,
            width,
            height,
            backgroundColor: backgroundColor,
            backgroundAlpha: transparent ? 0 : 1,
            autoStart: false, // Critical: Disabled for deterministic rendering
            resolution: window.devicePixelRatio || 1,
            antialias: true,
        }).then(() => {
            if (!active) {
                pixiApp.destroy(false, { children: true });
                return;
            }
            setApp(pixiApp);
            continueRender(handle);
        });

        return () => {
            active = false;
            // Clean up if already fully initialized
            if (pixiApp.renderer) {
                pixiApp.destroy(false, { children: true });
            }
        };
    }, [width, height, backgroundColor, transparent]);

    // 2. Deterministic Synchronization Loop
    useEffect(() => {
        if (!app) return;

        // Calculate the exact elapsed time based on the specific Remotion frame
        // Ticker expects time in milliseconds
        const elapsedMS = (frame / fps) * 1000;

        // Force the Pixi application to render at this exact slice in time
        // Note: PIXI.Ticker.shared.update takes current time.
        // For physics engines, we often just want to step the ticker mathematically.
        app.ticker.update(elapsedMS);
        app.render();

    }, [frame, fps, app]);

    return (
        <div style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, ...style }}>
            <canvas ref={canvasRef} style={{ width: '100%', height: '100%', display: 'block' }} />
            {/* Render any React children that need the PIXI.Application context */}
            {app && children && children(app)}
        </div>
    );
};
