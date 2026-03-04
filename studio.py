"""
FILE: studio.py
PURPOSE: Unified CLI for Studio_System1 pipeline.

This CLI unifies all the separate scripts within the scripts/ directory
into a single, easy-to-use command-line interface.

USAGE EXAMPLES:
  python studio.py render video_001
  python studio.py render --all --limit 5
  python studio.py clean
  python studio.py validate
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS_DIR = ROOT / 'scripts'

def run_script(script_name: str, args: list[str]) -> None:
    cmd = [sys.executable, str(SCRIPTS_DIR / script_name)] + args
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

    args = parser.parse_args()

    if args.command == "build":
        cmd_args = ["--materialize"] if args.materialize else []
        run_script("build_topic_library.py", cmd_args)

    elif args.command == "render":
        if args.all or args.limit or args.start_from or args.force:
            cmd_args = []
            if args.limit: cmd_args.extend(["--limit", str(args.limit)])
            if args.start_from: cmd_args.extend(["--start-from", args.start_from])
            if args.force: cmd_args.append("--force")
            if args.crf != 20: cmd_args.extend(["--crf", str(args.crf)])
            run_script("render_all.py", cmd_args)
        elif args.video_id:
            cmd_args = [args.video_id, "--crf", str(args.crf)]
            run_script("render.py", cmd_args)
        else:
            parser_render.print_help()

    elif args.command == "clean":
        cmd_args = []
        if args.output_only: cmd_args.append("--output-only")
        if args.tmp_only: cmd_args.append("--tmp-only")
        run_script("clean_output.py", cmd_args)

    elif args.command == "thumbnail":
        if args.all:
            cmd_args = ["--all"]
            if args.limit: cmd_args.extend(["--limit", str(args.limit)])
            run_script("export_thumbnail.py", cmd_args)
        elif args.video_id:
            run_script("export_thumbnail.py", [args.video_id, "--frame", str(args.frame)])
        else:
            parser_thumb.print_help()

    elif args.command == "metadata":
        if args.all:
            run_script("metadata_generator.py", ["--all"])
        elif args.video_id:
            run_script("metadata_generator.py", ["--video-id", args.video_id])
        else:
            parser_meta.print_help()

    elif args.command == "validate":
        run_script("validate_library.py", [])

if __name__ == "__main__":
    main()
