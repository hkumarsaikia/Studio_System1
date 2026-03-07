import React from 'react';
import { AbsoluteFill } from 'remotion';
import { WaveField } from './fx/WaveField';

export const LandscapeBackdrop: React.FC = () => {
    return (
        <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
            <WaveField accentColor="#38bdf8" duration={300} />
        </AbsoluteFill>
    );
};
