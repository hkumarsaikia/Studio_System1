import React, { useMemo } from 'react';
import { AbsoluteFill, useVideoConfig, useCurrentFrame, interpolate, Easing } from 'remotion';
import { motion } from 'framer-motion';

/**
 * FILE: NeuralCore.tsx
 * PURPOSE: A mesmerizing, glowing radial neural network.
 * It pulses data from outer layers into an inner core, synchronized
 * with the Remotion timeline. It uses Framer Motion for smooth ring rotations.
 */
export const NeuralCore: React.FC<{ accentColor?: string }> = ({ accentColor = '#a78bfa' }) => {
    const frame = useCurrentFrame();
    const { fps, width, height } = useVideoConfig();

    const cx = width / 2;
    const cy = height / 2;

    // The scale of the "breathing" effect over a 4-second loop
    const breath = interpolate(
        frame % (fps * 4),
        [0, fps * 2, fps * 4],
        [1, 1.05, 1],
        { easing: Easing.inOut(Easing.ease) }
    );

    // Radii for the 3 network layers
    const layers = [120, 240, 380];
    const nodesPerLayer = [8, 16, 24];

    // Pre-calculate node positions mathematically
    const nodes = useMemo(() => {
        const result = [];
        for (let l = 0; l < layers.length; l++) {
            const r = layers[l];
            const count = nodesPerLayer[l];
            for (let i = 0; i < count; i++) {
                const angle = (i / count) * Math.PI * 2;
                result.push({
                    x: cx + r * Math.cos(angle),
                    y: cy + r * Math.sin(angle),
                    layer: l,
                    angle: angle
                });
            }
        }
        return result;
    }, [cx, cy]);

    // Calculate intense glow filters
    const filter = `drop-shadow(0 0 40px ${accentColor})`;

    return (
        <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
            <motion.svg
                width={width}
                height={height}
                style={{ filter, transform: `scale(${breath})` }}
                // Smooth global rotation using framer-motion integrated tightly with frame time
                animate={{ rotate: (frame / fps) * 10 }}
                transition={{ ease: "linear", duration: 0 }}
            >
                {/* Draw connections from Layer 2 to Layer 1 (Outer to middle) */}
                <g stroke={accentColor} strokeWidth="1" opacity={0.3}>
                    {nodes.filter(n => n.layer === 2).map((outerNode, i) => {
                        // Connect to a nearest node in layer 1
                        const innerNode = nodes.find(n => n.layer === 1 && Math.abs(n.angle - outerNode.angle) < 0.5);
                        if (!innerNode) return null;

                        // Line pulses opacity based on frame to simulate data transfer
                        const pulse = interpolate(
                            (frame - i * 2) % 60,
                            [0, 30, 60],
                            [0.1, 0.8, 0.1]
                        );

                        return (
                            <line
                                key={`line2-1-${i}`}
                                x1={outerNode.x} y1={outerNode.y}
                                x2={innerNode.x} y2={innerNode.y}
                                opacity={pulse}
                            />
                        );
                    })}
                </g>

                {/* Draw connections from Layer 1 to Layer 0 (Middle to Core) */}
                <g stroke={accentColor} strokeWidth="2" opacity={0.6}>
                    {nodes.filter(n => n.layer === 1).map((midNode, i) => {
                        const coreNode = nodes.find(n => n.layer === 0 && Math.abs(n.angle - midNode.angle) < 1.0);
                        if (!coreNode) return null;

                        const pulse = interpolate(
                            (frame - i * 2 + 15) % 30, // Moves faster near the core
                            [0, 15, 30],
                            [0.2, 1.0, 0.2]
                        );

                        return (
                            <line
                                key={`line1-0-${i}`}
                                x1={midNode.x} y1={midNode.y}
                                x2={coreNode.x} y2={coreNode.y}
                                opacity={pulse}
                            />
                        );
                    })}
                </g>

                {/* Draw the Nodes */}
                {nodes.map((n, i) => {
                    // Core nodes are largest
                    const size = n.layer === 0 ? 12 : n.layer === 1 ? 8 : 4;
                    const opacity = n.layer === 0 ? 1 : n.layer === 1 ? 0.7 : 0.4;
                    return (
                        <circle
                            key={`node-${i}`}
                            cx={n.x}
                            cy={n.y}
                            r={size}
                            fill={n.layer === 0 ? '#ffffff' : accentColor}
                            opacity={opacity}
                        />
                    );
                })}

                {/* The Central Processing Core Ring */}
                <circle
                    cx={cx} cy={cy} r={60}
                    fill="none"
                    stroke="#ffffff"
                    strokeWidth="4"
                    opacity={0.8}
                    strokeDasharray="20 10"
                />
            </motion.svg>
        </AbsoluteFill>
    );
};
