import React from 'react';
import { transparentize } from 'polished';
import { AssetSprite, ScenePaletteInput, humanizeAssetName } from './AssetSprite';

export interface SystemIconProps {
    name: string;
    x?: number;
    y?: number;
    size?: number;
    color?: string;
    palette?: ScenePaletteInput;
}

export const SystemIcon: React.FC<SystemIconProps> = ({
    name,
    x = 0,
    y = 0,
    size = 120,
    color = '#38bdf8',
    palette,
}) => {
    return (
        <div
            style={{
                position: 'absolute',
                left: x,
                top: y,
                width: size,
                height: size,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
            }}
        >
            <AssetSprite name={name} size={size} accentColor={color} scenePalette={palette} />
        </div>
    );
};

export interface SystemIconGridProps {
    icons?: string[];
    size?: number;
    color?: string;
    palette?: ScenePaletteInput;
}

export const SystemIconGrid: React.FC<SystemIconGridProps> = ({
    icons = [],
    size = 80,
    color = '#38bdf8',
    palette,
}) => {
    const displayIcons = icons.slice(0, 9);
    const columns = Math.min(3, Math.max(1, displayIcons.length));

    return (
        <div
            style={{
                width: '100%',
                maxWidth: 980,
                display: 'grid',
                gridTemplateColumns: `repeat(${columns}, minmax(0, 1fr))`,
                gap: 28,
                alignContent: 'center',
                justifyContent: 'center',
            }}
        >
            {displayIcons.map((name, index) => (
                <div
                    key={`${name}-${index}`}
                    style={{
                        minHeight: 168,
                        padding: '22px 20px 18px',
                        borderRadius: 24,
                        border: `1px solid ${transparentize(0.5, color)}`,
                        background: `linear-gradient(160deg, ${transparentize(0.78, color)} 0%, rgba(15,23,42,0.88) 52%, rgba(15,23,42,0.96) 100%)`,
                        boxShadow: `0 24px 50px ${transparentize(0.82, '#020617')}, inset 0 1px 0 ${transparentize(0.75, '#FFFFFF')}`,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        gap: 16,
                    }}
                >
                    <div
                        style={{
                            width: Math.max(88, size + 22),
                            height: Math.max(88, size + 22),
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            borderRadius: 22,
                            background: `radial-gradient(circle at 30% 20%, ${transparentize(0.78, color)} 0%, rgba(15,23,42,0) 72%)`,
                        }}
                    >
                        <AssetSprite name={name} size={size} accentColor={color} scenePalette={palette} />
                    </div>
                    <div
                        style={{
                            color: '#F8FAFC',
                            fontSize: 15,
                            fontWeight: 700,
                            letterSpacing: '0.08em',
                            textTransform: 'uppercase',
                            textAlign: 'center',
                            lineHeight: 1.2,
                        }}
                    >
                        {humanizeAssetName(name)}
                    </div>
                </div>
            ))}
        </div>
    );
};
