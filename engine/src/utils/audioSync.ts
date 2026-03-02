export interface SceneInfo {
    audio?: string | null;
    hasAudio?: boolean;
    duration: number;
    [key: string]: any;
}

export interface AudioOffset {
    audio: string | null;
    startFrame: number;
    duration: number;
}

export const buildAudioPath = (videoId: string, sceneIndex: number): string => {
    const paddedScene = String(sceneIndex + 1).padStart(2, '0');
    return `${videoId}_scene_${paddedScene}.mp3`;
};

export const resolveAudioSource = (scene: SceneInfo, videoId: string, sceneIndex: number): string | null => {
    if (scene.audio && typeof scene.audio === 'string') {
        return scene.audio;
    }
    if (scene.hasAudio) {
        return buildAudioPath(videoId, sceneIndex);
    }
    return null;
};

export const getSceneStartFrame = (scenes: SceneInfo[], sceneIndex: number): number => {
    return scenes.slice(0, sceneIndex).reduce((acc, scene) => acc + scene.duration, 0);
};

export const mapAudioOffsets = (scenes: SceneInfo[], videoId: string): AudioOffset[] => {
    return scenes
        .map((scene, index) => {
            const audioFile = resolveAudioSource(scene, videoId, index);
            return {
                audio: audioFile,
                startFrame: getSceneStartFrame(scenes, index),
                duration: scene.duration,
            };
        })
        .filter((item) => Boolean(item.audio));
};
