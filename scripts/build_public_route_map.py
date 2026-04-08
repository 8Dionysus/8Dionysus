#!/usr/bin/env python3
"""Build the public profile-owned route map surface."""

from __future__ import annotations

import argparse

from public_route_map_common import PUBLIC_ROUTE_MAP_PATH, build_payload, render_payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build 8Dionysus generated/public_route_map.min.json.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify the generated file matches the canonical rebuild instead of rewriting it.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_payload()
    rendered = render_payload(payload)
    PUBLIC_ROUTE_MAP_PATH.parent.mkdir(parents=True, exist_ok=True)
    if args.check:
        current = PUBLIC_ROUTE_MAP_PATH.read_text(encoding="utf-8")
        if current != rendered:
            raise SystemExit("generated/public_route_map.min.json is out of date")
        print("[ok] verified generated/public_route_map.min.json")
        return 0
    PUBLIC_ROUTE_MAP_PATH.write_text(rendered, encoding="utf-8")
    print("[ok] wrote generated/public_route_map.min.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
