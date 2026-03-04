import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';

export interface MatrixRainProps {
    color?: string;
    density?: number;
}

export const MatrixRain: React.FC<MatrixRainProps> = ({
    color = '#22c55e', // Default Matrix Green
    density = 40       // Number of columns
}) => {
    const frame = useCurrentFrame();
    const { fps, width } = useVideoConfig();

    // Character set for the rain (Katakana + Latin + Digits)
    const CHARS = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレゲゼデベペオォコソトノホモヨョロゴゾドボポヴッン0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';

    // Generate deterministic column data based on index
    const columns = Array.from({ length: density }).map((_, i) => {
        // Pseudo-random deterministic values so it renders identically every time
        const speed = 2 + (Math.sin(i * 123.45) * 0.5 + 0.5) * 3; // 2 to 5 pixels per frame
        const startY = -800 + (Math.cos(i * 987.65) * 0.5 + 0.5) * 800;
        const length = Math.floor(10 + (Math.sin(i * 456.78) * 0.5 + 0.5) * 15);
        const charOffset = Math.floor((Math.sin(i * 321.12) * 0.5 + 0.5) * CHARS.length);

        // Calculate current vertical position based on frame and speed
        // Wrap around screen when it falls past the bottom
        const y = (startY + frame * speed * (fps / 30)) % 1500;

        return {
            x: (i / density) * width + (width / density) / 2, // Centered in column slot
            y,
            speed,
            length,
            charOffset
        };
    });

    return (
        <AbsoluteFill style={{ backgroundColor: '#000', overflow: 'hidden' }}>
            <svg width="100%" height="100%">
                {columns.map((col, i) => {
                    return (
                        <g key={i}>
                            {Array.from({ length: col.length }).map((_, charIdx) => {
                                // Determine which character to show (changes slowly based on frame)
                                const charIndex = Math.floor((col.charOffset + charIdx + frame * 0.1) % CHARS.length);
                                const char = CHARS[charIndex];

                                // Position of this specific character in the trail
                                const charY = col.y - charIdx * 25;

                                // Fade out the tail
                                const opacity = 1 - (charIdx / col.length);

                                // Highlight the leading character
                                const isLeader = charIdx === 0;

                                return (
                                    <text
                                        key={charIdx}
                                        x={col.x}
                                        y={charY}
                                        fill={isLeader ? '#ffffff' : color}
                                        fontSize={22}
                                        fontWeight={isLeader ? 800 : 400}
                                        fontFamily="monospace"
                                        textAnchor="middle"
                                        opacity={opacity}
                                        style={{
                                            // Slight glow on the leader
                                            filter: isLeader ? `drop-shadow(0 0 8px ${color})` : 'none'
                                        }}
                                    >
                                        {char}
                                    </text>
                                );
                            })}
                        </g>
                    );
                })}
            </svg>
        </AbsoluteFill>
    );
};
