// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Studio System — Master Theme & Color Architecture (Phase 17)
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

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

// ── Core Semantic Color Tokens ────────────────────────────────────
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

// ── Extended Modern Color Library ─────────────────────────────────
// A large collection of curated modern colors for use across visuals
export const modernColors = {
    // User-requested palette
    lemonGlow: '#EFF396',
    mintBreeze: '#74E291',
    arcticTeal: '#59B4C3',
    deepIndigo: '#211C6A',

    // Warm Gradient Family
    peachFuzz: '#FFBE98',
    coralBlush: '#FF6B6B',
    sunsetRose: '#FF9A8B',
    goldenHour: '#F6D365',
    amberFlare: '#FFA234',
    tropicalMango: '#FFB347',

    // Cool Gradient Family
    electricBlue: '#00D2FF',
    frostedLilac: '#C9B1FF',
    lavenderMist: '#E8D5F5',
    iceBerg: '#A0E7E5',
    skyDream: '#89CFF0',
    oceanDeep: '#0077B6',

    // Neon & Cyberpunk
    neonPink: '#FF10F0',
    neonGreen: '#39FF14',
    neonYellow: '#DFFF00',
    neonCyan: '#00FFFF',
    hotMagenta: '#FF00FF',
    laserLemon: '#FEFE22',

    // Earth & Nature
    forestCanopy: '#2D6A4F',
    mossGreen: '#52B788',
    sandDune: '#DDB892',
    clayRed: '#C1694F',
    oceanFoam: '#99E1D9',
    twilightPurple: '#7B2D8E',

    // Pastel & Soft
    pastelPink: '#FFD1DC',
    pastelBlue: '#AEC6CF',
    pastelGreen: '#B5EAD7',
    pastelYellow: '#FFEAA7',
    pastelPurple: '#D4A5A5',
    pastelOrange: '#FFD3B6',

    // Metallic & Premium
    roseGold: '#B76E79',
    champagne: '#F7E7CE',
    platinum: '#E5E4E2',
    bronzeSheen: '#CD7F32',
    silverFrost: '#C0C0C0',

    // Gradient Mesh Colors
    ultraViolet: '#6C5CE7',
    livingCoral: '#FF6F61',
    classicBlue: '#0F4C81',
    illuminating: '#F5DF4D',
    veryPeri: '#6667AB',
    digitalLavender: '#E6E6FA',

    // Dark & Moody
    obsidian: '#0B0B0B',
    charcoalSmoke: '#36454F',
    midnightNavy: '#191970',
    voidBlack: '#0A0A0A',
    stormGray: '#708090',
};

// ── Palette Interface ─────────────────────────────────────────────
export interface Palette {
    background: string;
    secondary: string;
    accent: string;
}

// ── Category Palettes (Original 5) ────────────────────────────────
export const palettes: Record<string, Palette> = {
    everydaySystems: { background: '#0f172a', secondary: '#1e293b', accent: '#38bdf8' },
    moneyEconomics: { background: '#052e16', secondary: '#14532d', accent: '#22c55e' },
    informationSystems: { background: '#1a0524', secondary: '#3b0764', accent: '#f472b6' },
    powerInstitutions: { background: '#1e1b4b', secondary: '#312e81', accent: '#a78bfa' },
    futureSystems: { background: '#042f2e', secondary: '#134e4a', accent: '#14b8a6' },

    // Phase 16
    cyberpunk: { background: '#000000', secondary: '#0f172a', accent: '#ec4899' },
    corporate: { background: '#1e3a8a', secondary: '#3b82f6', accent: '#ffffff' },
    nature: { background: '#166534', secondary: '#4ade80', accent: '#38bdf8' },

    // Phase 17 — Modern Aesthetic Palettes
    tropicalSunset: { background: '#1a1423', secondary: '#FF6B6B', accent: '#FFB347' },
    arcticAurora: { background: '#0a192f', secondary: '#59B4C3', accent: '#74E291' },
    neonCity: { background: '#0B0B0B', secondary: '#FF10F0', accent: '#00FFFF' },
    pastelDream: { background: '#FFF5EE', secondary: '#FFD1DC', accent: '#AEC6CF' },
    desertStorm: { background: '#2C1A1D', secondary: '#DDB892', accent: '#C1694F' },
    deepOcean: { background: '#001233', secondary: '#0077B6', accent: '#00D2FF' },
    lavenderNight: { background: '#1B1040', secondary: '#6C5CE7', accent: '#E6E6FA' },
    goldenEmpire: { background: '#1C1200', secondary: '#CD7F32', accent: '#F5DF4D' },
    springMeadow: { background: '#0D2818', secondary: '#52B788', accent: '#EFF396' },
    roseQuartz: { background: '#2A0E26', secondary: '#B76E79', accent: '#FFD1DC' },
    midnightElectric: { background: '#0A0A2E', secondary: '#211C6A', accent: '#39FF14' },
    cosmicDust: { background: '#0F0A1A', secondary: '#7B2D8E', accent: '#C9B1FF' },
};

// ── Theme Interface (for Templates) ───────────────────────────────
export interface Theme {
    background: string;
    text: string;
    accent: string;
}

export const themes: Record<string, Theme> = {
    dark: { background: colors.background, text: colors.text, accent: colors.surface },
    slate: { background: '#0f172a', text: '#38bdf8', accent: '#1e293b' },
    minimal: { background: '#f8fafc', text: '#0f172a', accent: '#e2e8f0' },
    cyberpunk: { background: '#000000', text: '#06b6d4', accent: '#ec4899' },
    corporate: { background: '#1e3a8a', text: '#ffffff', accent: '#3b82f6' },
    nature: { background: '#166534', text: '#f8fafc', accent: '#4ade80' },
    neonCity: { background: '#0B0B0B', text: '#00FFFF', accent: '#FF10F0' },
    pastelDream: { background: '#FFF5EE', text: '#4A4A4A', accent: '#AEC6CF' },
    deepOcean: { background: '#001233', text: '#89CFF0', accent: '#0077B6' },
    goldenEmpire: { background: '#1C1200', text: '#F5DF4D', accent: '#CD7F32' },
    arcticAurora: { background: '#0a192f', text: '#74E291', accent: '#59B4C3' },
    cosmicDust: { background: '#0F0A1A', text: '#C9B1FF', accent: '#7B2D8E' },
};

// ── Gradient Presets ──────────────────────────────────────────────
// Pre-built CSS gradient strings for backgrounds and overlays
export const gradients = {
    sunsetBlaze: 'linear-gradient(135deg, #FF6B6B 0%, #FFB347 100%)',
    arcticShimmer: 'linear-gradient(135deg, #59B4C3 0%, #74E291 100%)',
    neonPulse: 'linear-gradient(135deg, #FF10F0 0%, #00FFFF 100%)',
    deepSpace: 'linear-gradient(135deg, #0F0A1A 0%, #211C6A 50%, #6C5CE7 100%)',
    goldenHour: 'linear-gradient(135deg, #F6D365 0%, #FFA234 100%)',
    oceanWave: 'linear-gradient(135deg, #0077B6 0%, #00D2FF 100%)',
    pastelBreeze: 'linear-gradient(135deg, #FFD1DC 0%, #AEC6CF 50%, #B5EAD7 100%)',
    forestMist: 'linear-gradient(135deg, #2D6A4F 0%, #52B788 50%, #EFF396 100%)',
    roseGarden: 'linear-gradient(135deg, #B76E79 0%, #FFD1DC 100%)',
    midnightFlare: 'linear-gradient(135deg, #191970 0%, #FF10F0 100%)',
    lemonLime: 'linear-gradient(135deg, #EFF396 0%, #74E291 100%)',
    electricDream: 'linear-gradient(135deg, #211C6A 0%, #59B4C3 50%, #EFF396 100%)',
    lavenderSunrise: 'linear-gradient(135deg, #E6E6FA 0%, #FF9A8B 100%)',
    cosmicRift: 'linear-gradient(135deg, #7B2D8E 0%, #C9B1FF 50%, #00D2FF 100%)',
};

// ── Category Resolver ─────────────────────────────────────────────
export const categoryPalette = (category: string): Palette => {
    switch (category) {
        case 'EVERYDAY SYSTEMS': return palettes.everydaySystems;
        case 'MONEY & ECONOMICS': return palettes.moneyEconomics;
        case 'INFORMATION SYSTEMS': return palettes.informationSystems;
        case 'POWER & INSTITUTIONS': return palettes.powerInstitutions;
        case 'FUTURE SYSTEMS': return palettes.futureSystems;
        case 'CYBERPUNK': return palettes.cyberpunk;
        case 'CORPORATE': return palettes.corporate;
        case 'NATURE': return palettes.nature;
        case 'TROPICAL SUNSET': return palettes.tropicalSunset;
        case 'ARCTIC AURORA': return palettes.arcticAurora;
        case 'NEON CITY': return palettes.neonCity;
        case 'PASTEL DREAM': return palettes.pastelDream;
        case 'DESERT STORM': return palettes.desertStorm;
        case 'DEEP OCEAN': return palettes.deepOcean;
        case 'LAVENDER NIGHT': return palettes.lavenderNight;
        case 'GOLDEN EMPIRE': return palettes.goldenEmpire;
        case 'SPRING MEADOW': return palettes.springMeadow;
        case 'ROSE QUARTZ': return palettes.roseQuartz;
        case 'MIDNIGHT ELECTRIC': return palettes.midnightElectric;
        case 'COSMIC DUST': return palettes.cosmicDust;
        default: return palettes.everydaySystems;
    }
};
