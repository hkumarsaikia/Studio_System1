export const DEFAULT_SCENE_DURATION = 300;

export const normalizeSceneDuration = (scene: any, fallback: number = DEFAULT_SCENE_DURATION): number => {
    const duration = Number(scene?.duration);
    return Number.isFinite(duration) && duration > 0 ? Math.round(duration) : fallback;
};

export const computeTotalFrames = (scenes: any[]): number => {
    return scenes.reduce((acc, scene) => acc + normalizeSceneDuration(scene), 0);
};
