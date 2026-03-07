"""
FILE: src/studio/cli.py
PURPOSE: The Master CLI entrypoint mapping the unified environment cleanly to sub-scripts.
"""
import argparse
import subprocess
import sys
from pathlib import Path
from src.studio.config import SRC_DIR

def run_script(module_name: str, args: list[str]) -> None:
    # Instead of running filepath scripts, we now run proper Python modules
    cmd = [sys.executable, "-m", f"src.studio.{module_name}"] + args
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\n[Studio System] Interrupted by user.")
        sys.exit(1)

def main() -> None:
    parser = argparse.ArgumentParser(description="Studio_System1 Unified CLI")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # 1. Build
    parser_build = subparsers.add_parser("build", help="Build the 500-video JSON library")
    parser_build.add_argument("--materialize", action="store_true", help="Write all JSON payloads to disk")
    parser_build.add_argument("--force-storyboards", action="store_true", help="Regenerate storyboard skeletons even when they already exist")

    # 2. Render
    parser_render = subparsers.add_parser("render", help="Render video(s) to MP4")
    parser_render.add_argument("video_id", nargs="?", help="Render single video (e.g., video_001)")
    parser_render.add_argument("--all", action="store_true", help="Render all videos with resume support")
    parser_render.add_argument("--limit", type=int, help="Render only first N videos")
    parser_render.add_argument("--start-from", type=str, help="Resume rendering from specific video ID")
    parser_render.add_argument("--force", action="store_true", help="Re-render even if the output file exists")
    parser_render.add_argument("--crf", type=int, default=20, help="Output quality (default 20)")

    # 3. Clean
    parser_clean = subparsers.add_parser("clean", help="Clean output and temporary folders")
    parser_clean.add_argument("--output-only", action="store_true", help="Only clean output/")
    parser_clean.add_argument("--tmp-only", action="store_true", help="Only clean engine/tmp/")

    # 4. Thumbnails
    parser_thumb = subparsers.add_parser("thumbnail", help="Export frame thumbnails")
    parser_thumb.add_argument("video_id", nargs="?", help="Single video ID to export")
    parser_thumb.add_argument("--frame", type=int, default=150, help="Frame to capture (default: 150)")
    parser_thumb.add_argument("--all", action="store_true", help="Export thumbnails for all videos")
    parser_thumb.add_argument("--limit", type=int, help="Limit batch export to N videos")

    # 5. Metadata
    parser_meta = subparsers.add_parser("metadata", help="Generate YouTube metadata JSON")
    parser_meta.add_argument("video_id", nargs="?", help="Single video ID")
    parser_meta.add_argument("--all", action="store_true", help="Generate metadata for all videos")

    # 6. Validate
    parser_validate = subparsers.add_parser("validate", help="Validate the data library integrity")

    # 7. Assets Toolchain
    parser_assets = subparsers.add_parser("assets", help="Manage SVG generation and React transpilation")
    asset_subparsers = parser_assets.add_subparsers(dest="asset_command", required=True)
    parser_assets_build = asset_subparsers.add_parser("build", help="Run Inkscape optimization and SVG-to-React transpilation")
    view_group = parser_assets_build.add_mutually_exclusive_group()
    view_group.add_argument("--view", dest="open_gui", action="store_true", help="Open processed SVGs in the Inkscape GUI. This is the default.")
    view_group.add_argument("--no-view", dest="open_gui", action="store_false", help="Skip opening processed SVGs in the Inkscape GUI.")
    parser_assets_build.set_defaults(open_gui=True)
    parser_assets_build.add_argument("--no-optimize", action="store_true", help="Skip the optional SVGO pass")
    parser_assets_build.add_argument("--asset", action="append", help="Build only the named asset. Repeat for multiple assets.")

    args = parser.parse_args()

    if args.command == "build":
        cmd_args = ["--materialize"] if args.materialize else []
        if args.force_storyboards:
            cmd_args.append("--force-storyboards")
        run_script("generators.topic_library", cmd_args)

    elif args.command == "render":
        if args.all or args.limit or args.start_from or args.force:
            cmd_args = []
            if args.limit: cmd_args.extend(["--limit", str(args.limit)])
            if args.start_from: cmd_args.extend(["--start-from", args.start_from])
            if args.force: cmd_args.append("--force")
            if args.crf != 20: cmd_args.extend(["--crf", str(args.crf)])
            run_script("render.render_all", cmd_args)
        elif args.video_id:
            cmd_args = [args.video_id, "--crf", str(args.crf)]
            run_script("render.render_single", cmd_args)
        else:
            parser_render.print_help()

    elif args.command == "clean":
        cmd_args = []
        if args.output_only: cmd_args.append("--output-only")
        if args.tmp_only: cmd_args.append("--tmp-only")
        run_script("utils.clean", cmd_args)

    elif args.command == "thumbnail":
        if args.all:
            cmd_args = ["--all"]
            if args.limit: cmd_args.extend(["--limit", str(args.limit)])
            run_script("utils.export_thumbnail", cmd_args)
        elif args.video_id:
            run_script("utils.export_thumbnail", [args.video_id, "--frame", str(args.frame)])
        else:
            parser_thumb.print_help()

    elif args.command == "metadata":
        if args.all:
            run_script("generators.metadata", ["--all"])
        elif args.video_id:
            run_script("generators.metadata", ["--video-id", args.video_id])
        else:
            parser_meta.print_help()

    elif args.command == "validate":
        run_script("utils.validate", [])

    elif args.command == "assets":
        if args.asset_command == "build":
            # Direct mapping replacing the old root space build_assets.py
            cmd_args = []
            if not args.open_gui:
                cmd_args.append("--no-view")
            if args.no_optimize:
                cmd_args.append("--no-optimize")
            if args.asset:
                for asset_name in args.asset:
                    cmd_args.extend(["--asset", asset_name])
            run_script("assets.toolchain", cmd_args)

if __name__ == "__main__":
    main()
