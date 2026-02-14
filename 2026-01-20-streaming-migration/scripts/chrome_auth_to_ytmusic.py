#!/usr/bin/env python3
"""Generate ytmusicapi browser auth JSON from Chrome "Copy as cURL (bash)".

Examples:
  pbpaste | uv run python scripts/chrome_auth_to_ytmusic.py
  uv run python scripts/chrome_auth_to_ytmusic.py -i request.curl
"""

from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path


DEFAULT_OUTPUT = Path(__file__).parent.parent / "data" / "ytmusicapi-browser.json"


def parse_curl_headers(text: str) -> dict[str, str]:
    """Parse headers from a curl command string."""
    normalized = text.replace("\\\n", " ").replace("\\\r\n", " ")
    try:
        tokens = shlex.split(normalized)
    except ValueError:
        return {}

    headers: dict[str, str] = {}
    i = 0
    while i < len(tokens):
        token = tokens[i]
        header_blob = None
        cookie_blob = None
        if token in ("-H", "--header") and i + 1 < len(tokens):
            header_blob = tokens[i + 1]
            i += 1
        elif token in ("-b", "--cookie") and i + 1 < len(tokens):
            cookie_blob = tokens[i + 1]
            i += 1
        elif token.startswith("-H") and token != "-H":
            header_blob = token[2:]
        elif token.startswith("--header="):
            header_blob = token.split("=", 1)[1]
        elif token.startswith("--cookie="):
            cookie_blob = token.split("=", 1)[1]

        if header_blob and ":" in header_blob:
            name, value = header_blob.split(":", 1)
            headers[name.strip().lower()] = value.strip()
        if cookie_blob is not None:
            headers["cookie"] = cookie_blob.strip()
        i += 1

    return headers


def build_auth_payload(headers: dict[str, str]) -> dict[str, str]:
    """Build ytmusicapi browser auth JSON payload."""
    authorization = headers.get("authorization", "")
    cookie = headers.get("cookie", "")
    if not authorization or not cookie:
        missing = []
        if not authorization:
            missing.append("Authorization")
        if not cookie:
            missing.append("Cookie")
        missing_str = ", ".join(missing)
        raise ValueError(f"Missing required headers: {missing_str}")

    x_goog_authuser = headers.get("x-goog-authuser") or "0"
    x_origin = (
        headers.get("x-origin") or headers.get("origin") or "https://music.youtube.com"
    )
    accept = headers.get("accept") or "*/*"
    content_type = headers.get("content-type") or "application/json"

    return {
        "Accept": accept,
        "Authorization": authorization,
        "Content-Type": content_type,
        "X-Goog-AuthUser": x_goog_authuser,
        "x-origin": x_origin,
        "Cookie": cookie,
    }


def read_input(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    if sys.stdin.isatty():
        print("Paste Chrome 'Copy as cURL (bash)', then Ctrl-D:", file=sys.stderr)
    return sys.stdin.read()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert Chrome 'Copy as cURL (bash)' into ytmusicapi browser auth JSON"
    )
    parser.add_argument("-i", "--input", help="Input file path (default: read stdin)")
    parser.add_argument(
        "-o",
        "--output",
        default=str(DEFAULT_OUTPUT),
        help=f"Output JSON path (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--print-only",
        action="store_true",
        help="Print JSON to stdout instead of writing file",
    )
    args = parser.parse_args()

    text = read_input(args.input).strip()
    if not text:
        print("Error: no input provided", file=sys.stderr)
        return 1

    headers = parse_curl_headers(text)
    if not headers:
        print("Error: could not parse curl headers from input", file=sys.stderr)
        return 1

    try:
        payload = build_auth_payload(headers)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    json_text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"

    if args.print_only:
        sys.stdout.write(json_text)
        return 0

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json_text, encoding="utf-8")

    print(f"Wrote {out_path}")
    print("Tip: verify with a dry run, e.g. playlist_to_library.py -n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
