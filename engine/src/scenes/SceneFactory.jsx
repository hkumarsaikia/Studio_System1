/**
 * FILE: SceneFactory.jsx
 * PURPOSE: Maps the `visual` type string from scene JSON to the correct
 *          React component for rendering.
 *
 * This is a classic factory pattern — the video JSON says "show me a
 * 'flow' diagram" and this component returns a <FlowDiagram /> with the
 * right props. It decouples the data layer from the rendering layer.
 *
 * SUPPORTED VISUAL TYPES:
 *   crowd     → Crowd component (group of Person figures)
 *   bars      → DataBars (animated bar chart)
 *   flow      → FlowDiagram (cause-effect chain)
 *   network   → SystemNetwork (pentagon node graph)
 *   icons     → SystemIconGrid (SVG icon cards, replaces old emoji grid)
 *   landscape → LandscapeBackdrop (nature/horizon scene)
 *   city      → CityStreetBackdrop (urban scene)
 *   animals   → AnimalSilhouettes (ecology visuals)
 *   none      → Empty (text-only scene)
 *
 * PROPS:
 *   @param {object} scene - Scene object containing visual type + parametric data
 */
import React from 'react';
import { AbsoluteFill } from 'remotion';
import { Crowd } from '../components/Crowd.jsx';
import { DataBars } from '../components/DataBars.jsx';
import { FlowDiagram } from '../components/FlowDiagram.tsx';
import { SystemNetwork } from '../components/SystemNetwork.jsx';
import { SystemIconGrid } from '../components/SystemIcons.jsx';
import { LandscapeBackdrop } from '../components/LandscapeBackdrop.jsx';
import { CityStreetBackdrop } from '../components/CityStreetBackdrop.jsx';
import { AnimalSilhouettes } from '../components/AnimalSilhouettes.jsx';
import { GeoEarth } from '../components/GeoEarth.jsx';
import { GenerativeDataLattice } from '../components/p5/GenerativeDataLattice.tsx';
import { NeuralCore } from '../components/intelligence/NeuralCore.tsx';
import { ChalkboardEquation } from '../components/manim/ChalkboardEquation.tsx';

export const SceneFactory = ({ scene }) => {
  const visual = scene.visual || 'none';

  switch (visual) {
    // ── People & crowd scenes ──
    case 'crowd':
      return (
        <AbsoluteFill style={{ justifyContent: 'flex-end' }}>
          <Crowd count={scene.crowdCount || 8} />
        </AbsoluteFill>
      );

    // ── Data visualization ──
    case 'bars':
      return (
        <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', padding: 80 }}>
          <DataBars values={scene.barValues || [20, 35, 52, 68, 84]} />
        </AbsoluteFill>
      );

    // ── Process / cause-effect diagrams ──
    case 'flow':
      return (
        <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', padding: 80 }}>
          <FlowDiagram
            labels={scene.flowLabels || ['Input', 'System', 'Output']}
            direction={scene.flowDirection || 'horizontal'}
            accent={scene.accentColor}
          />
        </AbsoluteFill>
      );

    // ── System relationship graphs ──
    case 'network':
      return (
        <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', padding: 80 }}>
          <SystemNetwork nodes={scene.networkNodes || ['State', 'Market', 'Labor', 'Capital', 'Public']} />
        </AbsoluteFill>
      );

    // ── Icon grid (proper SVG, replaces old emoji IconGrid) ──
    case 'icons':
      return (
        <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', padding: 70 }}>
          <SystemIconGrid
            icons={scene.icons || ['bank', 'factory', 'home', 'cart', 'law', 'media']}
            color={scene.accentColor || '#38bdf8'}
          />
        </AbsoluteFill>
      );

    // ── Backdrop scenes (no interactive data) ──
    case 'landscape':
      return (
        <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
          <LandscapeBackdrop />
        </AbsoluteFill>
      );

    case 'city':
      return (
        <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
          <CityStreetBackdrop />
        </AbsoluteFill>
      );

    // ── Ecology / nature scenes ──
    case 'animals':
      return (
        <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', padding: 70 }}>
          <AnimalSilhouettes animals={scene.animals || ['bird', 'fish', 'deer']} />
        </AbsoluteFill>
      );

    // ── Mathematical & Abstract Systems ──
    case 'lattice':
      return <GenerativeDataLattice accentColor={scene.accentColor || '#f472b6'} />;

    // ── Intelligence & Processing Systems ──
    case 'neural_core':
      return <NeuralCore accentColor={scene.accentColor || '#a78bfa'} />;

    case 'math_equation':
      return <ChalkboardEquation accentColor={scene.accentColor || '#ffffff'} />;

    // ── Global & Geo Systems ──
    case 'earth':
      return (
        <GeoEarth
          accentColor={scene.accentColor || '#38bdf8'}
          palette={scene.palette || { secondary: '#1e293b' }}
        />
      );

    // ── Empty scene (text-only) ──
    case 'none':
    default:
      return null;
  }
};
