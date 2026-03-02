import React from 'react';

// Font stack: Montserrat first for headings, Outfit as modern alternative,
// Inter as body fallback, then system fonts.
export const fontFamily = "'Montserrat', 'Outfit', 'Inter', 'Segoe UI', Roboto, sans-serif";
export const monoFamily = "'JetBrains Mono', 'Fira Code', 'Consolas', monospace";

export interface TypographyStyle {
    fontFamily: string;
    fontSize: number;
    fontWeight: number;
    lineHeight: number;
    letterSpacing?: number;
    textTransform?: string;
}

// ── Type Scale ─────────────────────────────────────────────────────
export const typography: Record<string, TypographyStyle> = {
    hero: {
        fontFamily,
        fontSize: 84,
        fontWeight: 800,
        lineHeight: 1.05,
        letterSpacing: -1,
    },
    title: {
        fontFamily,
        fontSize: 70,
        fontWeight: 700,
        lineHeight: 1.08,
        letterSpacing: -0.5,
    },
    subtitle: {
        fontFamily,
        fontSize: 42,
        fontWeight: 500,
        lineHeight: 1.25,
    },
    body: {
        fontFamily,
        fontSize: 32,
        fontWeight: 400,
        lineHeight: 1.4,
    },
    caption: {
        fontFamily,
        fontSize: 22,
        fontWeight: 600,
        lineHeight: 1.3,
        letterSpacing: 0.5,
        textTransform: 'uppercase',
    },
    label: {
        fontFamily,
        fontSize: 18,
        fontWeight: 700,
        lineHeight: 1.2,
        letterSpacing: 1,
        textTransform: 'uppercase',
    },
    // Phase 17: New type styles for data and code visuals
    mono: {
        fontFamily: monoFamily,
        fontSize: 20,
        fontWeight: 400,
        lineHeight: 1.6,
        letterSpacing: 0.5,
    },
    stat: {
        fontFamily,
        fontSize: 96,
        fontWeight: 800,
        lineHeight: 1.0,
        letterSpacing: -2,
    },
    badge: {
        fontFamily,
        fontSize: 16,
        fontWeight: 700,
        lineHeight: 1.0,
        letterSpacing: 1.5,
        textTransform: 'uppercase',
    },
};
