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

Config.setChromiumDisableWebSecurity(true);
Config.setChromiumIgnoreCertificateErrors(true);

// Use absolute highest-quality rendering codecs for cinematic outputs
Config.setCodec('h264'); // Using h264 for web compatibility
// Note: videoBitrate is NOT set here — render.py controls quality via --crf flag

// ⚡ PERFORMANCE TUNING FOR RENDERING SPEED ⚡
// 1. Switch from uncompressed PNG buffers to JPEG frames. Skips alpha-channel calculation 
//    and cuts disk write IO speeds by up to 70%, drastically speeding up Remotion's frame builder.
Config.setVideoImageFormat('jpeg');

// 2. Disable audio multiplexing entirely. This skips the final FFMPEG audio stitching phase,
//    as our data visualizations currently run without a soundtrack, saving substantial post-render time.
Config.setMuted(true);

// 3. Maximize parallel frame rendering against the CPU.
Config.setConcurrency(10);

// 4. Request hardware acceleration where supported by platform + codec.
Config.setHardwareAcceleration('if-possible');
Config.setChromiumOpenGlRenderer('angle');
Config.setBinariesDirectory(path.join(process.cwd(), 'remotion-binaries-nvenc'));

// 5. Force NVENC for the final stitch step to leverage NVIDIA GPU encoding.
Config.overrideFfmpegCommand(({ type, args }) => {
    if (type !== 'stitcher') {
        return args;
    }

    const nextArgs = [...args];
    const codecFlagIndex = nextArgs.indexOf('-c:v');

    if (codecFlagIndex !== -1 && codecFlagIndex + 1 < nextArgs.length) {
        nextArgs[codecFlagIndex + 1] = 'h264_nvenc';
    } else {
        nextArgs.push('-c:v', 'h264_nvenc');
    }

    console.log('[NVENC] FFmpeg stitcher codec forced to h264_nvenc');
    return nextArgs;
});

// 6. Verbose logs to make encoder selection visible in PowerShell transcript.
Config.setLevel('verbose');

