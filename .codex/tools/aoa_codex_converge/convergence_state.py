from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlsplit

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore


EXPECTED_SUBAGENTS = [
    "architect",
    "coder",
    "reviewer",
    "evaluator",
    "memory-keeper",
]


@dataclass
class SurfaceStatus:
    name: str
    status: str
    required: bool
    summary: str
    evidence: list[str]
    next_step: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _read_toml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("rb") as fh:
        return tomllib.load(fh)


def _read_json(path: Path) -> Any:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _normalize_workspace_root(workspace_root: Path | str) -> Path:
    return Path(workspace_root).expanduser().resolve()


def _collect_toml_names(agents_dir: Path) -> list[str]:
    names: list[str] = []
    if not agents_dir.exists():
        return names
    for path in sorted(agents_dir.glob("*.toml")):
        try:
            data = _read_toml(path)
        except Exception:
            continue
        name = data.get("name")
        if isinstance(name, str) and name.strip():
            names.append(name.strip())
    return names


def _resolve_mcp_script(
    workspace_root: Path,
    entry: object,
) -> tuple[Path | None, list[str]]:
    evidence: list[str] = []
    if not isinstance(entry, Mapping):
        return None, evidence

    command = entry.get("command")
    if isinstance(command, str) and command:
        evidence.append(f"command={command}")

    base = workspace_root
    cwd = entry.get("cwd")
    if isinstance(cwd, str) and cwd:
        base = Path(cwd).expanduser()
        if not base.is_absolute():
            base = (workspace_root / base).resolve()
        else:
            base = base.resolve()
        evidence.append(f"cwd={base}")

    args = entry.get("args")
    if isinstance(args, list):
        evidence.append(f"args={args!r}")
        for arg in args:
            if isinstance(arg, str) and arg.endswith(".py"):
                script = Path(arg)
                if not script.is_absolute():
                    script = (base / script).resolve()
                else:
                    script = script.resolve()
                return script, evidence

    return None, evidence


def _is_loopback_mcp_url(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError:
        return False
    return (
        parsed.scheme == "http"
        and parsed.hostname in {"127.0.0.1", "::1", "localhost"}
        and port is not None
        and parsed.path == "/mcp"
        and parsed.username is None
        and parsed.password is None
        and not parsed.query
        and not parsed.fragment
    )


def build_report(workspace_root: Path | str) -> dict[str, Any]:
    root = _normalize_workspace_root(workspace_root)

    marker_path = root / "AOA_WORKSPACE_ROOT"
    codex_config_path = root / ".codex" / "config.toml"
    agents_dir = root / ".codex" / "agents"
    convergence_scripts_dir = root / ".codex" / "scripts"
    convergence_bin_dir = root / ".codex" / "bin"
    workspace_skill_dir = root / ".agents" / "skills"
    shared_skill_profiles_path = root / "aoa-skills" / "config" / "skill_pack_profiles.json"
    entry_home_manifest_path = root / "8Dionysus" / "skills" / "port.manifest.json"
    stats_repo = root / "aoa-stats"
    stats_catalog = stats_repo / "generated" / "summary_surface_catalog.min.json"
    stats_source_home = stats_repo / "stats" / "source_home.manifest.json"
    stats_owner_inventory = stats_repo / "stats" / "federation" / "owner-inventory.json"
    stats_launcher = root / ".codex" / "bin" / "aoa-stats-mcp-server.py"
    dionysus_repo = root / "Dionysus"
    dionysus_catalog = dionysus_repo / "generated" / "seed_route_map.min.json"
    memo_service = Path.home() / "src" / "abyss-stack" / "mcp" / "services" / "aoa-memo-mcp"
    session_memory_service = Path.home() / "src" / "abyss-stack" / "mcp" / "services" / "aoa-session-memory-mcp"
    evals_repo = root / "aoa-evals"
    evals_catalog = evals_repo / "generated" / "eval_catalog.min.json"
    evals_contract = evals_repo / "docs" / "architecture" / "AOA_EVALS_MCP_CONTRACT.md"
    evals_service = Path.home() / "src" / "abyss-stack" / "mcp" / "services" / "aoa-evals-mcp"
    decisions_service = Path.home() / "src" / "abyss-stack" / "mcp" / "services" / "aoa-decisions-mcp"
    machine_service = Path.home() / "src" / "abyss-stack" / "mcp" / "services" / "abyss-machine-mcp"

    config = _read_toml(codex_config_path)
    shared_skill_profiles = _read_json(shared_skill_profiles_path)
    entry_home_manifest = _read_json(entry_home_manifest_path)
    subagent_names = _collect_toml_names(agents_dir)
    mcp_servers = config.get("mcp_servers", {}) if isinstance(config, dict) else {}
    project_root_markers = config.get("project_root_markers", []) if isinstance(config, dict) else []

    surfaces: list[SurfaceStatus] = []

    marker_exists = marker_path.exists()
    surfaces.append(
        SurfaceStatus(
            name="workspace_root_anchor",
            status="ok" if marker_exists else "missing",
            required=True,
            summary="Workspace root marker is present." if marker_exists else "Missing AOA_WORKSPACE_ROOT marker.",
            evidence=[str(marker_path)] if marker_exists else [],
            next_step="Create AOA_WORKSPACE_ROOT at the intended sibling workspace root.",
        )
    )

    config_exists = codex_config_path.exists()
    surfaces.append(
        SurfaceStatus(
            name="codex_project_config",
            status="ok" if config_exists else "missing",
            required=True,
            summary="Workspace .codex/config.toml exists." if config_exists else "Missing workspace .codex/config.toml.",
            evidence=[str(codex_config_path)] if config_exists else [],
            next_step="Create or merge a trusted project-scoped .codex/config.toml at the workspace root.",
        )
    )

    marker_listed = isinstance(project_root_markers, list) and "AOA_WORKSPACE_ROOT" in project_root_markers
    surfaces.append(
        SurfaceStatus(
            name="project_root_marker_config",
            status="ok" if marker_listed else ("warn" if config_exists else "missing"),
            required=True,
            summary="project_root_markers includes AOA_WORKSPACE_ROOT."
            if marker_listed
            else "project_root_markers does not include AOA_WORKSPACE_ROOT.",
            evidence=[f"project_root_markers={project_root_markers!r}"] if config_exists else [],
            next_step="Add AOA_WORKSPACE_ROOT to project_root_markers so sibling repos do not steal project-root discovery.",
        )
    )

    workspace_entry = mcp_servers.get("aoa_workspace") if isinstance(mcp_servers, dict) else None
    workspace_script_path, workspace_mcp_evidence = _resolve_mcp_script(root, workspace_entry)
    if isinstance(mcp_servers, dict) and "aoa_workspace" in mcp_servers:
        workspace_mcp_evidence.insert(0, "[mcp_servers.aoa_workspace] in .codex/config.toml")
    if workspace_script_path is not None and workspace_script_path.exists():
        workspace_mcp_evidence.append(str(workspace_script_path))
    workspace_mcp_ok = (
        isinstance(mcp_servers, dict)
        and "aoa_workspace" in mcp_servers
        and workspace_script_path is not None
        and workspace_script_path.exists()
    )
    surfaces.append(
        SurfaceStatus(
            name="workspace_mcp",
            status="ok" if workspace_mcp_ok else "missing",
            required=True,
            summary="Workspace MCP is configured and resolves to a live script."
            if workspace_mcp_ok
            else "Workspace MCP is not fully converged.",
            evidence=workspace_mcp_evidence,
            next_step="Ensure [mcp_servers.aoa_workspace] exists and its cwd/args resolve to a live aoa_workspace MCP server script.",
        )
    )

    stats_repo_exists = stats_repo.exists()
    stats_entry = mcp_servers.get("aoa_stats") if isinstance(mcp_servers, dict) else None
    stats_script_path, stats_evidence = _resolve_mcp_script(root, stats_entry)
    stats_url = stats_entry.get("url") if isinstance(stats_entry, Mapping) else None
    if stats_repo_exists:
        stats_evidence.insert(0, str(stats_repo))
    if isinstance(mcp_servers, dict) and "aoa_stats" in mcp_servers:
        stats_evidence.insert(1 if stats_repo_exists else 0, "[mcp_servers.aoa_stats] in .codex/config.toml")
    if stats_script_path is not None and stats_script_path.exists():
        stats_evidence.append(str(stats_script_path))
    if isinstance(stats_url, str) and stats_url:
        stats_evidence.append(f"url={stats_url}")
    if stats_source_home.exists():
        stats_evidence.append(str(stats_source_home))
    if stats_owner_inventory.exists():
        stats_evidence.append(str(stats_owner_inventory))
    if stats_catalog.exists():
        stats_evidence.append(str(stats_catalog))
    stats_source_wrapper_ok = (
        stats_script_path is not None
        and stats_script_path == stats_launcher.resolve()
        and stats_script_path.exists()
    )
    stats_http_ok = _is_loopback_mcp_url(stats_url)
    stats_mcp_ok = (
        not stats_repo_exists
        or (
            isinstance(mcp_servers, dict)
            and "aoa_stats" in mcp_servers
            and (stats_source_wrapper_ok or stats_http_ok)
            and stats_source_home.exists()
            and stats_owner_inventory.exists()
            and stats_catalog.exists()
        )
    )
    surfaces.append(
        SurfaceStatus(
            name="stats_mcp",
            status="info" if not stats_repo_exists else ("ok" if stats_mcp_ok else "warn"),
            required=False,
            summary=(
                "aoa-stats repo not present under the workspace root."
                if not stats_repo_exists
                else ("Stack-owned aoa-stats MCP access plane looks wired." if stats_mcp_ok else "aoa-stats repo exists but its stack-owned access seam is incomplete.")
            ),
            evidence=stats_evidence,
            next_step="Wire aoa_stats through the shared wrapper or its authenticated loopback endpoint, and preserve the aoa-stats source home, owner inventory, and generated catalog.",
        )
    )

    dionysus_repo_exists = dionysus_repo.exists()
    dionysus_entry = mcp_servers.get("dionysus") if isinstance(mcp_servers, dict) else None
    dionysus_script_path, dionysus_evidence = _resolve_mcp_script(root, dionysus_entry)
    if dionysus_repo_exists:
        dionysus_evidence.insert(0, str(dionysus_repo))
    if isinstance(mcp_servers, dict) and "dionysus" in mcp_servers:
        dionysus_evidence.insert(
            1 if dionysus_repo_exists else 0,
            "[mcp_servers.dionysus] in .codex/config.toml",
        )
    if dionysus_script_path is not None and dionysus_script_path.exists():
        dionysus_evidence.append(str(dionysus_script_path))
    if dionysus_catalog.exists():
        dionysus_evidence.append(str(dionysus_catalog))
    dionysus_mcp_ok = (
        not dionysus_repo_exists
        or (
            isinstance(mcp_servers, dict)
            and "dionysus" in mcp_servers
            and dionysus_script_path is not None
            and dionysus_script_path.exists()
            and dionysus_catalog.exists()
        )
    )
    surfaces.append(
        SurfaceStatus(
            name="dionysus_mcp",
            status="info" if not dionysus_repo_exists else ("ok" if dionysus_mcp_ok else "warn"),
            required=False,
            summary=(
                "Dionysus repo not present under the workspace root."
                if not dionysus_repo_exists
                else ("Dionysus MCP surface looks wired." if dionysus_mcp_ok else "Dionysus repo exists but its MCP seam is incomplete.")
            ),
            evidence=dionysus_evidence,
            next_step="Wire dionysus into workspace .codex/config.toml and ensure the repo-local server plus generated seed route map exist.",
        )
    )

    memo_entry = mcp_servers.get("aoa_memo") if isinstance(mcp_servers, dict) else None
    memo_script_path, memo_evidence = _resolve_mcp_script(root, memo_entry)
    if isinstance(mcp_servers, dict) and "aoa_memo" in mcp_servers:
        memo_evidence.insert(0, "[mcp_servers.aoa_memo] in .codex/config.toml")
    if memo_script_path is not None and memo_script_path.exists():
        memo_evidence.append(str(memo_script_path))
    if memo_service.exists():
        memo_evidence.append(str(memo_service))
    memo_mcp_ok = (
        isinstance(mcp_servers, dict)
        and "aoa_memo" in mcp_servers
        and memo_script_path is not None
        and memo_script_path.exists()
    )
    surfaces.append(
        SurfaceStatus(
            name="memo_mcp",
            status="ok" if memo_mcp_ok else "warn",
            required=False,
            summary=(
                "aoa-memo MCP access plane is configured."
                if memo_mcp_ok
                else "aoa-memo MCP access plane is not wired into the Codex plane."
            ),
            evidence=memo_evidence,
            next_step="Wire [mcp_servers.aoa_memo] to .codex/bin/aoa-memo-mcp-server.py and keep the service source under abyss-stack.",
        )
    )

    session_memory_entry = mcp_servers.get("aoa_session_memory") if isinstance(mcp_servers, dict) else None
    session_memory_script_path, session_memory_evidence = _resolve_mcp_script(root, session_memory_entry)
    if isinstance(mcp_servers, dict) and "aoa_session_memory" in mcp_servers:
        session_memory_evidence.insert(0, "[mcp_servers.aoa_session_memory] in .codex/config.toml")
    if session_memory_script_path is not None and session_memory_script_path.exists():
        session_memory_evidence.append(str(session_memory_script_path))
    if (root / ".aoa").exists():
        session_memory_evidence.append(str(root / ".aoa"))
    if session_memory_service.exists():
        session_memory_evidence.append(str(session_memory_service))
    session_memory_mcp_ok = (
        isinstance(mcp_servers, dict)
        and "aoa_session_memory" in mcp_servers
        and session_memory_script_path is not None
        and session_memory_script_path.exists()
        and (root / ".aoa").exists()
    )
    surfaces.append(
        SurfaceStatus(
            name="session_memory_mcp",
            status="ok" if session_memory_mcp_ok else "warn",
            required=False,
            summary=(
                "aoa-session-memory MCP access plane looks wired."
                if session_memory_mcp_ok
                else "aoa-session-memory MCP access plane is not wired into the Codex plane."
            ),
            evidence=session_memory_evidence,
            next_step="Wire [mcp_servers.aoa_session_memory] to .codex/bin/aoa-session-memory-mcp-server.py and keep raw session truth in .aoa.",
        )
    )

    evals_entry = mcp_servers.get("aoa_evals") if isinstance(mcp_servers, dict) else None
    evals_script_path, evals_evidence = _resolve_mcp_script(root, evals_entry)
    if evals_repo.exists():
        evals_evidence.insert(0, str(evals_repo))
    if isinstance(mcp_servers, dict) and "aoa_evals" in mcp_servers:
        evals_evidence.insert(
            1 if evals_repo.exists() else 0,
            "[mcp_servers.aoa_evals] in .codex/config.toml",
        )
    if evals_script_path is not None and evals_script_path.exists():
        evals_evidence.append(str(evals_script_path))
    if evals_catalog.exists():
        evals_evidence.append(str(evals_catalog))
    if evals_contract.exists():
        evals_evidence.append(str(evals_contract))
    if evals_service.exists():
        evals_evidence.append(str(evals_service))
    evals_mcp_ok = (
        not evals_repo.exists()
        or (
            isinstance(mcp_servers, dict)
            and "aoa_evals" in mcp_servers
            and evals_script_path is not None
            and evals_script_path.exists()
            and evals_catalog.exists()
            and evals_contract.exists()
        )
    )
    surfaces.append(
        SurfaceStatus(
            name="evals_mcp",
            status="info" if not evals_repo.exists() else ("ok" if evals_mcp_ok else "warn"),
            required=False,
            summary=(
                "aoa-evals repo not present under the workspace root."
                if not evals_repo.exists()
                else ("aoa-evals MCP access plane looks wired." if evals_mcp_ok else "aoa-evals repo exists but its MCP seam is incomplete.")
            ),
            evidence=evals_evidence,
            next_step="Wire [mcp_servers.aoa_evals] to .codex/bin/aoa-evals-mcp-server.py and keep proof authority in aoa-evals.",
        )
    )

    decisions_entry = mcp_servers.get("aoa_decisions") if isinstance(mcp_servers, dict) else None
    decisions_script_path, decisions_evidence = _resolve_mcp_script(root, decisions_entry)
    if isinstance(mcp_servers, dict) and "aoa_decisions" in mcp_servers:
        decisions_evidence.insert(0, "[mcp_servers.aoa_decisions] in .codex/config.toml")
    if decisions_script_path is not None and decisions_script_path.exists():
        decisions_evidence.append(str(decisions_script_path))
    if decisions_service.exists():
        decisions_evidence.append(str(decisions_service))
    decisions_mcp_ok = (
        isinstance(mcp_servers, dict)
        and "aoa_decisions" in mcp_servers
        and decisions_script_path is not None
        and decisions_script_path.exists()
    )
    surfaces.append(
        SurfaceStatus(
            name="decisions_mcp",
            status="ok" if decisions_mcp_ok else "warn",
            required=False,
            summary=(
                "aoa-decisions MCP access plane looks wired."
                if decisions_mcp_ok
                else "aoa-decisions MCP access plane is not wired into the Codex plane."
            ),
            evidence=decisions_evidence,
            next_step="Wire [mcp_servers.aoa_decisions] to .codex/bin/aoa-decisions-mcp-server.py and keep decision truth in repo-local docs/decisions lanes.",
        )
    )

    machine_entry = mcp_servers.get("abyss_machine") if isinstance(mcp_servers, dict) else None
    machine_script_path, machine_evidence = _resolve_mcp_script(root, machine_entry)
    if isinstance(mcp_servers, dict) and "abyss_machine" in mcp_servers:
        machine_evidence.insert(0, "[mcp_servers.abyss_machine] in .codex/config.toml")
    if machine_script_path is not None and machine_script_path.exists():
        machine_evidence.append(str(machine_script_path))
    if machine_service.exists():
        machine_evidence.append(str(machine_service))
    machine_mcp_ok = (
        isinstance(mcp_servers, dict)
        and "abyss_machine" in mcp_servers
        and machine_script_path is not None
        and machine_script_path.exists()
    )
    surfaces.append(
        SurfaceStatus(
            name="machine_mcp",
            status="ok" if machine_mcp_ok else "warn",
            required=False,
            summary=(
                "abyss-machine MCP access plane looks wired."
                if machine_mcp_ok
                else "abyss-machine MCP access plane is not wired into the Codex plane."
            ),
            evidence=machine_evidence,
            next_step="Wire [mcp_servers.abyss_machine] to .codex/bin/abyss-machine-mcp-server.py and keep host truth in abyss-machine.",
        )
    )

    missing_subagents = [name for name in EXPECTED_SUBAGENTS if name not in subagent_names]
    subagents_ok = not missing_subagents and agents_dir.exists()
    subagent_evidence = [str(agents_dir)] if agents_dir.exists() else []
    subagent_evidence.extend(f"name={name}" for name in subagent_names)
    surfaces.append(
        SurfaceStatus(
            name="subagents_surface",
            status="ok" if subagents_ok else "warn",
            required=True,
            summary="Expected AoA subagents are present." if subagents_ok else "Some expected AoA subagents are missing.",
            evidence=subagent_evidence,
            next_step="Generate or copy the AoA subagent TOML files into .codex/agents/ and register them in workspace config if needed.",
        )
    )

    workspace_skill_entries = (
        sorted(path.name for path in workspace_skill_dir.iterdir())
        if workspace_skill_dir.exists()
        else []
    )
    profiles = (
        shared_skill_profiles.get("profiles", {})
        if isinstance(shared_skill_profiles, dict)
        else {}
    )
    user_default = profiles.get("user-default", {}) if isinstance(profiles, dict) else {}
    shared_profile_declared = (
        isinstance(user_default, dict)
        and user_default.get("scope") == "user"
        and isinstance(user_default.get("skills"), list)
        and bool(user_default["skills"])
    )
    entry_home_declared = (
        isinstance(entry_home_manifest, dict)
        and entry_home_manifest.get("owner_repo") == "8Dionysus"
        and isinstance(entry_home_manifest.get("bundles"), list)
        and bool(entry_home_manifest["bundles"])
        and isinstance(entry_home_manifest.get("projection"), dict)
        and entry_home_manifest["projection"].get("root") == ".agents/skills"
    )
    skill_evidence: list[str] = []
    if shared_profile_declared:
        skill_evidence.append(str(shared_skill_profiles_path))
        skill_evidence.append("aoa-skills profile=user-default scope=user")
    if entry_home_declared:
        skill_evidence.append(str(entry_home_manifest_path))
    if workspace_skill_entries:
        skill_evidence.append(f"{workspace_skill_dir}: {workspace_skill_entries!r}")
        skill_status = "warn"
        skill_summary = "Workspace-root .agents/skills contains entries that require explicit owner review."
        skill_next_step = (
            "Classify each workspace-root entry against its owner before mutation; "
            "do not restore a shared workspace skill bridge."
        )
    elif shared_profile_declared and entry_home_declared:
        skill_status = "info"
        skill_summary = "Owner-scoped skill delivery sources are declared; live host visibility is not inferred."
        skill_next_step = (
            "Verify the user-default install through aoa-sdk, validate each repository home "
            "with its pinned owner contract, and inspect a fresh prompt inventory."
        )
    else:
        skill_status = "warn"
        skill_summary = "Owner-scoped shared-profile or repository-home source is incomplete."
        skill_next_step = (
            "Restore the missing owner source or manifest; do not replace it with a "
            "workspace-visible .agents/skills bridge."
        )
    surfaces.append(
        SurfaceStatus(
            name="skill_delivery_contract",
            status=skill_status,
            required=False,
            summary=skill_summary,
            evidence=skill_evidence,
            next_step=skill_next_step,
        )
    )

    convergence_tooling_evidence: list[str] = []
    tooling_ok = True
    for path in (
        convergence_scripts_dir / "aoa_codex_bootstrap.py",
        convergence_scripts_dir / "aoa_codex_doctor.py",
        convergence_scripts_dir / "aoa_codex_status.py",
        convergence_bin_dir / "aoa-codex-bootstrap",
        convergence_bin_dir / "aoa-codex-doctor",
        convergence_bin_dir / "aoa-codex-status",
    ):
        if path.exists():
            convergence_tooling_evidence.append(str(path))
        else:
            tooling_ok = False
    surfaces.append(
        SurfaceStatus(
            name="convergence_tooling",
            status="ok" if tooling_ok else "warn",
            required=False,
            summary="Convergence tooling is installed under .codex."
            if tooling_ok
            else "Convergence tooling is only partially installed under .codex.",
            evidence=convergence_tooling_evidence,
            next_step="Install the aoa_codex_converge package plus the .codex/scripts and .codex/bin wrappers.",
        )
    )

    counts = {"ok": 0, "warn": 0, "missing": 0, "info": 0}
    for surface in surfaces:
        counts[surface.status] = counts.get(surface.status, 0) + 1

    ready = not any(surface.required and surface.status != "ok" for surface in surfaces)
    return {
        "workspace_root": str(root),
        "ready": ready,
        "counts": counts,
        "surfaces": [surface.to_dict() for surface in surfaces],
    }


def report_to_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# AoA Codex convergence report",
        "",
        f"- workspace_root: `{report.get('workspace_root', '')}`",
        f"- ready: `{report.get('ready', False)}`",
    ]
    counts = report.get("counts", {})
    lines.append(
        f"- counts: ok={counts.get('ok', 0)}, warn={counts.get('warn', 0)}, "
        f"missing={counts.get('missing', 0)}, info={counts.get('info', 0)}"
    )
    lines.append("")
    lines.append("## Surfaces")
    lines.append("")
    for surface in report.get("surfaces", []):
        lines.append(f"### {surface.get('name', '')}")
        lines.append("")
        lines.append(f"- status: `{surface.get('status', '')}`")
        lines.append(f"- required: `{surface.get('required', False)}`")
        lines.append(f"- summary: {surface.get('summary', '')}")
        evidence = surface.get("evidence", [])
        if evidence:
            lines.append("- evidence:")
            for item in evidence:
                lines.append(f"  - `{item}`")
        else:
            lines.append("- evidence: none")
        lines.append(f"- next_step: {surface.get('next_step', '')}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


BOOTSTRAP_CONFIG_SNIPPET = """# Review-only convergence snippet.
# Merge this into /srv/AbyssOS/.codex/config.toml only if the marker entry is missing.
project_root_markers = ["AOA_WORKSPACE_ROOT", ".git"]
"""

BOOTSTRAP_WRAPPER_DOCTOR = """#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

python "${WORKSPACE_ROOT}/.codex/scripts/aoa_codex_doctor.py" --workspace-root "${WORKSPACE_ROOT}" "$@"
"""

BOOTSTRAP_WRAPPER_STATUS = """#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

python "${WORKSPACE_ROOT}/.codex/scripts/aoa_codex_status.py" --workspace-root "${WORKSPACE_ROOT}" "$@"
"""

BOOTSTRAP_WRAPPER_BOOTSTRAP = """#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

python "${WORKSPACE_ROOT}/.codex/scripts/aoa_codex_bootstrap.py" --workspace-root "${WORKSPACE_ROOT}" "$@"
"""


def write_bootstrap_scaffold(workspace_root: Path | str) -> dict[str, str]:
    root = _normalize_workspace_root(workspace_root)
    created: dict[str, str] = {}

    directories = [
        root / ".codex",
        root / ".codex" / "agents",
        root / ".codex" / "bin",
        root / ".codex" / "generated",
        root / ".codex" / "generated" / "codex",
        root / ".codex" / "scripts",
        root / ".codex" / "tools",
        root / ".agents",
    ]
    for path in directories:
        path.mkdir(parents=True, exist_ok=True)
        created[str(path)] = "dir"

    marker = root / "AOA_WORKSPACE_ROOT"
    if not marker.exists():
        marker.write_text("AoA sibling workspace root marker.\n", encoding="utf-8")
        created[str(marker)] = "file"

    config_snippet = root / ".codex" / "generated" / "codex" / "config.convergence.generated.toml"
    config_snippet.write_text(BOOTSTRAP_CONFIG_SNIPPET, encoding="utf-8")
    created[str(config_snippet)] = "file"

    wrapper_specs = {
        root / ".codex" / "bin" / "aoa-codex-doctor": BOOTSTRAP_WRAPPER_DOCTOR,
        root / ".codex" / "bin" / "aoa-codex-status": BOOTSTRAP_WRAPPER_STATUS,
        root / ".codex" / "bin" / "aoa-codex-bootstrap": BOOTSTRAP_WRAPPER_BOOTSTRAP,
    }
    for path, text in wrapper_specs.items():
        path.write_text(text, encoding="utf-8")
        os.chmod(path, 0o755)
        created[str(path)] = "file"

    return created
