import { normalizeSceneDuration } from '@/utils/sceneTiming';

export const validateScene = (scene: any, index: number) => {
    if (!scene || typeof scene !== 'object') {
        throw new Error(`Scene at index ${index} is invalid.`);
    }

    if (!scene.text || typeof scene.text !== 'string') {
        throw new Error(`Scene at index ${index} must include a text string.`);
    }

    return {
        ...scene,
        duration: normalizeSceneDuration(scene),
    };
};

export const validateScenes = (scenes: any[] = []) => {
    if (!Array.isArray(scenes) || scenes.length === 0) {
        throw new Error('Video must include at least one scene.');
    }

    return scenes.map((scene, index) => validateScene(scene, index));
};
