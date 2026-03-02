/**
 * FILE: typography.js
 * PURPOSE: Typography scale and font definitions for the Studio System.
 *
 * All text rendered in videos — titles, subtitles, labels, captions — uses
 * these predefined styles. This ensures visual consistency across all 500
 * videos without any ad-hoc font sizing.
 *
 * FONTS:
 *   - Montserrat: Primary display font (titles, hero text)
 *   - Inter: Secondary font (body text, captions)
 *   Both are loaded via Google Fonts in global.css.
 *
 * USAGE:
 *   import { typography } from '../styles/typography.js';
 *   <h1 style={typography.title}>Scene Title</h1>
 */

// Font stack: Montserrat first for headings, Inter as fallback for body,
// then system fonts as final fallback if Google Fonts fails to load.
export const fontFamily = "'Montserrat', 'Inter', 'Segoe UI', Roboto, sans-serif";

// ── Type Scale ─────────────────────────────────────────────────────
// Six levels from largest (hero) to smallest (label).
// Each level is a complete style object that can be spread into JSX.
export const typography = {
  // Hero: Used for the main topic title on the opening scene
  hero: {
    fontFamily,
    fontSize: 84,
    fontWeight: 800,
    lineHeight: 1.05,
    letterSpacing: -1,
  },

  // Title: Used for scene headings (e.g. "Cause layer 1", "Data lens")
  title: {
    fontFamily,
    fontSize: 70,
    fontWeight: 700,
    lineHeight: 1.08,
    letterSpacing: -0.5,
  },

  // Subtitle: Used for scene subtext / supporting explanations
  subtitle: {
    fontFamily,
    fontSize: 42,
    fontWeight: 500,
    lineHeight: 1.25,
  },

  // Body: Used for longer descriptive text within scenes
  body: {
    fontFamily,
    fontSize: 32,
    fontWeight: 400,
    lineHeight: 1.4,
  },

  // Caption: Used for category labels, data annotations
  caption: {
    fontFamily,
    fontSize: 22,
    fontWeight: 600,
    lineHeight: 1.3,
    letterSpacing: 0.5,
    textTransform: 'uppercase',
  },

  // Label: Smallest text — icon labels, axis labels, footnotes
  label: {
    fontFamily,
    fontSize: 18,
    fontWeight: 700,
    lineHeight: 1.2,
    letterSpacing: 1,
    textTransform: 'uppercase',
  },
};