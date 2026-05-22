#!/usr/bin/env python3
"""Build the OS Abyss workspace memory overlay map.

This script is intentionally local-only. It scans checked-out roots and known
pilot places, then publishes a compact status map that tells agents where
memory routes exist without turning this repository into the memory authority.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from audit_agents_map import (
    KNOWN_REPOSITORIES,
    expand_manifest_path,
    path_hint,
    read_text,
    repo_path_for_name,
    workspace_manifest_repo_paths,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = "8dionysus_workspace_memory_map_v1"
SCHEMA_REF = "schemas/workspace-memory-map.schema.json"
OWNER_REPO = "8Dionysus"
DEFAULT_JSON_PATH = REPO_ROOT / "generated" / "workspace_memory_map.min.json"
DEFAULT_MARKDOWN_PATH = REPO_ROOT / "docs" / "WORKSPACE_MEMORY_MAP.md"

MEMORY_ROUTE_MARKERS = (
    "## Memory route",
    "aoa_memo",
    "repo/memo",
    ".aoa",
    "memory candidate",
    "local memo port",
)

PORT_LEVELS = ("none", "route_only", "stub_port", "full_port", "mature_port")
MEMORY_ROUTE_STATUSES = (
    "missing",
    "root_memory_route",
    "local_port_route",
    "session_evidence_route",
)
TERMINAL_REVIEW_STATES = {"rejected", "landed", "superseded", "archived"}

FULL_PORT_RECOMMENDED = frozenset(
    {
        "Agents-of-Abyss",
        "Tree-of-Sophia",
        "Dionysus",
        "abyss-stack",
        "abyss-machine",
        "aoa-agents",
        "aoa-skills",
        "aoa-techniques",
        "aoa-playbooks",
    }
)

ROUTE_ONLY_RECOMMENDED = frozenset(
    {
        "8Dionysus",
        "ATM10-Agent",
        "aoa-evals",
        "aoa-kag",
        "aoa-memo",
        "aoa-routing",
        "aoa-sdk",
        "aoa-stats",
        ".agents",
        ".codex",
        ".aoa",
    }
)

MEMORY_ROLE_BY_NAME = {
    "aoa-memo": "reviewed-memory-owner",
    ".aoa": "session-evidence-kernel",
    "abyss-stack": "mcp-access-plane-owner",
    "abyss-machine": "host-local-memory-port",
    "8Dionysus": "workspace-route-map-owner",
}

REFACTOR_STATE_BY_NAME = {
    "Agents-of-Abyss": "reference-topology",
    "aoa-memo": "active-memory-authority",
    "aoa-skills": "reference-topology",
    "aoa-techniques": "reference-topology",
    "abyss-stack": "pilot-access-plane",
    "abyss-machine": "pilot-host-plane",
    ".aoa": "session-memory-kernel",
    ".codex": "codex-plane",
    ".agents": "agent-install-plane",
}

EXTERNAL_PLACE_SPECS: tuple[dict[str, Any], ...] = (
    {
        "name": "abyss-machine",
        "kind": "host-runtime",
        "role": "host-local machine state, AI runtime posture, telemetry, and operational evidence",
        "place_kind": "host-place",
        "preferred": ("/var/lib/abyss-machine",),
    },
)

WORKSPACE_PLACE_SPECS: tuple[dict[str, Any], ...] = (
    {
        "name": ".aoa",
        "kind": "session-memory-kernel",
        "role": "Codex session preservation, compaction intervals, indexes, diagnostics, search, rehydration, and review packets",
        "place_kind": "workspace-place",
    },
    {
        "name": ".codex",
        "kind": "codex-plane",
        "role": "workspace Codex configuration, hooks, agents, prompts, tools, and MCP wiring",
        "place_kind": "workspace-place",
    },
    {
        "name": ".agents",
        "kind": "agent-install-plane",
        "role": "workspace agent, skill, and plugin install projection surface",
        "place_kind": "workspace-place",
    },
)


def _posix(path: Path) -> str:
    return path.as_posix()


def _read_optional_text(path: Path) -> str:
    if not path.is_file():
        return ""
    return read_text(path)


def _has_memory_route(root: Path) -> bool:
    text = _read_optional_text(root / "AGENTS.md")
    return any(marker in text for marker in MEMORY_ROUTE_MARKERS)


def _count_packet_files(path: Path) -> int:
    if not path.is_dir():
        return 0
    return sum(1 for item in path.iterdir() if item.is_file() and not item.name.startswith("."))


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _packet_files(path: Path) -> list[Path]:
    if not path.is_dir():
        return []
    return sorted(item for item in path.iterdir() if item.is_file() and item.suffix == ".json")


def _copied_intake_exists(workspace_root: Path, repo: str, export_path: Path) -> bool:
    copied = workspace_root / "aoa-memo" / "memo" / "intake" / "reviewed" / f"{repo}.{export_path.name}"
    return copied.is_file()


def _port_packet_counts(memo_root: Path, dirs: Mapping[str, str], repo: str, workspace_root: Path) -> dict[str, int]:
    candidates = _packet_files(memo_root / dirs["candidates"])
    receipts = _packet_files(memo_root / dirs["receipts"])
    exports = _packet_files(memo_root / dirs["exports"])
    local_records = _packet_files(memo_root / dirs["local"])

    pending_candidates = 0
    for path in candidates:
        payload = _load_json(path)
        review_state = str(payload.get("review_state") or "candidate")
        if review_state not in TERMINAL_REVIEW_STATES:
            pending_candidates += 1

    landed_exports = 0
    ready_exports = 0
    blocked_exports = 0
    for path in exports:
        payload = _load_json(path)
        if _copied_intake_exists(workspace_root, repo, path):
            landed_exports += 1
        elif payload.get("allowed_result") == "reviewed_write" and payload.get("receipt_refs"):
            ready_exports += 1
        else:
            blocked_exports += 1

    return {
        "local_candidates": len(candidates),
        "pending_candidates": pending_candidates,
        "validation_receipts": len(receipts),
        "total_exports": len(exports),
        "pending_exports": ready_exports + blocked_exports,
        "ready_exports": ready_exports,
        "blocked_exports": blocked_exports,
        "landed_exports": landed_exports,
        "local_records": len(local_records),
    }


def _parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.isdigit():
        return int(value)
    return value


def parse_port_yaml(path: Path) -> dict[str, Any]:
    """Parse the small local memo PORT.yaml subset without adding a dependency."""
    if not path.is_file():
        return {}
    payload: dict[str, Any] = {}
    current_key: str | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not line.startswith(" ") and ":" in line:
            key, raw_value = line.split(":", 1)
            key = key.strip()
            value = raw_value.strip()
            if value:
                payload[key] = _parse_scalar(value)
                current_key = None
            else:
                payload[key] = []
                current_key = key
            continue
        if current_key and stripped.startswith("- "):
            value = stripped[2:].strip()
            current = payload.setdefault(current_key, [])
            if isinstance(current, list):
                current.append(_parse_scalar(value))
    return payload


def memo_port_record(root: Path, workspace_root: Path) -> dict[str, Any]:
    memo_root = root / "memo"
    port_yaml = memo_root / "PORT.yaml"
    port = parse_port_yaml(port_yaml)
    dirs = {
        "candidates": str(port.get("candidate_dir", "candidates")),
        "receipts": str(port.get("receipt_dir", "receipts")),
        "exports": str(port.get("export_dir", "exports")),
        "local": str(port.get("local_dir", "local")),
    }
    required_files = ("AGENTS.md", "README.md", "PORT.yaml")
    missing_files = [name for name in required_files if not (memo_root / name).is_file()]
    missing_dirs = [name for name, rel in dirs.items() if not (memo_root / rel).is_dir()]
    index_present = (memo_root / "index.min.json").is_file()
    present = memo_root.is_dir() and port_yaml.is_file()

    if present and not missing_files and not missing_dirs and index_present:
        level = "full_port"
    elif present and (memo_root / "AGENTS.md").is_file() and port_yaml.is_file():
        level = "stub_port"
    else:
        level = "none"

    root_hint = path_hint(root, workspace_root)
    memo_hint = f"{root_hint}/memo" if present else ""
    packet_counts = _port_packet_counts(
        memo_root,
        dirs,
        str(port.get("repo") or root.name),
        workspace_root,
    )

    return {
        "present": present,
        "path_hint": memo_hint,
        "port_level": level,
        "schema": port.get("schema", ""),
        "owner": port.get("owner", ""),
        "stronger_memory_owner": port.get("stronger_memory_owner", ""),
        "default_mode": port.get("default_mode", ""),
        "port_scope": port.get("port_scope", ""),
        "allowed_routes": port.get("allowed_routes", []),
        "privacy_posture": port.get("privacy_posture", ""),
        "index_present": index_present,
        "missing_files": missing_files,
        "missing_dirs": missing_dirs,
        **packet_counts,
    }


def recommended_port_level(name: str) -> str:
    if name in FULL_PORT_RECOMMENDED:
        return "full_port"
    if name in ROUTE_ONLY_RECOMMENDED:
        return "route_only"
    return "route_only"


def memory_role(name: str) -> str:
    if name in MEMORY_ROLE_BY_NAME:
        return MEMORY_ROLE_BY_NAME[name]
    if name in FULL_PORT_RECOMMENDED:
        return "local-memory-port-candidate"
    return "workspace-memory-route"


def refactor_state(name: str) -> str:
    return REFACTOR_STATE_BY_NAME.get(name, "pending-deep-refactor")


def detect_mcp_status(workspace_root: Path) -> dict[str, Any]:
    config_path = workspace_root / ".codex" / "config.toml"
    config_text = _read_optional_text(config_path)
    registered = "[mcp_servers.aoa_memo]" in config_text or "aoa_memo" in config_text
    stack_paths = (
        workspace_root / "abyss-stack" / "mcp" / "services" / "aoa-memo-mcp",
        Path.home() / "src" / "abyss-stack" / "mcp" / "services" / "aoa-memo-mcp",
    )
    service_source_hint = ""
    for path in stack_paths:
        if path.is_dir():
            service_source_hint = path_hint(path, workspace_root)
            break
    return {
        "name": "aoa_memo",
        "status": "registered" if registered else "not-registered",
        "runtime_status": "not_asserted_by_workspace_map",
        "access_plane_owner": "abyss-stack",
        "authority_owner": "aoa-memo",
        "service_source_hint": service_source_hint,
        "smoke_check": "python scripts/smoke_aoa_memo_mcp.py --workspace-root <workspace-root>",
    }


def place_record(
    *,
    name: str,
    kind: str,
    role: str,
    place_kind: str,
    root: Path | None,
    workspace_root: Path,
    mcp_status: Mapping[str, Any],
) -> dict[str, Any]:
    issues: list[str] = []
    if root is None or not root.is_dir():
        return {
            "name": name,
            "kind": kind,
            "role": role,
            "place_kind": place_kind,
            "checkout_state": "missing",
            "path_hint": name,
            "memory_role": memory_role(name),
            "refactor_state": refactor_state(name),
            "root_agents_present": False,
            "memory_route_status": "missing",
            "current_port_level": "none",
            "recommended_port_level": recommended_port_level(name),
            "reviewed_memory_route": "aoa-memo:reviewed-intake",
            "evidence_route": ".aoa:retrieve/rehydrate/review-packet",
            "mcp": dict(mcp_status),
            "memo_port": memo_port_record(Path("__missing__"), workspace_root),
            "validation_command": "python scripts/build_workspace_memory_map.py --check",
            "issues": ["place root not found"],
        }

    root_agents_present = (root / "AGENTS.md").is_file()
    has_memory_route = _has_memory_route(root)
    memo_port = memo_port_record(root, workspace_root)
    current_level = memo_port["port_level"]
    if current_level == "none" and has_memory_route:
        current_level = "route_only"

    route_status = "root_memory_route" if has_memory_route else "missing"
    if name == ".aoa" and root_agents_present:
        route_status = "session_evidence_route"
        if current_level == "none":
            current_level = "route_only"
    if memo_port["present"] and has_memory_route:
        route_status = "local_port_route"

    if not root_agents_present:
        issues.append("missing root AGENTS.md")
    if route_status == "missing":
        issues.append("missing root Memory route")
    if memo_port["present"]:
        for missing in memo_port["missing_files"]:
            issues.append(f"memo port missing {missing}")
        for missing in memo_port["missing_dirs"]:
            issues.append(f"memo port missing {missing}/")
        if not memo_port["index_present"]:
            issues.append("memo port index missing")
    if recommended_port_level(name) == "full_port" and current_level in {"none", "route_only"}:
        issues.append("recommended full memo port not yet present")

    validation_command = "python scripts/build_workspace_memory_map.py --check"
    if memo_port["present"]:
        validation_command = f"python -m aoa_memo_mcp.cli validate-port --repo {name}"

    return {
        "name": name,
        "kind": kind,
        "role": role,
        "place_kind": place_kind,
        "checkout_state": "scanned",
        "path_hint": path_hint(root, workspace_root),
        "memory_role": memory_role(name),
        "refactor_state": refactor_state(name),
        "root_agents_present": root_agents_present,
        "memory_route_status": route_status,
        "current_port_level": current_level,
        "recommended_port_level": recommended_port_level(name),
        "reviewed_memory_route": "aoa-memo:reviewed-intake",
        "evidence_route": ".aoa:retrieve/rehydrate/review-packet",
        "mcp": dict(mcp_status),
        "memo_port": memo_port,
        "validation_command": validation_command,
        "issues": sorted(set(issues)),
    }


def _resolve_external_place(spec: Mapping[str, Any], workspace_root: Path) -> Path | None:
    for raw in spec.get("preferred", ()):
        candidate = expand_manifest_path(str(raw), workspace_root)
        if candidate.is_dir():
            return candidate
    return None


def workspace_place_records(workspace_root: Path, mcp_status: Mapping[str, Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for spec in WORKSPACE_PLACE_SPECS:
        root = workspace_root / str(spec["name"])
        records.append(
            place_record(
                name=str(spec["name"]),
                kind=str(spec["kind"]),
                role=str(spec["role"]),
                place_kind=str(spec["place_kind"]),
                root=root,
                workspace_root=workspace_root,
                mcp_status=mcp_status,
            )
        )
    return records


def build_workspace_memory_map(workspace_root: Path) -> dict[str, Any]:
    workspace_root = workspace_root.resolve()
    mcp_status = detect_mcp_status(workspace_root)
    manifest_repo_paths = workspace_manifest_repo_paths(workspace_root)
    places: list[dict[str, Any]] = []

    for repo in KNOWN_REPOSITORIES:
        name = repo["name"]
        root = repo_path_for_name(workspace_root, name, manifest_repo_paths)
        places.append(
            place_record(
                name=name,
                kind=repo["kind"],
                role=repo["role"],
                place_kind="workspace-repo",
                root=root,
                workspace_root=workspace_root,
                mcp_status=mcp_status,
            )
        )

    for spec in EXTERNAL_PLACE_SPECS:
        root = manifest_repo_paths.get(str(spec["name"])) or _resolve_external_place(spec, workspace_root)
        places.append(
            place_record(
                name=str(spec["name"]),
                kind=str(spec["kind"]),
                role=str(spec["role"]),
                place_kind=str(spec["place_kind"]),
                root=root,
                workspace_root=workspace_root,
                mcp_status=mcp_status,
            )
        )

    places.extend(workspace_place_records(workspace_root, mcp_status))

    totals = {
        "places_listed": len(places),
        "places_scanned": sum(1 for place in places if place["checkout_state"] == "scanned"),
        "memory_routes": sum(1 for place in places if place["memory_route_status"] != "missing"),
        "root_memory_routes": sum(
            1
            for place in places
            if place["memory_route_status"] in {"root_memory_route", "local_port_route"}
        ),
        "session_evidence_routes": sum(
            1 for place in places if place["memory_route_status"] == "session_evidence_route"
        ),
        "full_ports": sum(1 for place in places if place["current_port_level"] == "full_port"),
        "route_only": sum(1 for place in places if place["current_port_level"] == "route_only"),
        "recommended_full_ports_missing": sum(
            1
            for place in places
            if place["recommended_port_level"] == "full_port"
            and place["current_port_level"] in {"none", "route_only"}
        ),
        "local_candidates": sum(int(place["memo_port"]["local_candidates"]) for place in places),
        "pending_candidates": sum(int(place["memo_port"]["pending_candidates"]) for place in places),
        "pending_exports": sum(int(place["memo_port"]["pending_exports"]) for place in places),
        "ready_exports": sum(int(place["memo_port"]["ready_exports"]) for place in places),
        "landed_exports": sum(int(place["memo_port"]["landed_exports"]) for place in places),
        "places_with_issues": sum(1 for place in places if place["issues"]),
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "schema_ref": SCHEMA_REF,
        "owner_repo": OWNER_REPO,
        "surface_kind": "workspace_memory_overlay_map",
        "generated_by": "scripts/build_workspace_memory_map.py",
        "workspace_root_hint": "workspace-relative, home-relative, or external:name only; no absolute paths are stored",
        "taxonomy": {
            "port_levels": list(PORT_LEVELS),
            "meaning": {
                "none": "no visible local memo route in this place yet",
                "route_only": "root AGENTS.md or owner-local route points to aoa_memo/.aoa/reviewed memory without a local memo port",
                "stub_port": "memo/ exists with route card and PORT.yaml, but is not yet fully indexed",
                "full_port": "memo/ has route card, PORT.yaml, packet dirs, and index",
                "mature_port": "future state: local port is connected to reviewed landing, stats/evals, and repo vocabulary",
            },
        },
        "reviewed_memory_owner": "aoa-memo",
        "session_evidence_owner": ".aoa",
        "access_plane": dict(mcp_status),
        "totals": totals,
        "places": places,
    }


def render_payload(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def render_markdown(payload: Mapping[str, Any]) -> str:
    totals = payload["totals"]
    places: Sequence[Mapping[str, Any]] = payload["places"]
    lines = [
        "# Workspace memory map",
        "",
        "This generated map is the first OS Abyss memory overlay surface.",
        "It tells agents where memory routes, local ports, session evidence, and reviewed memory handoff currently live.",
        "It is not memory authority; reviewed memory belongs to `aoa-memo`, session evidence belongs to `.aoa`, and MCP is only an access plane.",
        "",
        "## Regenerate",
        "",
        "```bash",
        "python scripts/build_workspace_memory_map.py \\",
        "  --workspace-root <workspace-root> \\",
        "  --write generated/workspace_memory_map.min.json \\",
        "  --markdown docs/WORKSPACE_MEMORY_MAP.md",
        "python scripts/build_workspace_memory_map.py --check",
        "python scripts/validate_workspace_memory_map.py",
        "```",
        "",
        "## Totals",
        "",
    ]
    for key in sorted(totals):
        lines.append(f"- `{key}`: {totals[key]}")
    access_plane = payload["access_plane"]
    lines.extend(
        [
            "",
            "## Access Plane",
            "",
            f"- `name`: `{access_plane['name']}`",
            f"- `registration_status`: `{access_plane['status']}`",
            f"- `runtime_status`: `{access_plane.get('runtime_status', 'not_asserted_by_workspace_map')}`",
            f"- `owner`: `{access_plane['access_plane_owner']}`",
            f"- `authority`: `{access_plane['authority_owner']}`",
            f"- `source`: `{access_plane.get('service_source_hint', '')}`",
            f"- `smoke_check`: `{access_plane.get('smoke_check', '')}`",
        ]
    )
    lines.extend(
        [
            "",
            "## Port Levels",
            "",
            "| Level | Meaning |",
            "|---|---|",
        ]
    )
    meaning = payload["taxonomy"]["meaning"]
    for level in payload["taxonomy"]["port_levels"]:
        lines.append(f"| `{level}` | {meaning[level]} |")
    lines.extend(
        [
            "",
            "## Places",
            "",
            "| Place | Role | Current | Recommended | Route | Pending candidates | Pending exports | Ready | Landed | Validator | Issues |",
            "|---|---|---|---|---|---:|---:|---:|---:|---|---|",
        ]
    )
    for place in places:
        issues = ", ".join(place["issues"]) if place["issues"] else "ok"
        lines.append(
            "| {name} | {memory_role} | `{current}` | `{recommended}` | {route} | {candidates} | {exports} | {ready} | {landed} | `{validator}` | {issues} |".format(
                name=place["name"],
                memory_role=place["memory_role"],
                current=place["current_port_level"],
                recommended=place["recommended_port_level"],
                route=place["memory_route_status"],
                candidates=place["memo_port"]["pending_candidates"],
                exports=place["memo_port"]["pending_exports"],
                ready=place["memo_port"]["ready_exports"],
                landed=place["memo_port"]["landed_exports"],
                validator=place["validation_command"],
                issues=issues,
            )
        )
    lines.extend(
        [
            "",
            "## Route Contract",
            "",
            "- Need continuity or reviewed recall: use `aoa_memo` through the Codex MCP plane when available.",
            "- Need session evidence, compaction recovery, or raw transcript grounding: route to `.aoa` retrieval or rehydration packets.",
            "- Need to preserve local memory in a place that has a port: write a candidate under `repo/memo/`, validate it, then export for reviewed intake.",
            "- Need durable cross-system memory: land through `aoa-memo` reviewed intake and validators.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, default=REPO_ROOT.parent)
    parser.add_argument("--write", type=Path, default=DEFAULT_JSON_PATH)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN_PATH)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    payload = build_workspace_memory_map(args.workspace_root)
    rendered = render_payload(payload)
    markdown = render_markdown(payload)
    if args.check:
        current = args.write.read_text(encoding="utf-8")
        if current != rendered:
            raise SystemExit(f"{args.write} is out of date")
        if args.markdown.is_file() and args.markdown.read_text(encoding="utf-8") != markdown:
            raise SystemExit(f"{args.markdown} is out of date")
        print("[ok] verified workspace memory map")
        return 0

    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(rendered, encoding="utf-8")
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.write_text(markdown, encoding="utf-8")
    print(f"[ok] wrote {args.write}")
    print(f"[ok] wrote {args.markdown}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
