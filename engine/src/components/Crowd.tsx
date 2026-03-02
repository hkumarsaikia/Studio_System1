import React from 'react';
import { useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { Person } from './Person';

export interface CrowdProps {
    count?: number;
    width?: number;
    height?: number;
}

export const Crowd: React.FC<CrowdProps> = ({ count = 8, width = 900, height = 600 }) => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    const people = Array.from({ length: count }).map((_, i) => {
        const row = Math.floor(i / 4);
        const col = i % 4;
        const delay = i * 4;

        const pop = spring({
            frame: frame - delay,
            fps,
            config: {
                damping: 12,
                stiffness: 150,
            },
        });

        return {
            key: i,
            x: width * 0.2 + col * 170,
            y: height * 0.72 + row * 18,
            scale: (0.8 + row * 0.08) * pop,
            shirt: ['#2563eb', '#14b8a6', '#f97316', '#8b5cf6'][i % 4],
        };
    });

    return (
        <svg viewBox={`0 0 ${width} ${height}`} style={{ width: '100%', height: '100%' }}>
            {people.map((person) => (
                <Person
                    key={person.key}
                    x={person.x}
                    y={person.y}
                    scale={person.scale}
                    shirt={person.shirt}
                />
            ))}
        </svg>
    );
};
