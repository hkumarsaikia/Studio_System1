import React, { useEffect, useState } from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, staticFile, delayRender, continueRender } from 'remotion';
import { geoOrthographic, geoPath } from 'd3-geo';

const fallbackGeo = { type: 'FeatureCollection', features: [] };

export interface GeoEarthProps {
    accentColor?: string;
    palette?: { secondary: string; background?: string;[key: string]: any };
}

export const GeoEarth: React.FC<GeoEarthProps> = ({ accentColor = '#38bdf8', palette = { secondary: '#1e293b' } }) => {
    const frame = useCurrentFrame();
    const { durationInFrames } = useVideoConfig();
    const [geoData, setGeoData] = useState<any>(fallbackGeo);
    const [handle] = useState(() => delayRender("Loading GeoJSON dataset"));

    useEffect(() => {
        fetch(staticFile('data/world.geo.json'))
            .then((res) => res.json())
            .then((data) => {
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

    const projection = geoOrthographic()
        .scale(350)
        .translate([540, 960]);

    const rotation = interpolate(frame, [0, durationInFrames], [-30, 60], {
        extrapolateRight: 'clamp',
    });

    projection.rotate([rotation, -10]);

    const pathGenerator = geoPath().projection(projection);

    const globeDropShadow = {
        filter: `drop-shadow(0 0 60px ${accentColor}40)`,
    };

    return (
        <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
            <svg width="1080" height="1920" style={globeDropShadow}>
                <circle
                    cx="540"
                    cy="960"
                    r="350"
                    fill={palette.secondary}
                    opacity={0.3}
                    stroke={accentColor}
                    strokeWidth="2"
                />

                <g>
                    {geoData.features.map((feature: any, i: number) => {
                        const isHighlighted = i % 7 === 0;
                        return (
                            <path
                                key={i}
                                d={pathGenerator(feature) || ''}
                                fill={isHighlighted ? accentColor : palette.secondary}
                                stroke={palette.background || '#000'}
                                strokeWidth={isHighlighted ? 2 : 1}
                                opacity={isHighlighted ? 0.9 : 0.6}
                            />
                        );
                    })}
                </g>
            </svg>
        </AbsoluteFill>
    );
};
