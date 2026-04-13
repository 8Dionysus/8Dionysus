#!/usr/bin/env python3
"""Shared builder helpers for the public route map surface."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = REPO_ROOT.parent
PUBLIC_ENTRY_POSTURE_PATH = REPO_ROOT / "docs" / "PUBLIC_ENTRY_POSTURE.md"
PUBLIC_ROUTE_MAP_PATH = REPO_ROOT / "generated" / "public_route_map.min.json"
SCHEMA_REF = "schemas/public-route-map.schema.json"
VALIDATION_REFS = (
    "scripts/build_public_route_map.py",
    "scripts/validate_public_route_map.py",
    "tests/test_public_route_map.py",
)
FORBIDDEN_LOW_CONTEXT_PREFIXES = ("src/", "scripts/")

SURFACE_PAYLOAD = {
    "schema_version": "8dionysus_public_route_map_v2",
    "schema_ref": SCHEMA_REF,
    "owner_repo": "8Dionysus",
    "surface_kind": "orientation_surface",
    "authority_ref": "docs/PUBLIC_ENTRY_POSTURE.md",
    "posture": "route-map-only",
    "validation_refs": list(VALIDATION_REFS),
}

ROUTE_METADATA_BY_NEED = {
    "ecosystem understanding": {
        "route_id": "ecosystem-understanding",
        "capsule_ref": "Agents-of-Abyss:generated/center_entry_map.min.json",
        "authority_ref": "Agents-of-Abyss:CHARTER.md",
        "verification_refs": [
            "Agents-of-Abyss:generated/ecosystem_registry.min.json",
            "Agents-of-Abyss:generated/federation_supporting_inventory.min.json",
        ],
    },
    "local workspace bootstrap and typed control-plane use": {
        "route_id": "workspace-bootstrap",
        "capsule_ref": "aoa-sdk:generated/workspace_control_plane.min.json",
        "authority_ref": "aoa-sdk:docs/boundaries.md",
        "verification_refs": [
            "aoa-sdk:docs/workspace-layout.md",
            "aoa-sdk:docs/versioning.md",
            "8Dionysus:docs/WORKSPACE_INSTALL.md",
            "8Dionysus:docs/CODEX_PLANE_REGENERATION.md",
        ],
    },
    "profile-only route or glossary correction": {
        "route_id": "profile-correction",
        "capsule_ref": "8Dionysus:GLOSSARY.md",
        "authority_ref": "8Dionysus:docs/PUBLIC_ENTRY_POSTURE.md",
        "verification_refs": [
            "8Dionysus:README.md",
            "8Dionysus:docs/QUESTBOOK_PROFILE_BOUNDARY.md",
        ],
    },
}

EXPECTED_CANONICAL_REPOS = {
    "ecosystem understanding": "Agents-of-Abyss",
    "local workspace bootstrap and typed control-plane use": "aoa-sdk",
    "profile-only route or glossary correction": "8Dionysus",
}


def _parse_markdown_table_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        raise ValueError(f"not a markdown table row: {line!r}")
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def parse_public_entry_posture_rows(text: str) -> list[dict[str, str]]:
    lines = text.splitlines()
    start_index: int | None = None
    for index, line in enumerate(lines):
        if line.strip() == "## Shortest onboarding paths":
            start_index = index
            break
    if start_index is None:
        raise ValueError("PUBLIC_ENTRY_POSTURE.md is missing '## Shortest onboarding paths'")

    table_lines: list[str] = []
    started = False
    for line in lines[start_index + 1 :]:
        stripped = line.strip()
        if not stripped:
            if started:
                break
            continue
        if stripped.startswith("|"):
            table_lines.append(stripped)
            started = True
            continue
        if started:
            break

    if len(table_lines) < 3:
        raise ValueError("PUBLIC_ENTRY_POSTURE.md is missing the onboarding table rows")

    header = [cell.lower() for cell in _parse_markdown_table_row(table_lines[0])]
    if header[:2] != ["need", "canonical home"]:
        raise ValueError("PUBLIC_ENTRY_POSTURE.md onboarding table must start with need/canonical home")

    rows: list[dict[str, str]] = []
    for raw_line in table_lines[2:]:
        cells = _parse_markdown_table_row(raw_line)
        if len(cells) != len(header):
            raise ValueError(f"PUBLIC_ENTRY_POSTURE.md row has wrong column count: {raw_line!r}")
        row = dict(zip(header, cells, strict=True))
        row["canonical home"] = row["canonical home"].strip("`")
        rows.append(row)
    return rows


def build_payload() -> dict[str, object]:
    rows = parse_public_entry_posture_rows(PUBLIC_ENTRY_POSTURE_PATH.read_text(encoding="utf-8"))
    if len(rows) != len(ROUTE_METADATA_BY_NEED):
        raise ValueError("PUBLIC_ENTRY_POSTURE.md must publish exactly three onboarding rows")

    routes: list[dict[str, object]] = []
    seen_needs: set[str] = set()
    for row in rows:
        need = row["need"]
        canonical_repo = row["canonical home"]
        if need not in ROUTE_METADATA_BY_NEED:
            raise ValueError(f"unexpected public route need '{need}'")
        if need in seen_needs:
            raise ValueError(f"duplicate public route need '{need}'")
        seen_needs.add(need)
        expected_repo = EXPECTED_CANONICAL_REPOS[need]
        if canonical_repo != expected_repo:
            raise ValueError(
                f"need '{need}' must keep canonical home '{expected_repo}', got '{canonical_repo}'"
            )
        metadata = ROUTE_METADATA_BY_NEED[need]
        validate_low_context_repo_ref(metadata["capsule_ref"], f"route:{metadata['route_id']}.capsule_ref")
        validate_low_context_repo_ref(metadata["authority_ref"], f"route:{metadata['route_id']}.authority_ref")
        for ref in metadata["verification_refs"]:
            validate_low_context_repo_ref(ref, f"route:{metadata['route_id']}.verification_refs")
        routes.append(
            {
                "route_id": metadata["route_id"],
                "need": need,
                "canonical_repo": canonical_repo,
                "capsule_ref": metadata["capsule_ref"],
                "authority_ref": metadata["authority_ref"],
                "verification_refs": list(metadata["verification_refs"]),
            }
        )

    resolve_local_ref(SURFACE_PAYLOAD["schema_ref"])
    resolve_local_ref(SURFACE_PAYLOAD["authority_ref"])
    for ref in SURFACE_PAYLOAD["validation_refs"]:
        resolve_local_ref(ref)

    payload = {
        **SURFACE_PAYLOAD,
        "routes": routes,
    }
    validate_payload_schema(payload)
    return payload


def render_payload(payload: dict[str, object]) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n"


def resolve_local_ref(value: str) -> Path:
    target_path = REPO_ROOT / value
    if not target_path.exists():
        raise ValueError(f"missing ref target '{value}'")
    return target_path


def resolve_repo_ref(value: str) -> Path:
    repo_name, separator, relative_path = value.partition(":")
    if separator != ":" or not repo_name or not relative_path:
        raise ValueError(f"invalid repo-qualified ref '{value}'")
    repo_root = REPO_ROOT if repo_name == "8Dionysus" else WORKSPACE_ROOT / repo_name
    target_path = repo_root / relative_path
    if not target_path.exists():
        raise ValueError(f"missing ref target '{value}'")
    return target_path


def validate_low_context_repo_ref(value: str, location: str) -> Path:
    _, _, relative_path = value.partition(":")
    for prefix in FORBIDDEN_LOW_CONTEXT_PREFIXES:
        if relative_path.startswith(prefix):
            raise ValueError(f"{location} must not point to implementation path '{value}'")
    return resolve_repo_ref(value)


def load_schema() -> dict[str, object]:
    schema_path = resolve_local_ref(SCHEMA_REF)
    return json.loads(schema_path.read_text(encoding="utf-8"))


def validate_payload_schema(payload: dict[str, object]) -> None:
    validator = Draft202012Validator(load_schema())
    errors = sorted(validator.iter_errors(payload), key=lambda error: list(error.absolute_path))
    if not errors:
        return
    error = errors[0]
    path = "".join(f"[{item}]" if isinstance(item, int) else f".{item}" for item in error.absolute_path)
    if path.startswith("."):
        path = path[1:]
    if path:
        raise ValueError(f"schema violation at '{path}': {error.message}")
    raise ValueError(f"schema violation: {error.message}")
