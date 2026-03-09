"""
FILE: src/studio/cli.py
PURPOSE: Unified CLI for the multi-format programmable media studio.
"""
import argparse
import subprocess
import sys


def run_script(module_name: str, args: list[str]) -> None:
    cmd = [sys.executable, '-m', f'src.studio.{module_name}'] + args
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
    except KeyboardInterrupt:
        print('\n[Studio System] Interrupted by user.')
        sys.exit(1)



def main() -> None:
    parser = argparse.ArgumentParser(description='Studio_System1 Unified CLI')
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

    parser_build = subparsers.add_parser('build', help='Build the topic catalog, storyboards, manifests, and compiled payloads')
    parser_build.add_argument('--materialize', action='store_true', help='Write storyboards, compiled payloads, registries, and manifests to disk')
    parser_build.add_argument('--force-storyboards', action='store_true', help='Regenerate storyboard skeletons even when they already exist')
    parser_build.add_argument('--profile', action='append', help='Compile only the selected profile id. Repeat for multiple profiles.')

    parser_render = subparsers.add_parser('render', help='Render video(s) to MP4')
    parser_render.add_argument('video_id', nargs='?', help='Render single video (e.g. video_001 or demo_graphics_showcase_v2)')
    parser_render.add_argument('--all', action='store_true', help='Render all production videos with resume support')
    parser_render.add_argument('--limit', type=int, help='Render only first N videos')
    parser_render.add_argument('--start-from', type=str, help='Resume rendering from specific video ID')
    parser_render.add_argument('--force', action='store_true', help='Re-render even if the output file exists')
    parser_render.add_argument('--crf', type=int, default=20, help='Output quality (default 20)')
    parser_render.add_argument('--profile', type=str, help='Render only the selected production profile')
    parser_render.add_argument('--all-profiles', action='store_true', help='Render every supported production profile for the selected video(s)')

    parser_clean = subparsers.add_parser('clean', help='Clean output and temporary folders')
    parser_clean.add_argument('--output-only', action='store_true', help='Only clean output/')
    parser_clean.add_argument('--tmp-only', action='store_true', help='Only clean engine/tmp/')

    parser_thumb = subparsers.add_parser('thumbnail', help='Export frame thumbnails')
    parser_thumb.add_argument('video_id', nargs='?', help='Single video ID to export')
    parser_thumb.add_argument('--frame', type=int, default=150, help='Frame to capture (default: 150)')
    parser_thumb.add_argument('--all', action='store_true', help='Export thumbnails for all production videos')
    parser_thumb.add_argument('--limit', type=int, help='Limit batch export to N videos')
    parser_thumb.add_argument('--profile', type=str, help='Profile to use for production thumbnails')
    parser_thumb.add_argument('--all-profiles', action='store_true', help='Export production thumbnails for every supported profile')

    parser_meta = subparsers.add_parser('metadata', help='Generate metadata packs')
    parser_meta.add_argument('video_id', nargs='?', help='Single video ID')
    parser_meta.add_argument('--all', action='store_true', help='Generate metadata for all production videos')

    subparsers.add_parser('validate', help='Validate the data library integrity')

    parser_assets = subparsers.add_parser('assets', help='Manage SVG generation and React transpilation')
    asset_subparsers = parser_assets.add_subparsers(dest='asset_command', required=True)
    parser_assets_build = asset_subparsers.add_parser('build', help='Run Inkscape optimization and SVG-to-React transpilation')
    view_group = parser_assets_build.add_mutually_exclusive_group()
    view_group.add_argument('--view', dest='open_gui', action='store_true', help='Open processed SVGs in the Inkscape GUI. This is the default.')
    view_group.add_argument('--no-view', dest='open_gui', action='store_false', help='Skip opening processed SVGs in the Inkscape GUI.')
    parser_assets_build.set_defaults(open_gui=True)
    parser_assets_build.add_argument('--no-optimize', action='store_true', help='Skip the optional SVGO pass')
    parser_assets_build.add_argument('--asset', action='append', help='Build only the named asset. Repeat for multiple assets.')

    # 8. Shorts Pipeline
    parser_shorts = subparsers.add_parser("shorts", help="Generate a YouTube Short from a single topic")
    shorts_group = parser_shorts.add_mutually_exclusive_group()
    shorts_group.add_argument("--topic-index", type=int, help="Topic number from Topics.txt (1-500)")
    shorts_group.add_argument("--random", action="store_true", help="Pick a random topic")
    parser_shorts.add_argument("--render", action="store_true", help="Also render the video to MP4")
    parser_shorts.add_argument("--crf", type=int, default=20, help="Output quality for render (default: 20)")

    args = parser.parse_args()

    if args.command == 'build':
        cmd_args: list[str] = []
        if args.materialize:
            cmd_args.append('--materialize')
        if args.force_storyboards:
            cmd_args.append('--force-storyboards')
        if args.profile:
            for profile_id in args.profile:
                cmd_args.extend(['--profile', profile_id])
        run_script('generators.topic_library', cmd_args)
        return

    if args.command == 'render':
        if args.all or args.limit or args.start_from or args.force:
            cmd_args = []
            if args.limit:
                cmd_args.extend(['--limit', str(args.limit)])
            if args.start_from:
                cmd_args.extend(['--start-from', args.start_from])
            if args.force:
                cmd_args.append('--force')
            if args.crf != 20:
                cmd_args.extend(['--crf', str(args.crf)])
            if args.profile:
                cmd_args.extend(['--profile', args.profile])
            if args.all_profiles:
                cmd_args.append('--all-profiles')
            run_script('render.render_all', cmd_args)
        elif args.video_id:
            cmd_args = [args.video_id, '--crf', str(args.crf)]
            if args.profile:
                cmd_args.extend(['--profile', args.profile])
            if args.all_profiles:
                cmd_args.append('--all-profiles')
            run_script('render.render_single', cmd_args)
        else:
            parser_render.print_help()
        return

    if args.command == 'clean':
        cmd_args = []
        if args.output_only:
            cmd_args.append('--output-only')
        if args.tmp_only:
            cmd_args.append('--tmp-only')
        run_script('utils.clean', cmd_args)
        return

    if args.command == 'thumbnail':
        if args.all:
            cmd_args = ['--all']
            if args.limit:
                cmd_args.extend(['--limit', str(args.limit)])
            if args.profile:
                cmd_args.extend(['--profile', args.profile])
            if args.all_profiles:
                cmd_args.append('--all-profiles')
            run_script('utils.export_thumbnail', cmd_args)
        elif args.video_id:
            cmd_args = [args.video_id, '--frame', str(args.frame)]
            if args.profile:
                cmd_args.extend(['--profile', args.profile])
            if args.all_profiles:
                cmd_args.append('--all-profiles')
            run_script('utils.export_thumbnail', cmd_args)
        else:
            parser_thumb.print_help()
        return

    if args.command == 'metadata':
        if args.all:
            run_script('generators.metadata', ['--all'])
        elif args.video_id:
            run_script('generators.metadata', ['--video-id', args.video_id])
        else:
            parser_meta.print_help()
        return

    if args.command == 'validate':
        run_script('utils.validate', [])
        return

    if args.command == 'assets' and args.asset_command == 'build':
        cmd_args = []
        if not args.open_gui:
            cmd_args.append('--no-view')
        if args.no_optimize:
            cmd_args.append('--no-optimize')
        if args.asset:
            for asset_name in args.asset:
                cmd_args.extend(['--asset', asset_name])
        run_script('assets.toolchain', cmd_args)
        return

    if args.command == "shorts":
        cmd_args = []
        if hasattr(args, 'topic_index') and args.topic_index is not None:
            cmd_args.extend(["--topic-index", str(args.topic_index)])
        if hasattr(args, 'random') and args.random:
            cmd_args.append("--random")
        if args.render:
            cmd_args.append("--render")
        if args.crf != 20:
            cmd_args.extend(["--crf", str(args.crf)])
        run_script("shorts_pipeline", cmd_args)
        return


if __name__ == '__main__':
    main()

