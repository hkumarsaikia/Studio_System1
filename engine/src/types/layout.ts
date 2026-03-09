export interface LayoutProfile {
    padding: number;
    titleScale: number;
    subtitleScale: number;
    categoryScale: number;
    visualScale: number;
    textMaxWidth: number;
    textAlign: string;
}

export const defaultLayoutProfile: LayoutProfile = {
    padding: 80,
    titleScale: 1,
    subtitleScale: 1,
    categoryScale: 1,
    visualScale: 1,
    textMaxWidth: 920,
    textAlign: 'center',
};

export const mergeLayoutProfile = (
    layout: Partial<LayoutProfile> | null | undefined,
): LayoutProfile => ({
    ...defaultLayoutProfile,
    ...(layout ?? {}),
});
