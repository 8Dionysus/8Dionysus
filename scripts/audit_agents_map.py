#!/usr/bin/env python3
"""Build an AGENTS.md coverage map for the AoA / ToS workspace.

The script is intentionally local-only: it does not call GitHub, MCP servers,
network APIs, or workspace launchers. It scans checked-out repositories and
turns the current AGENTS.md surface into a compact, reviewable map.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import tomllib
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = "8dionysus_agents_map_v1"
SCHEMA_REF = "schemas/agents-map.schema.json"
OWNER_REPO = "8Dionysus"
ROOT_AGENTS_LONG_LINE_THRESHOLD = 240
REQUIRED_AGENTS_VARIABLES = frozenset({"REQUIRED_AGENTS", "REQUIRED_AGENTS_DOCS"})

KNOWN_REPOSITORIES: tuple[dict[str, str], ...] = (
    {
        "name": "8Dionysus",
        "role": "public routing, glossary alignment, profile-level orientation, and selected shared-root install surfaces",
        "kind": "public-route-map",
    },
    {
        "name": "Agents-of-Abyss",
        "role": "ecosystem identity, charter, layer map, federation rules, and program-level direction",
        "kind": "constitutional-center",
    },
    {
        "name": "Tree-of-Sophia",
        "role": "source-linked knowledge, texts, concepts, lineages, and interpretive architecture",
        "kind": "knowledge-root",
    },
    {
        "name": "abyss-stack",
        "role": "runtime, deployment, storage, lifecycle services, and infrastructure posture",
        "kind": "runtime-infrastructure",
    },
    {
        "name": "ATM10-Agent",
        "role": "local-first companion behavior, perception, memory, voice, and safe automation surfaces",
        "kind": "operator-companion",
    },
    {
        "name": "Dionysus",
        "role": "seed-garden experiments, staging, and early forms",
        "kind": "seed-garden",
    },
    {
        "name": "aoa-sdk",
        "role": "typed workspace integration, compatibility checks, bounded activation, and controlled orchestration",
        "kind": "control-plane-sdk",
    },
    {
        "name": "aoa-techniques",
        "role": "reusable engineering practice",
        "kind": "technique-canon",
    },
    {
        "name": "aoa-skills",
        "role": "bounded execution workflows",
        "kind": "skill-canon",
    },
    {
        "name": "aoa-evals",
        "role": "portable proof and evaluation surfaces",
        "kind": "evaluation-layer",
    },
    {
        "name": "aoa-stats",
        "role": "derived observability from source-owned receipts and verdicts",
        "kind": "derived-observability",
    },
    {
        "name": "aoa-routing",
        "role": "navigation, typing, dispatch hints, and derived cross-repo entry surfaces",
        "kind": "routing-layer",
    },
    {
        "name": "aoa-memo",
        "role": "explicit memory objects, provenance threads, temporal relevance, salience, and recall contracts",
        "kind": "memory-layer",
    },
    {
        "name": "aoa-agents",
        "role": "role contracts, profiles, handoff posture, memory posture, and evaluation posture",
        "kind": "agent-role-layer",
    },
    {
        "name": "aoa-playbooks",
        "role": "recurring operations, scenario composition, handoffs, fallback paths, and validation posture",
        "kind": "scenario-composition",
    },
    {
        "name": "aoa-kag",
        "role": "derived provenance-aware knowledge substrates and retrieval-ready projections",
        "kind": "knowledge-substrate",
    },
)

KNOWN_REPO_NAMES: tuple[str, ...] = tuple(repo["name"] for repo in KNOWN_REPOSITORIES)
KNOWN_REPO_BY_NAME: dict[str, dict[str, str]] = {repo["name"]: repo for repo in KNOWN_REPOSITORIES}

HIGH_RISK_DIRECTORIES: tuple[str, ...] = (
    ".agents",
    ".codex",
    ".github",
    "bundles",
    "compose",
    "config",
    "docs",
    "env",
    "examples",
    "generated",
    "githooks",
    "manifests",
    "playbooks",
    "profile",
    "quests",
    "schemas",
    "scripts",
    "seed_notes",
    "seed_staging",
    "skills",
    "src",
    "systemd",
    "templates",
    "tests",
)

SKIP_DIR_NAMES: frozenset[str] = frozenset(
    {
        ".git",
        ".hg",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".svn",
        ".tox",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "node_modules",
        "venv",
    }
)

PUBLIC_BASELINE_COUNTS: dict[str, int] = {
    "known_public_repositories": 16,
    "root_agents_observed_lower_bound": 16,
    "validator_declared_nested_agents_lower_bound": 59,
    "additional_nested_agents_observed_lower_bound": 11,
    "agents_md_observed_lower_bound": 86,
}


def posix(path: Path) -> str:
    return path.as_posix()


def relpath(path: Path, root: Path) -> str:
    try:
        return posix(path.relative_to(root)) or "."
    except ValueError:
        return posix(path)


def path_hint(path: Path, workspace_root: Path) -> str:
    try:
        return posix(path.relative_to(workspace_root)) or "."
    except ValueError:
        home = Path.home().resolve()
        try:
            return "~/" + posix(path.relative_to(home))
        except ValueError:
            return f"external:{path.name}"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def line_count(text: str) -> int:
    if not text:
        return 0
    return text.count("\n") + (0 if text.endswith("\n") else 1)


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def iter_agents_files(repo_root: Path) -> list[Path]:
    if not repo_root.is_dir():
        return []
    found: list[Path] = []
    for current_root, dirs, files in os.walk(repo_root):
        current = Path(current_root)
        relative_current = current.relative_to(repo_root)
        dirs[:] = [
            name
            for name in dirs
            if name not in SKIP_DIR_NAMES and not should_skip(relative_current / name)
        ]
        if "AGENTS.md" in files:
            found.append(current / "AGENTS.md")
    return sorted(found, key=lambda path: posix(path.relative_to(repo_root)))


def extract_required_agents_from_validator(validator_path: Path) -> list[str]:
    """Return REQUIRED_AGENTS keys without executing the validator."""
    if not validator_path.is_file():
        return []
    text = read_text(validator_path)
    try:
        tree = ast.parse(text, filename=str(validator_path))
    except SyntaxError:
        return []

    for node in tree.body:
        value_node: ast.AST | None = None
        targets: Sequence[ast.AST] = ()
        if isinstance(node, ast.Assign):
            value_node = node.value
            targets = node.targets
        elif isinstance(node, ast.AnnAssign):
            value_node = node.value
            targets = (node.target,)
        if value_node is None:
            continue
        if not any(
            isinstance(target, ast.Name) and target.id in REQUIRED_AGENTS_VARIABLES
            for target in targets
        ):
            continue
        try:
            value = ast.literal_eval(value_node)
        except (ValueError, TypeError):
            return []
        if not isinstance(value, dict):
            return []
        return sorted(str(key) for key in value if str(key).endswith("AGENTS.md"))
    return []


def agents_file_record(path: Path, repo_root: Path) -> dict[str, Any]:
    relative = Path(relpath(path, repo_root))
    text = read_text(path)
    parent = relative.parent.as_posix()
    return {
        "path": posix(relative),
        "scope": "." if parent == "." else parent,
        "heading_ok": text.lstrip().startswith("# AGENTS.md"),
        "lines": line_count(text),
        "bytes": path.stat().st_size,
    }


def high_risk_dirs(repo_root: Path) -> tuple[list[str], list[str]]:
    present: list[str] = []
    without_local_agents: list[str] = []
    for relative in HIGH_RISK_DIRECTORIES:
        path = repo_root / relative
        if not path.is_dir():
            continue
        present.append(relative)
        if not (path / "AGENTS.md").is_file():
            without_local_agents.append(relative)
    return present, without_local_agents


def scan_repo(repo_root: Path, workspace_root: Path, name: str) -> dict[str, Any]:
    role_record = KNOWN_REPO_BY_NAME.get(
        name, {"name": name, "role": "extra scanned repository", "kind": "extra"}
    )
    agents_paths = iter_agents_files(repo_root)
    agents_by_rel = {relpath(path, repo_root): path for path in agents_paths}
    root_agents = agents_by_rel.get("AGENTS.md")
    nested_agents = [rel for rel in sorted(agents_by_rel) if rel != "AGENTS.md"]
    validator_path = repo_root / "scripts" / "validate_nested_agents.py"
    required_agents = extract_required_agents_from_validator(validator_path)
    required_set = set(required_agents)
    missing_required = [relative for relative in required_agents if not (repo_root / relative).is_file()]
    unvalidated_nested = [relative for relative in nested_agents if relative not in required_set]
    present_risk_dirs, risk_dirs_without_agents = high_risk_dirs(repo_root)

    records = [agents_file_record(path, repo_root) for path in agents_paths]
    issues: list[str] = []
    if not root_agents:
        issues.append("missing root AGENTS.md")
    if nested_agents and not validator_path.is_file():
        issues.append("nested AGENTS.md files exist without scripts/validate_nested_agents.py")
    if missing_required:
        issues.append("validator-required nested AGENTS.md files are missing")
    if any(not record["heading_ok"] for record in records):
        issues.append("one or more AGENTS.md files do not start with '# AGENTS.md'")

    root_lines = line_count(read_text(root_agents)) if root_agents else 0
    if root_lines > ROOT_AGENTS_LONG_LINE_THRESHOLD:
        issues.append(f"root AGENTS.md is long ({root_lines} lines; threshold {ROOT_AGENTS_LONG_LINE_THRESHOLD})")

    return {
        "name": name,
        "kind": role_record["kind"],
        "role": role_record["role"],
        "checkout_state": "scanned",
        "path_hint": path_hint(repo_root, workspace_root),
        "agents_md_count": len(agents_paths),
        "root_agents_present": bool(root_agents),
        "root_agents_line_count": root_lines,
        "long_root_agents": root_lines > ROOT_AGENTS_LONG_LINE_THRESHOLD,
        "nested_agents_count": len(nested_agents),
        "validator_present": validator_path.is_file(),
        "validator_required_count": len(required_agents),
        "validator_required_agents": required_agents,
        "missing_required_agents": missing_required,
        "unvalidated_nested_agents": unvalidated_nested,
        "high_risk_dirs_present": present_risk_dirs,
        "high_risk_dirs_without_agents": risk_dirs_without_agents,
        "agents_files": records,
        "issues": sorted(set(issues)),
    }


def missing_repo_record(name: str) -> dict[str, Any]:
    role_record = KNOWN_REPO_BY_NAME[name]
    return {
        "name": name,
        "kind": role_record["kind"],
        "role": role_record["role"],
        "checkout_state": "missing",
        "path_hint": name,
        "agents_md_count": 0,
        "root_agents_present": False,
        "root_agents_line_count": 0,
        "long_root_agents": False,
        "nested_agents_count": 0,
        "validator_present": False,
        "validator_required_count": 0,
        "validator_required_agents": [],
        "missing_required_agents": [],
        "unvalidated_nested_agents": [],
        "high_risk_dirs_present": [],
        "high_risk_dirs_without_agents": [],
        "agents_files": [],
        "issues": ["known repository checkout not found under workspace root"],
    }


def infer_workspace_root(repo_root: Path) -> Path:
    repo_root = repo_root.resolve()
    parent = repo_root.parent
    sibling_hits = [
        name
        for name in KNOWN_REPO_NAMES
        if name != repo_root.name and (parent / name).is_dir()
    ]
    if repo_root.name in KNOWN_REPO_NAMES and sibling_hits:
        return parent
    return repo_root


def expand_manifest_path(raw_value: str, workspace_root: Path) -> Path:
    expanded = raw_value.replace("{workspace_parent}", str(workspace_root))
    expanded = expanded.replace("{workspace_root}", str(workspace_root))
    return Path(expanded).expanduser().resolve()


def workspace_manifest_repo_paths(workspace_root: Path) -> dict[str, Path]:
    manifest_path = workspace_root / "aoa-sdk" / ".aoa" / "workspace.toml"
    if not manifest_path.is_file():
        return {}
    try:
        data = tomllib.loads(read_text(manifest_path))
    except tomllib.TOMLDecodeError:
        return {}

    repo_paths: dict[str, Path] = {}
    repos = data.get("repos", {})
    if not isinstance(repos, dict):
        return repo_paths
    for name, record in repos.items():
        if not isinstance(name, str) or not isinstance(record, dict):
            continue
        preferred = record.get("preferred", [])
        if isinstance(preferred, str):
            preferred_values = [preferred]
        elif isinstance(preferred, list):
            preferred_values = [value for value in preferred if isinstance(value, str)]
        else:
            preferred_values = []
        for value in preferred_values:
            candidate = expand_manifest_path(value, workspace_root)
            if candidate.is_dir():
                repo_paths[name] = candidate
                break
    return repo_paths


def repo_path_for_name(
    workspace_root: Path,
    name: str,
    manifest_repo_paths: Mapping[str, Path] | None = None,
) -> Path | None:
    if manifest_repo_paths and name in manifest_repo_paths:
        return manifest_repo_paths[name]
    if workspace_root.name == name and (workspace_root / "AGENTS.md").is_file():
        return workspace_root
    candidate = workspace_root / name
    if candidate.is_dir():
        return candidate
    return None


def discover_extra_repos(workspace_root: Path, known_names: set[str]) -> list[tuple[str, Path]]:
    extras: list[tuple[str, Path]] = []
    if not workspace_root.is_dir():
        return extras
    for child in sorted(workspace_root.iterdir(), key=lambda path: path.name.lower()):
        if child.name in known_names or not child.is_dir() or child.name in SKIP_DIR_NAMES:
            continue
        if (child / "AGENTS.md").is_file() or (child / ".git").is_dir():
            extras.append((child.name, child))
    return extras


def summarize(repositories: Sequence[Mapping[str, Any]]) -> dict[str, int]:
    scanned = [repo for repo in repositories if repo["checkout_state"] == "scanned"]
    missing = [repo for repo in repositories if repo["checkout_state"] == "missing"]
    return {
        "known_repositories": len(KNOWN_REPOSITORIES),
        "repositories_listed": len(repositories),
        "repositories_scanned": len(scanned),
        "known_repositories_missing": len([repo for repo in missing if repo["name"] in KNOWN_REPO_BY_NAME]),
        "agents_md_files": sum(int(repo["agents_md_count"]) for repo in scanned),
        "root_agents_present": sum(1 for repo in scanned if repo["root_agents_present"]),
        "nested_agents_files": sum(int(repo["nested_agents_count"]) for repo in scanned),
        "validators_present": sum(1 for repo in scanned if repo["validator_present"]),
        "validator_required_agents": sum(int(repo["validator_required_count"]) for repo in scanned),
        "missing_required_agents": sum(len(repo["missing_required_agents"]) for repo in scanned),
        "unvalidated_nested_agents": sum(len(repo["unvalidated_nested_agents"]) for repo in scanned),
        "high_risk_dirs_without_agents": sum(len(repo["high_risk_dirs_without_agents"]) for repo in scanned),
        "repos_with_issues": sum(1 for repo in repositories if repo["issues"]),
        "long_root_agents": sum(1 for repo in scanned if repo["long_root_agents"]),
    }


def build_agents_map(
    workspace_root: Path,
    *,
    known_repositories: Sequence[str] = KNOWN_REPO_NAMES,
    include_extra_repos: bool = True,
) -> dict[str, Any]:
    workspace_root = workspace_root.resolve()
    known_set = set(known_repositories)
    repositories: list[dict[str, Any]] = []
    manifest_repo_paths = workspace_manifest_repo_paths(workspace_root)

    for name in known_repositories:
        repo_path = repo_path_for_name(workspace_root, name, manifest_repo_paths)
        if repo_path is None:
            repositories.append(missing_repo_record(name))
        else:
            repositories.append(scan_repo(repo_path.resolve(), workspace_root, name))

    if include_extra_repos:
        for name, path in discover_extra_repos(workspace_root, known_set):
            repositories.append(scan_repo(path.resolve(), workspace_root, name))

    return {
        "schema_version": SCHEMA_VERSION,
        "schema_ref": SCHEMA_REF,
        "owner_repo": OWNER_REPO,
        "surface_kind": "agents_map_audit",
        "generated_by": "scripts/audit_agents_map.py",
        "audit_mode": "live-workspace",
        "workspace_root_hint": "workspace-relative; no absolute paths are stored",
        "known_repositories": list(known_repositories),
        "high_risk_directory_kinds": list(HIGH_RISK_DIRECTORIES),
        "totals": summarize(repositories),
        "repositories": repositories,
    }


def build_public_baseline_map() -> dict[str, Any]:
    repositories = [
        {
            "name": repo["name"],
            "kind": repo["kind"],
            "role": repo["role"],
            "checkout_state": "public-baseline",
        }
        for repo in KNOWN_REPOSITORIES
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "schema_ref": SCHEMA_REF,
        "owner_repo": OWNER_REPO,
        "surface_kind": "agents_map_public_baseline",
        "generated_by": "scripts/audit_agents_map.py --public-baseline",
        "audit_mode": "public-baseline",
        "baseline_date": "2026-04-24",
        "baseline_note": "Public lower-bound seed. Run live-workspace mode from the sibling checkout root for exact local counts.",
        "known_repositories": list(KNOWN_REPO_NAMES),
        "high_risk_directory_kinds": list(HIGH_RISK_DIRECTORIES),
        "totals": dict(PUBLIC_BASELINE_COUNTS),
        "repositories": repositories,
    }


def render_markdown(payload: Mapping[str, Any]) -> str:
    totals = payload.get("totals", {})
    repositories = payload.get("repositories", [])
    lines: list[str] = [
        "# AGENTS map",
        "",
        "This map is the audit surface for `AGENTS.md` coverage across the AoA / ToS workspace.",
        "It is not repository doctrine and it does not replace the nearest `AGENTS.md` rule.",
        "",
        "## How to regenerate",
        "",
        "For a live sibling-workspace scan:",
        "",
        "```bash",
        "python scripts/audit_agents_map.py \\",
        "  --workspace-root <workspace-root> \\",
        "  --write generated/agents_map.min.json \\",
        "  --markdown docs/AGENTS_MAP.md",
        "```",
        "",
        "For the public bootstrap baseline:",
        "",
        "```bash",
        "python scripts/audit_agents_map.py --public-baseline \\",
        "  --write generated/agents_map.min.json \\",
        "  --markdown docs/AGENTS_MAP.md",
        "```",
        "",
        "## Current totals",
        "",
    ]
    for key in sorted(totals):
        lines.append(f"- `{key}`: {totals[key]}")
    lines.extend(["", "## Repository coverage", ""])
    lines.append("| Repository | State | AGENTS.md | Nested | Validator | Issues |")
    lines.append("|---|---:|---:|---:|---:|---|")
    for repo in repositories:
        state = repo.get("checkout_state", "unknown")
        agents_count = repo.get("agents_md_count", "")
        nested_count = repo.get("nested_agents_count", "")
        validator = repo.get("validator_present", "")
        issues = repo.get("issues", [])
        if state == "public-baseline":
            agents_count = ""
            nested_count = ""
            validator = ""
            issue_text = "baseline only"
        else:
            issue_text = "; ".join(issues) if issues else ""
        lines.append(
            f"| `{repo['name']}` | `{state}` | {agents_count} | {nested_count} | {validator} | {issue_text} |"
        )
    lines.extend(
        [
            "",
            "## How to read the signals",
            "",
            "- `missing` means the known public repository was not found under the selected workspace root.",
            "- `unvalidated_nested_agents` means a nested `AGENTS.md` exists but is not declared by `scripts/validate_nested_agents.py`.",
            "- `high_risk_dirs_without_agents` marks common contract, generated, test, runtime, or source directories without a direct local instruction file.",
            "- `long_root_agents` marks roots that may be ready for slimming after local instructions are pushed down-tree.",
            "",
            "Use this document as a compass before AGENTS refactors: measure first, then move doctrine to the smallest owner surface.",
            "",
        ]
    )
    return "\n".join(lines)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def write_markdown(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(payload), encoding="utf-8")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit AGENTS.md coverage across an AoA / ToS workspace.")
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT, help="Path to the 8Dionysus repository root.")
    parser.add_argument("--workspace-root", type=Path, help="Sibling workspace root to scan. Defaults to an inferred local root.")
    parser.add_argument("--write", type=Path, help="Write compact JSON payload to this path.")
    parser.add_argument("--markdown", type=Path, help="Write markdown report to this path.")
    parser.add_argument("--public-baseline", action="store_true", help="Emit the public bootstrap baseline instead of scanning local checkouts.")
    parser.add_argument("--no-extra-repos", action="store_true", help="Only list known public repositories; do not add extra sibling checkouts.")
    parser.add_argument("--pretty", action="store_true", help="Print pretty JSON instead of compact JSON.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = args.repo_root.resolve()
    workspace_root = args.workspace_root.resolve() if args.workspace_root else infer_workspace_root(repo_root)
    payload = (
        build_public_baseline_map()
        if args.public_baseline
        else build_agents_map(workspace_root, include_extra_repos=not args.no_extra_repos)
    )

    if args.write:
        write_json(args.write, payload)
    if args.markdown:
        write_markdown(args.markdown, payload)

    if not args.write and not args.markdown:
        indent = 2 if args.pretty else None
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=indent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
