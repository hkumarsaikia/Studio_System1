import React from 'react';
import { AbsoluteFill } from 'remotion';

export const ThumbnailTemplate = ({ title, subtitle }) => {
  return (
    <AbsoluteFill
      style={{
        background: 'linear-gradient(155deg, #0f172a 0%, #1e293b 100%)',
        color: '#f8fafc',
        padding: 80,
        justifyContent: 'center',
      }}
    >
      <div style={{ fontSize: 72, fontWeight: 800, lineHeight: 1.1, marginBottom: 28 }}>{title}</div>
      {subtitle ? (
        <div style={{ fontSize: 34, color: '#cbd5e1', maxWidth: 1000, lineHeight: 1.3 }}>{subtitle}</div>
      ) : null}
      <div
        style={{
          marginTop: 42,
          display: 'inline-block',
          padding: '12px 18px',
          borderRadius: 999,
          backgroundColor: '#38bdf8',
          color: '#0f172a',
          fontWeight: 700,
          fontSize: 26,
          width: 'fit-content',
        }}
      >
        SYSTEMS EXPLAINER
      </div>
    </AbsoluteFill>
  );
};
