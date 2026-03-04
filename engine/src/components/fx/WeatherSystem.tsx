import React, { useEffect, useRef } from 'react';
import * as PIXI from 'pixi.js';
import * as particles from '@pixi/particle-emitter';

export interface WeatherSystemProps {
    app: PIXI.Application;
    intensity?: number;
    type?: 'rain' | 'snow';
}

export const WeatherSystem: React.FC<WeatherSystemProps> = ({
    app,
    intensity = 1.0,
    type = 'rain'
}) => {
    const containerRef = useRef<PIXI.Container>(null);
    const emitterRef = useRef<particles.Emitter | null>(null);

    useEffect(() => {
        // Create a dedicated container for weather particles
        const container = new PIXI.Container();
        app.stage.addChild(container);
        containerRef.current = container;

        // Generate a simple procedural texture for the particle
        // White line for rain, white circle for snow
        const graphics = new PIXI.Graphics();
        graphics.beginFill(0xffffff, 0.6);
        if (type === 'rain') {
            graphics.drawRect(0, 0, 2, 20); // Streak
        } else {
            graphics.drawCircle(5, 5, 5); // Flake
        }
        graphics.endFill();
        const texture = app.renderer.generateTexture(graphics);

        // Configure the Emitter based on Kurzgesagt style (constant heavy flow, varying scale)
        const emitter = new particles.Emitter(container as any, {
            lifetime: { min: 1, max: 2 },
            frequency: Math.max(0.001, 0.02 / intensity),
            particlesPerWave: Math.ceil(10 * intensity),
            maxParticles: 5000,
            addAtBack: false,
            pos: { x: 0, y: 0 },
            behaviors: [
                {
                    type: 'alpha',
                    config: { alpha: { list: [{ value: 0.8, time: 0 }, { value: 0.2, time: 1 }] } }
                },
                {
                    type: 'scale',
                    config: { scale: { list: [{ value: type === 'rain' ? 1 : 0.5, time: 0 }, { value: type === 'rain' ? 1.5 : 1, time: 1 }] } }
                },
                {
                    type: 'color',
                    config: { color: { list: [{ value: "ffffff", time: 0 }, { value: "cbd5e1", time: 1 }] } }
                },
                {
                    type: 'moveSpeed',
                    config: { speed: { list: [{ value: type === 'rain' ? 1500 : 300, time: 0 }, { value: type === 'rain' ? 2000 : 400, time: 1 }] } }
                },
                {
                    type: 'rotation',
                    config: { minStart: type === 'rain' ? 80 : 0, maxStart: type === 'rain' ? 100 : 360 }
                },
                {
                    type: 'spawnShape',
                    config: { type: 'rect', data: { x: -500, y: -100, w: app.screen.width + 1000, h: 10 } }
                }
            ]
        });

        // Emitter requires its own ticking bounded to the Pixi app we hijacked
        emitterRef.current = emitter;
        emitter.emit = true;

        // We tap into the app.ticker which is ALREADY bound to Remotion via PixiCanvas
        const tickerFn = (ticker: any) => {
            // Delta is elapsed MS passed from app.ticker.update in PixiCanvas
            // Ticker delta is actually an internal PIXI scalar, let's use app.ticker.elapsedMS
            emitter.update(app.ticker.elapsedMS * 0.001);
        };

        app.ticker.add(tickerFn);

        return () => {
            app.ticker.remove(tickerFn);
            emitter.destroy();
            texture.destroy();
            if (container) {
                app.stage.removeChild(container);
                container.destroy({ children: true });
            }
        };
    }, [app, intensity, type]);

    // Renders nothing to DOM, it purely manages the PIXI canvas WebGL context
    return null;
};
