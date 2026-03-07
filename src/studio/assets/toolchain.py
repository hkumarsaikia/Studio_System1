import argparse
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from src.studio.assets.background_builder import build_background
from src.studio.assets.character_builder import build_character
from src.studio.assets.declarative_builder import build_declarative_prop
from src.studio.assets.props_builder import build_prop
from src.studio.assets.transpiler import transpile_to_react
from src.studio.config import (
    PROCESSED_ASSETS_DIR,
    RAW_ASSETS_DIR,
    REACT_COMPONENTS_DIR,
    ensure_directories,
)


@dataclass(frozen=True)
class AssetSpec:
    component_name: str
    builder: Callable[..., None]
    builder_kwargs: dict[str, object]

    @property
    def filename(self) -> str:
        return f"{self.component_name}.svg"


ASSET_SPECS = (
    AssetSpec(
        component_name="BackgroundCyber",
        builder=build_background,
        builder_kwargs={"palette": "cyber"},
    ),
    AssetSpec(
        component_name="BackgroundSunset",
        builder=build_background,
        builder_kwargs={"palette": "sunset"},
    ),
    AssetSpec(
        component_name="CharacterAngry",
        builder=build_character,
        builder_kwargs={
            "skin_index": 4,
            "shirt_index": 3,
            "mood": "angry",
            "hair": "long",
        },
    ),
    AssetSpec(
        component_name="CharacterGeek",
        builder=build_character,
        builder_kwargs={
            "skin_index": 1,
            "shirt_index": 0,
            "mood": "happy",
            "accessory": "glasses",
            "hair": "spiky",
        },
    ),
    AssetSpec(
        component_name="CharacterHappy",
        builder=build_character,
        builder_kwargs={
            "skin_index": 0,
            "shirt_index": 0,
            "mood": "happy",
            "hair": "none",
        },
    ),
    AssetSpec(
        component_name="CharacterSad",
        builder=build_character,
        builder_kwargs={
            "skin_index": 3,
            "shirt_index": 2,
            "mood": "sad",
            "hair": "none",
        },
    ),
    AssetSpec(
        component_name="PropDeclarativeRobot",
        builder=build_declarative_prop,
        builder_kwargs={"prop_type": "Robot"},
    ),
    AssetSpec(
        component_name="PropDeclarativeSaturn",
        builder=build_declarative_prop,
        builder_kwargs={"prop_type": "Saturn"},
    ),
    AssetSpec(
        component_name="PropServer",
        builder=build_prop,
        builder_kwargs={"prop_type": "server_rack", "accent_index": 2},
    ),
    AssetSpec(
        component_name="PropTelescope",
        builder=build_prop,
        builder_kwargs={"prop_type": "telescope", "accent_index": 1},
    ),
)


def find_inkscape() -> str:
    """Locate the Inkscape executable on Windows."""
    ink_path = shutil.which("inkscape")
    if ink_path:
        return ink_path

    fallbacks = [
        r"C:\Program Files\Inkscape\bin\inkscape.exe",
        r"C:\Program Files\Inkscape\inkscape.exe",
        r"C:\Program Files (x86)\Inkscape\bin\inkscape.exe",
        r"C:\Program Files (x86)\Inkscape\inkscape.exe",
    ]
    for path in fallbacks:
        if os.path.exists(path):
            return path

    raise RuntimeError("Inkscape executable not found. Please ensure Inkscape is installed.")


def resolve_asset_specs(only_assets: list[str] | None) -> list[AssetSpec]:
    if not only_assets:
        return list(ASSET_SPECS)

    spec_map = {spec.component_name.lower(): spec for spec in ASSET_SPECS}
    selected: list[AssetSpec] = []
    missing: list[str] = []

    for asset_name in only_assets:
        spec = spec_map.get(asset_name.lower())
        if spec is None:
            missing.append(asset_name)
            continue
        if spec not in selected:
            selected.append(spec)

    if missing:
        valid_names = ", ".join(spec.component_name for spec in ASSET_SPECS)
        missing_names = ", ".join(missing)
        raise ValueError(f"Unknown assets requested: {missing_names}. Valid asset names: {valid_names}")

    return selected


def write_generated_index(output_dir: Path) -> None:
    index_path = output_dir / "index.ts"
    exports = [f"export * from './{spec.component_name}';" for spec in ASSET_SPECS]
    index_path.write_text("\n".join(exports) + "\n", encoding="utf-8")
    print(f"[{os.path.basename(__file__)}] Wrote React export index: {index_path}")


def process_svg(input_path: Path, output_path: Path, optimize: bool = True, open_gui: bool = True) -> None:
    """
    Run an SVG through Inkscape's command line to normalize it,
    then optionally run SVGO to optimize it.
    """
    inkscape_exe = find_inkscape()

    print(f"[{os.path.basename(__file__)}] Processing {input_path.name} via Inkscape CLI...")

    cmd = [
        inkscape_exe,
        str(input_path),
        f"--export-filename={output_path}",
        "--export-plain-svg",
        "--export-text-to-path",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        error_text = result.stderr.strip() or result.stdout.strip() or "Unknown Inkscape error."
        raise RuntimeError(f"Inkscape processing failed for {input_path.name}: {error_text}")

    if optimize:
        print(f"[{os.path.basename(__file__)}] Optimizing {output_path.name} via SVGO...")
        npx_exe = shutil.which("npx") or shutil.which("npx.cmd")
        if npx_exe:
            svgo_cmd = [npx_exe, "svgo", str(output_path), "--multipass"]
            svgo_result = subprocess.run(svgo_cmd, capture_output=True, text=True)
            if svgo_result.returncode != 0:
                warning_text = svgo_result.stderr.strip() or svgo_result.stdout.strip() or "Unknown SVGO error."
                print(f"[{os.path.basename(__file__)}] Warning: SVGO skipped for {output_path.name}: {warning_text}")
        else:
            print(f"[{os.path.basename(__file__)}] Warning: npx not found, skipping SVGO optimization.")

    print(f"[{os.path.basename(__file__)}] Built processed SVG: {output_path}")

    if open_gui:
        print(f"[{os.path.basename(__file__)}] Launching Inkscape GUI for {output_path.name}...")
        subprocess.Popen([inkscape_exe, str(output_path)])


def build_assets(open_gui: bool = True, optimize: bool = True, only_assets: list[str] | None = None) -> list[str]:
    print("=" * 60)
    print(" Studio System - Asset Compilation Pipeline")
    print("=" * 60)

    ensure_directories()
    selected_specs = resolve_asset_specs(only_assets)
    raw_dir = RAW_ASSETS_DIR
    processed_dir = PROCESSED_ASSETS_DIR
    react_out_dir = REACT_COMPONENTS_DIR

    print(f"[{os.path.basename(__file__)}] Inkscape executable: {find_inkscape()}")
    print(f"[{os.path.basename(__file__)}] Target assets: {', '.join(spec.component_name for spec in selected_specs)}")

    print("\n[1/3] Generating raw SVGs via Python builders...")
    raw_outputs: list[tuple[AssetSpec, Path, Path]] = []
    for spec in selected_specs:
        raw_path = raw_dir / spec.filename
        processed_path = processed_dir / spec.filename
        spec.builder(str(raw_path), **spec.builder_kwargs)
        raw_outputs.append((spec, raw_path, processed_path))

    print("\n[2/3] Processing SVGs via Inkscape CLI...")
    for spec, raw_path, processed_path in raw_outputs:
        process_svg(raw_path, processed_path, optimize=optimize, open_gui=open_gui)

    print("\n[3/3] Transpiling SVGs to React components...")
    for spec, _, processed_path in raw_outputs:
        transpile_to_react(str(processed_path), spec.component_name, str(react_out_dir))

    write_generated_index(react_out_dir)

    print("\n[DONE] Asset pipeline complete.")
    print(f"Raw SVGs: {raw_dir}")
    print(f"Processed SVGs: {processed_dir}")
    print(f"React components: {react_out_dir}")
    return [spec.component_name for spec in selected_specs]


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Studio System Inkscape-backed asset builder")
    view_group = parser.add_mutually_exclusive_group()
    view_group.add_argument(
        "--view",
        dest="open_gui",
        action="store_true",
        help="Open each processed SVG in the Inkscape GUI after the headless export completes. This is the default.",
    )
    view_group.add_argument(
        "--no-view",
        dest="open_gui",
        action="store_false",
        help="Skip launching the Inkscape GUI after SVG generation.",
    )
    parser.set_defaults(open_gui=True)
    parser.add_argument(
        "--no-optimize",
        action="store_true",
        help="Skip the optional SVGO pass after Inkscape export.",
    )
    parser.add_argument(
        "--asset",
        action="append",
        dest="assets",
        help="Build only the named asset. Repeat the flag to build multiple assets.",
    )
    return parser


def cli(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    build_assets(open_gui=args.open_gui, optimize=not args.no_optimize, only_assets=args.assets)
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
