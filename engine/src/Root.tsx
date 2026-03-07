import React, { useEffect, useMemo, useState } from 'react';
import { Composition, cancelRender, continueRender, delayRender } from 'remotion';
import { loadFont } from '@remotion/google-fonts/Outfit';
import { TemplateLoader } from './core/TemplateLoader';
import { getVideoData } from './generated/videoManifest';
import { parseVideoData } from './utils/dataParser';
import { computeTotalFrames } from './utils/sceneTiming';
import { AdvancedShowcase } from './components/AdvancedShowcase';
import { AdvancedAnimationShowcase } from './components/AdvancedAnimationShowcase';
import { EffectsShowcase } from './components/fx/EffectsShowcase';

loadFont();

const getVideoIdFromEnv = (): string => {
    const envId = process.env.REMOTION_VIDEO_ID;
    return envId && typeof envId === 'string' ? envId : 'video_001';
};

const getDatasetFromEnv = (videoId: string): 'production' | 'demo' => {
    const envDataset = process.env.REMOTION_DATASET;
    if (envDataset === 'demo' || envDataset === 'production') {
        return envDataset;
    }
    return videoId.startsWith('demo_') ? 'demo' : 'production';
};

const getSegmentIndexFromEnv = (): number | null => {
    const envIndex = process.env.REMOTION_SEGMENT_INDEX;
    if (!envIndex) {
        return null;
    }
    const parsed = Number(envIndex);
    return Number.isFinite(parsed) && parsed > 0 ? Math.round(parsed) : null;
};

export const RemotionRoot: React.FC = () => {
    const [videoData, setVideoData] = useState<any>(null);
    const [handle] = useState(() => delayRender('Loading selected video data'));
    const videoId = useMemo(() => getVideoIdFromEnv(), []);
    const dataset = useMemo(() => getDatasetFromEnv(videoId), [videoId]);
    const requestedSegmentIndex = useMemo(() => getSegmentIndexFromEnv(), []);

    useEffect(() => {
        let active = true;

        getVideoData(dataset, videoId)
            .then((data: any) => {
                if (!active) {
                    return;
                }
                const parsed = parseVideoData(data);
                if (requestedSegmentIndex && !parsed.scenes?.[requestedSegmentIndex - 1]) {
                    throw new Error(`Segment ${requestedSegmentIndex} is out of range for ${videoId}.`);
                }
                setVideoData(parsed);
                continueRender(handle);
            })
            .catch((error: Error) => {
                cancelRender(error);
            });

        return () => {
            active = false;
        };
    }, [dataset, handle, requestedSegmentIndex, videoId]);

    if (!videoData) {
        return null;
    }

    const totalDuration = computeTotalFrames(videoData.scenes);
    const segmentScenes = requestedSegmentIndex ? [videoData.scenes[requestedSegmentIndex - 1]] : [];
    const segmentDuration = segmentScenes.length > 0 ? computeTotalFrames(segmentScenes) : 1;

    return (
        <>
            <Composition
                id="MainComposition"
                component={TemplateLoader as React.FC<any>}
                durationInFrames={totalDuration}
                fps={videoData.fps}
                width={videoData.width}
                height={videoData.height}
                defaultProps={{
                    template: videoData.template,
                    scenes: videoData.scenes,
                }}
            />
            {segmentScenes.length > 0 ? (
                <Composition
                    id="SegmentComposition"
                    component={TemplateLoader as React.FC<any>}
                    durationInFrames={segmentDuration}
                    fps={videoData.fps}
                    width={videoData.width}
                    height={videoData.height}
                    defaultProps={{
                        template: videoData.template,
                        scenes: segmentScenes,
                    }}
                />
            ) : null}
            <Composition
                id="AdvancedShowcase"
                component={AdvancedShowcase}
                durationInFrames={150}
                fps={30}
                width={1920}
                height={1080}
            />
            <Composition
                id="AdvancedAnimationShowcase"
                component={AdvancedAnimationShowcase}
                durationInFrames={150}
                fps={30}
                width={1920}
                height={1080}
            />
            <Composition
                id="EffectsShowcase"
                component={EffectsShowcase}
                durationInFrames={150}
                fps={30}
                width={1920}
                height={1080}
            />
        </>
    );
};
