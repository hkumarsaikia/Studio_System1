import { validateScenes } from '@/utils/propsValidator';

export interface VideoData {
    fps?: number;
    width?: number;
    height?: number;
    template?: string;
    scenes?: any[];
    [key: string]: any;
}

export const parseVideoData = (videoData: Partial<VideoData> | null | undefined) => {
    const scenes = validateScenes(videoData?.scenes ?? []);

    return {
        ...videoData,
        fps: Number(videoData?.fps) || 30,
        width: Number(videoData?.width) || 1080,
        height: Number(videoData?.height) || 1920,
        template: videoData?.template || 'shorts',
        scenes,
    };
};
