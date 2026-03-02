import React from 'react';

export interface SystemIconProps {
    name: string;
    x?: number;
    y?: number;
    size?: number;
    color?: string;
}

export const SystemIcon: React.FC<SystemIconProps> = ({ name, x = 0, y = 0, size = 64, color = '#38bdf8' }) => {
    const icon = getIconPath(name, color);
    return (
        <g transform={`translate(${x}, ${y})`}>
            <svg viewBox="0 0 64 64" width={size} height={size}>
                {icon}
            </svg>
        </g>
    );
};

function getIconPath(name: string, color: string): React.ReactNode {
    switch (name) {
        case 'bank':
            return (
                <g fill={color}>
                    <polygon points="32,6 4,22 60,22" opacity="0.9" />
                    <rect x="4" y="22" width="56" height="4" rx="1" />
                    <rect x="10" y="28" width="6" height="24" rx="1" />
                    <rect x="22" y="28" width="6" height="24" rx="1" />
                    <rect x="36" y="28" width="6" height="24" rx="1" />
                    <rect x="48" y="28" width="6" height="24" rx="1" />
                    <rect x="4" y="52" width="56" height="6" rx="2" />
                </g>
            );
        case 'algorithm':
            return (
                <g fill="none" stroke={color} strokeWidth="2.5">
                    <rect x="22" y="4" width="20" height="12" rx="3" />
                    <rect x="6" y="28" width="20" height="12" rx="3" />
                    <rect x="38" y="28" width="20" height="12" rx="3" />
                    <rect x="22" y="48" width="20" height="12" rx="3" />
                    <line x1="32" y1="16" x2="16" y2="28" />
                    <line x1="32" y1="16" x2="48" y2="28" />
                    <line x1="16" y1="40" x2="32" y2="48" />
                    <line x1="48" y1="40" x2="32" y2="48" />
                </g>
            );
        case 'pollution':
            return (
                <g>
                    <circle cx="20" cy="42" r="14" fill={color} opacity="0.2" />
                    <circle cx="36" cy="36" r="18" fill={color} opacity="0.15" />
                    <circle cx="44" cy="46" r="12" fill={color} opacity="0.25" />
                    <path d="M8 56 L14 38 L22 48 L30 30 L38 44 L46 34 L56 56 Z" fill={color} opacity="0.3" />
                    <rect x="28" y="10" width="4" height="22" rx="2" fill={color} opacity="0.6" />
                    <rect x="36" y="14" width="4" height="18" rx="2" fill={color} opacity="0.5" />
                </g>
            );
        case 'factory':
            return (
                <g fill={color}>
                    <rect x="6" y="28" width="52" height="30" rx="3" />
                    <rect x="10" y="8" width="10" height="20" rx="2" />
                    <rect x="26" y="14" width="10" height="14" rx="2" />
                    <rect x="44" y="10" width="8" height="18" rx="2" />
                    <rect x="14" y="38" width="10" height="14" rx="2" fill="#0f172a" opacity="0.4" />
                    <rect x="30" y="38" width="10" height="14" rx="2" fill="#0f172a" opacity="0.4" />
                </g>
            );
        case 'coin':
            return (
                <g>
                    <circle cx="32" cy="32" r="24" fill={color} opacity="0.2" stroke={color} strokeWidth="3" />
                    <circle cx="32" cy="32" r="16" fill="none" stroke={color} strokeWidth="2" />
                    <text x="32" y="39" textAnchor="middle" fontSize="22" fill={color} fontWeight="700">$</text>
                </g>
            );
        case 'shield':
            return (
                <g>
                    <path d="M32 4 L56 16 L56 36 Q56 52 32 60 Q8 52 8 36 L8 16 Z" fill={color} opacity="0.2" stroke={color} strokeWidth="2.5" />
                    <path d="M26 32 L30 38 L40 24" fill="none" stroke={color} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
                </g>
            );
        case 'globe':
            return (
                <g>
                    <circle cx="32" cy="32" r="24" fill="none" stroke={color} strokeWidth="2.5" />
                    <ellipse cx="32" cy="32" rx="12" ry="24" fill="none" stroke={color} strokeWidth="1.5" />
                    <line x1="8" y1="32" x2="56" y2="32" stroke={color} strokeWidth="1.5" />
                    <line x1="32" y1="8" x2="32" y2="56" stroke={color} strokeWidth="1.5" />
                </g>
            );
        case 'lightning':
            return (
                <g>
                    <polygon points="36,4 16,34 28,34 24,60 48,26 34,26" fill={color} />
                </g>
            );
        case 'gear':
            return (
                <g fill={color}>
                    <circle cx="32" cy="32" r="10" fill="none" stroke={color} strokeWidth="3" />
                    <rect x="29" y="2" width="6" height="12" rx="2" />
                    <rect x="29" y="50" width="6" height="12" rx="2" />
                    <rect x="2" y="29" width="12" height="6" rx="2" />
                    <rect x="50" y="29" width="12" height="6" rx="2" />
                    <rect x="10" y="10" width="10" height="5" rx="2" transform="rotate(45,15,12.5)" />
                    <rect x="44" y="49" width="10" height="5" rx="2" transform="rotate(45,49,51.5)" />
                    <rect x="44" y="10" width="10" height="5" rx="2" transform="rotate(-45,49,12.5)" />
                    <rect x="10" y="49" width="10" height="5" rx="2" transform="rotate(-45,15,51.5)" />
                </g>
            );
        case 'people':
            return (
                <g fill={color}>
                    <circle cx="22" cy="18" r="8" />
                    <rect x="14" y="28" width="16" height="24" rx="6" />
                    <circle cx="42" cy="18" r="8" />
                    <rect x="34" y="28" width="16" height="24" rx="6" />
                </g>
            );
        case 'chart':
            return (
                <g fill={color}>
                    <rect x="8" y="40" width="10" height="18" rx="2" />
                    <rect x="22" y="28" width="10" height="30" rx="2" />
                    <rect x="36" y="18" width="10" height="40" rx="2" />
                    <rect x="50" y="8" width="10" height="50" rx="2" />
                    <line x1="4" y1="58" x2="62" y2="58" stroke={color} strokeWidth="2" />
                </g>
            );
        case 'arrow':
            return (
                <g fill="none" stroke={color} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="8" y1="32" x2="50" y2="32" />
                    <polyline points="40,22 50,32 40,42" />
                </g>
            );
        case 'loop':
            return (
                <g fill="none" stroke={color} strokeWidth="2.5" strokeLinecap="round">
                    <path d="M32 8 A24 24 0 1 1 8 32" />
                    <polygon points="8,24 8,40 16,32" fill={color} />
                </g>
            );
        case 'scale':
            return (
                <g fill="none" stroke={color} strokeWidth="2.5">
                    <line x1="32" y1="8" x2="32" y2="56" />
                    <line x1="12" y1="20" x2="52" y2="20" />
                    <path d="M12 20 L6 40 L18 40 Z" fill={color} opacity="0.3" />
                    <path d="M52 20 L46 40 L58 40 Z" fill={color} opacity="0.3" />
                    <rect x="24" y="52" width="16" height="6" rx="2" fill={color} />
                </g>
            );
        case 'network':
            return (
                <g>
                    <line x1="18" y1="18" x2="46" y2="18" stroke={color} strokeWidth="1.5" />
                    <line x1="18" y1="18" x2="18" y2="46" stroke={color} strokeWidth="1.5" />
                    <line x1="46" y1="18" x2="46" y2="46" stroke={color} strokeWidth="1.5" />
                    <line x1="18" y1="46" x2="46" y2="46" stroke={color} strokeWidth="1.5" />
                    <line x1="18" y1="18" x2="46" y2="46" stroke={color} strokeWidth="1.5" />
                    <circle cx="18" cy="18" r="6" fill={color} />
                    <circle cx="46" cy="18" r="6" fill={color} />
                    <circle cx="18" cy="46" r="6" fill={color} />
                    <circle cx="46" cy="46" r="6" fill={color} />
                </g>
            );
        case 'lock':
            return (
                <g>
                    <rect x="14" y="28" width="36" height="28" rx="4" fill={color} />
                    <path d="M22 28 V20 A10 10 0 0 1 42 20 V28" fill="none" stroke={color} strokeWidth="3" />
                    <circle cx="32" cy="42" r="4" fill="#0f172a" />
                </g>
            );
        case 'book':
            return (
                <g>
                    <rect x="12" y="8" width="40" height="48" rx="3" fill={color} opacity="0.2" stroke={color} strokeWidth="2" />
                    <line x1="22" y1="8" x2="22" y2="56" stroke={color} strokeWidth="2" />
                    <line x1="28" y1="20" x2="44" y2="20" stroke={color} strokeWidth="2" />
                    <line x1="28" y1="28" x2="44" y2="28" stroke={color} strokeWidth="1.5" />
                    <line x1="28" y1="34" x2="40" y2="34" stroke={color} strokeWidth="1.5" />
                </g>
            );
        case 'wave':
            return (
                <g fill="none" stroke={color} strokeWidth="3" strokeLinecap="round">
                    <path d="M4 32 Q12 12 20 32 T36 32 T52 32 T60 32" />
                    <path d="M4 44 Q12 24 20 44 T36 44 T52 44 T60 44" opacity="0.5" />
                </g>
            );
        case 'home':
            return (
                <g fill={color}>
                    <polygon points="32,8 8,30 14,30 14,54 50,54 50,30 56,30" />
                    <rect x="26" y="36" width="12" height="18" rx="2" fill="#0f172a" opacity="0.4" />
                </g>
            );
        case 'hospital':
            return (
                <g fill={color}>
                    <rect x="12" y="16" width="40" height="40" rx="4" />
                    <rect x="28" y="24" width="8" height="24" rx="1" fill="#0f172a" opacity="0.4" />
                    <rect x="20" y="32" width="24" height="8" rx="1" fill="#0f172a" opacity="0.4" />
                </g>
            );
        case 'school':
            return (
                <g fill={color}>
                    <rect x="10" y="24" width="44" height="32" rx="3" />
                    <polygon points="32,6 6,24 58,24" opacity="0.9" />
                    <rect x="26" y="38" width="12" height="18" rx="2" fill="#0f172a" opacity="0.4" />
                </g>
            );
        case 'transport':
            return (
                <g fill={color}>
                    <rect x="8" y="20" width="48" height="28" rx="6" />
                    <rect x="14" y="26" width="14" height="14" rx="2" fill="#0f172a" opacity="0.3" />
                    <rect x="34" y="26" width="14" height="14" rx="2" fill="#0f172a" opacity="0.3" />
                    <circle cx="18" cy="52" r="5" fill="#0f172a" />
                    <circle cx="46" cy="52" r="5" fill="#0f172a" />
                    <circle cx="18" cy="52" r="2.5" fill={color} />
                    <circle cx="46" cy="52" r="2.5" fill={color} />
                </g>
            );
        case 'energy':
            return (
                <g>
                    <polygon points="36,4 16,34 28,34 24,60 48,26 34,26" fill={color} />
                </g>
            );
        case 'law':
            return (
                <g fill="none" stroke={color} strokeWidth="2.5">
                    <line x1="32" y1="8" x2="32" y2="56" />
                    <line x1="12" y1="18" x2="52" y2="18" />
                    <path d="M12 18 L6 36 L18 36 Z" fill={color} opacity="0.3" />
                    <path d="M52 18 L46 36 L58 36 Z" fill={color} opacity="0.3" />
                    <rect x="22" y="52" width="20" height="6" rx="2" fill={color} />
                </g>
            );
        case 'media':
            return (
                <g>
                    <circle cx="32" cy="20" r="14" fill="none" stroke={color} strokeWidth="2.5" />
                    <rect x="30" y="34" width="4" height="18" fill={color} />
                    <rect x="22" y="48" width="20" height="4" rx="2" fill={color} />
                    <path d="M18 10 Q18 4 24 6" stroke={color} strokeWidth="2" fill="none" />
                    <path d="M12 14 Q10 4 20 4" stroke={color} strokeWidth="1.5" fill="none" />
                </g>
            );
        case 'cloud':
            return (
                <g fill={color}>
                    <circle cx="24" cy="32" r="14" />
                    <circle cx="38" cy="28" r="12" />
                    <circle cx="44" cy="36" r="10" />
                    <rect x="14" y="32" width="36" height="14" rx="4" />
                </g>
            );
        case 'ai':
            return (
                <g>
                    <rect x="16" y="12" width="32" height="28" rx="6" fill={color} opacity="0.2" stroke={color} strokeWidth="2" />
                    <circle cx="26" cy="26" r="4" fill={color} />
                    <circle cx="38" cy="26" r="4" fill={color} />
                    <line x1="26" y1="34" x2="38" y2="34" stroke={color} strokeWidth="2" />
                    <line x1="32" y1="40" x2="32" y2="52" stroke={color} strokeWidth="2" />
                    <line x1="22" y1="52" x2="42" y2="52" stroke={color} strokeWidth="2" />
                    <line x1="16" y1="22" x2="8" y2="18" stroke={color} strokeWidth="2" />
                    <line x1="48" y1="22" x2="56" y2="18" stroke={color} strokeWidth="2" />
                </g>
            );
        case 'cart':
            return (
                <g fill="none" stroke={color} strokeWidth="2.5">
                    <polyline points="8,12 16,12 24,42 52,42" />
                    <rect x="22" y="22" width="28" height="16" rx="3" fill={color} opacity="0.2" />
                    <circle cx="28" cy="52" r="5" fill={color} />
                    <circle cx="46" cy="52" r="5" fill={color} />
                </g>
            );
        default:
            return (
                <g>
                    <polygon points="32,6 58,32 32,58 6,32" fill={color} opacity="0.3" stroke={color} strokeWidth="2" />
                    <circle cx="32" cy="32" r="8" fill={color} />
                </g>
            );
    }
}

export interface SystemIconGridProps {
    icons?: string[];
    size?: number;
    color?: string;
}

export const SystemIconGrid: React.FC<SystemIconGridProps> = ({ icons = [], size = 80, color = '#38bdf8' }) => {
    const cols = Math.min(icons.length, 3);
    return (
        <svg viewBox="0 0 900 520" style={{ width: '100%', height: '100%' }}>
            {icons.slice(0, 9).map((name, idx) => {
                const row = Math.floor(idx / cols);
                const col = idx % cols;
                const x = 120 + col * 260;
                const y = 90 + row * 150;

                return (
                    <g key={`${name}-${idx}`} transform={`translate(${x}, ${y})`}>
                        <rect width="180" height="110" rx="20" fill="#0f172a" stroke={color} strokeWidth="2" />
                        <g transform="translate(58, 8)">
                            <SystemIcon name={name} size={48} color={color} />
                        </g>
                        <text
                            x="90" y="88"
                            textAnchor="middle" fontSize="18" fill="#cbd5e1"
                            style={{ textTransform: 'uppercase', fontFamily: "'Montserrat', sans-serif" }}
                        >
                            {name}
                        </text>
                    </g>
                );
            })}
        </svg>
    );
};
