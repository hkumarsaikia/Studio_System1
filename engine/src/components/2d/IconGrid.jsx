import React from 'react';

const glyphs = {
  bank: '🏦',
  factory: '🏭',
  home: '🏠',
  cart: '🛒',
  hospital: '🏥',
  school: '🏫',
  transport: '🚇',
  energy: '⚡',
  law: '⚖️',
  media: '📡',
  cloud: '☁️',
  ai: '🤖',
};

export const IconGrid = ({ icons = ['bank', 'factory', 'home', 'cart', 'law', 'media'] }) => {
  return (
    <svg viewBox="0 0 900 520" style={{ width: '100%', height: '100%' }}>
      {icons.slice(0, 9).map((icon, idx) => {
        const row = Math.floor(idx / 3);
        const col = idx % 3;
        const x = 120 + col * 260;
        const y = 90 + row * 150;

        return (
          <g key={`${icon}-${idx}`} transform={`translate(${x}, ${y})`}>
            <rect width="180" height="110" rx="20" fill="#0f172a" stroke="#38bdf8" strokeWidth="2" />
            <text x="90" y="48" textAnchor="middle" fontSize="42">
              {glyphs[icon] || '🔷'}
            </text>
            <text x="90" y="88" textAnchor="middle" fontSize="18" fill="#cbd5e1" style={{ textTransform: 'uppercase' }}>
              {icon}
            </text>
          </g>
        );
      })}
    </svg>
  );
};
