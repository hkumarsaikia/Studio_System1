export interface ColorTokens {
    background: string;
    backgroundAlt: string;
    surface: string;
    text: string;
    textMuted: string;
    textSubtle: string;
    primarySystem: string;
    moneyGreen: string;
    dangerRed: string;
    techPurple: string;
    warmOrange: string;
    tealAccent: string;
    pinkHighlight: string;
}

export const colors: ColorTokens = {
    background: '#0f172a',
    backgroundAlt: '#1e293b',
    surface: '#334155',
    text: '#f8fafc',
    textMuted: '#94a3b8',
    textSubtle: '#cbd5e1',

    primarySystem: '#38bdf8',
    moneyGreen: '#22c55e',
    dangerRed: '#ef4444',
    techPurple: '#a78bfa',
    warmOrange: '#f97316',
    tealAccent: '#14b8a6',
    pinkHighlight: '#f472b6',
};

export interface Palette {
    background: string;
    secondary: string;
    accent: string;
}

export const palettes: Record<string, Palette> = {
    everydaySystems: { background: '#0f172a', secondary: '#1e293b', accent: '#38bdf8' },
    moneyEconomics: { background: '#052e16', secondary: '#14532d', accent: '#22c55e' },
    informationSystems: { background: '#1a0524', secondary: '#3b0764', accent: '#f472b6' },
    powerInstitutions: { background: '#1e1b4b', secondary: '#312e81', accent: '#a78bfa' },
    futureSystems: { background: '#042f2e', secondary: '#134e4a', accent: '#14b8a6' },

    // Phase 16: New Graphical Theming Palettes
    cyberpunk: { background: '#000000', secondary: '#0f172a', accent: '#ec4899' },
    corporate: { background: '#1e3a8a', secondary: '#3b82f6', accent: '#ffffff' },
    nature: { background: '#166534', secondary: '#4ade80', accent: '#38bdf8' },
};

export interface Theme {
    background: string;
    text: string;
    accent: string;
}

export const themes: Record<string, Theme> = {
    dark: {
        background: colors.background,
        text: colors.text,
        accent: colors.surface,
    },
    slate: {
        background: '#0f172a',
        text: '#38bdf8',
        accent: '#1e293b',
    },
    minimal: {
        background: '#f8fafc',
        text: '#0f172a',
        accent: '#e2e8f0',
    },
    cyberpunk: {
        background: '#000000',
        text: '#06b6d4',
        accent: '#ec4899',
    },
    corporate: {
        background: '#1e3a8a',
        text: '#ffffff',
        accent: '#3b82f6',
    },
    nature: {
        background: '#166534',
        text: '#f8fafc',
        accent: '#4ade80',
    }
};

export const categoryPalette = (category: string): Palette => {
    switch (category) {
        case 'EVERYDAY SYSTEMS':
            return palettes.everydaySystems;
        case 'MONEY & ECONOMICS':
            return palettes.moneyEconomics;
        case 'INFORMATION SYSTEMS':
            return palettes.informationSystems;
        case 'POWER & INSTITUTIONS':
            return palettes.powerInstitutions;
        case 'FUTURE SYSTEMS':
            return palettes.futureSystems;
        case 'CYBERPUNK':
            return palettes.cyberpunk;
        case 'CORPORATE':
            return palettes.corporate;
        case 'NATURE':
            return palettes.nature;
        default:
            return palettes.everydaySystems;
    }
};
