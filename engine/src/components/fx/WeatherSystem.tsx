import * as PIXI from 'pixi.js';

/**
 * FILE: WeatherSystem.ts (Renamed logic)
 * PURPOSE: Imperative PixiJS weather logic that avoids React lifecycle.
 */

export interface WeatherSystemConfig {
    app: PIXI.Application;
    intensity?: number;
    type?: 'rain' | 'snow';
}

interface WeatherParticle {
    graphics: PIXI.Graphics;
    x: number;
    y: number;
    speed: number;
    opacity: number;
    scale: number;
}

export function createWeatherSystem(config: WeatherSystemConfig) {
    const { app, intensity = 1.0, type = 'rain' } = config;

    // 1. Setup Container
    const container = new PIXI.Container();
    app.stage.addChild(container);

    // 2. Initialize Particles
    const particleCount = Math.ceil((type === 'rain' ? 250 : 150) * intensity);
    const particles: WeatherParticle[] = [];

    for (let i = 0; i < particleCount; i++) {
        const graphics = new PIXI.Graphics();
        graphics.beginFill(0xffffff, 1.0);
        if (type === 'rain') {
            graphics.drawRect(0, 0, 1.2, 30);
        } else {
            graphics.drawCircle(0, 0, 5);
        }
        graphics.endFill();

        container.addChild(graphics);

        const p: WeatherParticle = {
            graphics,
            x: Math.random() * (app.screen.width + 600) - 300,
            y: Math.random() * (app.screen.height + 200) - 100,
            speed: type === 'rain' ? 15 + Math.random() * 10 : 1.5 + Math.random() * 2,
            opacity: 0.15 + Math.random() * 0.45,
            scale: 0.4 + Math.random() * 0.8,
        };

        p.graphics.x = p.x;
        p.graphics.y = p.y;
        p.graphics.alpha = p.opacity;
        p.graphics.scale.set(p.scale);

        if (type === 'rain') {
            p.graphics.rotation = 0.08;
        }

        particles.push(p);
    }

    // 3. Ticker Update Function
    const tickerFn = () => {
        const dt = app.ticker.deltaTime || 1;

        for (let i = 0; i < particles.length; i++) {
            const p = particles[i];
            p.y += p.speed * dt;

            if (type === 'rain') {
                p.x += p.speed * 0.08 * dt;
            } else {
                p.x += Math.sin(p.y * 0.01 + i) * 0.5 * dt;
            }

            if (p.y > app.screen.height + 50) {
                p.y = -50;
                p.x = Math.random() * (app.screen.width + 600) - 300;
            }

            if (p.x > app.screen.width + 400) p.x = -300;
            if (p.x < -400) p.x = app.screen.width + 300;

            p.graphics.x = p.x;
            p.graphics.y = p.y;
        }
    };

    app.ticker.add(tickerFn);

    // 4. Return Cleanup Function
    return () => {
        app.ticker.remove(tickerFn);
        app.stage.removeChild(container);
        container.destroy({ children: true });
    };
}
