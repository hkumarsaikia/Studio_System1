import React from 'react';

export interface DataBarsProps {
    values?: number[];
}

export const DataBars: React.FC<DataBarsProps> = ({ values = [20, 35, 52, 68, 84] }) => {
    const barWidth = 110;
    const gap = 30;

    return (
        <svg viewBox="0 0 760 480" style={{ width: '100%', height: '100%' }}>
            <line x1="50" y1="420" x2="700" y2="420" stroke="#94a3b8" strokeWidth="4" />

            {values.map((value, index) => {
                const x = 70 + index * (barWidth + gap);
                const h = value * 3;
                const y = 420 - h;
                return (
                    <g key={index}>
                        <rect x={x} y={y} width={barWidth} height={h} rx="10" fill="#38bdf8" opacity={0.85} />
                        <text x={x + barWidth / 2} y={y - 12} fill="#e2e8f0" fontSize="22" textAnchor="middle">
                            {value}
                        </text>
                    </g>
                );
            })}
        </svg>
    );
};
