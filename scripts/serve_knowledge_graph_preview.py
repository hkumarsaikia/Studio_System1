from __future__ import annotations

import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


class NoCacheHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(REPO_ROOT), **kwargs)

    def end_headers(self) -> None:
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()


def main() -> None:
    parser = argparse.ArgumentParser(description='Serve the repository root for the knowledge graph dashboard.')
    parser.add_argument('--port', type=int, default=4173)
    args = parser.parse_args()

    server = ThreadingHTTPServer(('127.0.0.1', args.port), NoCacheHandler)
    print(f'Serving {REPO_ROOT} on http://127.0.0.1:{args.port}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
