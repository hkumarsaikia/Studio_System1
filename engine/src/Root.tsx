import React, { useEffect, useMemo, useState } from 'react';
import { Composition, cancelRender, continueRender, delayRender } from 'remotion';
import { TemplateLoader } from './core/TemplateLoader';
import { getVideoData } from './generated/videoManifest';
import { parseVideoData } from './utils/dataParser';
import { computeTotalFrames } from './utils/sceneTiming';
const getVideoIdFromEnv = (): string => {
    const envId = process.env.REMOTION_VIDEO_ID;
    return envId && typeof envId === 'string' ? envId : 'video_001';
};

export const RemotionRoot: React.FC = () => {
    // We register the composition dynamically so Remotion can discover the correct duration
    // based on the parsed video data before rendering.
    return (
        <>
            <Composition
                id="MainComposition"
                component={RootContent}
                durationInFrames={900} // Default duration, overridden by calculateMetadata
                calculateMetadata={async () => {
                    const videoId = getVideoIdFromEnv();
                    const data = await getVideoData(videoId);
                    const parsed = parseVideoData(data);
                    const duration = computeTotalFrames(parsed.scenes);
                    return {
                        durationInFrames: duration > 0 ? duration : 900
                    };
                }}
                fps={30}
                width={1920}
                height={1080}
            />
        </>
    );
};

const RootContent: React.FC = () => {
    const [videoData, setVideoData] = useState<any>(null);
    const [handle] = useState(() => delayRender('Loading selected video data'));
    const videoId = useMemo(() => getVideoIdFromEnv(), []);

    useEffect(() => {
        let active = true;

        getVideoData(videoId)
            .then((data: any) => {
                if (!active) return;
                setVideoData(parseVideoData(data));
                continueRender(handle);
            })
            .catch((error: Error) => {
                cancelRender(error);
            });

        return () => { active = false; };
    }, [handle, videoId]);

    if (!videoData) return null;

    return (
        <TemplateLoader
            template={videoData.template}
            scenes={videoData.scenes}
        />
    );
};
