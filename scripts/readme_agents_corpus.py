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

from project_workspace_root import render_agents_text


DOCUMENT_NAMES = frozenset({"AGENTS.md", "README.md"})
SUPPLEMENTAL_AGENT_DOCUMENT_NAMES = frozenset({"DESIGN.AGENTS.md"})
SHARED_ROOT_OWNER_PATHS = {
    "AGENTS.md": "AGENTS.md",
    "README.md": "docs/WORKSPACE_ROOT_ENTRY.md",
}
AGENTS_CHAIN_BUDGET_BYTES = 32 * 1024
REPEATED_AGENTS_BLOCK_MIN_BYTES = 180
REPEATED_AGENTS_BLOCK_MIN_FILES = 4
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
AGENTS_FENCE_CLASSIFICATIONS = frozenset(
    {
        "agent-card-template",
        "conceptual-sequence",
        "decision-record-heading-template",
        "diagram-example",
        "filename-template",
        "operating-contract-template",
        "source-code-example",
        "structured-data-example",
    }
)
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
RUNTIME_SESSION_PARTS = frozenset({".aoa"})
AUTHORED_SCOPE_EXCLUSION_FLAGS = (
    "generated",
    "vendor",
    "fixture",
    "archive",
    "runtime_session",
)
README_TOKEN_RE = re.compile(r"(?P<path>(?:\.\.?/)?[A-Za-z0-9_.@+-]+(?:/[A-Za-z0-9_.@+-]+)*/README\.md|README\.md)")
DOC_LINK_RE = re.compile(
    r"\[[^\]]*\]\((?P<link>[^)]+(?:README|AGENTS)\.md(?:#[^)]*)?)\)"
)
MANDATORY_READ_RE = re.compile(
    r"\b(read(?!\s+models?\b)|open|consult|before|start\s+(?:here|from)|"
    r"прочит\w*|сначала|изуч\w*)\b",
    re.IGNORECASE,
)
NEGATED_READ_RE = re.compile(
    r"\b(do\s+not|don't|not\s+(?:mandatory|required)|none\s+is\s+mandatory|optional|"
    r"does\s+not\s+require|не\s+(?:читать|нужно|требуется))\b",
    re.IGNORECASE,
)
CONDITIONAL_READ_RE = re.compile(
    r"\b(?:only\s+(?:when|if)|if\b|when\b|on[- ]demand|as\s+needed|"
    r"only\s+the\s+route\s+needed|"
    r"(?:read|open|consult|use)\b.{0,160}\bfor\b|"
    r"when\b.{0,180}\b(?:relevant|needed|required|material))\b",
    re.IGNORECASE,
)
MARKDOWN_LIST_ITEM_RE = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)")
MARKDOWN_HEADING_RE = re.compile(r"^(?P<marks>#{1,6})\s+(?P<title>.+?)\s*$")
MANDATORY_READ_SECTION_RE = re.compile(
    r"\b(read\s+before(?:\s+editing|\s+changing)?|reading\s+order|read\s+first|"
    r"required\s+reading|порядок\s+чтения|прочитать\s+перед|сначала\s+прочитать)\b",
    re.IGNORECASE,
)
FENCE_START_RE = re.compile(r"^(?P<marker>`{3,}|~{3,})")
VALIDATION_COMMAND_FENCE_RE = re.compile(
    r"^ {0,3}```(?:bash|console|sh|shell|zsh|powershell|pwsh|text|plaintext|terminal)?(?:\s+.*)?$",
    re.IGNORECASE,
)
EXECUTABLE_VALIDATION_LINE_RE = re.compile(
    r"^(?:(?:[A-Za-z_][A-Za-z0-9_]*=[^\s]+)\s+)*(?:"
    r"python3?(?:\s+-m)?\s+|pytest(?:\s|$)|uv\s+run\s+|"
    r"git\s+|gh\s+|aoa\s+|skills-ref\s+|ruff\s+|mypy(?:\s|$)|"
    r"bash\s+|sh\s+|make(?:\s|$)|npm\s+|pnpm\s+|cargo\s+|"
    r"go\s+|docker\s+|podman\s+)",
    re.IGNORECASE,
)
VALIDATION_ROUTE_ONLY_ASSERTION_RES = (
    re.compile(r"\bowns no distinct executable procedure\b", re.IGNORECASE),
    re.compile(
        r"\bExecutable validation for this (?:part|surface) is routed through\b",
        re.IGNORECASE,
    ),
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


def _is_supplemental_agent_document(path: str) -> bool:
    return PurePosixPath(path).name in SUPPLEMENTAL_AGENT_DOCUMENT_NAMES


def _fallback_document_paths(repo_root: Path) -> list[str]:
    found: list[str] = []
    for current_root, dirs, files in os.walk(repo_root):
        current = Path(current_root)
        dirs[:] = [name for name in dirs if name not in FALLBACK_SKIP_DIRS]
        for name in DOCUMENT_NAMES.intersection(files):
            found.append((current / name).relative_to(repo_root).as_posix())
    return sorted(found)


def _fallback_validation_paths(repo_root: Path) -> list[str]:
    found: list[str] = []
    for current_root, dirs, files in os.walk(repo_root):
        current = Path(current_root)
        dirs[:] = [name for name in dirs if name not in FALLBACK_SKIP_DIRS]
        if "VALIDATION.md" in files:
            found.append((current / "VALIDATION.md").relative_to(repo_root).as_posix())
    return sorted(found)


def _fallback_supplemental_agent_paths(repo_root: Path) -> list[str]:
    found: list[str] = []
    for current_root, dirs, files in os.walk(repo_root):
        current = Path(current_root)
        dirs[:] = [name for name in dirs if name not in FALLBACK_SKIP_DIRS]
        for name in SUPPLEMENTAL_AGENT_DOCUMENT_NAMES.intersection(files):
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
        fenced_blocks = record.get("fenced_blocks", [])
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
        if not isinstance(fenced_blocks, list):
            issues.append(f"{repository}:{document_path} has invalid fenced_blocks")
            continue
        seen_fence_digests: set[str] = set()
        invalid_fence = False
        for fence_index, fence in enumerate(fenced_blocks):
            if not isinstance(fence, dict):
                issues.append(
                    f"{repository}:{document_path} fenced_blocks[{fence_index}] is not an object"
                )
                invalid_fence = True
                continue
            digest = fence.get("sha256")
            classification = fence.get("classification")
            reason = fence.get("reason")
            if (
                not isinstance(digest, str)
                or not re.fullmatch(r"[0-9a-f]{64}", digest)
                or classification not in AGENTS_FENCE_CLASSIFICATIONS
                or not isinstance(reason, str)
                or not reason.strip()
            ):
                issues.append(
                    f"{repository}:{document_path} fenced_blocks[{fence_index}] is invalid"
                )
                invalid_fence = True
                continue
            if digest in seen_fence_digests:
                issues.append(
                    f"{repository}:{document_path} repeats fenced block digest {digest}"
                )
                invalid_fence = True
            seen_fence_digests.add(digest)
        if invalid_fence:
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
        "runtime_session": bool(parts & RUNTIME_SESSION_PARTS),
        "mechanics": "mechanics" in parts,
    }


def _validation_commands(text: str) -> list[tuple[int, str]]:
    """Extract normalized executable invocations from shell command fences."""

    commands: list[tuple[int, str]] = []
    in_command_fence = False
    buffer: list[str] = []
    start_line = 0

    def flush() -> None:
        nonlocal buffer, start_line
        if not buffer:
            return
        command = " ".join(part.strip().rstrip("\\`").strip() for part in buffer)
        command = re.sub(r"\s+", " ", command).strip()
        if EXECUTABLE_VALIDATION_LINE_RE.match(command):
            commands.append((start_line, command))
        buffer = []
        start_line = 0

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()
        if not in_command_fence:
            if VALIDATION_COMMAND_FENCE_RE.match(raw_line):
                in_command_fence = True
            continue
        if stripped.startswith("```"):
            flush()
            in_command_fence = False
            continue
        if not stripped or stripped.startswith("#"):
            flush()
            continue
        line = re.sub(r"^(?:\$|PS>)\s*", "", stripped)
        if buffer:
            buffer.append(line)
            if not line.endswith(("\\", "`")):
                flush()
            continue
        # A shell environment prefix commonly occupies its own continued line,
        # so it cannot match the executable regex until the following line is
        # joined. Start any explicit continuation and decide whether it is an
        # executable invocation only after the complete logical command exists.
        if EXECUTABLE_VALIDATION_LINE_RE.match(line) or line.endswith(("\\", "`")):
            buffer = [line]
            start_line = line_number
            if not line.endswith(("\\", "`")):
                flush()
    flush()
    return commands


def _command_group(command: str, locations: Sequence[dict[str, Any]]) -> dict[str, Any]:
    return {
        "fingerprint": hashlib.sha256(command.encode("utf-8")).hexdigest(),
        "command": command,
        "occurrences": len(locations),
        "locations": sorted(locations, key=lambda item: (item["path"], item["line"])),
    }


def has_level_one_heading(text: str) -> bool:
    """Accept an owner-specific H1 title without requiring one literal label."""

    first_nonempty = next((line.strip() for line in text.splitlines() if line.strip()), "")
    heading = MARKDOWN_HEADING_RE.match(first_nonempty)
    return bool(heading and len(heading.group("marks")) == 1)


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
    readme_reference_classifications: list[dict[str, Any]] = []
    mandatory_section_level: int | None = None
    lines = text.splitlines()
    paragraph_context: dict[int, str] = {}
    paragraph_lines: list[tuple[int, str]] = []
    paragraph_kind: str | None = None
    fenced_lines: set[int] = set()
    fence_marker: str | None = None

    def flush_paragraph() -> None:
        nonlocal paragraph_kind
        if not paragraph_lines:
            return
        context = " ".join(line.strip() for _, line in paragraph_lines)
        for number, _ in paragraph_lines:
            paragraph_context[number] = context
        paragraph_lines.clear()
        paragraph_kind = None

    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()
        fence = FENCE_START_RE.match(stripped)
        if fence:
            flush_paragraph()
            marker = fence.group("marker")
            if fence_marker is None:
                fence_marker = marker[0]
            elif marker[0] == fence_marker:
                fence_marker = None
            fenced_lines.add(line_number)
            continue
        if fence_marker is not None:
            fenced_lines.add(line_number)
            continue
        if not stripped or MARKDOWN_HEADING_RE.match(stripped):
            flush_paragraph()
            continue
        line_kind = (
            "list"
            if MARKDOWN_LIST_ITEM_RE.match(line)
            else "table"
            if stripped.startswith("|")
            else "prose"
        )
        if paragraph_lines and (
            line_kind in {"list", "table"}
            or (
                paragraph_kind in {"list", "table"}
                and not line[:1].isspace()
            )
        ):
            flush_paragraph()
        paragraph_lines.append((line_number, line))
        if paragraph_kind is None:
            paragraph_kind = line_kind
    flush_paragraph()

    for line_number, line in enumerate(lines, start=1):
        heading = (
            None
            if line_number in fenced_lines
            else MARKDOWN_HEADING_RE.match(line.strip())
        )
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
            paragraph = paragraph_context.get(line_number, line)
            sentences = re.split(r"(?<=[.!?])\s+", paragraph)
            matching_sentences = [
                sentence
                for sentence in sentences
                if any(token in sentence for token in readme_tokens)
            ]
            context = " ".join(matching_sentences) or line
            conditional = bool(
                CONDITIONAL_READ_RE.search(context)
                or NEGATED_READ_RE.search(context)
            )
            explicit_directive = bool(MANDATORY_READ_RE.search(context))
            section_list_item = (
                mandatory_section_level is not None
                and bool(MARKDOWN_LIST_ITEM_RE.match(line))
            )
            mandatory = (
                explicit_directive or section_list_item
            ) and not conditional and line_number not in fenced_lines
            classification = (
                "fenced-example"
                if line_number in fenced_lines
                else "mandatory-preload"
                if mandatory
                else "conditional-on-demand"
                if conditional
                else "navigational-reference"
            )
            readme_reference_classifications.append(
                {
                    "line": line_number,
                    "classification": classification,
                    "tokens": sorted(set(readme_tokens)),
                }
            )
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
        "readme_reference_classifications": readme_reference_classifications,
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


def _agents_prose_blocks(text: str) -> list[str]:
    """Return normalized prompt-visible prose blocks outside fenced examples."""

    blocks: list[str] = []
    current: list[str] = []
    fence_marker: str | None = None

    def flush() -> None:
        if not current:
            return
        normalized = " ".join(current)
        if normalized:
            blocks.append(normalized)
        current.clear()

    for raw_line in text.splitlines():
        line = raw_line.strip()
        fence = FENCE_START_RE.match(line)
        if fence:
            marker = fence.group("marker")
            if fence_marker is None:
                flush()
                fence_marker = marker[0]
            elif marker[0] == fence_marker:
                fence_marker = None
            continue
        if fence_marker is not None:
            continue
        if not line:
            flush()
            continue
        if MARKDOWN_HEADING_RE.match(line):
            flush()
            continue
        current.append(line)
    flush()
    return blocks


def _agents_fenced_blocks(text: str) -> list[dict[str, Any]]:
    """Return content-addressed fenced blocks for explicit semantic review."""

    blocks: list[dict[str, Any]] = []
    fence_marker: str | None = None
    language = ""
    body: list[str] = []
    start_line = 0
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()
        fence = FENCE_START_RE.match(stripped)
        if fence:
            marker = fence.group("marker")
            if fence_marker is None:
                fence_marker = marker[0]
                start_line = line_number
                language = stripped[len(marker) :].strip().split(maxsplit=1)[0].lower() if stripped[len(marker) :].strip() else ""
                body = []
            elif marker[0] == fence_marker:
                normalized = "\n".join(body).strip()
                wrapped = f"```{language}\n{normalized}\n```\n"
                blocks.append(
                    {
                        "start_line": start_line,
                        "end_line": line_number,
                        "language": language or None,
                        "sha256": hashlib.sha256(normalized.encode("utf-8")).hexdigest(),
                        "bytes": len(normalized.encode("utf-8")),
                        "executable_invocations": len(_validation_commands(wrapped)),
                    }
                )
                fence_marker = None
                language = ""
                body = []
                start_line = 0
            continue
        if fence_marker is not None:
            body.append(raw_line)
    return blocks


def _repeated_agents_blocks(records: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    """Describe exact long prose blocks repeated across several tracked cards."""

    occurrences: dict[str, dict[str, Any]] = {}
    for record in records:
        if record["document_kind"] != "agents" or not record["tracked"]:
            continue
        unique_blocks = set(_agents_prose_blocks(record["_text"]))
        for block in unique_blocks:
            block_bytes = len(block.encode("utf-8"))
            if block_bytes < REPEATED_AGENTS_BLOCK_MIN_BYTES:
                continue
            fingerprint = hashlib.sha256(block.encode("utf-8")).hexdigest()
            group = occurrences.setdefault(
                fingerprint,
                {
                    "fingerprint": fingerprint,
                    "normalized_bytes": block_bytes,
                    "paths": [],
                },
            )
            group["paths"].append(record["path"])

    record_by_path = {record["path"]: record for record in records}
    groups: list[dict[str, Any]] = []
    for group in occurrences.values():
        paths = sorted(group["paths"])
        if len(paths) < REPEATED_AGENTS_BLOCK_MIN_FILES:
            continue
        excluded = all(
            any(
                record_by_path[path]["scope_flags"][name]
                for name in AUTHORED_SCOPE_EXCLUSION_FLAGS
            )
            for path in paths
        )
        normalized_bytes = int(group["normalized_bytes"])
        groups.append(
            {
                "fingerprint": group["fingerprint"],
                "normalized_bytes": normalized_bytes,
                "occurrences": len(paths),
                "normalized_redundant_bytes": normalized_bytes * (len(paths) - 1),
                "scope": "excluded" if excluded else "authored",
                "paths": paths,
            }
        )
        for path in paths:
            record_by_path[path].setdefault(
                "repeated_long_agents_block_fingerprints", []
            ).append(group["fingerprint"])

    return sorted(
        groups,
        key=lambda group: (
            -int(group["occurrences"]),
            -int(group["normalized_bytes"]),
            str(group["fingerprint"]),
        ),
    )


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
            "fenced_blocks": [],
        }
    return {
        "review_state": record["review_state"],
        "disposition": record.get("disposition"),
        "owner_evidence": list(record.get("owner_evidence", [])),
        "note": record.get("note"),
        "fenced_blocks": list(record.get("fenced_blocks", [])),
    }


def _reviewed_fenced_blocks(
    text: str,
    review: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[str]]:
    declared = {item["sha256"]: item for item in review["fenced_blocks"]}
    blocks = _agents_fenced_blocks(text)
    observed_digests = {block["sha256"] for block in blocks}
    for block in blocks:
        declaration = declared.get(block["sha256"])
        block["classification"] = (
            declaration["classification"] if declaration else None
        )
        block["classification_reason"] = (
            declaration["reason"] if declaration else None
        )
    return blocks, sorted(set(declared) - observed_digests)


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
        tracked_supplemental_agent_paths = _fallback_supplemental_agent_paths(
            repo_root
        )
        untracked_supplemental_agent_paths: list[str] = []
        tracked_validation_paths = _fallback_validation_paths(repo_root)
        untracked_validation_paths: list[str] = []
        corpus_source = "filesystem-fallback"
    else:
        tracked_documents = [path for path in tracked_paths if _is_document(path)]
        untracked_paths = _git_nul_paths(repo_root, ["ls-files", "-z", "--others", "--exclude-standard"])
        untracked_documents = [path for path in (untracked_paths or []) if _is_document(path)]
        tracked_supplemental_agent_paths = [
            path for path in tracked_paths if _is_supplemental_agent_document(path)
        ]
        untracked_supplemental_agent_paths = [
            path
            for path in (untracked_paths or [])
            if _is_supplemental_agent_document(path)
        ]
        tracked_validation_paths = [
            path for path in tracked_paths if PurePosixPath(path).name == "VALIDATION.md"
        ]
        untracked_validation_paths = [
            path
            for path in (untracked_paths or [])
            if PurePosixPath(path).name == "VALIDATION.md"
        ]
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
                    has_level_one_heading(text)
                    if PurePosixPath(relative).name == "AGENTS.md"
                    else None
                ),
                "scope_flags": _scope_flags(relative),
                "_text": text,
            }
        )

    supplemental_agent_records: list[dict[str, Any]] = []
    for relative, tracked in [
        *((path, True) for path in tracked_supplemental_agent_paths),
        *((path, False) for path in untracked_supplemental_agent_paths),
    ]:
        raw, content_source, exists = _read_document(repo_root, relative, tracked)
        text = raw.decode("utf-8", errors="replace")
        review = _review_record(repository, relative, dispositions)
        fenced_blocks, stale_fences = _reviewed_fenced_blocks(text, review)
        supplemental_agent_records.append(
            {
                "path": relative,
                "document_kind": "design-agents",
                "tracked": tracked,
                "worktree_status": statuses.get(relative),
                "exists_in_worktree": exists,
                "content_source": content_source,
                "lines": text.count("\n")
                + (0 if not text or text.endswith("\n") else 1),
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "heading_ok": has_level_one_heading(text),
                "scope_flags": _scope_flags(relative),
                "review": review,
                "fenced_blocks": fenced_blocks,
                "stale_fenced_block_classifications": stale_fences,
            }
        )

    validation_records: list[dict[str, Any]] = []
    validation_occurrences: dict[str, list[dict[str, Any]]] = {}
    validation_route_only_claim_conflicts: list[dict[str, Any]] = []
    for relative, tracked in [
        *((path, True) for path in tracked_validation_paths),
        *((path, False) for path in untracked_validation_paths),
    ]:
        raw, content_source, exists = _read_document(repo_root, relative, tracked)
        text = raw.decode("utf-8", errors="replace")
        scope_flags = _scope_flags(relative)
        commands = _validation_commands(text) if exists else []
        record = {
            "path": relative,
            "tracked": tracked,
            "worktree_status": statuses.get(relative),
            "exists_in_worktree": exists,
            "content_source": content_source,
            "lines": text.count("\n") + (0 if not text or text.endswith("\n") else 1),
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "scope_flags": scope_flags,
            "executable_invocations": len(commands),
        }
        validation_records.append(record)
        if exists and not any(
            scope_flags[name] for name in AUTHORED_SCOPE_EXCLUSION_FLAGS
        ):
            if commands:
                conflicting_lines = sorted(
                    {
                        line_number
                        for line_number, line in enumerate(text.splitlines(), start=1)
                        if any(
                            pattern.search(line)
                            for pattern in VALIDATION_ROUTE_ONLY_ASSERTION_RES
                        )
                    }
                )
                if conflicting_lines:
                    validation_route_only_claim_conflicts.append(
                        {
                            "path": relative,
                            "claim_lines": conflicting_lines,
                            "executable_invocations": len(commands),
                        }
                    )
            for line_number, command in commands:
                validation_occurrences.setdefault(command, []).append(
                    {"path": relative, "line": line_number, "tracked": tracked}
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
        if record["document_kind"] == "agents":
            (
                record["fenced_blocks"],
                record["stale_fenced_block_classifications"],
            ) = _reviewed_fenced_blocks(
                record["_text"], record["review"]
            )

    repeated_agents_blocks = _repeated_agents_blocks(raw_records)
    document_command_occurrences: dict[str, dict[str, list[dict[str, Any]]]] = {
        "agents": {},
        "readme": {},
    }
    for record in raw_records:
        if not record["exists_in_worktree"] or any(
            record["scope_flags"][name]
            for name in AUTHORED_SCOPE_EXCLUSION_FLAGS
        ):
            continue
        kind = record["document_kind"]
        for line_number, command in _validation_commands(record["_text"]):
            document_command_occurrences[kind].setdefault(command, []).append(
                {
                    "path": record["path"],
                    "line": line_number,
                    "tracked": record["tracked"],
                }
            )

    duplicate_validation_commands = [
        _command_group(command, locations)
        for command, locations in validation_occurrences.items()
        if len(locations) > 1
    ]
    duplicate_validation_commands.sort(key=lambda group: group["fingerprint"])

    command_overlaps: dict[str, list[dict[str, Any]]] = {}
    for kind in ("agents", "readme"):
        for command in sorted(
            set(validation_occurrences) & set(document_command_occurrences[kind])
        ):
            command_overlaps.setdefault(kind, []).append(
                {
                    **_command_group(command, validation_occurrences[command]),
                    "document_locations": sorted(
                        document_command_occurrences[kind][command],
                        key=lambda item: (item["path"], item["line"]),
                    ),
                }
            )

    for record in raw_records:
        if record["document_kind"] == "agents":
            record.setdefault("repeated_long_agents_block_fingerprints", [])
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
            for name in AUTHORED_SCOPE_EXCLUSION_FLAGS
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
    tracked_supplemental_agents = [
        record for record in supplemental_agent_records if record["tracked"]
    ]
    reviews = [record["review"]["review_state"] for record in tracked]
    reviews.extend(
        record["review"]["review_state"] for record in tracked_supplemental_agents
    )
    disposition_counts: dict[str, int] = {}
    for record in [*tracked, *tracked_supplemental_agents]:
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
        "tracked_design_agents_files": len(tracked_supplemental_agents),
        "tracked_design_agents_bytes": sum(
            record["bytes"] for record in tracked_supplemental_agents
        ),
        "untracked_design_agents_candidates": len(supplemental_agent_records)
        - len(tracked_supplemental_agents),
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
        "runtime_session_document_files": sum(
            record["scope_flags"]["runtime_session"] for record in tracked
        ),
        "mechanics_document_files": sum(record["scope_flags"]["mechanics"] for record in tracked),
        "agents_files_referencing_readme": sum(bool(record["readme_reference_lines"]) for record in tracked_agents),
        "agents_files_declaring_mandatory_readme": sum(
            bool(record["mandatory_readme_reference_lines"]) for record in tracked_agents
        ),
        "declared_mandatory_readme_bytes": sum(
            record["declared_mandatory_readme_bytes"] for record in tracked_agents
        ),
        "agents_readme_reference_lines": sum(
            len(record["readme_reference_classifications"])
            for record in tracked_agents
        ),
        "agents_conditional_readme_reference_lines": sum(
            item["classification"] == "conditional-on-demand"
            for record in tracked_agents
            for item in record["readme_reference_classifications"]
        ),
        "agents_navigational_readme_reference_lines": sum(
            item["classification"] == "navigational-reference"
            for record in tracked_agents
            for item in record["readme_reference_classifications"]
        ),
        "agents_fenced_example_readme_reference_lines": sum(
            item["classification"] == "fenced-example"
            for record in tracked_agents
            for item in record["readme_reference_classifications"]
        ),
        "active_authored_agents_fenced_blocks": sum(
            len(record.get("fenced_blocks", []))
            for record in tracked_agents
            if not any(
                record["scope_flags"][name]
                for name in AUTHORED_SCOPE_EXCLUSION_FLAGS
            )
        ),
        "active_authored_agents_classified_fenced_blocks": sum(
            bool(block["classification"])
            for record in tracked_agents
            if not any(
                record["scope_flags"][name]
                for name in AUTHORED_SCOPE_EXCLUSION_FLAGS
            )
            for block in record.get("fenced_blocks", [])
        ),
        "active_authored_agents_unclassified_fenced_blocks": sum(
            not block["classification"]
            for record in tracked_agents
            if not any(
                record["scope_flags"][name]
                for name in AUTHORED_SCOPE_EXCLUSION_FLAGS
            )
            for block in record.get("fenced_blocks", [])
        ),
        "active_authored_agents_fenced_executable_invocations": sum(
            block["executable_invocations"]
            for record in tracked_agents
            if not any(
                record["scope_flags"][name]
                for name in AUTHORED_SCOPE_EXCLUSION_FLAGS
            )
            for block in record.get("fenced_blocks", [])
        ),
        "stale_agents_fenced_block_classifications": sum(
            len(record.get("stale_fenced_block_classifications", []))
            for record in tracked_agents
        ),
        "active_authored_design_agents_fenced_blocks": sum(
            len(record["fenced_blocks"])
            for record in tracked_supplemental_agents
            if not any(
                record["scope_flags"][name]
                for name in AUTHORED_SCOPE_EXCLUSION_FLAGS
            )
        ),
        "active_authored_design_agents_classified_fenced_blocks": sum(
            bool(block["classification"])
            for record in tracked_supplemental_agents
            if not any(
                record["scope_flags"][name]
                for name in AUTHORED_SCOPE_EXCLUSION_FLAGS
            )
            for block in record["fenced_blocks"]
        ),
        "active_authored_design_agents_unclassified_fenced_blocks": sum(
            not block["classification"]
            for record in tracked_supplemental_agents
            if not any(
                record["scope_flags"][name]
                for name in AUTHORED_SCOPE_EXCLUSION_FLAGS
            )
            for block in record["fenced_blocks"]
        ),
        "active_authored_design_agents_fenced_executable_invocations": sum(
            block["executable_invocations"]
            for record in tracked_supplemental_agents
            if not any(
                record["scope_flags"][name]
                for name in AUTHORED_SCOPE_EXCLUSION_FLAGS
            )
            for block in record["fenced_blocks"]
        ),
        "stale_design_agents_fenced_block_classifications": sum(
            len(record["stale_fenced_block_classifications"])
            for record in tracked_supplemental_agents
        ),
        "repeated_long_agents_block_groups": len(repeated_agents_blocks),
        "authored_repeated_long_agents_block_groups": sum(
            group["scope"] == "authored" for group in repeated_agents_blocks
        ),
        "excluded_repeated_long_agents_block_groups": sum(
            group["scope"] == "excluded" for group in repeated_agents_blocks
        ),
        "repeated_long_agents_block_instances": sum(
            group["occurrences"] for group in repeated_agents_blocks
        ),
        "repeated_long_agents_normalized_redundant_bytes": sum(
            group["normalized_redundant_bytes"] for group in repeated_agents_blocks
        ),
        "tracked_validation_files": sum(record["tracked"] for record in validation_records),
        "untracked_validation_candidates": sum(
            not record["tracked"] for record in validation_records
        ),
        "active_authored_validation_files": sum(
            record["exists_in_worktree"]
            and not any(
                record["scope_flags"][name]
                for name in AUTHORED_SCOPE_EXCLUSION_FLAGS
            )
            for record in validation_records
        ),
        "active_authored_validation_bytes": sum(
            record["bytes"]
            for record in validation_records
            if record["exists_in_worktree"]
            and not any(
                record["scope_flags"][name]
                for name in AUTHORED_SCOPE_EXCLUSION_FLAGS
            )
        ),
        "active_authored_validation_command_owner_files": sum(
            bool(record["executable_invocations"])
            for record in validation_records
            if record["exists_in_worktree"]
            and not any(
                record["scope_flags"][name]
                for name in AUTHORED_SCOPE_EXCLUSION_FLAGS
            )
        ),
        "active_authored_validation_route_only_files": sum(
            not record["executable_invocations"]
            for record in validation_records
            if record["exists_in_worktree"]
            and not any(
                record["scope_flags"][name]
                for name in AUTHORED_SCOPE_EXCLUSION_FLAGS
            )
        ),
        "active_authored_validation_invocations": sum(
            len(locations) for locations in validation_occurrences.values()
        ),
        "active_authored_unique_validation_invocations": len(validation_occurrences),
        "duplicate_validation_command_groups": len(duplicate_validation_commands),
        "duplicate_validation_command_occurrences": sum(
            group["occurrences"] - 1 for group in duplicate_validation_commands
        ),
        "agents_validation_command_overlap_groups": len(
            command_overlaps.get("agents", [])
        ),
        "readme_validation_command_overlap_groups": len(
            command_overlaps.get("readme", [])
        ),
        "validation_route_only_claim_conflicts": len(
            validation_route_only_claim_conflicts
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
        "repeated_long_agents_blocks": repeated_agents_blocks,
        "validation_files": sorted(validation_records, key=lambda record: record["path"]),
        "duplicate_validation_commands": duplicate_validation_commands,
        "agents_validation_command_overlaps": command_overlaps.get("agents", []),
        "readme_validation_command_overlaps": command_overlaps.get("readme", []),
        "validation_route_only_claim_conflicts": sorted(
            validation_route_only_claim_conflicts,
            key=lambda record: record["path"],
        ),
        "agents_files": sorted(
            [record for record in raw_records if record["document_kind"] == "agents"],
            key=lambda record: record["path"],
        ),
        "readme_files": sorted(
            [record for record in raw_records if record["document_kind"] == "readme"],
            key=lambda record: record["path"],
        ),
        "design_agents_files": sorted(
            supplemental_agent_records,
            key=lambda record: record["path"],
        ),
    }


def scan_shared_root(
    workspace_root: Path,
    owner_repo_root: Path,
    dispositions: Mapping[tuple[str, str], Mapping[str, Any]],
) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for name, owner_relative in SHARED_ROOT_OWNER_PATHS.items():
        live_path = workspace_root / name
        owner_path = owner_repo_root / owner_relative
        if not live_path.is_file():
            continue
        live = live_path.read_bytes()
        owner = (
            render_agents_text(owner_path.read_text(encoding="utf-8"), workspace_root).encode(
                "utf-8"
            )
            if owner_path.is_file()
            else b""
        )
        records.append(
            {
                "path": name,
                "document_kind": "agents" if name == "AGENTS.md" else "readme",
                "tracked": False,
                "bytes": len(live),
                "sha256": hashlib.sha256(live).hexdigest(),
                "owner_path": f"8Dionysus/{owner_relative}",
                "owner_sha256": hashlib.sha256(owner).hexdigest() if owner else None,
                "owner_parity": bool(owner) and live == owner,
                "declared_projection_surface": True,
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
                for name in AUTHORED_SCOPE_EXCLUSION_FLAGS
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
        "tracked_design_agents_files": sum(
            item["tracked_design_agents_files"] for item in summaries
        ),
        "tracked_design_agents_bytes": sum(
            item["tracked_design_agents_bytes"] for item in summaries
        ),
        "untracked_design_agents_candidates": sum(
            item["untracked_design_agents_candidates"] for item in summaries
        ),
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
        "agents_readme_reference_lines": sum(
            item["agents_readme_reference_lines"] for item in summaries
        ),
        "agents_conditional_readme_reference_lines": sum(
            item["agents_conditional_readme_reference_lines"] for item in summaries
        ),
        "agents_navigational_readme_reference_lines": sum(
            item["agents_navigational_readme_reference_lines"] for item in summaries
        ),
        "agents_fenced_example_readme_reference_lines": sum(
            item["agents_fenced_example_readme_reference_lines"] for item in summaries
        ),
        "active_authored_agents_fenced_blocks": sum(
            item["active_authored_agents_fenced_blocks"] for item in summaries
        ),
        "active_authored_agents_classified_fenced_blocks": sum(
            item["active_authored_agents_classified_fenced_blocks"]
            for item in summaries
        ),
        "active_authored_agents_unclassified_fenced_blocks": sum(
            item["active_authored_agents_unclassified_fenced_blocks"]
            for item in summaries
        ),
        "active_authored_agents_fenced_executable_invocations": sum(
            item["active_authored_agents_fenced_executable_invocations"]
            for item in summaries
        ),
        "stale_agents_fenced_block_classifications": sum(
            item["stale_agents_fenced_block_classifications"] for item in summaries
        ),
        "repeated_long_agents_block_groups": sum(
            item["repeated_long_agents_block_groups"] for item in summaries
        ),
        "authored_repeated_long_agents_block_groups": sum(
            item["authored_repeated_long_agents_block_groups"] for item in summaries
        ),
        "excluded_repeated_long_agents_block_groups": sum(
            item["excluded_repeated_long_agents_block_groups"] for item in summaries
        ),
        "repeated_long_agents_block_instances": sum(
            item["repeated_long_agents_block_instances"] for item in summaries
        ),
        "repeated_long_agents_normalized_redundant_bytes": sum(
            item["repeated_long_agents_normalized_redundant_bytes"] for item in summaries
        ),
        "tracked_validation_files": sum(item["tracked_validation_files"] for item in summaries),
        "untracked_validation_candidates": sum(
            item["untracked_validation_candidates"] for item in summaries
        ),
        "active_authored_validation_files": sum(
            item["active_authored_validation_files"] for item in summaries
        ),
        "active_authored_validation_bytes": sum(
            item["active_authored_validation_bytes"] for item in summaries
        ),
        "active_authored_validation_command_owner_files": sum(
            item["active_authored_validation_command_owner_files"]
            for item in summaries
        ),
        "active_authored_design_agents_fenced_blocks": sum(
            item["active_authored_design_agents_fenced_blocks"]
            for item in summaries
        ),
        "active_authored_design_agents_classified_fenced_blocks": sum(
            item["active_authored_design_agents_classified_fenced_blocks"]
            for item in summaries
        ),
        "active_authored_design_agents_unclassified_fenced_blocks": sum(
            item["active_authored_design_agents_unclassified_fenced_blocks"]
            for item in summaries
        ),
        "active_authored_design_agents_fenced_executable_invocations": sum(
            item["active_authored_design_agents_fenced_executable_invocations"]
            for item in summaries
        ),
        "stale_design_agents_fenced_block_classifications": sum(
            item["stale_design_agents_fenced_block_classifications"]
            for item in summaries
        ),
        "active_authored_validation_route_only_files": sum(
            item["active_authored_validation_route_only_files"]
            for item in summaries
        ),
        "active_authored_validation_invocations": sum(
            item["active_authored_validation_invocations"] for item in summaries
        ),
        "active_authored_unique_validation_invocations": sum(
            item["active_authored_unique_validation_invocations"] for item in summaries
        ),
        "duplicate_validation_command_groups": sum(
            item["duplicate_validation_command_groups"] for item in summaries
        ),
        "duplicate_validation_command_occurrences": sum(
            item["duplicate_validation_command_occurrences"] for item in summaries
        ),
        "agents_validation_command_overlap_groups": sum(
            item["agents_validation_command_overlap_groups"] for item in summaries
        ),
        "readme_validation_command_overlap_groups": sum(
            item["readme_validation_command_overlap_groups"] for item in summaries
        ),
        "validation_route_only_claim_conflicts": sum(
            item["validation_route_only_claim_conflicts"] for item in summaries
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
