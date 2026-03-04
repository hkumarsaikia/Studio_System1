import React from 'react';

export const CityStreetBackdrop: React.FC = () => {
    return (
        <svg viewBox="0 0 1200 900" style={{ width: '100%', height: '100%' }}>
            <rect width="1200" height="900" fill="#d8f2f1" />
            <rect x="0" y="590" width="1200" height="310" fill="#8b7a86" />

            <rect x="40" y="120" width="250" height="470" fill="#b3d1e6" />
            <rect x="930" y="160" width="230" height="430" fill="#b8d5e8" />
            <rect x="420" y="300" width="150" height="290" fill="#9cb7cf" />
            <rect x="630" y="260" width="170" height="330" fill="#93afc6" />

            {Array.from({ length: 10 }).map((_, i) => (
                <rect key={i} x={490 + i * 65} y="710" width="34" height="16" fill="#eadfbf" />
            ))}

            <rect x="360" y="680" width="480" height="36" fill="#efe4c8" />

            <circle cx="250" cy="470" r="52" fill="#9ccf5a" />
            <circle cx="970" cy="470" r="58" fill="#9ccf5a" />
        </svg>
    );
};
