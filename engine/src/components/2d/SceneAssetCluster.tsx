import React from 'react';
import { transparentize } from 'polished';
import { AssetSprite, ScenePaletteInput, humanizeAssetName, resolveAssetId } from './AssetSprite';

export interface SceneAssetClusterProps {
    assetTags?: string[];
    accentColor?: string;
    palette?: ScenePaletteInput;
}

export const SceneAssetCluster: React.FC<SceneAssetClusterProps> = ({
    assetTags = [],
    accentColor = '#38bdf8',
    palette,
}) => {
    const displayAssets = Array.from(new Set(assetTags.filter(Boolean))).slice(0, 3);

    if (!displayAssets.length) {
        return null;
    }

    return (
        <div
            style={{
                position: 'absolute',
                top: '7%',
                right: '4.5%',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'flex-end',
                gap: 16,
                zIndex: 12,
                pointerEvents: 'none',
            }}
        >
            {displayAssets.map((assetId, index) => {
                const resolvedId = resolveAssetId(assetId);
                const rotation = index % 2 === 0 ? -3 : 2;

                return (
                    <div
                        key={`${resolvedId}-${index}`}
                        style={{
                            width: 178,
                            padding: '14px 16px',
                            borderRadius: 22,
                            border: `1px solid ${transparentize(0.62, accentColor)}`,
                            background: `linear-gradient(165deg, ${transparentize(0.84, accentColor)} 0%, rgba(15,23,42,0.88) 48%, rgba(15,23,42,0.96) 100%)`,
                            boxShadow: `0 18px 36px rgba(2,6,23,0.34), inset 0 1px 0 rgba(255,255,255,0.08)`,
                            transform: `translateX(${-index * 20}px) rotate(${rotation}deg)`,
                            transformOrigin: 'top right',
                            display: 'flex',
                            alignItems: 'center',
                            gap: 14,
                        }}
                    >
                        <div
                            style={{
                                width: 58,
                                height: 58,
                                borderRadius: 18,
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                background: `radial-gradient(circle at 30% 20%, ${transparentize(0.78, accentColor)} 0%, rgba(15,23,42,0) 72%)`,
                                flexShrink: 0,
                            }}
                        >
                            <AssetSprite name={resolvedId} size={48} accentColor={accentColor} scenePalette={palette} />
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                            <div
                                style={{
                                    color: accentColor,
                                    fontSize: 10,
                                    fontWeight: 700,
                                    letterSpacing: '0.18em',
                                    textTransform: 'uppercase',
                                }}
                            >
                                Asset Tag
                            </div>
                            <div
                                style={{
                                    color: '#F8FAFC',
                                    fontSize: 15,
                                    fontWeight: 700,
                                    lineHeight: 1.2,
                                }}
                            >
                                {humanizeAssetName(resolvedId)}
                            </div>
                        </div>
                    </div>
                );
            })}
        </div>
    );
};
