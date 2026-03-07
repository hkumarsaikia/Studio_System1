import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { Person } from './Person';
import { springPop } from '@/utils/sceneTransitions';

export interface CrowdProps {
    count?: number;
    width?: number;
    height?: number;
}

export const Crowd: React.FC<CrowdProps> = ({ count = 8, width = 900, height = 600 }) => {
    const frame = useCurrentFrame();

    const people = Array.from({ length: count }).map((_, i) => {
        const row = Math.floor(i / 4);
        const col = i % 4;
        const delay = i * 4;

        const pop = springPop(frame, 20, delay);

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
                    size={person.scale}
                    shirt={person.shirt}
                />
            ))}
        </svg>
    );
};
