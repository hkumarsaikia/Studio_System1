import React from 'react';
import { darken, mix, transparentize } from 'polished';
import assetRegistryData from '../../../../data/asset_registry.json';
import * as GeneratedAssets from '@/components/generated';

type AssetRegistryEntry = {
    id: string;
    componentName?: string;
    aliases?: string[];
    catalogKind?: string;
};

export interface ScenePaletteInput {
    background?: string;
    secondary?: string;
}

export interface AssetTokenPalette {
    base?: string;
    accent?: string;
    muted?: string;
    stroke?: string;
}

export interface AssetSpriteProps extends React.SVGProps<SVGSVGElement> {
    name: string;
    size?: number | string;
    accentColor?: string;
    scenePalette?: ScenePaletteInput;
    palette?: AssetTokenPalette;
}

type GeneratedAssetComponent = React.ComponentType<
    React.SVGProps<SVGSVGElement> & {
        size?: number | string;
        palette?: AssetTokenPalette;
    }
>;

const assetRegistry = assetRegistryData as Record<string, AssetRegistryEntry>;
const assetEntries = Object.values(assetRegistry);
const catalogKinds = new Set(['master', 'compatibility']);

const normalizeAssetKey = (assetId: string): string => assetId.trim().replace(/[\s-]+/g, '_').toLowerCase();

const assetLookup = assetEntries.reduce<Record<string, AssetRegistryEntry>>((lookup, entry) => {
    lookup[normalizeAssetKey(entry.id)] = entry;
    if (entry.componentName) {
        lookup[normalizeAssetKey(entry.componentName)] = entry;
    }
    for (const alias of entry.aliases ?? []) {
        lookup[normalizeAssetKey(alias)] = entry;
    }
    return lookup;
}, {});

const canonicalCatalogAssetIds = new Set(
    assetEntries.filter((entry) => catalogKinds.has(String(entry.catalogKind ?? ''))).map((entry) => entry.id)
);

const resolveAssetEntry = (name: string): AssetRegistryEntry | undefined => assetLookup[normalizeAssetKey(name)];

export const resolveAssetId = (name: string): string => resolveAssetEntry(name)?.id ?? name;

export const humanizeAssetName = (name: string): string =>
    resolveAssetId(name)
        .split('_')
        .filter(Boolean)
        .map((segment) => segment.charAt(0).toUpperCase() + segment.slice(1))
        .join(' ');

export const buildAssetPalette = (
    accentColor: string,
    scenePalette?: ScenePaletteInput,
    overrides?: AssetTokenPalette
): AssetTokenPalette => {
    const secondary = scenePalette?.secondary ?? '#37506A';
    const background = scenePalette?.background ?? '#0F172A';

    return {
        base: overrides?.base ?? secondary,
        accent: overrides?.accent ?? accentColor,
        muted: overrides?.muted ?? mix(0.72, '#FFFFFF', secondary),
        stroke: overrides?.stroke ?? darken(0.04, background),
    };
};

const GenericPlaceholder: React.FC<{ size: number | string; accentColor: string }> = ({ size, accentColor }) => (
    <svg viewBox="0 0 100 100" width={size} height={size}>
        <circle cx="50" cy="50" r="32" fill={transparentize(0.82, accentColor)} stroke={transparentize(0.18, accentColor)} strokeWidth="4" />
        <circle cx="50" cy="50" r="10" fill={transparentize(0.25, accentColor)} />
    </svg>
);

const MissingCanonicalAsset: React.FC<{ assetId: string; size: number | string; accentColor: string }> = ({
    assetId,
    size,
    accentColor,
}) => (
    <svg viewBox="0 0 100 100" width={size} height={size}>
        <rect x="12" y="12" width="76" height="76" rx="16" fill={transparentize(0.9, accentColor)} stroke={accentColor} strokeWidth="4" strokeDasharray="8 8" />
        <path d="M32 32 L68 68 M68 32 L32 68" stroke={accentColor} strokeWidth="6" strokeLinecap="round" />
        <title>{`Missing canonical asset: ${assetId}`}</title>
    </svg>
);

export const AssetSprite: React.FC<AssetSpriteProps> = ({
    name,
    size = '100%',
    accentColor = '#38BDF8',
    scenePalette,
    palette,
    ...props
}) => {
    const entry = resolveAssetEntry(name);
    const resolvedPalette = buildAssetPalette(accentColor, scenePalette, palette);
    const componentName = entry?.componentName;
    const AssetComponent = componentName
        ? (GeneratedAssets[componentName as keyof typeof GeneratedAssets] as GeneratedAssetComponent | undefined)
        : undefined;

    if (AssetComponent) {
        return <AssetComponent size={size} palette={resolvedPalette} {...props} />;
    }

    if (entry && canonicalCatalogAssetIds.has(entry.id)) {
        return <MissingCanonicalAsset assetId={entry.id} size={size} accentColor={resolvedPalette.accent ?? accentColor} />;
    }

    return <GenericPlaceholder size={size} accentColor={resolvedPalette.accent ?? accentColor} />;
};
