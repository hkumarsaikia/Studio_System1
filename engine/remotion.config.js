import { Config } from '@remotion/cli/config';
import path from 'path';

/**
 * FILE: remotion.config.js
 * PURPOSE: Optimizes the Remotion build and rendering pipeline.
 */

// Override Webpack config to allow cleaner alias imports (e.g., '@/components/...')
// and to automatically resolve modern TypeScript file extensions.
Config.overrideWebpackConfig((currentConfiguration) => {
    return {
        ...currentConfiguration,
        resolve: {
            ...currentConfiguration.resolve,
            extensions: [
                ...(currentConfiguration.resolve?.extensions || []),
                '.ts',
                '.tsx',
                '.js',
                '.jsx'
            ],
            alias: {
                ...(currentConfiguration.resolve?.alias ?? {}),
                '@': path.join(process.cwd(), 'src'),
            },
        },
    };
});

// Use absolute highest-quality rendering codecs for cinematic outputs
Config.setCodec('h264'); // Using h264 for web compatibility but maximum bitrate
Config.setVideoBitrate('20M'); // Bumps the bitrate way up for noise/grain clarity

// ⚡ PERFORMANCE TUNING FOR RENDERING SPEED ⚡
// 1. Switch from uncompressed PNG buffers to JPEG frames. Skips alpha-channel calculation 
//    and cuts disk write IO speeds by up to 70%, drastically speeding up Remotion's frame builder.
Config.setVideoImageFormat('jpeg');

// 2. Disable audio multiplexing entirely. This skips the final FFMPEG audio stitching phase,
//    as our data visualizations currently run without a soundtrack, saving substantial post-render time.
Config.setMuted(true);

// 3. Maximize parallel frame rendering against the CPU.
Config.setConcurrency(8);

