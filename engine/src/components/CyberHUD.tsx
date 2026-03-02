import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';

export interface CyberHUDProps {
    color?: string;
    dangerLevel?: number; // 0 to 1
}

export const CyberHUD: React.FC<CyberHUDProps> = ({
    color = '#06b6d4', // Cyberpunk Cyan
    dangerLevel = 0.2
}) => {
    const frame = useCurrentFrame();
    const { width, height } = useVideoConfig();

    // Rotation angles that continuous spin
    const rot1 = (frame * 1.5) % 360;
    const rot2 = (-frame * 0.8) % 360;
    const rot3 = (frame * 3.2) % 360;

    // Blinking effect for the "Recording" or danger indicator
    const blink = Math.floor(frame / 15) % 2 === 0;

    // Dynamic color shift if danger is high
    const activeColor = dangerLevel > 0.7 && blink ? '#ef4444' : color;

    return (
        <AbsoluteFill style={{ pointerEvents: 'none', zIndex: 100 }}>
            <svg width="100%" height="100%" viewBox={`0 0 ${width} ${height}`}>
                {/* Frame Borders */}
                <polyline points={`40,120 40,40 120,40`} fill="none" stroke={activeColor} strokeWidth={4} />
                <polyline points={`${width - 120},40 ${width - 40},40 ${width - 40},120`} fill="none" stroke={activeColor} strokeWidth={4} />
                <polyline points={`40,${height - 120} 40,${height - 40} 120,${height - 40}`} fill="none" stroke={activeColor} strokeWidth={4} />
                <polyline points={`${width - 120},${height - 40} ${width - 40},${height - 40} ${width - 40},${height - 120}`} fill="none" stroke={activeColor} strokeWidth={4} />

                {/* Diagonal Tech Cutouts at Corners */}
                <line x1={40} y1={40} x2={80} y2={80} stroke={activeColor} strokeWidth={2} opacity={0.5} />
                <line x1={width - 40} y1={40} x2={width - 80} y2={80} stroke={activeColor} strokeWidth={2} opacity={0.5} />
                <line x1={40} y1={height - 40} x2={80} y2={height - 80} stroke={activeColor} strokeWidth={2} opacity={0.5} />
                <line x1={width - 40} y1={height - 40} x2={width - 80} y2={height - 80} stroke={activeColor} strokeWidth={2} opacity={0.5} />

                {/* Center Reticle Assembly (Offset slightly higher for focus) */}
                <g transform={`translate(${width / 2}, ${height * 0.45})`}>
                    {/* Inner Dashed Target */}
                    <circle r={60} fill="none" stroke={activeColor} strokeWidth={2} strokeDasharray="10 10" transform={`rotate(${rot1})`} opacity={0.8} />

                    {/* Middle Complex Ring */}
                    <circle r={120} fill="none" stroke={color} strokeWidth={1} strokeDasharray="40 120 40 20" transform={`rotate(${rot2})`} opacity={0.4} />

                    {/* Outer Measurement Ring */}
                    <circle r={240} fill="none" stroke={color} strokeWidth={3} strokeDasharray="2 18" transform={`rotate(${rot3})`} opacity={0.2} />

                    {/* Static Crosshairs */}
                    <line x1={-300} y1={0} x2={-140} y2={0} stroke={color} strokeWidth={1} opacity={0.5} />
                    <line x1={140} y1={0} x2={300} y2={0} stroke={color} strokeWidth={1} opacity={0.5} />
                    <line x1={0} y1={-300} x2={0} y2={-140} stroke={color} strokeWidth={1} opacity={0.5} />
                    <line x1={0} y1={140} x2={0} y2={300} stroke={color} strokeWidth={1} opacity={0.5} />

                    {/* Center Dot */}
                    <circle r={4} fill={activeColor} />
                </g>

                {/* Bottom Data Streams */}
                <g transform={`translate(${width / 2}, ${height - 80})`} textAnchor="middle" fill={color} fontFamily="monospace" fontSize={16} opacity={0.7}>
                    <text y={0}>SYS.OP: NORMAL | TGT.LOCK: {rot1.toFixed(1)}° | FLUX: {(Math.sin(frame * 0.1) * 100).toFixed(0)}%</text>
                    <text y={20} fontSize={12} opacity={0.5}>COORD: 34.0522° N, 118.2437° W // SECTOR 7G // OVERRIDE: NULL</text>
                </g>

                {/* Top Left Rec Indicator */}
                <g transform="translate(60, 80)">
                    {blink && <circle cx={10} cy={-5} r={6} fill={activeColor} />}
                    <text x={26} fill={activeColor} fontFamily="monospace" fontSize={18} fontWeight="bold">
                        {dangerLevel > 0.7 ? 'WARNING' : 'REC'}
                    </text>
                </g>

                {/* Top Right Timer */}
                <g transform={`translate(${width - 240}, 80)`}>
                    <text fill={color} fontFamily="monospace" fontSize={22} letterSpacing="2">
                        T-MINUS: 00:00:{(frame / 30).toFixed(2).padStart(5, '0')}
                    </text>
                </g>

                {/* Left Side Audio Waveform Simulator */}
                <g transform="translate(60, 400)">
                    {Array.from({ length: 15 }).map((_, i) => {
                        const barHeight = Math.abs(Math.sin((frame + i * 10) * 0.2)) * 40 + 10;
                        return (
                            <rect
                                key={i}
                                x={0}
                                y={i * 12}
                                width={barHeight}
                                height={6}
                                fill={color}
                                opacity={0.6}
                            />
                        );
                    })}
                </g>

                {/* Right Side Vertical Metrics */}
                <g transform={`translate(${width - 120}, 400)`}>
                    {Array.from({ length: 8 }).map((_, i) => {
                        const width = Math.abs(Math.cos((frame - i * 5) * 0.1)) * 60 + 20;
                        return (
                            <rect
                                key={i}
                                x={80 - width} // Align Right
                                y={i * 20}
                                width={width}
                                height={8}
                                fill={color}
                                opacity={1 - (i * 0.1)}
                            />
                        );
                    })}
                </g>

            </svg>
        </AbsoluteFill>
    );
};
