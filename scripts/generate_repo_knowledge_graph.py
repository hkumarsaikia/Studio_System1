from __future__ import annotations

import ast
import json
import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable

REPO_ROOT = Path(__file__).resolve().parents[1]
GRAPH_OUTPUT_DIR = REPO_ROOT / "data" / "knowledge-graph"
BACKWARD_COMPAT_OUTPUT = REPO_ROOT / "data" / "repository_knowledge_graph.json"
MARKDOWN_OUTPUT = REPO_ROOT / "docs" / "KNOWLEDGE_GRAPH.md"
TS_EXTENSIONS = (".ts", ".tsx", ".js", ".jsx")
EXCLUDED_PREFIXES = (
    "logs/",
    "output/",
    "data/knowledge-graph/",
    "data/repository_knowledge_graph.json",
    ".codex/",
)

PACKAGE_IMPORT_RE = re.compile(r"^(@[^/]+/[^/]+|@[^/]+|[^./][^/]*)")
IMPORT_RE = re.compile(r"import\s+(?:type\s+)?(?P<bindings>.+?)\s+from\s+[\"\'](?P<spec>[^\"\']+)[\"\']", re.S)
EXPORT_RE = re.compile(
    r"export\s+(?:default\s+)?(?:const|function|class|interface|type|enum)\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)"
)
TOP_LEVEL_CONST_RE = re.compile(r"^(?:export\s+)?(?:const|let|var)\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*=", re.M)
ENV_PROCESS_RE = re.compile(r"process\.env\.([A-Z0-9_]+)")
ENV_PY_RE = re.compile(r"os\.environ(?:\.get)?\(\s*[\"\']([^\"\']+)[\"\']")

FILE_RELATION_HINTS = {
    "src/studio/cli.py": "Python CLI entrypoint",
    "build_assets.py": "Direct asset CLI wrapper",
    "src/studio/generators/topic_library.py": "Storyboard compiler and manifest builder",
    "src/studio/generators/metadata.py": "Metadata generator",
    "src/studio/render/render_single.py": "Single video render orchestration",
    "src/studio/render/render_all.py": "Batch render orchestration",
    "src/studio/utils/validate.py": "Schema-backed validation",
    "src/studio/assets/toolchain.py": "SVG asset build pipeline",
    "src/studio/assets/transpiler.py": "SVG to React transpiler",
    "scripts/open_knowledge_graph_preview.ps1": "Chrome Dev preview launcher",
    "scripts/serve_knowledge_graph_preview.py": "Local static graph preview server",
    "engine/src/Root.tsx": "Remotion root composition loader",
    "engine/src/scenes/SceneFactory.tsx": "Scene visual selector",
    "engine/src/scenes/GenericScene.tsx": "Generic scene shell",
    "engine/src/generated/videoManifest.js": "Runtime payload locator",
    "tools/knowledge-graph-viewer/index.html": "Standalone graph dashboard shell",
    "tools/knowledge-graph-viewer/app.js": "Standalone graph dashboard logic",
}

NODE_TYPE_LABELS = {
    "collection": "Collection",
    "environment_variable": "Environment Variable",
    "file": "File",
    "node_dependency": "Node Dependency",
    "python_class": "Python Class",
    "python_dependency": "Python Dependency",
    "python_function": "Python Function",
    "python_variable": "Python Variable",
    "ts_symbol": "TS/JS Symbol",
    "ts_variable": "TS/JS Variable",
    "unknown": "Unknown",
}

RELATION_LABELS = {
    "calls": "Calls",
    "calls_into": "Calls Into",
    "defines": "Defines",
    "delegates_to": "Delegates To",
    "depends_on": "Depends On",
    "dispatches_to": "Dispatches To",
    "drives": "Drives",
    "imports": "Imports",
    "iterates_over": "Iterates Over",
    "loads": "Loads",
    "references": "References",
    "uses_component": "Uses Component",
    "uses_env": "Uses Environment Variable",
    "uses_runtime": "Uses Runtime",
    "validates_with": "Validates With",
    "writes": "Writes",
}


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    relation: str
    note: str | None = None

    def as_dict(self) -> dict:
        payload = {
            "source": self.source,
            "target": self.target,
            "relation": self.relation,
        }
        if self.note:
            payload["note"] = self.note
        return payload


class GraphBuilder:
    def __init__(self) -> None:
        self.nodes: dict[str, dict] = {}
        self.edges: list[Edge] = []
        self.edge_keys: set[tuple[str, str, str, str]] = set()

    def add_node(self, node_id: str, **payload: object) -> None:
        current = self.nodes.get(node_id, {"id": node_id})
        current.update(payload)
        self.nodes[node_id] = current

    def add_edge(self, source: str, target: str, relation: str, note: str | None = None) -> None:
        if source not in self.nodes:
            self.add_node(source, type="unknown")
        if target not in self.nodes:
            self.add_node(target, type="unknown")
        key = (source, target, relation, note or "")
        if key in self.edge_keys:
            return
        self.edge_keys.add(key)
        self.edges.append(Edge(source=source, target=target, relation=relation, note=note))


def repo_rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def safe_read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def file_id(rel_path: str) -> str:
    return f"file:{rel_path}"


def symbol_id(rel_path: str, name: str, kind: str) -> str:
    return f"{kind}:{rel_path}:{name}"


def collection_id(path: str) -> str:
    return f"collection:{path}"


def env_id(name: str) -> str:
    return f"env:{name}"


def dependency_id(ecosystem: str, name: str) -> str:
    return f"dependency:{ecosystem}:{name}"


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-files", "--cached", "--others", "--exclude-standard"],
        check=True,
        capture_output=True,
        text=True,
    )
    files: list[Path] = []
    for line in result.stdout.splitlines():
        rel = line.strip().replace("\\", "/")
        if not rel or any(rel.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
            continue
        candidate = REPO_ROOT / rel
        if candidate.exists() and candidate.is_file():
            files.append(candidate)
    return sorted(files)


def build_python_module_map(py_files: Iterable[Path]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for path in py_files:
        rel = Path(repo_rel(path))
        parts = list(rel.with_suffix("").parts)
        if parts and parts[-1] == "__init__":
            parts = parts[:-1]
        if not parts:
            continue
        mapping[".".join(parts)] = rel.as_posix()
    return mapping


def resolve_python_module(current_module: str, level: int, module: str | None) -> str:
    if level <= 0:
        return module or current_module
    bits = current_module.split(".")
    if current_module.endswith(".__init__"):
        bits = bits[:-1]
    base = bits[:-level]
    if module:
        base += module.split(".")
    return ".".join(part for part in base if part)


def resolve_python_import(module_map: dict[str, str], current_module: str, node: ast.AST) -> dict[str, str]:
    resolved: dict[str, str] = {}
    if isinstance(node, ast.Import):
        for alias in node.names:
            alias_name = alias.asname or alias.name.split(".")[0]
            if alias.name in module_map:
                resolved[alias_name] = file_id(module_map[alias.name])
            else:
                resolved[alias_name] = dependency_id("python", alias.name.split(".")[0])
    elif isinstance(node, ast.ImportFrom):
        base_module = resolve_python_module(current_module, node.level, node.module)
        for alias in node.names:
            alias_name = alias.asname or alias.name
            candidate_module = f"{base_module}.{alias.name}" if alias.name != "*" else base_module
            if candidate_module in module_map:
                resolved[alias_name] = file_id(module_map[candidate_module])
            elif base_module in module_map:
                resolved[alias_name] = file_id(module_map[base_module])
            elif base_module:
                resolved[alias_name] = dependency_id("python", base_module.split(".")[0])
    return resolved


def python_symbol_metadata(path: str, name: str, kind: str, line: int | None = None) -> dict:
    return {
        "type": kind,
        "path": path,
        "name": name,
        "line": line,
        "label": name,
    }


def extract_python_symbols(tree: ast.AST, rel_path: str, graph: GraphBuilder) -> tuple[dict[str, str], dict[str, ast.AST], dict[str, str]]:
    defs: dict[str, str] = {}
    def_nodes: dict[str, ast.AST] = {}
    top_level_vars: dict[str, str] = {}
    for node in getattr(tree, "body", []):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            node_id = symbol_id(rel_path, node.name, "pyfunc")
            graph.add_node(node_id, **python_symbol_metadata(rel_path, node.name, "python_function", node.lineno))
            graph.add_edge(file_id(rel_path), node_id, "defines")
            defs[node.name] = node_id
            def_nodes[node.name] = node
        elif isinstance(node, ast.ClassDef):
            node_id = symbol_id(rel_path, node.name, "pyclass")
            graph.add_node(node_id, **python_symbol_metadata(rel_path, node.name, "python_class", node.lineno))
            graph.add_edge(file_id(rel_path), node_id, "defines")
            defs[node.name] = node_id
            def_nodes[node.name] = node
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets: list[ast.expr] = list(node.targets) if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name):
                    node_id = symbol_id(rel_path, target.id, "pyvar")
                    graph.add_node(
                        node_id,
                        type="python_variable",
                        path=rel_path,
                        name=target.id,
                        label=target.id,
                        line=getattr(node, "lineno", None),
                    )
                    graph.add_edge(file_id(rel_path), node_id, "defines")
                    top_level_vars[target.id] = node_id
    return defs, def_nodes, top_level_vars


def call_name(node: ast.Call) -> tuple[str | None, str | None]:
    if isinstance(node.func, ast.Name):
        return node.func.id, None
    if isinstance(node.func, ast.Attribute):
        if isinstance(node.func.value, ast.Name):
            return node.func.attr, node.func.value.id
        return node.func.attr, None
    return None, None


def analyze_python_file(path: Path, module_map: dict[str, str], graph: GraphBuilder) -> None:
    rel_path = repo_rel(path)
    source = safe_read_text(path)
    graph.add_node(
        file_id(rel_path),
        type="file",
        path=rel_path,
        language="python",
        extension=path.suffix,
        size=path.stat().st_size,
        hint=FILE_RELATION_HINTS.get(rel_path),
        label=rel_path,
    )
    tree = ast.parse(source)
    current_module = rel_path.replace("/", ".").replace(".py", "")
    imported_symbols: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports = resolve_python_import(module_map, current_module, node)
            for alias_name, target in imports.items():
                imported_symbols[alias_name] = target
                graph.add_edge(file_id(rel_path), target, "imports", note=alias_name)
    local_defs, def_nodes, top_level_vars = extract_python_symbols(tree, rel_path, graph)
    for def_name, def_node in def_nodes.items():
        caller_id = local_defs[def_name]
        for call in [n for n in ast.walk(def_node) if isinstance(n, ast.Call)]:
            name, base = call_name(call)
            if not name:
                continue
            if name in local_defs:
                graph.add_edge(caller_id, local_defs[name], "calls")
            elif base and base in imported_symbols:
                graph.add_edge(caller_id, imported_symbols[base], "calls_into", note=name)
            elif name in imported_symbols:
                graph.add_edge(caller_id, imported_symbols[name], "calls_into")
        for name_node in [n for n in ast.walk(def_node) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)]:
            if name_node.id in top_level_vars:
                graph.add_edge(caller_id, top_level_vars[name_node.id], "references")
    env_names = sorted(set(ENV_PY_RE.findall(source)))
    for env_name in env_names:
        graph.add_node(env_id(env_name), type="environment_variable", name=env_name, label=env_name)
        graph.add_edge(file_id(rel_path), env_id(env_name), "uses_env")

def resolve_ts_import(current_rel: str, spec: str) -> str | None:
    current_path = REPO_ROOT / current_rel
    if spec.startswith("@/"):
        base = REPO_ROOT / "engine" / "src" / spec[2:]
    elif spec.startswith("."):
        base = (current_path.parent / spec).resolve()
    else:
        match = PACKAGE_IMPORT_RE.match(spec)
        if not match:
            return None
        return dependency_id("node", match.group(1))

    candidates: list[Path] = []
    if base.suffix in TS_EXTENSIONS:
        candidates.append(base)
    else:
        for ext in TS_EXTENSIONS:
            candidates.append(base.with_suffix(ext))
        for ext in TS_EXTENSIONS:
            candidates.append(base / f"index{ext}")
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return file_id(repo_rel(candidate))
    return None


def extract_ts_import_bindings(binding_text: str) -> list[str]:
    cleaned = " ".join(binding_text.replace("\n", " ").split())
    names: list[str] = []
    if "{" in cleaned and "}" in cleaned:
        before, after = cleaned.split("{", 1)
        default_part = before.strip().strip(",")
        if default_part:
            names.append(default_part)
        named_part, _tail = after.split("}", 1)
        for chunk in named_part.split(","):
            chunk = chunk.strip()
            if not chunk:
                continue
            names.append(chunk.split(" as ")[-1].strip())
        return [name for name in names if name and name != "type"]

    for chunk in cleaned.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if chunk.startswith("* as "):
            names.append(chunk[5:].strip())
        else:
            names.append(chunk)
    return [name for name in names if name and name != "type"]


def analyze_ts_file(path: Path, graph: GraphBuilder) -> None:
    rel_path = repo_rel(path)
    source = safe_read_text(path)
    language = "typescript" if path.suffix in {".ts", ".tsx"} else "javascript"
    graph.add_node(
        file_id(rel_path),
        type="file",
        path=rel_path,
        language=language,
        extension=path.suffix,
        size=path.stat().st_size,
        hint=FILE_RELATION_HINTS.get(rel_path),
        label=rel_path,
    )
    imported_symbols: dict[str, str] = {}
    for match in IMPORT_RE.finditer(source):
        spec = match.group("spec")
        target = resolve_ts_import(rel_path, spec)
        if not target:
            continue
        graph.add_edge(file_id(rel_path), target, "imports", note=spec)
        for binding in extract_ts_import_bindings(match.group("bindings")):
            imported_symbols[binding] = target

    exported_names = {match.group("name") for match in EXPORT_RE.finditer(source)}
    for name in sorted(exported_names):
        node_id = symbol_id(rel_path, name, "tssymbol")
        graph.add_node(node_id, type="ts_symbol", path=rel_path, name=name, label=name)
        graph.add_edge(file_id(rel_path), node_id, "defines")

    top_level_vars = {match.group("name") for match in TOP_LEVEL_CONST_RE.finditer(source)}
    for name in sorted(top_level_vars):
        node_id = symbol_id(rel_path, name, "tsvar")
        graph.add_node(node_id, type="ts_variable", path=rel_path, name=name, label=name)
        graph.add_edge(file_id(rel_path), node_id, "defines")
        if len(re.findall(rf"\b{re.escape(name)}\b", source)) > 1:
            graph.add_edge(file_id(rel_path), node_id, "references")

    for name, target in imported_symbols.items():
        if re.search(rf"\b{re.escape(name)}\s*\(", source):
            graph.add_edge(file_id(rel_path), target, "calls_into", note=name)
        if re.search(rf"<{re.escape(name)}\b", source):
            graph.add_edge(file_id(rel_path), target, "uses_component", note=name)

    env_names = sorted(set(ENV_PROCESS_RE.findall(source)))
    for env_name in env_names:
        graph.add_node(env_id(env_name), type="environment_variable", name=env_name, label=env_name)
        graph.add_edge(file_id(rel_path), env_id(env_name), "uses_env")


def add_file_inventory(graph: GraphBuilder, files: list[Path]) -> Counter:
    counter: Counter = Counter()
    for path in files:
        rel_path = repo_rel(path)
        top_level = rel_path.split("/", 1)[0]
        counter[top_level] += 1
        graph.add_node(
            file_id(rel_path),
            type="file",
            path=rel_path,
            extension=path.suffix,
            size=path.stat().st_size,
            top_level=top_level,
            hint=FILE_RELATION_HINTS.get(rel_path),
            label=rel_path,
        )
    return counter


def parse_requirements(graph: GraphBuilder) -> list[str]:
    path = REPO_ROOT / "requirements.txt"
    deps: list[str] = []
    if not path.exists():
        return deps
    graph.add_node(file_id("requirements.txt"), type="file", path="requirements.txt", label="requirements.txt")
    for line in safe_read_text(path).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        name = re.split(r"[<>=!~ ]", stripped, maxsplit=1)[0]
        deps.append(name)
        dep_id = dependency_id("python", name)
        graph.add_node(dep_id, type="python_dependency", name=name, label=name)
        graph.add_edge(file_id("requirements.txt"), dep_id, "depends_on")
    return sorted(deps)


def parse_package_json(graph: GraphBuilder) -> dict[str, list[str]]:
    path = REPO_ROOT / "engine" / "package.json"
    result = {"dependencies": [], "devDependencies": []}
    if not path.exists():
        return result
    graph.add_node(file_id("engine/package.json"), type="file", path="engine/package.json", label="engine/package.json")
    payload = json.loads(safe_read_text(path))
    for group in ("dependencies", "devDependencies"):
        names = sorted(payload.get(group, {}).keys())
        result[group] = names
        for name in names:
            dep_id = dependency_id("node", name)
            graph.add_node(dep_id, type="node_dependency", name=name, label=name, dependency_group=group)
            graph.add_edge(file_id("engine/package.json"), dep_id, "depends_on", note=group)
    return result


def add_collection_nodes(graph: GraphBuilder) -> dict[str, int]:
    collections = {
        "data/storyboards": len(list((REPO_ROOT / "data" / "storyboards").glob("*.json"))),
        "data/videos": len(list((REPO_ROOT / "data" / "videos").glob("*.json"))),
        "data/demos": len(list((REPO_ROOT / "data" / "demos").glob("*.json"))),
        "data/assets/raw": len(list((REPO_ROOT / "data" / "assets" / "raw").glob("*.svg"))),
        "data/assets/processed": len(list((REPO_ROOT / "data" / "assets" / "processed").glob("*.svg"))),
        "output": len(list((REPO_ROOT / "output").glob("*.mp4"))),
        "output/metadata": len(list((REPO_ROOT / "output" / "metadata").glob("*.json"))),
        "output/segments": len(list((REPO_ROOT / "output" / "segments").glob("**/*.mp4"))),
    }
    for path, count in collections.items():
        graph.add_node(collection_id(path), type="collection", path=path, count=count, label=path)
    return collections


def add_curated_relationships(graph: GraphBuilder) -> None:
    curated_edges = [
        (file_id("build_assets.py"), file_id("src/studio/assets/toolchain.py"), "delegates_to", "cli"),
        (file_id("src/studio/cli.py"), file_id("src/studio/generators/topic_library.py"), "dispatches_to", "build"),
        (file_id("src/studio/cli.py"), file_id("src/studio/render/render_single.py"), "dispatches_to", "render single"),
        (file_id("src/studio/cli.py"), file_id("src/studio/render/render_all.py"), "dispatches_to", "render all"),
        (file_id("src/studio/cli.py"), file_id("src/studio/utils/validate.py"), "dispatches_to", "validate"),
        (file_id("src/studio/cli.py"), file_id("src/studio/generators/metadata.py"), "dispatches_to", "metadata"),
        (file_id("src/studio/cli.py"), file_id("src/studio/assets/toolchain.py"), "dispatches_to", "assets build"),
        (file_id("src/studio/generators/topic_library.py"), collection_id("data/storyboards"), "writes", "storyboards"),
        (file_id("src/studio/generators/topic_library.py"), collection_id("data/videos"), "writes", "compiled payloads"),
        (file_id("src/studio/generators/topic_library.py"), collection_id("data/demos"), "writes", "demo payloads"),
        (file_id("src/studio/generators/topic_library.py"), file_id("data/video_manifest.json"), "writes"),
        (file_id("src/studio/generators/topic_library.py"), file_id("data/demo_manifest.json"), "writes"),
        (file_id("src/studio/generators/topic_library.py"), file_id("data/asset_library.json"), "writes"),
        (file_id("src/studio/generators/topic_library.py"), file_id("engine/src/generated/videoManifest.js"), "writes"),
        (file_id("src/studio/generators/metadata.py"), collection_id("output/metadata"), "writes"),
        (file_id("src/studio/utils/validate.py"), file_id("data/storyboard.schema.json"), "validates_with"),
        (file_id("src/studio/utils/validate.py"), file_id("data/video.schema.json"), "validates_with"),
        (file_id("src/studio/utils/validate.py"), file_id("data/production-manifest.schema.json"), "validates_with"),
        (file_id("src/studio/utils/validate.py"), file_id("data/demo-manifest.schema.json"), "validates_with"),
        (file_id("src/studio/assets/toolchain.py"), collection_id("data/assets/raw"), "writes", "raw SVGs"),
        (file_id("src/studio/assets/toolchain.py"), collection_id("data/assets/processed"), "writes", "processed SVGs"),
        (file_id("src/studio/assets/toolchain.py"), file_id("src/studio/assets/transpiler.py"), "calls_into"),
        (file_id("src/studio/assets/transpiler.py"), file_id("engine/src/components/generated/index.ts"), "writes"),
        (file_id("src/studio/render/render_single.py"), collection_id("output/segments"), "writes", "segment mp4s"),
        (file_id("src/studio/render/render_single.py"), collection_id("output"), "writes", "final stitched mp4"),
        (file_id("src/studio/render/render_single.py"), file_id("engine/src/Root.tsx"), "drives", "segment render via env"),
        (file_id("src/studio/render/render_single.py"), file_id("engine/remotion.config.js"), "uses_runtime"),
        (file_id("src/studio/render/render_all.py"), file_id("src/studio/render/render_single.py"), "iterates_over"),
        (file_id("engine/src/Root.tsx"), file_id("engine/src/generated/videoManifest.js"), "loads"),
        (file_id("engine/src/Root.tsx"), file_id("engine/src/scenes/SceneBlock.tsx"), "uses_component"),
        (file_id("engine/src/scenes/SceneBlock.tsx"), file_id("engine/src/scenes/GenericScene.tsx"), "uses_component"),
        (file_id("engine/src/scenes/GenericScene.tsx"), file_id("engine/src/scenes/SceneFactory.tsx"), "uses_component"),
        (file_id("engine/src/scenes/GenericScene.tsx"), file_id("engine/src/core/Camera.tsx"), "uses_component"),
        (file_id("engine/src/scenes/GenericScene.tsx"), file_id("engine/src/core/MotionLayer.tsx"), "uses_component"),
        (file_id("engine/src/scenes/GenericScene.tsx"), file_id("engine/src/overlays/CinematicText.tsx"), "uses_component"),
        (file_id("scripts/open_knowledge_graph_preview.ps1"), file_id("scripts/generate_repo_knowledge_graph.py"), "calls_into"),
        (file_id("scripts/open_knowledge_graph_preview.ps1"), file_id("scripts/serve_knowledge_graph_preview.py"), "calls_into"),
        (file_id("tools/knowledge-graph-viewer/index.html"), file_id("tools/knowledge-graph-viewer/app.js"), "loads"),
        (file_id("tools/knowledge-graph-viewer/index.html"), file_id("tools/knowledge-graph-viewer/app.css"), "loads"),
    ]
    for source, target, relation, *note in curated_edges:
        graph.add_edge(source, target, relation, note[0] if note else None)


def is_python_file(node: dict) -> bool:
    return node.get("type") == "file" and node.get("language") == "python"


def is_engine_file(node: dict) -> bool:
    path = node.get("path", "")
    return node.get("type") == "file" and (path.startswith("engine/") or path.startswith("tools/knowledge-graph-viewer/"))

def node_type_counts(nodes: list[dict]) -> dict[str, int]:
    counts: Counter = Counter(node.get("type", "unknown") for node in nodes)
    return dict(sorted(counts.items()))


def relation_counts(edges: list[dict]) -> dict[str, int]:
    counts: Counter = Counter(edge["relation"] for edge in edges)
    return dict(sorted(counts.items()))


def enrich_node(node: dict) -> dict:
    payload = dict(node)
    payload.setdefault("label", payload.get("path") or payload.get("name") or payload["id"])
    payload.setdefault("typeLabel", NODE_TYPE_LABELS.get(payload.get("type", "unknown"), payload.get("type", "Unknown")))
    return payload


def build_dataset(
    graph: GraphBuilder,
    *,
    dataset_id: str,
    title: str,
    description: str,
    node_filter: Callable[[dict], bool],
    relation_filter: Callable[[dict], bool],
) -> dict:
    allowed_node_ids = {node_id for node_id, node in graph.nodes.items() if node_filter(node)}
    selected_edges = []
    touched_node_ids: set[str] = set()
    for edge in graph.edges:
        edge_dict = edge.as_dict()
        if not relation_filter(edge_dict):
            continue
        if edge.source not in allowed_node_ids or edge.target not in allowed_node_ids:
            continue
        selected_edges.append(edge_dict)
        touched_node_ids.add(edge.source)
        touched_node_ids.add(edge.target)
    selected_nodes = [
        enrich_node(graph.nodes[node_id])
        for node_id in sorted(touched_node_ids or allowed_node_ids)
        if node_id in graph.nodes and node_id in allowed_node_ids
    ]
    selected_edges.sort(key=lambda item: (item["source"], item["relation"], item["target"], item.get("note", "")))
    return {
        "id": dataset_id,
        "title": title,
        "description": description,
        "summary": {
            "nodeCount": len(selected_nodes),
            "edgeCount": len(selected_edges),
            "nodeTypeCounts": node_type_counts(selected_nodes),
            "relationCounts": relation_counts(selected_edges),
        },
        "nodes": selected_nodes,
        "edges": selected_edges,
    }


def build_full_graph(graph: GraphBuilder) -> dict:
    nodes = [enrich_node(node) for node in sorted(graph.nodes.values(), key=lambda item: item["id"])]
    edges = [
        edge.as_dict()
        for edge in sorted(graph.edges, key=lambda item: (item.source, item.relation, item.target, item.note or ""))
    ]
    return {
        "id": "overview",
        "title": "Overview",
        "description": "Full repository graph with all known nodes and relationships.",
        "summary": {
            "nodeCount": len(nodes),
            "edgeCount": len(edges),
            "nodeTypeCounts": node_type_counts(nodes),
            "relationCounts": relation_counts(edges),
        },
        "nodes": nodes,
        "edges": edges,
    }


def build_pipeline_dataset(graph: GraphBuilder) -> dict:
    pipeline_files = {
        "data/raw/Topics.txt",
        "data/video_manifest.json",
        "data/demo_manifest.json",
        "data/storyboard.schema.json",
        "data/video.schema.json",
        "data/production-manifest.schema.json",
        "data/demo-manifest.schema.json",
        "src/studio/cli.py",
        "src/studio/generators/topic_library.py",
        "src/studio/generators/metadata.py",
        "src/studio/utils/validate.py",
        "src/studio/render/render_single.py",
        "src/studio/assets/toolchain.py",
        "src/studio/assets/transpiler.py",
        "engine/src/generated/videoManifest.js",
        "engine/src/Root.tsx",
    }
    relation_names = {
        "writes",
        "validates_with",
        "dispatches_to",
        "delegates_to",
        "drives",
        "loads",
        "uses_runtime",
        "imports",
        "iterates_over",
    }

    def node_filter(node: dict) -> bool:
        if node.get("type") == "collection":
            return True
        if node.get("type") != "file":
            return False
        path = node.get("path", "")
        return path.startswith("data/") or path.startswith("output/") or path in pipeline_files

    return build_dataset(
        graph,
        dataset_id="pipeline",
        title="Pipeline",
        description="Topics, storyboards, payloads, manifests, assets, and render outputs.",
        node_filter=node_filter,
        relation_filter=lambda edge: edge["relation"] in relation_names,
    )


def build_graph_suite(graph: GraphBuilder) -> dict[str, dict]:
    full_graph = build_full_graph(graph)
    return {
        "full-graph.json": full_graph,
        "file-dependency-graph.json": build_dataset(
            graph,
            dataset_id="files",
            title="Files",
            description="File imports, writes, dispatches, validation, and runtime links.",
            node_filter=lambda node: node.get("type") in {"file", "collection"},
            relation_filter=lambda edge: edge["relation"] in {
                "imports",
                "writes",
                "dispatches_to",
                "delegates_to",
                "drives",
                "loads",
                "uses_runtime",
                "iterates_over",
                "validates_with",
            },
        ),
        "python-call-graph.json": build_dataset(
            graph,
            dataset_id="python-calls",
            title="Python Calls",
            description="Python files, functions, classes, variables, imports, and call edges.",
            node_filter=lambda node: (
                node.get("type") in {"python_function", "python_class", "python_variable", "python_dependency", "environment_variable"}
                or is_python_file(node)
            ),
            relation_filter=lambda edge: edge["relation"] in {"defines", "imports", "calls", "calls_into", "references", "uses_env"},
        ),
        "engine-symbol-graph.json": build_dataset(
            graph,
            dataset_id="engine",
            title="Engine",
            description="TS/JS files, exported symbols, top-level variables, component use, and imports.",
            node_filter=lambda node: (
                node.get("type") in {"ts_symbol", "ts_variable", "node_dependency", "environment_variable"}
                or is_engine_file(node)
            ),
            relation_filter=lambda edge: edge["relation"] in {"defines", "imports", "calls_into", "uses_component", "references", "uses_env", "depends_on"},
        ),
        "data-pipeline-graph.json": build_pipeline_dataset(graph),
        "dependency-env-graph.json": build_dataset(
            graph,
            dataset_id="deps-env",
            title="Deps/Env",
            description="External packages, environment variables, and the files that use them.",
            node_filter=lambda node: node.get("type") in {"file", "node_dependency", "python_dependency", "environment_variable"},
            relation_filter=lambda edge: edge["relation"] in {"depends_on", "imports", "calls_into", "uses_env"},
        ),
    }


def most_connected_files(graph: GraphBuilder, limit: int = 15) -> list[dict]:
    scores: defaultdict[str, int] = defaultdict(int)
    for edge in graph.edges:
        if edge.source.startswith("file:"):
            scores[edge.source] += 1
        if edge.target.startswith("file:"):
            scores[edge.target] += 1
    ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))[:limit]
    return [
        {
            "path": graph.nodes[node_id].get("path"),
            "score": score,
            "hint": graph.nodes[node_id].get("hint"),
        }
        for node_id, score in ranked
    ]


def top_edges(graph: GraphBuilder, relations: set[str], limit: int = 25) -> list[dict]:
    rows: list[dict] = []
    for edge in graph.edges:
        if edge.relation not in relations:
            continue
        rows.append(
            {
                "source": graph.nodes[edge.source].get("path", graph.nodes[edge.source].get("name", edge.source)),
                "target": graph.nodes[edge.target].get("path", graph.nodes[edge.target].get("name", edge.target)),
                "relation": edge.relation,
                "note": edge.note,
            }
        )
    rows.sort(key=lambda row: (row["source"], row["target"], row["relation"]))
    return rows[:limit]


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def render_markdown(graph: GraphBuilder, manifest: dict, datasets: dict[str, dict]) -> str:
    summary = manifest["summary"]
    view_rows = []
    for view in manifest["views"]:
        view_rows.append([
            view["title"],
            view["file"],
            str(view["summary"]["nodeCount"]),
            str(view["summary"]["edgeCount"]),
            view["description"],
        ])

    connected_rows = [
        [row.get("path", ""), str(row.get("score", 0)), row.get("hint", "") or ""]
        for row in most_connected_files(graph)
    ]
    dispatch_rows = [
        [row["source"], row["relation"], row["target"], row.get("note", "") or ""]
        for row in top_edges(graph, {"dispatches_to", "delegates_to", "writes", "loads", "drives", "validates_with"})
    ]

    lines = [
        "# Repository Knowledge Graph",
        "",
        "This document describes the repository graph suite generated from the codebase. The graph data is written to `data/knowledge-graph/` and powers the standalone dashboard in `tools/knowledge-graph-viewer/`.",
        "",
        "## Generated Artifacts",
        "",
        f"- Full graph JSON: `data/knowledge-graph/full-graph.json`",
        f"- File dependency graph: `data/knowledge-graph/file-dependency-graph.json`",
        f"- Python call graph: `data/knowledge-graph/python-call-graph.json`",
        f"- Engine symbol graph: `data/knowledge-graph/engine-symbol-graph.json`",
        f"- Data pipeline graph: `data/knowledge-graph/data-pipeline-graph.json`",
        f"- Dependency and env graph: `data/knowledge-graph/dependency-env-graph.json`",
        f"- Graph manifest: `data/knowledge-graph/manifest.json`",
        f"- Backward-compatible full graph: `data/repository_knowledge_graph.json`",
        "",
        "## Summary",
        "",
        f"- Generated at: `{manifest['generatedAt']}`",
        f"- Tracked files: `{summary['trackedFileCount']}`",
        f"- Nodes: `{summary['nodeCount']}`",
        f"- Edges: `{summary['edgeCount']}`",
        "",
        "## Dashboard",
        "",
        "Launch the dashboard in Google Chrome Dev with DevTools open:",
        "",
        "```powershell",
        "powershell -ExecutionPolicy Bypass -File .\\scripts\\open_knowledge_graph_preview.ps1",
        "```",
        "",
        "The launcher regenerates all graph data, starts the static preview server on `http://127.0.0.1:4173`, resolves Chrome Dev from Windows App Paths, and opens `tools/knowledge-graph-viewer/` with a dedicated preview profile.",
        "",
        "## Views",
        "",
        markdown_table(["View", "File", "Nodes", "Edges", "Description"], view_rows),
        "",
        "## Navigation Notes",
        "",
        "- `Overview`: complete repository graph with all discovered nodes and relationships.",
        "- `Files`: file-to-file imports, writes, runtime links, and dispatches.",
        "- `Python Calls`: Python modules, functions, classes, constants, imports, and call edges.",
        "- `Engine`: TypeScript/JavaScript files, exports, variables, component usage, and imports.",
        "- `Pipeline`: topics, storyboards, compiled payloads, manifests, assets, and outputs.",
        "- `Deps/Env`: Python packages, Node packages, environment variables, and the files that use them.",
        "",
        "Use the dashboard search, node-type filters, relation filters, and inspector panel to move between files, symbols, dependencies, and outputs.",
        "",
        "## Highest-Connectivity Files",
        "",
        markdown_table(["Path", "Connections", "Hint"], connected_rows or [["n/a", "0", ""]]),
        "",
        "## Representative Relationships",
        "",
        markdown_table(["Source", "Relation", "Target", "Note"], dispatch_rows or [["n/a", "n/a", "n/a", ""]]),
        "",
        "## Refresh Workflow",
        "",
        "```powershell",
        "python .\\scripts\\generate_repo_knowledge_graph.py",
        "powershell -ExecutionPolicy Bypass -File .\\scripts\\open_knowledge_graph_preview.ps1",
        "```",
        "",
        "Regenerate the graph suite after code or data changes so the dashboard reflects the current repository state.",
    ]
    return "\n".join(lines) + "\n"


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def main() -> None:
    graph = GraphBuilder()
    files = tracked_files()
    add_file_inventory(graph, files)
    module_map = build_python_module_map(files)

    for path in files:
        if path.suffix == ".py":
            analyze_python_file(path, module_map, graph)
        elif path.suffix in TS_EXTENSIONS:
            analyze_ts_file(path, graph)

    parse_requirements(graph)
    parse_package_json(graph)
    add_collection_nodes(graph)
    add_curated_relationships(graph)

    graph_suite = build_graph_suite(graph)
    manifest = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "root": ".",
        "summary": {
            "trackedFileCount": len(files),
            "nodeCount": len(graph.nodes),
            "edgeCount": len(graph.edges),
        },
        "views": [
            {
                "id": dataset["id"],
                "title": dataset["title"],
                "description": dataset["description"],
                "file": filename,
                "summary": dataset["summary"],
            }
            for filename, dataset in graph_suite.items()
        ],
        "nodeTypeLabels": NODE_TYPE_LABELS,
        "relationTypeLabels": RELATION_LABELS,
    }

    GRAPH_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for filename, dataset in graph_suite.items():
        write_json(GRAPH_OUTPUT_DIR / filename, dataset)

    write_json(GRAPH_OUTPUT_DIR / "manifest.json", manifest)
    write_json(BACKWARD_COMPAT_OUTPUT, graph_suite["full-graph.json"])
    MARKDOWN_OUTPUT.write_text(render_markdown(graph, manifest, graph_suite), encoding="utf-8")

    print(f"Wrote full graph: {GRAPH_OUTPUT_DIR / 'full-graph.json'}")
    print(f"Wrote file dependency graph: {GRAPH_OUTPUT_DIR / 'file-dependency-graph.json'}")
    print(f"Wrote python call graph: {GRAPH_OUTPUT_DIR / 'python-call-graph.json'}")
    print(f"Wrote engine symbol graph: {GRAPH_OUTPUT_DIR / 'engine-symbol-graph.json'}")
    print(f"Wrote data pipeline graph: {GRAPH_OUTPUT_DIR / 'data-pipeline-graph.json'}")
    print(f"Wrote dependency/env graph: {GRAPH_OUTPUT_DIR / 'dependency-env-graph.json'}")
    print(f"Wrote manifest: {GRAPH_OUTPUT_DIR / 'manifest.json'}")
    print(f"Wrote backward-compatible graph: {BACKWARD_COMPAT_OUTPUT}")
    print(f"Wrote markdown: {MARKDOWN_OUTPUT}")
    print(f"Tracked files: {len(files)}")
    print(f"Graph nodes: {len(graph.nodes)}")
    print(f"Graph edges: {len(graph.edges)}")


if __name__ == "__main__":
    main()




