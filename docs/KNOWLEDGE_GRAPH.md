# Repository Knowledge Graph

This document describes the repository graph suite generated from the codebase. The graph data is written to `data/knowledge-graph/` and powers the standalone dashboard in `tools/knowledge-graph-viewer/`.

## Generated Artifacts

- Full graph JSON: `data/knowledge-graph/full-graph.json`
- File dependency graph: `data/knowledge-graph/file-dependency-graph.json`
- Python call graph: `data/knowledge-graph/python-call-graph.json`
- Engine symbol graph: `data/knowledge-graph/engine-symbol-graph.json`
- Data pipeline graph: `data/knowledge-graph/data-pipeline-graph.json`
- Dependency and env graph: `data/knowledge-graph/dependency-env-graph.json`
- Graph manifest: `data/knowledge-graph/manifest.json`
- Backward-compatible full graph: `data/repository_knowledge_graph.json`

## Summary

- Generated at: `2026-03-07T14:32:54.018854+00:00`
- Tracked files: `1228`
- Nodes: `1831`
- Edges: `1849`

## Dashboard

Launch the dashboard in Google Chrome Dev with DevTools open:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\open_knowledge_graph_preview.ps1
```

The launcher regenerates all graph data, starts the static preview server on `http://127.0.0.1:4173`, resolves Chrome Dev from Windows App Paths, and opens `tools/knowledge-graph-viewer/` with a dedicated preview profile.

## Views

| View | File | Nodes | Edges | Description |
| --- | --- | --- | --- | --- |
| Overview | full-graph.json | 1831 | 1849 | Full repository graph with all known nodes and relationships. |
| Files | file-dependency-graph.json | 123 | 219 | File imports, writes, dispatches, validation, and runtime links. |
| Python Calls | python-call-graph.json | 248 | 576 | Python files, functions, classes, variables, imports, and call edges. |
| Engine | engine-symbol-graph.json | 455 | 1074 | TS/JS files, exported symbols, top-level variables, component use, and imports. |
| Pipeline | data-pipeline-graph.json | 24 | 29 | Topics, storyboards, payloads, manifests, assets, and render outputs. |
| Deps/Env | dependency-env-graph.json | 192 | 687 | External packages, environment variables, and the files that use them. |

## Navigation Notes

- `Overview`: complete repository graph with all discovered nodes and relationships.
- `Files`: file-to-file imports, writes, runtime links, and dispatches.
- `Python Calls`: Python modules, functions, classes, constants, imports, and call edges.
- `Engine`: TypeScript/JavaScript files, exports, variables, component usage, and imports.
- `Pipeline`: topics, storyboards, compiled payloads, manifests, assets, and outputs.
- `Deps/Env`: Python packages, Node packages, environment variables, and the files that use them.

Use the dashboard search, node-type filters, relation filters, and inspector panel to move between files, symbols, dependencies, and outputs.

## Highest-Connectivity Files

| Path | Connections | Hint |
| --- | --- | --- |
| src/studio/generators/topic_library.py | 84 | Storyboard compiler and manifest builder |
| src/studio/config.py | 77 |  |
| scripts/generate_repo_knowledge_graph.py | 69 |  |
| engine/src/scenes/SceneFactory.tsx | 68 | Scene visual selector |
| src/studio/contracts.py | 58 |  |
| engine/package.json | 48 |  |
| engine/src/scenes/GenericScene.tsx | 39 | Generic scene shell |
| engine/src/utils/sceneTransitions.ts | 38 |  |
| src/studio/render/render_single.py | 37 | Single video render orchestration |
| engine/src/Root.tsx | 36 | Remotion root composition loader |
| engine/src/components/AdvancedShowcase.tsx | 32 |  |
| src/studio/assets/toolchain.py | 31 | SVG asset build pipeline |
| src/studio/utils/validate.py | 30 | Schema-backed validation |
| src/studio/generators/blueprints.py | 27 |  |
| src/studio/generators/metadata.py | 26 | Metadata generator |

## Representative Relationships

| Source | Relation | Target | Note |
| --- | --- | --- | --- |
| build_assets.py | delegates_to | src/studio/assets/toolchain.py | cli |
| engine/src/Root.tsx | loads | engine/src/generated/videoManifest.js |  |
| src/studio/assets/toolchain.py | writes | data/assets/processed | processed SVGs |
| src/studio/assets/toolchain.py | writes | data/assets/raw | raw SVGs |
| src/studio/assets/transpiler.py | writes | engine/src/components/generated/index.ts |  |
| src/studio/cli.py | dispatches_to | src/studio/assets/toolchain.py | assets build |
| src/studio/cli.py | dispatches_to | src/studio/generators/metadata.py | metadata |
| src/studio/cli.py | dispatches_to | src/studio/generators/topic_library.py | build |
| src/studio/cli.py | dispatches_to | src/studio/render/render_all.py | render all |
| src/studio/cli.py | dispatches_to | src/studio/render/render_single.py | render single |
| src/studio/cli.py | dispatches_to | src/studio/utils/validate.py | validate |
| src/studio/generators/metadata.py | writes | output/metadata |  |
| src/studio/generators/topic_library.py | writes | data/asset_library.json |  |
| src/studio/generators/topic_library.py | writes | data/demo_manifest.json |  |
| src/studio/generators/topic_library.py | writes | data/demos | demo payloads |
| src/studio/generators/topic_library.py | writes | data/storyboards | storyboards |
| src/studio/generators/topic_library.py | writes | data/video_manifest.json |  |
| src/studio/generators/topic_library.py | writes | data/videos | compiled payloads |
| src/studio/generators/topic_library.py | writes | engine/src/generated/videoManifest.js |  |
| src/studio/render/render_single.py | drives | engine/src/Root.tsx | segment render via env |
| src/studio/render/render_single.py | writes | output | final stitched mp4 |
| src/studio/render/render_single.py | writes | output/segments | segment mp4s |
| src/studio/utils/validate.py | validates_with | data/demo-manifest.schema.json |  |
| src/studio/utils/validate.py | validates_with | data/production-manifest.schema.json |  |
| src/studio/utils/validate.py | validates_with | data/storyboard.schema.json |  |

## Refresh Workflow

```powershell
python .\scripts\generate_repo_knowledge_graph.py
powershell -ExecutionPolicy Bypass -File .\scripts\open_knowledge_graph_preview.ps1
```

Regenerate the graph suite after code or data changes so the dashboard reflects the current repository state.
