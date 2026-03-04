import React, { useEffect, useMemo, useState } from 'react';
import { Composition, cancelRender, continueRender, delayRender } from 'remotion';
import { loadFont } from '@remotion/google-fonts/Outfit';
import { TemplateLoader } from './core/TemplateLoader';
import { getVideoData } from './generated/videoManifest';
import { parseVideoData } from './utils/dataParser';
import { computeTotalFrames } from './utils/sceneTiming';
import { AdvancedShowcase } from './components/AdvancedShowcase';

loadFont();

const getVideoIdFromEnv = (): string => {
    const envId = process.env.REMOTION_VIDEO_ID;
    return envId && typeof envId === 'string' ? envId : 'video_001';
};

export const RemotionRoot: React.FC = () => {
    const [videoData, setVideoData] = useState<any>(null);
    const [handle] = useState(() => delayRender('Loading selected video data'));
    const videoId = useMemo(() => getVideoIdFromEnv(), []);

    useEffect(() => {
        let active = true;

        getVideoData(videoId)
            .then((data: any) => {
                if (!active) {
                    return;
                }
                setVideoData(parseVideoData(data));
                continueRender(handle);
            })
            .catch((error: Error) => {
                cancelRender(error);
            });

        return () => {
            active = false;
        };
    }, [handle, videoId]);

    if (!videoData) {
        return null;
    }

    const totalDuration = computeTotalFrames(videoData.scenes);

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
            <Composition
                id="AdvancedShowcase"
                component={AdvancedShowcase}
                durationInFrames={150}
                fps={30}
                width={1920}
                height={1080}
            />
        </>
    );
};
