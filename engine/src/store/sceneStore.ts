import { create } from 'zustand';

/**
 * FILE: sceneStore.ts
 * PURPOSE: Global state management for complex scenes.
 * 
 * In advanced Kurzgesagt-style animations, multiple deeply nested elements
 * (like the 3D background, the midground SVG lattice, and foreground text)
 * all need to react to a single "Energy or Intensity" value without extreme prop-drilling.
 * 
 * Note: In Remotion, this state MUST be driven deterministically by `useCurrentFrame`,
 * not by user interaction or async timeouts.
 */

interface SceneState {
    globalIntensity: number;
    setGlobalIntensity: (val: number) => void;

    cameraZoom: number;
    setCameraZoom: (val: number) => void;

    activeThemeColor: string;
    setActiveThemeColor: (color: string) => void;
}

export const useSceneStore = create<SceneState>((set) => ({
    globalIntensity: 0,
    setGlobalIntensity: (val) => set({ globalIntensity: val }),

    cameraZoom: 1,
    setCameraZoom: (val) => set({ cameraZoom: val }),

    activeThemeColor: '#38bdf8',
    setActiveThemeColor: (color) => set({ activeThemeColor: color }),
}));
