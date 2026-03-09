import { validateScenes } from '@/utils/propsValidator';
import { mergeLayoutProfile } from '@/types/layout';

export interface VideoData {
    fps?: number;
    width?: number;
    height?: number;
    template?: string;
    profileId?: string;
    layoutProfile?: Record<string, unknown>;
    scenes?: any[];
    [key: string]: any;
}

export const parseVideoData = (videoData: Partial<VideoData> | null | undefined) => {
    const layoutProfile = mergeLayoutProfile(videoData?.layoutProfile as Record<string, unknown> | undefined);
    const scenes = validateScenes(videoData?.scenes ?? []).map((scene) => ({
        ...scene,
        layout: mergeLayoutProfile((scene.layout ?? layoutProfile) as Record<string, unknown> | undefined),
    }));

    return {
        ...videoData,
        fps: Number(videoData?.fps) || 30,
        width: Number(videoData?.width) || 1080,
        height: Number(videoData?.height) || 1920,
        template: videoData?.template || 'shorts',
        profileId: videoData?.profileId || 'shorts_vertical',
        layoutProfile,
        scenes,
    };
};
