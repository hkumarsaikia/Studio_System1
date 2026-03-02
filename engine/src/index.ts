/**
 * FILE: index.js
 * PURPOSE: Application entry point — registers the Remotion root component.
 *
 * This is the file that Remotion's bundler looks for when starting a
 * render or launching the Studio. It:
 *   1. Imports global CSS (fonts, color variables)
 *   2. Registers RemotionRoot as the top-level composition provider
 *
 * Referenced in: remotion.config.js, render commands (npx remotion render)
 */
import { registerRoot } from 'remotion';
import './styles/global.css';
import { RemotionRoot } from './Root';

// Register the root — Remotion will call RemotionRoot() to discover compositions
registerRoot(RemotionRoot);