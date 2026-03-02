/**
 * FILE: theme.js
 * PURPOSE: Central color and palette definitions for the entire Studio System.
 *
 * This file is the single source of truth for all colors used across the
 * 500-video explainer channel. Every component, scene, and template pulls
 * its colors from here rather than using hard-coded values.
 *
 * STRUCTURE:
 *   - `colors`          → Flat semantic color tokens (use in any component)
 *   - `palettes`        → Category-specific background/secondary/accent combos
 *   - `themes`          → Legacy 3-theme map (dark / slate / minimal)
 *   - `categoryPalette` → Helper function to resolve a category string to its palette
 *
 * USAGE:
 *   import { colors, categoryPalette } from '../styles/theme.js';
 *   const palette = categoryPalette('MONEY & ECONOMICS');
 *   // → { background: '#052e16', secondary: '#14532d', accent: '#22c55e' }
 */

// ── Semantic Color Tokens ──────────────────────────────────────────
// These are the "brand colors" — used for text, backgrounds, accents,
// and data visualizations across all 500 videos.
export const colors = {
  // Neutrals (backgrounds & text)
  background: '#0f172a',       // Primary dark background
  backgroundAlt: '#1e293b',    // Slightly lighter for layering
  surface: '#334155',          // Cards, panels, elevated surfaces
  text: '#f8fafc',             // Primary white text
  textMuted: '#94a3b8',        // De-emphasized text (captions, labels)
  textSubtle: '#cbd5e1',       // Mid-emphasis text (subtitles)

  // Semantic brand colors — each serves a specific content purpose
  primarySystem: '#38bdf8',    // Default system/flow color (sky blue)
  moneyGreen: '#22c55e',       // Financial topics, positive trends
  dangerRed: '#ef4444',        // Warnings, negative trends, stress
  techPurple: '#a78bfa',       // Technology, institutions, power
  warmOrange: '#f97316',       // Energy, urgency, attention
  tealAccent: '#14b8a6',       // Future systems, sustainability
  pinkHighlight: '#f472b6',    // Information systems, media
};

// ── Category Palettes ──────────────────────────────────────────────
// Each of the 5 content categories (100 videos each) gets its own
// background gradient + accent color so viewers can visually distinguish
// which "bucket" a video belongs to at a glance.
export const palettes = {
  everydaySystems: { background: '#0f172a', secondary: '#1e293b', accent: '#38bdf8' },
  moneyEconomics: { background: '#052e16', secondary: '#14532d', accent: '#22c55e' },
  informationSystems: { background: '#1a0524', secondary: '#3b0764', accent: '#f472b6' },
  powerInstitutions: { background: '#1e1b4b', secondary: '#312e81', accent: '#a78bfa' },
  futureSystems: { background: '#042f2e', secondary: '#134e4a', accent: '#14b8a6' },
};

// ── Legacy Themes ──────────────────────────────────────────────────
// Kept for backwards compatibility with the template system.
// Templates like ExplainerCinematic pass a theme name ("slate") to
// SceneManager, which resolves it here.
export const themes = {
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
};

// ── Category Resolver ──────────────────────────────────────────────
// Maps the category string from video JSON (e.g. "MONEY & ECONOMICS")
// to the corresponding palette object. Used by build_topic_library.py
// to embed the right palette into each scene.
/** @param {string} category - One of the 5 category strings */
export const categoryPalette = (category) => {
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
    default:
      return palettes.everydaySystems;
  }
};
