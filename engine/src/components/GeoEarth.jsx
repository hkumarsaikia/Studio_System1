/**
 * FILE: GeoEarth.jsx
 * PURPOSE: Renders an interactive, rotating SVG globe using D3 Geo projections.
 *
 * It uses `d3-geo` to project GeoJSON data (world.geo.json) onto an orthographic
 * (globe-like) SVG map. The globe gently rotates over the duration of the scene.
 *
 * PROPS:
 *   @param {string} accentColor - The primary brand color for highlighted countries
 *   @param {object} palette - The background and secondary colors
 */
import React, { useEffect, useState } from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, staticFile, delayRender, continueRender } from 'remotion';
import { geoOrthographic, geoPath } from 'd3-geo';

// Predefined fallback map if fetch fails (rare, but good for safety)
const fallbackGeo = { type: 'FeatureCollection', features: [] };

export const GeoEarth = ({ accentColor = '#38bdf8', palette = { secondary: '#1e293b' } }) => {
    const frame = useCurrentFrame();
    const { durationInFrames } = useVideoConfig();
    const [geoData, setGeoData] = useState(fallbackGeo);
    const [handle] = useState(() => delayRender("Loading GeoJSON dataset"));

    // Load the GeoJSON map data synchronously for Remotion to render flawlessly
    useEffect(() => {
        fetch(staticFile('data/world.geo.json'))
            .then((res) => res.json())
            .then((data) => {
                // Ensure features exist so .map doesn't fail
                if (data && data.features) {
                    setGeoData(data);
                }
                continueRender(handle);
            })
            .catch((err) => {
                console.error('Failed to load earth geojson:', err);
                continueRender(handle);
            });
    }, [handle]);

    // Set up the D3 Orthographic Projection (Globe)
    // 350px radius gives it a commanding presence in the vertical frame
    const projection = geoOrthographic()
        .scale(350)
        .translate([540, 960]); // Center of a 1080x1920 screen

    // Rotate the globe over time (simulate Earth spinning)
    // from -30 degrees longitude to +60 degrees longitude
    const rotation = interpolate(frame, [0, durationInFrames], [-30, 60], {
        extrapolateRight: 'clamp',
    });

    projection.rotate([rotation, -10]); // Slight tilt (-10) for a better angle

    const pathGenerator = geoPath().projection(projection);

    // A subtle glow/shadow effect for the water
    const globeDropShadow = {
        filter: `drop-shadow(0 0 60px ${accentColor}40)`,
    };

    return (
        <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
            <svg width="1080" height="1920" style={globeDropShadow}>
                {/* Ocean Background Circle */}
                <circle
                    cx="540"
                    cy="960"
                    r="350"
                    fill={palette.secondary}
                    opacity={0.3}
                    stroke={accentColor}
                    strokeWidth="2"
                />

                {/* Render each country as an SVG path */}
                <g>
                    {geoData.features.map((feature, i) => {
                        // Give every ~7th country the accent color to show specific "data nodes" dropping in
                        const isHighlighted = i % 7 === 0;
                        return (
                            <path
                                key={i}
                                d={pathGenerator(feature)}
                                fill={isHighlighted ? accentColor : palette.secondary}
                                stroke={palette.background}
                                strokeWidth={isHighlighted ? 2 : 1}
                                opacity={isHighlighted ? 0.9 : 0.6}
                            />
                        );
                    })}
                </g>

                {/* Lat/Lng Grid overlay (Graticule) - omitted for a cleaner minimalist look, 
            but kept standard outline for the circle boundary */}
            </svg>
        </AbsoluteFill>
    );
};
