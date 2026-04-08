#!/usr/bin/env python3
"""Validate the public route map surface against live profile posture."""

from __future__ import annotations

import json

from public_route_map_common import (
    PROFILE_PAYLOAD,
    PUBLIC_ROUTE_MAP_PATH,
    ROUTE_METADATA_BY_NEED,
    build_payload,
    resolve_repo_ref,
)


def main() -> int:
    expected_payload = build_payload()
    current_payload = json.loads(PUBLIC_ROUTE_MAP_PATH.read_text(encoding="utf-8"))
    if current_payload != expected_payload:
        raise SystemExit("generated/public_route_map.min.json does not match the canonical rebuild")

    profile = current_payload.get("profile")
    if profile != PROFILE_PAYLOAD:
        raise SystemExit("generated/public_route_map.min.json must stay orientation-only")

    routes = current_payload.get("routes")
    if not isinstance(routes, list) or len(routes) != len(ROUTE_METADATA_BY_NEED):
        raise SystemExit("generated/public_route_map.min.json must publish exactly three public routes")

    for route in routes:
        if not isinstance(route, dict):
            raise SystemExit("generated/public_route_map.min.json routes must be objects")
        for key in (
            "route_id",
            "need",
            "canonical_repo",
            "capsule_ref",
            "authority_ref",
            "verification_refs",
        ):
            value = route.get(key)
            if not value:
                raise SystemExit(f"generated/public_route_map.min.json is missing route field '{key}'")
        resolve_repo_ref(route["capsule_ref"])
        resolve_repo_ref(route["authority_ref"])
        verification_refs = route["verification_refs"]
        if not isinstance(verification_refs, list) or not verification_refs:
            raise SystemExit("generated/public_route_map.min.json verification_refs must be a non-empty list")
        for ref in verification_refs:
            if not isinstance(ref, str) or not ref.strip():
                raise SystemExit("generated/public_route_map.min.json verification_refs must contain strings")
            resolve_repo_ref(ref)

    print("[ok] validated generated/public_route_map.min.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
