#!/usr/bin/env python3
"""Build the README/AGENTS coverage and review map for the AoA / ToS workspace.

The script is intentionally local-only: it does not call GitHub, MCP servers,
network APIs, or workspace launchers. It scans checked-out repositories and
turns the current tracked README/AGENTS corpus into a compact, reviewable map.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
from typing import Any, Mapping, Sequence

from readme_agents_corpus import (
    AGENTS_CHAIN_BUDGET_BYTES,
    has_level_one_heading,
    load_dispositions,
    scan_repository_corpus,
    scan_shared_root,
    summarize_workspace_corpus,
)

try:
    import tomllib as _tomllib
except ModuleNotFoundError:  # pragma: no cover - exercised on Python 3.10.
    try:
        import tomli as _tomllib  # type: ignore[no-redef]
    except ModuleNotFoundError:  # pragma: no cover - exercised on dependency-free Python 3.10.
        _tomllib = None

if _tomllib is not None:
    TOML_DECODE_ERRORS = (_tomllib.TOMLDecodeError, ValueError, SyntaxError)
else:
    TOML_DECODE_ERRORS = (ValueError, SyntaxError)

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = "8dionysus_agents_map_v2"
SCHEMA_REF = "schemas/agents-map.schema.json"
OWNER_REPO = "8Dionysus"
DEFAULT_DISPOSITIONS_PATH = REPO_ROOT / "manifests" / "readme_agents_dispositions.v1.json"
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
        "name": "abyss-machine",
        "role": "portable host-machine facts, intake, bootstrap, service surfaces, and validation",
        "kind": "host-machine-organ",
    },
    {
        "name": "ATM10-Agent",
        "role": "local-first companion behavior, perception, memory, voice, and safe automation surfaces",
        "kind": "operator-companion",
    },
    {
        "name": "Dionysus",
        "role": "voice-first interview protocols, evidence-grounded claims, human review, and purpose-bounded personal portrait projections",
        "kind": "personal-portrait-protocol",
    },
    {
        "name": "aoa-sdk",
        "role": "typed workspace integration, canonical routing and dispatch, compatibility checks, passive skill inspection, and reviewed evidence handoff",
        "kind": "control-plane-sdk",
    },
    {
        "name": "aoa-dashboard",
        "role": "owner-bounded Goal Space and operator projections with explicit provenance, freshness, missingness, and non-executing action intents",
        "kind": "goal-space-projection",
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
        "role": "shared measurement grammar, owner-local stats federation, and derived non-sovereign read models",
        "kind": "statistical-measurability",
    },
    {
        "name": "aoa-routing",
        "role": "deprecated maintenance-only routing predecessor retained for reversible history and rollback review",
        "kind": "deprecated-routing-predecessor",
    },
    {
        "name": "aoa-memo",
        "role": "explicit memory objects, provenance threads, temporal relevance, salience, and recall contracts",
        "kind": "memory-layer",
    },
    {
        "name": "aoa-session-memory",
        "role": "evidence-linked preservation, inspection, and recovery of long agent-session history",
        "kind": "session-memory-layer",
    },
    {
        "name": "aoa-agents",
        "role": "role contracts, profiles, handoff posture, memory posture, and evaluation posture",
        "kind": "agent-role-layer",
    },
    {
        "name": "aoa-models",
        "role": "exact model identities and realizations, configuration-scoped claims, lifecycle, and fit projections",
        "kind": "model-canon",
    },
    {
        "name": "aoa-agon",
        "role": "governed model-formation lineage, candidate causality, material governance, and scoped lineage continuation",
        "kind": "model-formation-lineage",
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
OPTIONAL_REPO_NAMES: frozenset[str] = frozenset({"aoa-routing"})
PUBLIC_BASELINE_REPOSITORIES: tuple[dict[str, str], ...] = tuple(
    repo for repo in KNOWN_REPOSITORIES if repo["name"] != "aoa-agon"
)
PUBLIC_BASELINE_REPO_NAMES: tuple[str, ...] = tuple(
    repo["name"] for repo in PUBLIC_BASELINE_REPOSITORIES
)

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

REPO_SKIP_DIR_NAMES: dict[str, frozenset[str]] = {
    "Dionysus": frozenset({"legacy"}),
}

PUBLIC_BASELINE_COUNTS: dict[str, int] = {
    "known_public_repositories": 20,
    "required_repository_checkouts": 19,
    "optional_repository_checkouts": 1,
    "root_agents_observed_lower_bound": 19,
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


def should_skip(path: Path, skip_dir_names: frozenset[str] = SKIP_DIR_NAMES) -> bool:
    return any(part in skip_dir_names for part in path.parts)


def iter_agents_files(repo_root: Path, repo_name: str) -> list[Path]:
    if not repo_root.is_dir():
        return []
    skip_dir_names = SKIP_DIR_NAMES | REPO_SKIP_DIR_NAMES.get(repo_name, frozenset())
    found: list[Path] = []
    for current_root, dirs, files in os.walk(repo_root):
        current = Path(current_root)
        relative_current = current.relative_to(repo_root)
        dirs[:] = [
            name
            for name in dirs
            if name not in skip_dir_names
            and not should_skip(relative_current / name, skip_dir_names)
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
        "heading_ok": has_level_one_heading(text),
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


def scan_repo(
    repo_root: Path,
    workspace_root: Path,
    name: str,
    *,
    path_hint_override: str | None = None,
    dispositions: Mapping[tuple[str, str], Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    role_record = KNOWN_REPO_BY_NAME.get(
        name, {"name": name, "role": "extra scanned repository", "kind": "extra"}
    )
    corpus = scan_repository_corpus(repo_root, name, dispositions or {})
    tracked_agents_records = [
        record
        for record in corpus["agents_files"]
        if record["tracked"]
        and record["exists_in_worktree"]
        and not record["scope_flags"]["archive"]
    ]
    agents_paths = [repo_root / record["path"] for record in tracked_agents_records]
    agents_by_rel = {relpath(path, repo_root): path for path in agents_paths}
    root_agents = agents_by_rel.get("AGENTS.md")
    nested_agents = [rel for rel in sorted(agents_by_rel) if rel != "AGENTS.md"]
    validator_path = repo_root / "scripts" / "validate_nested_agents.py"
    required_agents = extract_required_agents_from_validator(validator_path)
    required_set = set(required_agents)
    missing_required = [relative for relative in required_agents if not (repo_root / relative).is_file()]
    unvalidated_nested = [relative for relative in nested_agents if relative not in required_set]
    present_risk_dirs, risk_dirs_without_agents = high_risk_dirs(repo_root)

    records = corpus["agents_files"]
    issues: list[str] = []
    if not root_agents:
        issues.append("missing root AGENTS.md")
    if nested_agents and not validator_path.is_file():
        issues.append("nested AGENTS.md files exist without scripts/validate_nested_agents.py")
    if missing_required:
        issues.append("validator-required nested AGENTS.md files are missing")
    if any(
        not record["heading_ok"]
        for record in records
        if record["tracked"] and record["exists_in_worktree"]
    ):
        issues.append("one or more AGENTS.md files do not start with a level-one heading")

    root_lines = line_count(read_text(root_agents)) if root_agents else 0
    if root_lines > ROOT_AGENTS_LONG_LINE_THRESHOLD:
        issues.append(f"root AGENTS.md is long ({root_lines} lines; threshold {ROOT_AGENTS_LONG_LINE_THRESHOLD})")
    repeated_groups = corpus["readme_agents_summary"][
        "authored_repeated_long_agents_block_groups"
    ]
    if repeated_groups:
        issues.append(
            f"authored AGENTS.md corpus has {repeated_groups} repeated long prose block group(s)"
        )
    duplicate_commands = corpus["readme_agents_summary"][
        "duplicate_validation_command_groups"
    ]
    if duplicate_commands:
        issues.append(
            f"active authored VALIDATION.md corpus has {duplicate_commands} exact duplicate command group(s)"
        )
    agents_command_overlaps = corpus["readme_agents_summary"][
        "agents_validation_command_overlap_groups"
    ]
    if agents_command_overlaps:
        issues.append(
            f"active AGENTS.md corpus repeats {agents_command_overlaps} validation command group(s)"
        )
    route_only_claim_conflicts = corpus["readme_agents_summary"][
        "validation_route_only_claim_conflicts"
    ]
    if route_only_claim_conflicts:
        issues.append(
            "active VALIDATION.md corpus has "
            f"{route_only_claim_conflicts} route-only ownership claim(s) in files that contain executable commands"
        )
    unclassified_fences = corpus["readme_agents_summary"][
        "active_authored_agents_unclassified_fenced_blocks"
    ]
    if unclassified_fences:
        issues.append(
            f"active AGENTS.md corpus has {unclassified_fences} unclassified fenced block(s)"
        )
    fenced_executables = corpus["readme_agents_summary"][
        "active_authored_agents_fenced_executable_invocations"
    ]
    if fenced_executables:
        issues.append(
            f"active AGENTS.md fences retain {fenced_executables} executable invocation(s)"
        )
    stale_fences = corpus["readme_agents_summary"][
        "stale_agents_fenced_block_classifications"
    ]
    if stale_fences:
        issues.append(
            f"AGENTS fence ledger has {stale_fences} stale classification(s)"
        )
    unclassified_design_fences = corpus["readme_agents_summary"][
        "active_authored_design_agents_unclassified_fenced_blocks"
    ]
    if unclassified_design_fences:
        issues.append(
            "active DESIGN.AGENTS.md corpus has "
            f"{unclassified_design_fences} unclassified fenced block(s)"
        )
    design_fenced_executables = corpus["readme_agents_summary"][
        "active_authored_design_agents_fenced_executable_invocations"
    ]
    if design_fenced_executables:
        issues.append(
            "active DESIGN.AGENTS.md fences retain "
            f"{design_fenced_executables} executable invocation(s)"
        )
    stale_design_fences = corpus["readme_agents_summary"][
        "stale_design_agents_fenced_block_classifications"
    ]
    if stale_design_fences:
        issues.append(
            "DESIGN.AGENTS fence ledger has "
            f"{stale_design_fences} stale classification(s)"
        )

    return {
        "name": name,
        "kind": role_record["kind"],
        "role": role_record["role"],
        "checkout_requirement": checkout_requirement(name),
        "checkout_state": "scanned",
        "path_hint": path_hint_override or path_hint(repo_root, workspace_root),
        "corpus_source": corpus["corpus_source"],
        "git_snapshot": corpus["git_snapshot"],
        "readme_agents_summary": corpus["readme_agents_summary"],
        "repeated_long_agents_blocks": corpus["repeated_long_agents_blocks"],
        "validation_files": corpus["validation_files"],
        "duplicate_validation_commands": corpus["duplicate_validation_commands"],
        "agents_validation_command_overlaps": corpus[
            "agents_validation_command_overlaps"
        ],
        "readme_validation_command_overlaps": corpus[
            "readme_validation_command_overlaps"
        ],
        "validation_route_only_claim_conflicts": corpus[
            "validation_route_only_claim_conflicts"
        ],
        "agents_md_count": len(tracked_agents_records),
        "readme_md_count": corpus["readme_agents_summary"]["tracked_readme_files"],
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
        "readme_files": corpus["readme_files"],
        "design_agents_files": corpus["design_agents_files"],
        "issues": sorted(set(issues)),
    }


def missing_repo_record(name: str) -> dict[str, Any]:
    role_record = KNOWN_REPO_BY_NAME[name]
    requirement = checkout_requirement(name)
    return {
        "name": name,
        "kind": role_record["kind"],
        "role": role_record["role"],
        "checkout_requirement": requirement,
        "checkout_state": "missing",
        "path_hint": name,
        "corpus_source": "unavailable",
        "git_snapshot": {
            "git_available": False,
            "remote_currentness": "unavailable",
        },
        "readme_agents_summary": {
            "tracked_document_files": 0,
            "tracked_agents_files": 0,
            "tracked_readme_files": 0,
            "tracked_document_bytes": 0,
            "tracked_agents_bytes": 0,
            "tracked_readme_bytes": 0,
            "tracked_design_agents_files": 0,
            "tracked_design_agents_bytes": 0,
            "untracked_design_agents_candidates": 0,
            "untracked_document_candidates": 0,
            "paired_directories": 0,
            "readme_only_directories": 0,
            "agents_only_directories": 0,
            "chain_scopes": 0,
            "chain_p50_bytes": 0,
            "chain_p95_bytes": 0,
            "chain_max_bytes": 0,
            "chain_scopes_over_budget": 0,
            "repeated_long_agents_block_groups": 0,
            "authored_repeated_long_agents_block_groups": 0,
            "excluded_repeated_long_agents_block_groups": 0,
            "repeated_long_agents_block_instances": 0,
            "repeated_long_agents_normalized_redundant_bytes": 0,
            "tracked_validation_files": 0,
            "untracked_validation_candidates": 0,
            "active_authored_validation_files": 0,
            "active_authored_validation_bytes": 0,
            "active_authored_validation_command_owner_files": 0,
            "active_authored_validation_route_only_files": 0,
            "active_authored_validation_invocations": 0,
            "active_authored_unique_validation_invocations": 0,
            "duplicate_validation_command_groups": 0,
            "duplicate_validation_command_occurrences": 0,
            "agents_validation_command_overlap_groups": 0,
            "readme_validation_command_overlap_groups": 0,
            "validation_route_only_claim_conflicts": 0,
            "agents_files_referencing_readme": 0,
            "agents_files_declaring_mandatory_readme": 0,
            "declared_mandatory_readme_bytes": 0,
            "agents_readme_reference_lines": 0,
            "agents_conditional_readme_reference_lines": 0,
            "agents_navigational_readme_reference_lines": 0,
            "agents_fenced_example_readme_reference_lines": 0,
            "active_authored_agents_fenced_blocks": 0,
            "active_authored_agents_classified_fenced_blocks": 0,
            "active_authored_agents_unclassified_fenced_blocks": 0,
            "active_authored_agents_fenced_executable_invocations": 0,
            "stale_agents_fenced_block_classifications": 0,
            "active_authored_design_agents_fenced_blocks": 0,
            "active_authored_design_agents_classified_fenced_blocks": 0,
            "active_authored_design_agents_unclassified_fenced_blocks": 0,
            "active_authored_design_agents_fenced_executable_invocations": 0,
            "stale_design_agents_fenced_block_classifications": 0,
            "reviewed_files": 0,
            "blocked_files": 0,
            "unreviewed_files": 0,
            "disposition_counts": {},
        },
        "agents_md_count": 0,
        "readme_md_count": 0,
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
        "readme_files": [],
        "design_agents_files": [],
        "validation_files": [],
        "repeated_long_agents_blocks": [],
        "duplicate_validation_commands": [],
        "agents_validation_command_overlaps": [],
        "readme_validation_command_overlaps": [],
        "validation_route_only_claim_conflicts": [],
        "issues": (
            []
            if requirement == "optional"
            else ["known repository checkout not found under workspace root"]
        ),
    }


def checkout_requirement(name: str) -> str:
    return "optional" if name in OPTIONAL_REPO_NAMES else "required"


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


def _strip_toml_inline_comment(line: str) -> str:
    in_single_quote = False
    in_double_quote = False
    escaped = False
    for index, char in enumerate(line):
        if escaped:
            escaped = False
            continue
        if in_double_quote and char == "\\":
            escaped = True
            continue
        if char == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
            continue
        if char == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
            continue
        if char == "#" and not in_single_quote and not in_double_quote:
            return line[:index].rstrip()
    return line.rstrip()


def _parse_limited_toml_value(raw_value: str) -> Any:
    value = raw_value.strip()
    if not value:
        raise ValueError("empty TOML value")
    if value[0] in {"'", '"'} or value.startswith("["):
        parsed = ast.literal_eval(value)
        if isinstance(parsed, (str, list)):
            return parsed
        raise ValueError(f"unsupported TOML value: {raw_value}")
    if value.isdigit():
        return int(value)
    raise ValueError(f"unsupported TOML value: {raw_value}")


def _parse_limited_workspace_toml(text: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_table: list[str] | None = None
    for raw_line in text.splitlines():
        line = _strip_toml_inline_comment(raw_line).strip()
        if not line:
            continue
        if line.startswith("[") and line.endswith("]"):
            table_name = line[1:-1].strip()
            if not table_name:
                raise ValueError("empty TOML table name")
            current_table = table_name.split(".")
            target = data
            for part in current_table:
                if not part:
                    raise ValueError(f"invalid TOML table name: {table_name}")
                next_target = target.setdefault(part, {})
                if not isinstance(next_target, dict):
                    raise ValueError(f"TOML table conflicts with value: {table_name}")
                target = next_target
            continue
        if "=" not in line:
            raise ValueError(f"unsupported TOML line: {raw_line}")
        key, raw_value = line.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"empty TOML key: {raw_line}")
        target = data
        if current_table:
            for part in current_table:
                target = target[part]
        target[key] = _parse_limited_toml_value(raw_value)
    return data


def load_workspace_toml(text: str) -> Mapping[str, Any]:
    if _tomllib is not None:
        return _tomllib.loads(text)
    return _parse_limited_workspace_toml(text)


def workspace_manifest_repo_paths(workspace_root: Path) -> dict[str, Path]:
    manifest_path = workspace_root / "aoa-sdk" / ".aoa" / "workspace.toml"
    if not manifest_path.is_file():
        return {}
    try:
        data = load_workspace_toml(read_text(manifest_path))
    except TOML_DECODE_ERRORS:
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
        "known_repositories_missing": len(
            [
                repo
                for repo in missing
                if repo["name"] in KNOWN_REPO_BY_NAME
                and repo.get("checkout_requirement", "required") == "required"
            ]
        ),
        "optional_repositories_missing": len(
            [
                repo
                for repo in missing
                if repo["name"] in KNOWN_REPO_BY_NAME
                and repo.get("checkout_requirement") == "optional"
            ]
        ),
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
    owner_repo_root: Path | None = None,
    disposition_manifest_path: Path | None = DEFAULT_DISPOSITIONS_PATH,
    use_workspace_manifest: bool = True,
) -> dict[str, Any]:
    workspace_root = workspace_root.resolve()
    owner_repo_root = owner_repo_root.resolve() if owner_repo_root else None
    known_set = set(known_repositories)
    repositories: list[dict[str, Any]] = []
    manifest_repo_paths = (
        workspace_manifest_repo_paths(workspace_root) if use_workspace_manifest else {}
    )
    dispositions, disposition_issues = load_dispositions(disposition_manifest_path)

    for name in known_repositories:
        owner_override = name == OWNER_REPO and owner_repo_root is not None
        repo_path = (
            owner_repo_root
            if owner_override
            else repo_path_for_name(workspace_root, name, manifest_repo_paths)
        )
        if repo_path is None:
            repositories.append(missing_repo_record(name))
        else:
            repositories.append(
                scan_repo(
                    repo_path.resolve(),
                    workspace_root,
                    name,
                    path_hint_override=name if owner_override else None,
                    dispositions=dispositions,
                )
            )

    if include_extra_repos:
        for name, path in discover_extra_repos(workspace_root, known_set):
            repositories.append(
                scan_repo(
                    path.resolve(),
                    workspace_root,
                    name,
                    dispositions=dispositions,
                )
            )

    resolved_owner_root = owner_repo_root or repo_path_for_name(
        workspace_root, OWNER_REPO, manifest_repo_paths
    )
    shared_root = (
        scan_shared_root(workspace_root, resolved_owner_root, dispositions)
        if resolved_owner_root is not None
        else {"files": []}
    )
    observed_disposition_keys = {
        (repo["name"], record["path"])
        for repo in repositories
        if repo.get("checkout_state") == "scanned"
        for record in [
            *repo.get("agents_files", []),
            *repo.get("readme_files", []),
            *repo.get("design_agents_files", []),
        ]
    }
    observed_disposition_keys.update(
        ("@workspace-root", record["path"])
        for record in shared_root.get("files", [])
    )
    for repository, path in sorted(set(dispositions) - observed_disposition_keys):
        record = dispositions[(repository, path)]
        expected_absence = (
            record.get("review_state") == "reviewed"
            and record.get("disposition") == "delete-obsolete-placeholder"
        )
        if not expected_absence:
            disposition_issues.append(
                f"disposition target is absent from current corpus: {repository}:{path}"
            )
    totals = summarize(repositories)
    totals.update(summarize_workspace_corpus(repositories, shared_root))

    return {
        "schema_version": SCHEMA_VERSION,
        "schema_ref": SCHEMA_REF,
        "owner_repo": OWNER_REPO,
        "surface_kind": "agents_map_audit",
        "generated_by": "scripts/audit_agents_map.py",
        "audit_mode": "live-workspace",
        "workspace_root_hint": "workspace-relative; no absolute paths are stored",
        "corpus_contract": {
            "canonical_scope": "git-tracked README.md and AGENTS.md in known owner repositories; tracked DESIGN.AGENTS.md is audited separately as an on-demand related design surface and excluded from inherited-chain bytes",
            "untracked_posture": "reported separately as candidates",
            "chain_budget_bytes": AGENTS_CHAIN_BUDGET_BYTES,
            "chain_percentile_method": "nearest-rank over unique document-directory scopes",
            "repeated_agents_block_threshold": "exact normalized prose, at least 180 bytes in at least 4 tracked AGENTS.md files; fenced examples excluded",
            "validation_command_ownership": "one exact executable invocation per active authored human owner inside each repository; other validation surfaces route by link, lane, runner, or manifest key",
            "validation_command_exclusions": "generated, vendor, fixture, and archive validation surfaces; README overlap is reported for owner review",
            "remote_currentness": "not claimed; refs are local snapshots until owner refresh",
            "disposition_authority": "owner evidence; this integration ledger does not decide sibling meaning",
            "workspace_manifest_used": use_workspace_manifest,
        },
        "disposition_manifest": (
            "manifests/readme_agents_dispositions.v1.json"
            if disposition_manifest_path is not None
            else None
        ),
        "disposition_issues": disposition_issues,
        "known_repositories": list(known_repositories),
        "high_risk_directory_kinds": list(HIGH_RISK_DIRECTORIES),
        "totals": totals,
        "shared_root": shared_root,
        "repositories": repositories,
    }


def build_public_baseline_map() -> dict[str, Any]:
    repositories = [
        {
            "name": repo["name"],
            "kind": repo["kind"],
            "role": repo["role"],
            "checkout_requirement": checkout_requirement(repo["name"]),
            "checkout_state": "public-baseline",
        }
        for repo in PUBLIC_BASELINE_REPOSITORIES
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
        "known_repositories": list(PUBLIC_BASELINE_REPO_NAMES),
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
        "This map is the audit and owner-review surface for the tracked `README.md` / `AGENTS.md` corpus across the AoA / ToS workspace.",
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
        "For a merge-bound baseline, scan an isolated matrix of clean owner worktrees and disable workspace-manifest redirection:",
        "",
        "```bash",
        "python scripts/audit_agents_map.py \\",
        "  --workspace-root <clean-worktree-matrix> \\",
        "  --repo-root <clean-worktree-matrix>/8Dionysus \\",
        "  --no-extra-repos --ignore-workspace-manifest \\",
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
        "After changing local `AGENTS.md` coverage, regenerate the frontier reconnaissance report:",
        "",
        "```bash",
        "python scripts/recon_agents_frontier.py \\",
        "  --map generated/agents_map.min.json \\",
        "  --write generated/agents_frontier_recon.min.json \\",
        "  --markdown generated/agents_frontier_recon.md",
        "```",
        "",
        "For reading guidance, see [AGENTS_FRONTIER_RECON](AGENTS_FRONTIER_RECON.md).",
        "",
        "## Current totals",
        "",
    ]
    for key in sorted(totals):
        lines.append(f"- `{key}`: {totals[key]}")
    lines.extend(["", "## Repository coverage", ""])
    lines.append(
        "| Repository | State | AGENTS corpus/active | README | VALIDATION files/cmds/duplicates | Pairs | Unique chain p95/max | Over 32 KiB authored/excluded | Repeated long blocks/redundant bytes | Reviewed/unreviewed | Issues |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for repo in repositories:
        state = repo.get("checkout_state", "unknown")
        agents_count = repo.get("agents_md_count", "")
        readme_count = repo.get("readme_md_count", "")
        summary = repo.get("readme_agents_summary", {})
        agents_corpus_count = summary.get("tracked_agents_files", agents_count)
        validation_files = summary.get("active_authored_validation_files", "")
        validation_commands = summary.get("active_authored_validation_invocations", "")
        validation_duplicates = summary.get("duplicate_validation_command_groups", "")
        pairs = summary.get("paired_directories", "")
        p95 = summary.get("unique_chain_p95_bytes", "")
        maximum = summary.get("unique_chain_max_bytes", "")
        over_budget_authored = summary.get("authored_unique_chains_over_budget", "")
        over_budget_excluded = summary.get("excluded_unique_chains_over_budget", "")
        repeated_groups = summary.get("authored_repeated_long_agents_block_groups", "")
        repeated_bytes = summary.get(
            "repeated_long_agents_normalized_redundant_bytes", ""
        )
        reviewed = summary.get("reviewed_files", "")
        unreviewed = summary.get("unreviewed_files", "")
        issues = repo.get("issues", [])
        if state == "public-baseline":
            agents_count = ""
            agents_corpus_count = ""
            readme_count = ""
            validation_files = ""
            validation_commands = ""
            validation_duplicates = ""
            pairs = ""
            p95 = ""
            maximum = ""
            over_budget_authored = ""
            over_budget_excluded = ""
            repeated_groups = ""
            repeated_bytes = ""
            reviewed = ""
            unreviewed = ""
            issue_text = "baseline only"
        else:
            issue_text = "; ".join(issues) if issues else ""
        lines.append(
            f"| `{repo['name']}` | `{state}` | {agents_corpus_count}/{agents_count} | {readme_count} | "
            f"{validation_files}/{validation_commands}/{validation_duplicates} | {pairs} | "
            f"{p95}/{maximum} | {over_budget_authored}/{over_budget_excluded} | "
            f"{repeated_groups}/{repeated_bytes} | "
            f"{reviewed}/{unreviewed} | {issue_text} |"
        )
    shared_root = payload.get("shared_root", {})
    if shared_root.get("files"):
        lines.extend(
            [
                "",
                "## Shared-root projection posture",
                "",
                "| File | Declared projection | Owner parity | Review |",
                "|---|---:|---:|---|",
            ]
        )
        for record in shared_root["files"]:
            review = record.get("review", {}).get("review_state", "unreviewed")
            lines.append(
                f"| `{record['path']}` | {record['declared_projection_surface']} | "
                f"{record['owner_parity']} | `{review}` |"
            )
    lines.extend(
        [
            "",
            "## How to read the signals",
            "",
            "- `missing` means the known public repository was not found under the selected workspace root.",
            "- `checkout_requirement: optional` means an absent retained predecessor is valid and does not create an audit issue.",
            "- Corpus counts use Git-tracked `README.md` and `AGENTS.md`; untracked documents are candidates, not canonical corpus members.",
            "- `tracked_design_agents_files` counts the related on-demand `DESIGN.AGENTS.md` corpus separately; these files require review and fenced-block classification but do not inflate inherited AGENTS-chain bytes.",
            "- `chain_scopes` measures unique document directories; `unique_agents_chains` collapses directories that inherit the same AGENTS path signature.",
            "- Chain percentiles use the nearest-rank method; the repository table reports unique chain signatures.",
            "- `Repeated long blocks` counts exact normalized prose blocks of at least 180 bytes appearing in at least four tracked `AGENTS.md` files; fenced examples are excluded and redundant bytes count copies beyond the first.",
            "- `VALIDATION files/cmds/duplicates` counts active authored on-demand files, normalized shell invocations, and exact command groups with more than one human owner inside one repository. Generated, vendor, fixture, and archive surfaces are excluded.",
            "- `readme_validation_command_overlap_groups` is a review signal: a public usage example may be valid, but required validation should route to its one procedure owner.",
            "- Dispositions remain `unreviewed` until an owner-evidenced record is added to the integration manifest.",
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
    parser = argparse.ArgumentParser(description="Audit README/AGENTS coverage across an AoA / ToS workspace.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Path to the 8Dionysus owner checkout to scan; also used to infer the workspace root.",
    )
    parser.add_argument("--workspace-root", type=Path, help="Sibling workspace root to scan. Defaults to an inferred local root.")
    parser.add_argument("--write", type=Path, help="Write compact JSON payload to this path.")
    parser.add_argument("--markdown", type=Path, help="Write markdown report to this path.")
    parser.add_argument(
        "--dispositions",
        type=Path,
        default=DEFAULT_DISPOSITIONS_PATH,
        help="Owner-evidenced README/AGENTS disposition overlay.",
    )
    parser.add_argument("--public-baseline", action="store_true", help="Emit the public bootstrap baseline instead of scanning local checkouts.")
    parser.add_argument("--no-extra-repos", action="store_true", help="Only list known public repositories; do not add extra sibling checkouts.")
    parser.add_argument(
        "--ignore-workspace-manifest",
        action="store_true",
        help="Resolve repository names only beneath --workspace-root (useful for an isolated clean-worktree matrix).",
    )
    parser.add_argument("--pretty", action="store_true", help="Print pretty JSON instead of compact JSON.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = args.repo_root.resolve()
    workspace_root = args.workspace_root.resolve() if args.workspace_root else infer_workspace_root(repo_root)
    payload = (
        build_public_baseline_map()
        if args.public_baseline
        else build_agents_map(
            workspace_root,
            include_extra_repos=not args.no_extra_repos,
            owner_repo_root=repo_root,
            disposition_manifest_path=args.dispositions,
            use_workspace_manifest=not args.ignore_workspace_manifest,
        )
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
