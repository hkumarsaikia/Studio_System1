import React, { useEffect, useRef } from 'react';
import * as PIXI from 'pixi.js';
import * as particles from '@pixi/particle-emitter';
import { useCurrentFrame } from 'remotion';

export interface ExplosionEffectProps {
    app: PIXI.Application;
    x?: number;
    y?: number;
    color?: string;
    triggerFrame?: number;
}

export const ExplosionEffect: React.FC<ExplosionEffectProps> = ({
    app,
    x = 960,
    y = 540,
    color = '#f59e0b', // Ambient orange/yellow standard explosion
    triggerFrame = 15
}) => {
    const frame = useCurrentFrame();
    const containerRef = useRef<PIXI.Container>(null);
    const emitterRef = useRef<particles.Emitter | null>(null);

    useEffect(() => {
        const container = new PIXI.Container();
        app.stage.addChild(container);
        containerRef.current = container;

        // Procedural particle: a fuzzy circle for glowing impacts
        const graphics = new PIXI.Graphics();
        graphics.beginFill(0xffffff);
        graphics.drawCircle(10, 10, 10);
        graphics.endFill();
        const texture = app.renderer.generateTexture(graphics);

        // Configure a burst (fireworks) style short-lifetime emitter
        const emitter = new particles.Emitter(container as any, {
            lifetime: { min: 0.3, max: 0.8 },
            frequency: 0.001,
            emitterLifetime: 0.1, // Burst only!
            maxParticles: 200,
            addAtBack: false,
            pos: { x, y },
            behaviors: [
                {
                    type: 'alpha',
                    config: { alpha: { list: [{ value: 1, time: 0 }, { value: 0, time: 1 }] } }
                },
                {
                    type: 'scale',
                    config: { scale: { list: [{ value: 1, time: 0 }, { value: 3, time: 1 }] } }
                },
                {
                    type: 'color',
                    config: { color: { list: [{ value: color.replace('#', ''), time: 0 }, { value: "333333", time: 1 }] } }
                },
                {
                    type: 'moveSpeed',
                    config: { speed: { list: [{ value: 800, time: 0 }, { value: 50, time: 1 }] } }
                },
                {
                    type: 'rotation',
                    config: { minStart: 0, maxStart: 360 }
                },
                {
                    type: 'spawnShape',
                    config: { type: 'torus', data: { x: 0, y: 0, radius: 10, innerRadius: 0 } }
                }
            ]
        });

        emitterRef.current = emitter;
        emitter.emit = false; // Wait for trigger

        const tickerFn = () => {
            emitter.update(app.ticker.elapsedMS * 0.001);
        };
        app.ticker.add(tickerFn);

        return () => {
            app.ticker.remove(tickerFn);
            emitter.destroy();
            texture.destroy();
            app.stage.removeChild(container);
            container.destroy({ children: true });
        };
    }, [app, x, y, color]);

    // Track frame to trigger explosion exactly
    useEffect(() => {
        if (emitterRef.current && frame === triggerFrame) {
            emitterRef.current.emit = true;
            emitterRef.current.resetPositionTracking();
            // A burst emitter naturally shuts itself off after 'emitterLifetime'
        }
    }, [frame, triggerFrame]);

    return null;
};
