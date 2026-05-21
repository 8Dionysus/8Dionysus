#!/usr/bin/env python3
"""Validate the generated OS Abyss workspace memory overlay map."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from build_workspace_memory_map import (
    DEFAULT_JSON_PATH,
    DEFAULT_MARKDOWN_PATH,
    OWNER_REPO,
    PORT_LEVELS,
    SCHEMA_REF,
    SCHEMA_VERSION,
    build_workspace_memory_map,
    render_markdown,
    render_payload,
)


FORBIDDEN_ABSOLUTE_PREFIXES = ('"/srv/', '"/home/', '"/var/', '"/mnt/')
REQUIRED_PLACES = (
    "8Dionysus",
    "Agents-of-Abyss",
    "aoa-memo",
    ".aoa",
    "abyss-stack",
    "abyss-machine",
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def validate_payload(payload: Mapping[str, Any]) -> None:
    _require(payload.get("schema_version") == SCHEMA_VERSION, "wrong schema_version")
    _require(payload.get("schema_ref") == SCHEMA_REF, "wrong schema_ref")
    _require(payload.get("owner_repo") == OWNER_REPO, "wrong owner_repo")
    _require(payload.get("reviewed_memory_owner") == "aoa-memo", "wrong reviewed memory owner")
    _require(payload.get("session_evidence_owner") == ".aoa", "wrong session evidence owner")

    taxonomy = payload.get("taxonomy")
    _require(isinstance(taxonomy, dict), "taxonomy must be an object")
    _require(tuple(taxonomy.get("port_levels", ())) == PORT_LEVELS, "port level taxonomy drifted")

    places = payload.get("places")
    _require(isinstance(places, list) and places, "places must be a non-empty list")
    by_name = {place.get("name"): place for place in places if isinstance(place, dict)}
    for name in REQUIRED_PLACES:
        _require(name in by_name, f"required memory place missing: {name}")

    for place in places:
        _require(isinstance(place, dict), "place records must be objects")
        for key in (
            "name",
            "memory_role",
            "current_port_level",
            "recommended_port_level",
            "reviewed_memory_route",
            "evidence_route",
            "mcp",
            "memo_port",
            "issues",
        ):
            _require(key in place, f"place missing required field: {key}")
        _require(place["current_port_level"] in PORT_LEVELS, f"invalid current port level for {place['name']}")
        _require(place["recommended_port_level"] in PORT_LEVELS, f"invalid recommended port level for {place['name']}")
        _require(place["reviewed_memory_route"] == "aoa-memo:reviewed-intake", "reviewed route must stay aoa-memo")
        _require(str(place["evidence_route"]).startswith(".aoa:"), "evidence route must stay in .aoa")
        memo_port = place["memo_port"]
        _require(isinstance(memo_port, dict), "memo_port must be an object")
        _require("local_candidates" in memo_port, "memo_port missing local_candidates")
        _require("pending_exports" in memo_port, "memo_port missing pending_exports")

    _require(
        by_name["aoa-memo"]["memory_role"] == "reviewed-memory-owner",
        "aoa-memo must stay the reviewed memory owner",
    )
    _require(
        by_name[".aoa"]["memory_role"] == "session-evidence-kernel",
        ".aoa must stay the session evidence kernel",
    )


def main() -> int:
    expected_payload = build_workspace_memory_map(Path(__file__).resolve().parents[2])
    current_payload = json.loads(DEFAULT_JSON_PATH.read_text(encoding="utf-8"))
    validate_payload(current_payload)
    expected_rendered = render_payload(expected_payload)
    if DEFAULT_JSON_PATH.read_text(encoding="utf-8") != expected_rendered:
        raise SystemExit("generated/workspace_memory_map.min.json does not match the canonical rebuild")
    if DEFAULT_MARKDOWN_PATH.read_text(encoding="utf-8") != render_markdown(expected_payload):
        raise SystemExit("docs/WORKSPACE_MEMORY_MAP.md does not match the canonical rebuild")

    rendered = json.dumps(current_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    for prefix in FORBIDDEN_ABSOLUTE_PREFIXES:
        if prefix in rendered:
            raise SystemExit(f"workspace memory map leaked absolute path prefix: {prefix}")

    print("[ok] validated generated/workspace_memory_map.min.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
