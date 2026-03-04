import React from 'react';
import { darken, lighten, transparentize } from 'polished';

export interface SystemIconProps {
    name: string;
    x?: number;
    y?: number;
    size?: number;
    color?: string;
    shadowColor?: string;
}

export const SystemIcon: React.FC<SystemIconProps> = ({
    name,
    x = 0,
    y = 0,
    size = 120, // Increased default size for more detail 
    color = '#38bdf8'
}) => {
    // Generate a deep, Kurzgesagt-style shadow color for this specific icon
    const shadowColor = darken(0.4, color);
    const highlightColor = lighten(0.2, color);
    const baseColor = color;

    // Scale down the 100x100 viewBox drawing coordinates to fit the requested size
    const scale = size / 100;

    const icon = getIconPath(name, baseColor, highlightColor, shadowColor);

    return (
        <g transform={`translate(${x}, ${y}) scale(${scale})`}>
            {/* The SVG viewBox is fixed to 100x100 internally for easy drawing */}
            <svg viewBox="0 0 100 100" width="100" height="100" style={{ overflow: 'visible' }}>
                <g filter="url(#kurzDropShadow)">
                    {icon}
                </g>
            </svg>
        </g>
    );
};

function getIconPath(name: string, base: string, highlight: string, shadow: string): React.ReactNode {
    // Helper colors
    const white = '#ffffff';
    const darkAcc = '#0f172a';

    switch (name) {
        case 'bank':
            return (
                <g>
                    {/* Back building drop shadow layer */}
                    <path d="M50 10 L10 35H90Z" fill={shadow} transform="translate(0, 4)" />
                    <rect x="10" y="35" width="80" height="8" rx="2" fill={shadow} transform="translate(0, 4)" />
                    <rect x="15" y="45" width="70" height="40" rx="2" fill={shadow} transform="translate(0, 4)" />

                    {/* Main Building Base (Columns) */}
                    <path d="M50 10 L10 35H90Z" fill={highlight} />
                    <polygon points="50,15 20,35 80,35" fill={base} />

                    <rect x="10" y="35" width="80" height="8" rx="2" fill={highlight} />
                    <rect x="15" y="45" width="10" height="40" rx="2" fill={base} />
                    <rect x="35" y="45" width="10" height="40" rx="2" fill={base} />
                    <rect x="55" y="45" width="10" height="40" rx="2" fill={base} />
                    <rect x="75" y="45" width="10" height="40" rx="2" fill={base} />
                    <rect x="10" y="85" width="80" height="8" rx="2" fill={highlight} />

                    {/* Details */}
                    <circle cx="50" cy="27" r="4" fill={shadow} opacity="0.5" />
                </g>
            );

        case 'pollution':
            return (
                <g>
                    {/* Smoke Clouds - layered, puffy geometry */}
                    <circle cx="35" cy="50" r="22" fill={transparentize(0.2, darkAcc)} filter="url(#neonGlow)" />
                    <circle cx="60" cy="40" r="30" fill={transparentize(0.2, darkAcc)} filter="url(#neonGlow)" />
                    <circle cx="75" cy="65" r="20" fill={transparentize(0.2, darkAcc)} filter="url(#neonGlow)" />

                    <circle cx="35" cy="50" r="20" fill={shadow} />
                    <circle cx="60" cy="40" r="28" fill={base} />
                    <circle cx="75" cy="65" r="18" fill={shadow} />

                    {/* Smoke Highlights */}
                    <circle cx="55" cy="30" r="8" fill={highlight} opacity="0.4" />
                    <circle cx="30" cy="42" r="6" fill={highlight} opacity="0.4" />

                    {/* Factory Stacks Base */}
                    <rect x="25" y="70" width="12" height="30" fill={shadow} />
                    <rect x="45" y="60" width="16" height="40" fill={highlight} />
                    <rect x="70" y="80" width="10" height="20" fill={base} />

                    <path d="M43 60 L63 60 L65 70 L41 70 Z" fill={shadow} />
                </g>
            );

        case 'network': // Or AI/Connectivity
            return (
                <g>
                    {/* Glowing Connection Lines */}
                    <g stroke={highlight} strokeWidth="6" strokeLinecap="round" opacity="0.8" filter="url(#neonGlow)">
                        <line x1="50" y1="20" x2="20" y2="70" />
                        <line x1="50" y1="20" x2="80" y2="70" />
                        <line x1="20" y1="70" x2="80" y2="70" />
                        <line x1="50" y1="50" x2="20" y2="70" />
                        <line x1="50" y1="50" x2="80" y2="70" />
                        <line x1="50" y1="20" x2="50" y2="50" />
                    </g>

                    {/* Nodes (Double layered for depth) */}
                    <circle cx="50" cy="20" r="14" fill={shadow} />
                    <circle cx="50" cy="20" r="10" fill="url(#metalShine)" />

                    <circle cx="20" cy="70" r="14" fill={shadow} />
                    <circle cx="20" cy="70" r="10" fill="url(#metalShine)" />

                    <circle cx="80" cy="70" r="14" fill={shadow} />
                    <circle cx="80" cy="70" r="10" fill="url(#metalShine)" />

                    <circle cx="50" cy="50" r="14" fill={base} />
                    <circle cx="50" cy="50" r="10" fill={highlight} />
                </g>
            );

        case 'shield':
            return (
                <g>
                    {/* Thick back plate */}
                    <path d="M50 10 L85 25 V55 C85 75 50 90 50 90 C50 90 15 75 15 55 V25 Z" fill={shadow} transform="translate(0, 4)" />
                    {/* Front plate */}
                    <path d="M50 10 L85 25 V55 C85 75 50 90 50 90 C50 90 15 75 15 55 V25 Z" fill={base} />
                    {/* Highlight slice (left side) */}
                    <path d="M50 10 L50 90 C50 90 15 75 15 55 V25 Z" fill={highlight} opacity="0.6" />

                    {/* Inner detail */}
                    <path d="M50 30 L65 40 M50 30 L35 40 M50 30 V65" stroke={shadow} strokeWidth="8" strokeLinecap="round" strokeLinejoin="round" fill="none" />
                </g>
            );

        case 'coin':
        case 'money':
            return (
                <g>
                    {/* Coin Stack 3D Effect */}
                    <ellipse cx="50" cy="75" rx="35" ry="15" fill={shadow} />
                    <rect x="15" y="60" width="70" height="15" fill={shadow} />

                    <ellipse cx="50" cy="60" rx="35" ry="15" fill={base} />
                    <rect x="15" y="45" width="70" height="15" fill={base} />

                    <ellipse cx="50" cy="45" rx="35" ry="15" fill={highlight} />
                    <ellipse cx="50" cy="45" rx="28" ry="10" fill={base} opacity="0.5" />

                    <text x="50" y="52" textAnchor="middle" fontSize="30" fontWeight="900" fill={shadow} style={{ fontFamily: 'monospace' }}>$</text>
                </g>
            );

        case 'globe':
        case 'earth':
            return (
                <g>
                    <circle cx="50" cy="50" r="45" fill={shadow} transform="translate(0, 4)" />

                    {/* Base Ocean */}
                    <circle cx="50" cy="50" r="45" fill={base} />
                    {/* Ocean gradient / Vignette */}
                    <circle cx="50" cy="50" r="45" fill="url(#deepVignette)" opacity="0.4" />

                    {/* Landmasses (Abstract geometries) */}
                    <path d="M25 25 Q45 15 60 25 T80 40 Q75 60 65 70 T40 85 Q25 80 15 65 T25 25Z" fill={highlight} opacity="0.9" />
                    <path d="M25 25 Q35 15 50 25 T70 40 Q65 60 55 70 T30 85 Q15 80 15 65 T25 25Z" fill={highlight} opacity="0.4" />

                    {/* Orbit Ring */}
                    <ellipse cx="50" cy="50" rx="55" ry="20" fill="none" stroke={white} strokeWidth="3" opacity="0.4" transform="rotate(-15 50 50)" />
                    {/* Satellite */}
                    <circle cx="15" cy="35" r="5" fill={highlight} filter="url(#neonGlow)" />
                </g>
            );

        case 'chart':
        case 'growth':
            return (
                <g>
                    {/* Graph Background Plane */}
                    <rect x="10" y="10" width="80" height="80" rx="10" fill={shadow} opacity="0.2" />

                    {/* Bar 1 */}
                    <rect x="20" y="60" width="15" height="30" rx="4" fill={shadow} />
                    <rect x="20" y="65" width="15" height="25" rx="4" fill={highlight} />
                    {/* Bar 2 */}
                    <rect x="42" y="40" width="15" height="50" rx="4" fill={base} />
                    <rect x="42" y="45" width="15" height="45" rx="4" fill={highlight} opacity="0.8" />
                    {/* Bar 3 */}
                    <rect x="64" y="20" width="15" height="70" rx="4" fill={shadow} filter="url(#neonGlow)" />
                    <rect x="64" y="20" width="15" height="70" rx="4" fill={highlight} />

                    {/* Trend Line */}
                    <path d="M15 60 L45 35 L75 10" fill="none" stroke={white} strokeWidth="6" strokeLinecap="round" filter="url(#neonGlow)" />
                </g>
            );

        case 'gear':
        case 'settings':
        case 'cog':
            return (
                <g>
                    {/* Base shadow for the entire gear */}
                    <g transform="translate(0, 4)">
                        <circle cx="50" cy="50" r="30" fill={shadow} />
                        {[0, 45, 90, 135].map(deg => (
                            <rect key={`shadow-${deg}`} x="40" y="5" width="20" height="90" rx="4" fill={shadow} transform={`rotate(${deg} 50 50)`} />
                        ))}
                    </g>

                    {/* Gear Base Layers */}
                    {[0, 45, 90, 135].map(deg => (
                        <rect key={`base-${deg}`} x="40" y="5" width="20" height="90" rx="4" fill={base} transform={`rotate(${deg} 50 50)`} />
                    ))}
                    <circle cx="50" cy="50" r="32" fill={base} />
                    <circle cx="50" cy="50" r="28" fill={highlight} />

                    {/* Inner hole */}
                    <circle cx="50" cy="50" r="14" fill={shadow} />
                    <circle cx="50" cy="50" r="14" fill="url(#deepVignette)" opacity="0.6" />
                </g>
            );

        case 'factory':
        case 'industry':
            return (
                <g>
                    {/* Back Building */}
                    <path d="M30 40 L60 40 L60 90 L30 90 Z" fill={shadow} />
                    <rect x="35" y="20" width="10" height="30" fill={shadow} />

                    {/* Front Building (sawtooth roof) */}
                    <path d="M10 90 L10 50 L30 35 L30 50 L50 35 L50 50 L70 35 L70 90 Z" fill={base} transform="translate(0,4)" />
                    <path d="M10 90 L10 50 L30 35 L30 50 L50 35 L50 50 L70 35 L70 90 Z" fill={highlight} />

                    {/* Doors/Windows */}
                    <rect x="25" y="70" width="15" height="20" rx="2" fill={shadow} />
                    <rect x="50" y="70" width="15" height="20" rx="2" fill={shadow} />
                </g>
            );

        case 'book':
        case 'education':
            return (
                <g>
                    {/* Back Cover */}
                    <rect x="15" y="15" width="70" height="75" rx="5" fill={shadow} transform="translate(4,4)" />
                    <rect x="15" y="15" width="70" height="75" rx="5" fill={base} />

                    {/* Pages Layer (Multi-layered effect) */}
                    <rect x="25" y="22" width="55" height="66" rx="2" fill="#e2e8f0" />
                    <rect x="22" y="20" width="55" height="66" rx="2" fill={white} />

                    {/* Bookmark */}
                    <polygon points="60,20 60,50 67,45 74,50 74,20" fill={highlight} filter="url(#kurzDropShadow)" />

                    {/* Binding spine */}
                    <rect x="15" y="15" width="8" height="75" rx="2" fill={shadow} opacity="0.4" />
                </g>
            );

        case 'media':
        case 'video':
        case 'play':
            return (
                <g>
                    {/* Big play button hexagon/circle hybrid */}
                    <circle cx="50" cy="50" r="45" fill={shadow} transform="translate(0, 5)" />
                    <circle cx="50" cy="50" r="45" fill={base} />
                    <circle cx="50" cy="50" r="40" fill={highlight} opacity="0.3" />

                    {/* Triangle Play Symbol */}
                    <polygon points="38,28 72,50 38,72" fill={shadow} transform="translate(4, 4)" />
                    <polygon points="38,28 72,50 38,72" fill={white} />
                </g>
            );

        case 'home':
        case 'house':
            return (
                <g>
                    {/* Roof layer */}
                    <polygon points="50,15 10,48 90,48" fill={highlight} transform="translate(0,4)" filter="url(#kurzDropShadow)" />
                    <polygon points="50,10 10,45 90,45" fill={base} />

                    {/* House body */}
                    <rect x="20" y="45" width="60" height="45" fill={shadow} />
                    <rect x="25" y="45" width="20" height="20" fill={highlight} opacity="0.3" />
                    <rect x="55" y="45" width="20" height="20" fill={highlight} opacity="0.3" />

                    {/* Door */}
                    <rect x="40" y="60" width="20" height="30" rx="3" fill="url(#metalShine)" />
                </g>
            );

        default:
            // High fidelity generic glowing orb placeholder
            return (
                <g>
                    <circle cx="50" cy="50" r="40" fill={shadow} filter="url(#neonGlow)" opacity="0.6" />
                    <circle cx="50" cy="50" r="35" fill={base} />
                    <circle cx="50" cy="50" r="28" fill={highlight} />
                    <circle cx="35" cy="35" r="8" fill={white} opacity="0.5" />
                </g>
            );
    }
}

// ── Generic Grid (Upgraded visually) ─────────────────────────────
export interface SystemIconGridProps {
    icons?: string[];
    size?: number;
    color?: string;
}

export const SystemIconGrid: React.FC<SystemIconGridProps> = ({ icons = [], size = 80, color = '#38bdf8' }) => {
    const cols = Math.min(icons.length, 3);
    const shadowColor = darken(0.4, color);

    return (
        <svg viewBox="0 0 900 520" style={{ width: '100%', height: '100%' }}>
            {icons.slice(0, 9).map((name, idx) => {
                const row = Math.floor(idx / cols);
                const col = idx % cols;
                const x = 120 + col * 260;
                const y = 90 + row * 150;

                return (
                    <g key={`${name}-${idx}`} transform={`translate(${x}, ${y})`} filter="url(#kurzDropShadow)">
                        {/* 3D Glass Card Container */}
                        <rect width="180" height="110" rx="20" fill={shadowColor} transform="translate(0, 6)" opacity="0.5" />
                        <rect width="180" height="110" rx="20" fill="#1e293b" stroke={color} strokeWidth="3" />

                        <g transform="translate(45, -5)">
                            <SystemIcon name={name} size={90} color={color} />
                        </g>

                        {/* Title text */}
                        <text
                            x="90" y="95"
                            textAnchor="middle" fontSize="16" fill="#f8fafc" fontWeight="bold"
                            style={{ textTransform: 'uppercase', fontFamily: "'Montserrat', sans-serif", letterSpacing: 1 }}
                        >
                            {name}
                        </text>
                    </g>
                );
            })}
        </svg>
    );
};
