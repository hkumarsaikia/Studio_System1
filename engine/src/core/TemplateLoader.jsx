/**
 * FILE: TemplateLoader.jsx
 * PURPOSE: Routes the video to the correct template layout.
 *
 * The Studio System supports multiple video templates:
 *   - explainer  → ExplainerCinematic (widescreen explainer format)
 *   - infographic → DataInfographic (data-heavy visual format)
 *   - protest     → ProtestCinematic (social movement format)
 *   - shorts      → ShortsVertical (9:16 vertical, default)
 *
 * The video JSON's `template` field determines which layout to use.
 * Root.jsx passes this field to TemplateLoader, which acts as a
 * switch to select the correct rendering template.
 *
 * PROPS:
 *   @param {string}   template - Template name (see above)
 *   @param {object[]} scenes   - Array of scene objects
 */
import React from 'react';
import { ShortsVertical } from '../templates/ShortsVertical.jsx';
import { ExplainerCinematic } from '../templates/ExplainerCinematic.jsx';
import { DataInfographic } from '../templates/DataInfographic.jsx';
import { ProtestCinematic } from '../templates/ProtestCinematic.jsx';

export const TemplateLoader = ({ template, scenes }) => {
  switch (template) {
    case 'explainer':
      return <ExplainerCinematic scenes={scenes} />;
    case 'infographic':
      return <DataInfographic scenes={scenes} />;
    case 'protest':
      return <ProtestCinematic scenes={scenes} />;
    case 'shorts':
    default:
      // ShortsVertical is the default — most of the 500 videos use this
      return <ShortsVertical scenes={scenes} />;
  }
};
