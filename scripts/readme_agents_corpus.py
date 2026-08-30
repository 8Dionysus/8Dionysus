#!/usr/bin/env python3
"""Read-only README/AGENTS corpus measurements for the workspace map.

The module reads local Git worktrees only.  It never fetches, mutates sibling
repositories, or treats the integration ledger as sibling-owner authority.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence


DOCUMENT_NAMES = frozenset({"AGENTS.md", "README.md"})
AGENTS_CHAIN_BUDGET_BYTES = 32 * 1024
DISPOSITIONS_SCHEMA_VERSION = "8dionysus_readme_agents_dispositions_v1"
DISPOSITIONS = frozenset(
    {
        "keep",
        "slim-rewrite",
        "merge-into-parent-agents",
        "merge-into-parent-readme",
        "move-to-owner-source",
        "generate-from-owner-source",
        "delete-obsolete-placeholder",
    }
)
REVIEW_STATES = frozenset({"reviewed", "blocked"})
FALLBACK_SKIP_DIRS = frozenset(
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
        "node_modules",
        "venv",
    }
)
GENERATED_PARTS = frozenset({"build", "dist", "generated"})
VENDOR_PARTS = frozenset({".repos", "node_modules", "third_party", "vendor", "vendored"})
FIXTURE_PARTS = frozenset({"fixture", "fixtures", "testdata"})
ARCHIVE_PARTS = frozenset({"archive", "archived", "legacy"})
README_TOKEN_RE = re.compile(r"(?P<path>(?:\.\.?/)?[A-Za-z0-9_.@+-]+(?:/[A-Za-z0-9_.@+-]+)*/README\.md|README\.md)")
DOC_LINK_RE = re.compile(
    r"\[[^\]]*\]\((?P<link>[^)]+(?:README|AGENTS)\.md(?:#[^)]*)?)\)"
)
MANDATORY_READ_RE = re.compile(
    r"\b(read|before|start\s+here|прочит\w*|сначала|изуч\w*)\b",
    re.IGNORECASE,
)
NEGATED_READ_RE = re.compile(
    r"\b(do\s+not|don't|not\s+required|optional|не\s+(?:читать|нужно|требуется))\b",
    re.IGNORECASE,
)
MARKDOWN_HEADING_RE = re.compile(r"^(?P<marks>#{1,6})\s+(?P<title>.+?)\s*$")
MANDATORY_READ_SECTION_RE = re.compile(
    r"\b(read\s+before(?:\s+editing|\s+changing)?|reading\s+order|read\s+first|"
    r"required\s+reading|порядок\s+чтения|прочитать\s+перед|сначала\s+прочитать)\b",
    re.IGNORECASE,
)


def _run_git(repo_root: Path, args: Sequence[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(repo_root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )


def _git_text(repo_root: Path, args: Sequence[str]) -> str | None:
    result = _run_git(repo_root, args)
    if result.returncode != 0:
        return None
    return result.stdout.decode("utf-8", errors="replace").strip() or None


def _git_nul_paths(repo_root: Path, args: Sequence[str]) -> list[str] | None:
    result = _run_git(repo_root, args)
    if result.returncode != 0:
        return None
    return sorted(
        value.decode("utf-8", errors="surrogateescape")
        for value in result.stdout.split(b"\0")
        if value
    )


def _is_document(path: str) -> bool:
    return PurePosixPath(path).name in DOCUMENT_NAMES


def _fallback_document_paths(repo_root: Path) -> list[str]:
    found: list[str] = []
    for current_root, dirs, files in os.walk(repo_root):
        current = Path(current_root)
        dirs[:] = [name for name in dirs if name not in FALLBACK_SKIP_DIRS]
        for name in DOCUMENT_NAMES.intersection(files):
            found.append((current / name).relative_to(repo_root).as_posix())
    return sorted(found)


def _status_map(repo_root: Path) -> tuple[dict[str, str], int]:
    result = _run_git(repo_root, ["status", "--porcelain=v1", "-z", "--untracked-files=all"])
    if result.returncode != 0:
        return {}, 0
    items = result.stdout.split(b"\0")
    statuses: dict[str, str] = {}
    index = 0
    count = 0
    while index < len(items):
        raw = items[index]
        index += 1
        if not raw:
            continue
        text = raw.decode("utf-8", errors="surrogateescape")
        if len(text) < 4:
            continue
        status = text[:2]
        path = text[3:]
        statuses[path] = status
        count += 1
        if "R" in status or "C" in status:
            index += 1
    return statuses, count


def git_snapshot(repo_root: Path) -> dict[str, Any]:
    head = _git_text(repo_root, ["rev-parse", "HEAD"])
    branch = _git_text(repo_root, ["branch", "--show-current"])
    origin_main = _git_text(repo_root, ["rev-parse", "--verify", "refs/remotes/origin/main"])
    ahead = behind = None
    if head and origin_main:
        counts = _git_text(repo_root, ["rev-list", "--left-right", "--count", "HEAD...origin/main"])
        if counts:
            left, right = counts.split()
            ahead, behind = int(left), int(right)
    statuses, status_entries = _status_map(repo_root)
    return {
        "head": head,
        "branch": branch,
        "origin_main": origin_main,
        "ahead_of_origin_main": ahead,
        "behind_origin_main": behind,
        "worktree_clean": status_entries == 0,
        "worktree_status_entries": status_entries,
        "remote_currentness": "not-claimed-local-ref-only",
        "git_available": head is not None,
        "_statuses": statuses,
    }


def load_dispositions(path: Path | None) -> tuple[dict[tuple[str, str], dict[str, Any]], list[str]]:
    if path is None or not path.is_file():
        return {}, []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"cannot load disposition manifest: {exc}"]
    issues: list[str] = []
    if payload.get("schema_version") != DISPOSITIONS_SCHEMA_VERSION:
        issues.append("unexpected disposition manifest schema_version")
    records: dict[tuple[str, str], dict[str, Any]] = {}
    for index, record in enumerate(payload.get("records", [])):
        if not isinstance(record, dict):
            issues.append(f"disposition record {index} is not an object")
            continue
        repository = record.get("repository")
        document_path = record.get("path")
        state = record.get("review_state")
        disposition = record.get("disposition")
        evidence = record.get("owner_evidence", [])
        key = (repository, document_path)
        if not isinstance(repository, str) or not isinstance(document_path, str):
            issues.append(f"disposition record {index} lacks repository/path")
            continue
        if state not in REVIEW_STATES:
            issues.append(f"{repository}:{document_path} has invalid review_state")
            continue
        if state == "reviewed" and disposition not in DISPOSITIONS:
            issues.append(f"{repository}:{document_path} has invalid disposition")
            continue
        if state == "blocked" and disposition is not None:
            issues.append(f"{repository}:{document_path} blocked record must not decide disposition")
            continue
        if not isinstance(evidence, list) or not all(isinstance(value, str) for value in evidence):
            issues.append(f"{repository}:{document_path} has invalid owner_evidence")
            continue
        if state == "reviewed" and not evidence:
            issues.append(f"{repository}:{document_path} reviewed record lacks owner_evidence")
            continue
        if key in records:
            issues.append(f"duplicate disposition record for {repository}:{document_path}")
            continue
        records[key] = record
    return records, issues


def _read_document(repo_root: Path, relative: str, tracked: bool) -> tuple[bytes, str, bool]:
    path = repo_root / relative
    if path.is_file():
        return path.read_bytes(), "working-tree", True
    if tracked:
        result = _run_git(repo_root, ["show", f"HEAD:{relative}"])
        if result.returncode == 0:
            return result.stdout, "head-fallback-for-missing-worktree-file", False
    return b"", "unavailable", False


def _scope_flags(relative: str) -> dict[str, bool]:
    parts = set(PurePosixPath(relative).parts[:-1])
    return {
        "root": len(PurePosixPath(relative).parts) == 1,
        "generated": bool(parts & GENERATED_PARTS),
        "vendor": bool(parts & VENDOR_PARTS),
        "fixture": bool(parts & FIXTURE_PARTS),
        "archive": bool(parts & ARCHIVE_PARTS),
        "mechanics": "mechanics" in parts,
    }


def _resolve_relative_reference(source: str, raw_target: str) -> str | None:
    target = raw_target.split("#", 1)[0].strip()
    if not target or "://" in target or target.startswith("/"):
        return None
    source_parent = PurePosixPath(source).parent
    normalized = PurePosixPath(os.path.normpath((source_parent / target).as_posix()))
    if normalized.parts and normalized.parts[0] == "..":
        return None
    return normalized.as_posix()


def _extract_references(source: str, text: str, known_paths: set[str]) -> dict[str, Any]:
    readme_lines: list[int] = []
    mandatory_lines: list[int] = []
    resolved_readmes: set[str] = set()
    mandatory_resolved_readmes: set[str] = set()
    unresolved_readmes: set[str] = set()
    outbound_docs: set[str] = set()
    mandatory_section_level: int | None = None
    for line_number, line in enumerate(text.splitlines(), start=1):
        heading = MARKDOWN_HEADING_RE.match(line.strip())
        if heading:
            level = len(heading.group("marks"))
            if mandatory_section_level is not None and level <= mandatory_section_level:
                mandatory_section_level = None
            title = heading.group("title")
            if MANDATORY_READ_SECTION_RE.search(title) and not NEGATED_READ_RE.search(title):
                mandatory_section_level = level
        readme_tokens = [match.group("path") for match in README_TOKEN_RE.finditer(line)]
        if readme_tokens:
            readme_lines.append(line_number)
            mandatory = (
                bool(MANDATORY_READ_RE.search(line))
                or mandatory_section_level is not None
            ) and not NEGATED_READ_RE.search(line)
            if mandatory:
                mandatory_lines.append(line_number)
            for token in readme_tokens:
                resolved = _resolve_relative_reference(source, token)
                if resolved and resolved in known_paths:
                    resolved_readmes.add(resolved)
                    if mandatory:
                        mandatory_resolved_readmes.add(resolved)
                else:
                    unresolved_readmes.add(token)
        for match in DOC_LINK_RE.finditer(line):
            resolved = _resolve_relative_reference(source, match.group("link"))
            if resolved and resolved in known_paths:
                outbound_docs.add(resolved)
    return {
        "readme_reference_lines": readme_lines,
        "mandatory_readme_reference_lines": mandatory_lines,
        "resolved_readme_references": sorted(resolved_readmes),
        "mandatory_resolved_readme_references": sorted(mandatory_resolved_readmes),
        "unresolved_readme_references": sorted(unresolved_readmes),
        "outbound_document_links": sorted(outbound_docs),
    }


def _chain_paths(relative: str, active_agents: Mapping[str, Mapping[str, Any]]) -> list[str]:
    parent = PurePosixPath(relative).parent
    parts = () if parent.as_posix() == "." else parent.parts
    candidates = ["AGENTS.md"]
    for depth in range(1, len(parts) + 1):
        candidates.append(PurePosixPath(*parts[:depth], "AGENTS.md").as_posix())
    return [candidate for candidate in candidates if candidate in active_agents]


def _nearest_rank(values: Sequence[int], percentile: float) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    index = max(0, math.ceil(percentile * len(ordered)) - 1)
    return ordered[index]


def _review_record(
    repository: str,
    relative: str,
    dispositions: Mapping[tuple[str, str], Mapping[str, Any]],
) -> dict[str, Any]:
    record = dispositions.get((repository, relative))
    if not record:
        return {
            "review_state": "unreviewed",
            "disposition": None,
            "owner_evidence": [],
            "note": None,
        }
    return {
        "review_state": record["review_state"],
        "disposition": record.get("disposition"),
        "owner_evidence": list(record.get("owner_evidence", [])),
        "note": record.get("note"),
    }


def scan_repository_corpus(
    repo_root: Path,
    repository: str,
    dispositions: Mapping[tuple[str, str], Mapping[str, Any]],
) -> dict[str, Any]:
    snapshot = git_snapshot(repo_root)
    statuses = snapshot.pop("_statuses")
    tracked_paths = _git_nul_paths(repo_root, ["ls-files", "-z"])
    if tracked_paths is None:
        tracked_documents = _fallback_document_paths(repo_root)
        untracked_documents: list[str] = []
        corpus_source = "filesystem-fallback"
    else:
        tracked_documents = [path for path in tracked_paths if _is_document(path)]
        untracked_paths = _git_nul_paths(repo_root, ["ls-files", "-z", "--others", "--exclude-standard"])
        untracked_documents = [path for path in (untracked_paths or []) if _is_document(path)]
        corpus_source = "git-tracked-plus-untracked-candidates"

    raw_records: list[dict[str, Any]] = []
    for relative, tracked in [
        *((path, True) for path in tracked_documents),
        *((path, False) for path in untracked_documents),
    ]:
        raw, content_source, exists = _read_document(repo_root, relative, tracked)
        text = raw.decode("utf-8", errors="replace")
        raw_records.append(
            {
                "path": relative,
                "document_kind": "agents" if PurePosixPath(relative).name == "AGENTS.md" else "readme",
                "tracked": tracked,
                "worktree_status": statuses.get(relative),
                "exists_in_worktree": exists,
                "content_source": content_source,
                "lines": text.count("\n") + (0 if not text or text.endswith("\n") else 1),
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "heading_ok": (
                    text.lstrip().startswith("# AGENTS.md")
                    if PurePosixPath(relative).name == "AGENTS.md"
                    else None
                ),
                "scope_flags": _scope_flags(relative),
                "_text": text,
            }
        )

    known_paths = {record["path"] for record in raw_records}
    by_directory: dict[str, set[str]] = {}
    for record in raw_records:
        directory = PurePosixPath(record["path"]).parent.as_posix()
        by_directory.setdefault(directory, set()).add(record["document_kind"])

    active_agents = {
        record["path"]: record
        for record in raw_records
        if record["document_kind"] == "agents" and record["exists_in_worktree"]
    }
    inbound_counts = {path: 0 for path in known_paths}
    for record in raw_records:
        references = _extract_references(record["path"], record["_text"], known_paths)
        record.update(references)
        for target in references["outbound_document_links"]:
            inbound_counts[target] += 1

    bytes_by_path = {record["path"]: record["bytes"] for record in raw_records}
    for record in raw_records:
        directory = PurePosixPath(record["path"]).parent.as_posix()
        kinds = by_directory[directory]
        if kinds == {"agents", "readme"}:
            pair_state = "paired"
        elif record["document_kind"] == "agents":
            pair_state = "agents-only"
        else:
            pair_state = "readme-only"
        chain = _chain_paths(record["path"], active_agents)
        chain_bytes = sum(bytes_by_path[path] for path in chain)
        mandatory_targets = record["mandatory_resolved_readme_references"]
        record.update(
            {
                "pair_state": pair_state,
                "inbound_document_link_count": inbound_counts[record["path"]],
                "agents_chain_paths": chain,
                "agents_chain_depth": len(chain),
                "agents_chain_bytes": chain_bytes,
                "agents_chain_budget_bytes": AGENTS_CHAIN_BUDGET_BYTES,
                "agents_chain_headroom_bytes": AGENTS_CHAIN_BUDGET_BYTES - chain_bytes,
                "agents_chain_over_budget": chain_bytes > AGENTS_CHAIN_BUDGET_BYTES,
                "declared_mandatory_readme_bytes": sum(
                    bytes_by_path[target] for target in mandatory_targets
                ),
                "review": _review_record(repository, record["path"], dispositions),
            }
        )
        record.pop("_text")

    tracked = [record for record in raw_records if record["tracked"]]
    tracked_agents = [record for record in tracked if record["document_kind"] == "agents"]
    tracked_readmes = [record for record in tracked if record["document_kind"] == "readme"]
    tracked_dirs: dict[str, set[str]] = {}
    for record in tracked:
        directory = PurePosixPath(record["path"]).parent.as_posix()
        tracked_dirs.setdefault(directory, set()).add(record["document_kind"])
    chain_by_scope: dict[str, int] = {}
    chain_signatures: dict[tuple[str, ...], dict[str, Any]] = {}
    for record in tracked:
        directory = PurePosixPath(record["path"]).parent.as_posix()
        chain_by_scope[directory] = max(chain_by_scope.get(directory, 0), record["agents_chain_bytes"])
        signature = tuple(record["agents_chain_paths"])
        excluded_surface = any(
            record["scope_flags"][name]
            for name in ("generated", "vendor", "fixture", "archive")
        )
        signature_record = chain_signatures.setdefault(
            signature,
            {"bytes": record["agents_chain_bytes"], "has_authored_scope": False},
        )
        signature_record["has_authored_scope"] = (
            signature_record["has_authored_scope"] or not excluded_surface
        )
    chain_values = list(chain_by_scope.values())
    unique_chain_values = [record["bytes"] for record in chain_signatures.values()]
    reviews = [record["review"]["review_state"] for record in tracked]
    disposition_counts: dict[str, int] = {}
    for record in tracked:
        disposition = record["review"]["disposition"]
        if disposition:
            disposition_counts[disposition] = disposition_counts.get(disposition, 0) + 1

    summary = {
        "tracked_document_files": len(tracked),
        "tracked_agents_files": len(tracked_agents),
        "tracked_readme_files": len(tracked_readmes),
        "tracked_document_bytes": sum(record["bytes"] for record in tracked),
        "tracked_agents_bytes": sum(record["bytes"] for record in tracked_agents),
        "tracked_readme_bytes": sum(record["bytes"] for record in tracked_readmes),
        "untracked_document_candidates": len(raw_records) - len(tracked),
        "paired_directories": sum(1 for kinds in tracked_dirs.values() if kinds == {"agents", "readme"}),
        "readme_only_directories": sum(1 for kinds in tracked_dirs.values() if kinds == {"readme"}),
        "agents_only_directories": sum(1 for kinds in tracked_dirs.values() if kinds == {"agents"}),
        "chain_scopes": len(chain_values),
        "chain_p50_bytes": _nearest_rank(chain_values, 0.50),
        "chain_p95_bytes": _nearest_rank(chain_values, 0.95),
        "chain_max_bytes": max(chain_values, default=0),
        "chain_scopes_over_budget": sum(value > AGENTS_CHAIN_BUDGET_BYTES for value in chain_values),
        "unique_agents_chains": len(unique_chain_values),
        "unique_chain_p50_bytes": _nearest_rank(unique_chain_values, 0.50),
        "unique_chain_p95_bytes": _nearest_rank(unique_chain_values, 0.95),
        "unique_chain_max_bytes": max(unique_chain_values, default=0),
        "unique_chains_over_budget": sum(
            value > AGENTS_CHAIN_BUDGET_BYTES for value in unique_chain_values
        ),
        "authored_unique_chains_over_budget": sum(
            record["bytes"] > AGENTS_CHAIN_BUDGET_BYTES and record["has_authored_scope"]
            for record in chain_signatures.values()
        ),
        "excluded_unique_chains_over_budget": sum(
            record["bytes"] > AGENTS_CHAIN_BUDGET_BYTES and not record["has_authored_scope"]
            for record in chain_signatures.values()
        ),
        "root_document_files": sum(record["scope_flags"]["root"] for record in tracked),
        "generated_document_files": sum(record["scope_flags"]["generated"] for record in tracked),
        "vendor_document_files": sum(record["scope_flags"]["vendor"] for record in tracked),
        "fixture_document_files": sum(record["scope_flags"]["fixture"] for record in tracked),
        "archive_document_files": sum(record["scope_flags"]["archive"] for record in tracked),
        "mechanics_document_files": sum(record["scope_flags"]["mechanics"] for record in tracked),
        "agents_files_referencing_readme": sum(bool(record["readme_reference_lines"]) for record in tracked_agents),
        "agents_files_declaring_mandatory_readme": sum(
            bool(record["mandatory_readme_reference_lines"]) for record in tracked_agents
        ),
        "declared_mandatory_readme_bytes": sum(
            record["declared_mandatory_readme_bytes"] for record in tracked_agents
        ),
        "reviewed_files": reviews.count("reviewed"),
        "blocked_files": reviews.count("blocked"),
        "unreviewed_files": reviews.count("unreviewed"),
        "disposition_counts": disposition_counts,
    }
    return {
        "corpus_source": corpus_source,
        "git_snapshot": snapshot,
        "readme_agents_summary": summary,
        "agents_files": sorted(
            [record for record in raw_records if record["document_kind"] == "agents"],
            key=lambda record: record["path"],
        ),
        "readme_files": sorted(
            [record for record in raw_records if record["document_kind"] == "readme"],
            key=lambda record: record["path"],
        ),
    }


def scan_shared_root(
    workspace_root: Path,
    owner_repo_root: Path,
    dispositions: Mapping[tuple[str, str], Mapping[str, Any]],
) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for name in ("AGENTS.md", "README.md"):
        live_path = workspace_root / name
        owner_path = owner_repo_root / name
        if not live_path.is_file():
            continue
        live = live_path.read_bytes()
        owner = owner_path.read_bytes() if owner_path.is_file() else b""
        records.append(
            {
                "path": name,
                "document_kind": "agents" if name == "AGENTS.md" else "readme",
                "tracked": False,
                "bytes": len(live),
                "sha256": hashlib.sha256(live).hexdigest(),
                "owner_path": f"8Dionysus/{name}",
                "owner_sha256": hashlib.sha256(owner).hexdigest() if owner else None,
                "owner_parity": bool(owner) and live == owner,
                "declared_projection_surface": name == "AGENTS.md",
                "review": _review_record("@workspace-root", name, dispositions),
            }
        )
    return {"files": records}


def summarize_workspace_corpus(
    repositories: Sequence[Mapping[str, Any]],
    shared_root: Mapping[str, Any],
) -> dict[str, Any]:
    scanned = [repo for repo in repositories if repo.get("checkout_state") == "scanned"]
    summaries = [repo["readme_agents_summary"] for repo in scanned]
    chain_scopes: list[int] = []
    unique_chains: dict[tuple[str, tuple[str, ...]], dict[str, Any]] = {}
    for repo in scanned:
        seen: dict[str, int] = {}
        for record in [*repo.get("agents_files", []), *repo.get("readme_files", [])]:
            if not record.get("tracked"):
                continue
            directory = PurePosixPath(record["path"]).parent.as_posix()
            seen[directory] = max(seen.get(directory, 0), record["agents_chain_bytes"])
            signature = (repo["name"], tuple(record["agents_chain_paths"]))
            excluded_surface = any(
                record["scope_flags"][name]
                for name in ("generated", "vendor", "fixture", "archive")
            )
            signature_record = unique_chains.setdefault(
                signature,
                {"bytes": record["agents_chain_bytes"], "has_authored_scope": False},
            )
            signature_record["has_authored_scope"] = (
                signature_record["has_authored_scope"] or not excluded_surface
            )
        chain_scopes.extend(seen.values())
    unique_chain_values = [record["bytes"] for record in unique_chains.values()]
    shared_reviews = [
        record.get("review", {}).get("review_state", "unreviewed")
        for record in shared_root.get("files", [])
    ]
    tracked_reviewed = sum(item["reviewed_files"] for item in summaries)
    tracked_blocked = sum(item["blocked_files"] for item in summaries)
    tracked_unreviewed = sum(item["unreviewed_files"] for item in summaries)
    return {
        "tracked_document_files": sum(item["tracked_document_files"] for item in summaries),
        "tracked_agents_files": sum(item["tracked_agents_files"] for item in summaries),
        "tracked_readme_files": sum(item["tracked_readme_files"] for item in summaries),
        "tracked_document_bytes": sum(item["tracked_document_bytes"] for item in summaries),
        "tracked_agents_bytes": sum(item["tracked_agents_bytes"] for item in summaries),
        "tracked_readme_bytes": sum(item["tracked_readme_bytes"] for item in summaries),
        "untracked_document_candidates": sum(item["untracked_document_candidates"] for item in summaries),
        "paired_directories": sum(item["paired_directories"] for item in summaries),
        "readme_only_directories": sum(item["readme_only_directories"] for item in summaries),
        "agents_only_directories": sum(item["agents_only_directories"] for item in summaries),
        "chain_scopes": len(chain_scopes),
        "chain_p50_bytes": _nearest_rank(chain_scopes, 0.50),
        "chain_p95_bytes": _nearest_rank(chain_scopes, 0.95),
        "chain_max_bytes": max(chain_scopes, default=0),
        "chain_scopes_over_budget": sum(value > AGENTS_CHAIN_BUDGET_BYTES for value in chain_scopes),
        "unique_agents_chains": len(unique_chain_values),
        "unique_chain_p50_bytes": _nearest_rank(unique_chain_values, 0.50),
        "unique_chain_p95_bytes": _nearest_rank(unique_chain_values, 0.95),
        "unique_chain_max_bytes": max(unique_chain_values, default=0),
        "unique_chains_over_budget": sum(
            value > AGENTS_CHAIN_BUDGET_BYTES for value in unique_chain_values
        ),
        "authored_unique_chains_over_budget": sum(
            record["bytes"] > AGENTS_CHAIN_BUDGET_BYTES and record["has_authored_scope"]
            for record in unique_chains.values()
        ),
        "excluded_unique_chains_over_budget": sum(
            record["bytes"] > AGENTS_CHAIN_BUDGET_BYTES and not record["has_authored_scope"]
            for record in unique_chains.values()
        ),
        "root_document_files": sum(item["root_document_files"] for item in summaries),
        "generated_document_files": sum(item["generated_document_files"] for item in summaries),
        "vendor_document_files": sum(item["vendor_document_files"] for item in summaries),
        "fixture_document_files": sum(item["fixture_document_files"] for item in summaries),
        "archive_document_files": sum(item["archive_document_files"] for item in summaries),
        "mechanics_document_files": sum(item["mechanics_document_files"] for item in summaries),
        "agents_files_referencing_readme": sum(item["agents_files_referencing_readme"] for item in summaries),
        "agents_files_declaring_mandatory_readme": sum(
            item["agents_files_declaring_mandatory_readme"] for item in summaries
        ),
        "declared_mandatory_readme_bytes": sum(
            item["declared_mandatory_readme_bytes"] for item in summaries
        ),
        "reviewed_files": tracked_reviewed,
        "blocked_files": tracked_blocked,
        "unreviewed_files": tracked_unreviewed,
        "shared_root_files": len(shared_root.get("files", [])),
        "shared_root_files_in_owner_parity": sum(
            bool(record.get("owner_parity")) for record in shared_root.get("files", [])
        ),
        "shared_root_reviewed_files": shared_reviews.count("reviewed"),
        "shared_root_blocked_files": shared_reviews.count("blocked"),
        "shared_root_unreviewed_files": shared_reviews.count("unreviewed"),
        "review_items_total": len(shared_reviews) + tracked_reviewed + tracked_blocked + tracked_unreviewed,
        "review_items_unreviewed": shared_reviews.count("unreviewed") + tracked_unreviewed,
    }
