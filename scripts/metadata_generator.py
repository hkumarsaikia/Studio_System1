"""
FILE: metadata_generator.py
PURPOSE: YouTube metadata generator — creates upload-ready JSON for each video.

Generates a metadata file for each video containing:
  - Title (truncated to 95 chars for YouTube)
  - Description (with timestamped structure overview)
  - Tags (category-specific + keyword-extracted)
  - Category, privacy, and language fields

The metadata files are saved to output/metadata/ and are ready to be
used with YouTube's upload API or manual upload tools.

USAGE:
  python automation/metadata_generator.py --video-id video_001
  python automation/metadata_generator.py --all
"""
import argparse
import json
from pathlib import Path

# ── Path Configuration ──────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[1]
VIDEOS_DIR = ROOT / 'data' / 'videos'
OUTPUT_DIR = ROOT / 'output' / 'metadata'

# ── Category-Specific Tag Pools ─────────────────────────────────────
# Each category has a curated set of hashtags to boost discoverability.
# These are combined with auto-extracted keyword tags from the title.
CATEGORY_TAGS = {
    'EVERYDAY SYSTEMS':     ['#DailyLife', '#Society', '#UrbanSystems', '#PublicPolicy'],
    'MONEY & ECONOMICS':    ['#Economics', '#Finance', '#Markets', '#MoneyExplained'],
    'INFORMATION SYSTEMS':  ['#Technology', '#DataSystems', '#DigitalAge', '#InfoTech'],
    'POWER & INSTITUTIONS': ['#Politics', '#Governance', '#Institutions', '#Power'],
    'FUTURE SYSTEMS':       ['#FutureTech', '#Innovation', '#Sustainability', '#FutureOfWork'],
}


def smart_tags(title: str, category: str) -> list[str]:
    """
    Generate a tag list from:
      1. Base tags (always included for channel consistency)
      2. Category-specific tags (top 2 from the pool)
      3. Keyword tags (capitalized words > 3 chars from the title)
    """
    base = ['#SystemsThinking', '#Explainer', '#HowItWorks']
    cat_tags = CATEGORY_TAGS.get(category, [])

    # Extract 2-3 keyword-based tags from capitalized words in the title
    words = [w for w in title.split() if len(w) > 3 and w[0].isupper()]
    keyword_tags = [f'#{w}' for w in words[:3]]

    return base + cat_tags[:2] + keyword_tags


def generate_metadata(video_id: str) -> dict:
    """
    Build a complete metadata dictionary for a single video.
    The metadata includes everything needed for a YouTube upload.
    """
    payload_path = VIDEOS_DIR / f'{video_id}.json'
    if not payload_path.exists():
        raise FileNotFoundError(f'Video data not found: {payload_path}')

    payload = json.loads(payload_path.read_text(encoding='utf-8'))
    title = payload['title']
    category = payload.get('category', 'EVERYDAY SYSTEMS')
    scene_count = len(payload.get('scenes', []))

    # Truncate title to YouTube's 100-char limit (with ... indicator)
    short_title = title if len(title) <= 95 else f'{title[:92]}...'
    tags = smart_tags(title, category)

    # Build a structured description with timestamps matching scene layout
    description = (
        f'{title}\n\n'
        f'Category: {category}\n\n'
        'This 2-minute visual explainer breaks down the topic using '
        'system maps, incentive structures, and feedback loops.\n\n'
        'Structure:\n'
        '00:00 – Hook & context\n'
        '00:20 – System boundary\n'
        '00:40 – Root causes (3 layers)\n'
        '01:20 – Data lens\n'
        '01:30 – Real-world scene\n'
        '01:40 – Externalities & ecology\n'
        '01:50 – Macro trend & takeaway\n\n'
        f'Video ID: {video_id}\n'
        f'Scenes: {scene_count}\n\n'
        + ' '.join(tags)
    )

    return {
        'videoId': video_id,
        'title': short_title,
        'description': description,
        'tags': tags,
        'category': 'Education',          # YouTube category
        'topicCategory': category,         # Internal category for reference
        'privacy': 'public',              # Default to public visibility
        'language': 'en',                 # Primary language
    }


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate YouTube metadata for one or all videos')
    parser.add_argument('--video-id', default=None, help='Single video ID (e.g. video_001)')
    parser.add_argument('--all', action='store_true', help='Generate metadata for all 500 videos')
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.all:
        # Batch mode: generate metadata for every video in the library
        count = 0
        for path in sorted(VIDEOS_DIR.glob('video_*.json')):
            video_id = path.stem
            meta = generate_metadata(video_id)
            (OUTPUT_DIR / f'{video_id}.json').write_text(
                json.dumps(meta, indent=2), encoding='utf-8'
            )
            count += 1
        print(f'Generated metadata for {count} videos → {OUTPUT_DIR}')
    elif args.video_id:
        # Single mode: generate metadata for one video
        meta = generate_metadata(args.video_id)
        out_file = OUTPUT_DIR / f'{args.video_id}.json'
        out_file.write_text(json.dumps(meta, indent=2), encoding='utf-8')
        print(f'Wrote {out_file}')
    else:
        raise SystemExit('Provide --video-id video_001 or --all')


if __name__ == '__main__':
    main()
