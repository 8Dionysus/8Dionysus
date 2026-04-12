from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT_PLACEHOLDER = "<workspace-root>"


@dataclass(frozen=True)
class SurfaceSpec:
    name: str
    source_rel: str
    dest_rel: str
    mode: str
    exclude_roots: tuple[str, ...] = ()
    exclude_names: tuple[str, ...] = ()
    exclude_suffixes: tuple[str, ...] = ()


@dataclass
class Operation:
    action: str
    surface: str
    dest_path: Path
    source_path: Path | None = None
    rendered_text: str | None = None
    symlink_target: str | None = None
    reason: str = ""
    file_mode: int | None = None

    def to_summary(self, workspace_root: Path) -> dict[str, object]:
        payload: dict[str, object] = {
            "action": self.action,
            "surface": self.surface,
            "dest_path": _display_path(self.dest_path, workspace_root),
            "reason": self.reason,
        }
        if self.source_path is not None:
            payload["source_path"] = self.source_path.as_posix()
        if self.symlink_target is not None:
            payload["symlink_target"] = self.symlink_target
        return payload


SHARED_ROOT_SURFACES = (
    SurfaceSpec("agents_doc", "AGENTS.md", "AGENTS.md", "render_text"),
    SurfaceSpec("workspace_marker", "AOA_WORKSPACE_ROOT", "AOA_WORKSPACE_ROOT", "copy_file"),
    SurfaceSpec("agent_install", ".agents", ".agents", "copy_tree"),
    SurfaceSpec(
        "codex_install",
        ".codex",
        ".codex",
        "copy_tree",
        exclude_roots=("generated",),
        exclude_names=("__pycache__", ".pytest_cache"),
        exclude_suffixes=(".pyc", ".pyo", ".pyd"),
    ),
)


def render_agents_text(source_text: str, workspace_root: Path) -> str:
    return source_text.replace(WORKSPACE_ROOT_PLACEHOLDER, workspace_root.as_posix())


def project_workspace_root(
    repo_root: Path,
    workspace_root: Path,
    *,
    execute: bool = False,
    prune: bool = False,
) -> dict[str, object]:
    repo_root = repo_root.resolve()
    workspace_root = workspace_root.resolve()
    operations = _build_operations(repo_root, workspace_root, prune=prune)
    if execute:
        for operation in operations:
            _apply_operation(operation)

    summary = [operation.to_summary(workspace_root) for operation in operations]
    projection_contract = _projection_contract(repo_root, workspace_root, changed=bool(summary))
    return {
        "repo_root": repo_root.as_posix(),
        "owner_repo": "8Dionysus",
        "workspace_root": workspace_root.as_posix(),
        "mode": "execute" if execute else "dry-run",
        "prune": prune,
        "changed": bool(summary),
        "surface_count": len(SHARED_ROOT_SURFACES),
        "managed_surfaces": [surface.dest_rel for surface in SHARED_ROOT_SURFACES],
        "projection_contract": projection_contract,
        "next_step": projection_contract["next_step"],
        "operation_count": len(summary),
        "operations": summary,
    }


def _projection_contract(repo_root: Path, workspace_root: Path, *, changed: bool) -> dict[str, object]:
    source_paths = [(repo_root / surface.source_rel).as_posix() for surface in SHARED_ROOT_SURFACES]
    projected_paths = [(workspace_root / surface.dest_rel).as_posix() for surface in SHARED_ROOT_SURFACES]
    if changed:
        next_step = (
            "Edit the source-owned surface under 8Dionysus if the change is real, then rerun "
            "aoa-workspace-project --execute. Do not patch the live workspace copy as the source of truth."
        )
    else:
        next_step = (
            "Projection is already in sync. If you need to change a shared-root surface, edit 8Dionysus first and "
            "then rerun aoa-workspace-project --execute."
        )
    return {
        "edit_source_first": True,
        "apply_via_projection": True,
        "do_not_edit_live_workspace_copy_as_source": True,
        "profile_readme_projected": False,
        "profile_readme_note": "8Dionysus/README.md stays profile-owned and is not part of the shared-root projection.",
        "source_root": repo_root.as_posix(),
        "workspace_root": workspace_root.as_posix(),
        "source_paths": source_paths,
        "projected_paths": projected_paths,
        "check_command": f"{(workspace_root / '.codex' / 'bin' / 'aoa-workspace-project').as_posix()} --check --json",
        "execute_command": f"{(workspace_root / '.codex' / 'bin' / 'aoa-workspace-project').as_posix()} --execute --json",
        "next_step": next_step,
    }


def _build_operations(repo_root: Path, workspace_root: Path, *, prune: bool) -> list[Operation]:
    operations: list[Operation] = []
    for surface in SHARED_ROOT_SURFACES:
        source_path = repo_root / surface.source_rel
        dest_path = workspace_root / surface.dest_rel

        if not source_path.exists():
            raise FileNotFoundError(f"missing source surface: {source_path}")

        if surface.mode == "render_text":
            operations.extend(_plan_rendered_file(surface, source_path, dest_path, workspace_root))
        elif surface.mode == "copy_file":
            operations.extend(_plan_regular_file(surface, source_path, dest_path))
        elif surface.mode == "copy_tree":
            operations.extend(_plan_tree(surface, source_path, dest_path, prune=prune))
        else:
            raise ValueError(f"unsupported surface mode: {surface.mode}")

    return operations


def _plan_rendered_file(
    surface: SurfaceSpec,
    source_path: Path,
    dest_path: Path,
    workspace_root: Path,
) -> list[Operation]:
    rendered = render_agents_text(source_path.read_text(encoding="utf-8"), workspace_root)
    if _same_text_file(dest_path, rendered):
        return []
    return [
        Operation(
            action="write_text",
            surface=surface.name,
            dest_path=dest_path,
            source_path=source_path,
            rendered_text=rendered,
            reason=_text_reason(dest_path),
            file_mode=stat.S_IMODE(source_path.stat().st_mode),
        )
    ]


def _plan_regular_file(surface: SurfaceSpec, source_path: Path, dest_path: Path) -> list[Operation]:
    if _same_regular_file(source_path, dest_path):
        return []
    return [
        Operation(
            action="copy_file",
            surface=surface.name,
            dest_path=dest_path,
            source_path=source_path,
            reason=_path_reason(dest_path),
            file_mode=stat.S_IMODE(source_path.stat().st_mode),
        )
    ]


def _plan_tree(surface: SurfaceSpec, source_root: Path, dest_root: Path, *, prune: bool) -> list[Operation]:
    operations: list[Operation] = []
    expected_entries: dict[Path, str] = {}

    for entry_type, rel_path, source_path in _iter_tree_entries(source_root, surface):
        expected_entries[rel_path] = entry_type
        dest_path = dest_root / rel_path

        if entry_type == "dir":
            if dest_path.exists():
                if dest_path.is_symlink() or not dest_path.is_dir():
                    operations.append(
                        Operation(
                            action="mkdir",
                            surface=surface.name,
                            dest_path=dest_path,
                            source_path=source_path,
                            reason="replace_non_directory",
                        )
                    )
            else:
                operations.append(
                    Operation(
                        action="mkdir",
                        surface=surface.name,
                        dest_path=dest_path,
                        source_path=source_path,
                        reason="missing_directory",
                    )
                )
            continue

        if entry_type == "symlink":
            symlink_target = os.readlink(source_path)
            if not dest_path.is_symlink() or os.readlink(dest_path) != symlink_target:
                operations.append(
                    Operation(
                        action="symlink",
                        surface=surface.name,
                        dest_path=dest_path,
                        source_path=source_path,
                        symlink_target=symlink_target,
                        reason=_path_reason(dest_path),
                    )
                )
            continue

        if not _same_regular_file(source_path, dest_path):
            operations.append(
                Operation(
                    action="copy_file",
                    surface=surface.name,
                    dest_path=dest_path,
                    source_path=source_path,
                    reason=_path_reason(dest_path),
                    file_mode=stat.S_IMODE(source_path.stat().st_mode),
                )
            )

    if prune and dest_root.exists():
        extras: list[Operation] = []
        for entry_type, rel_path, dest_path in _iter_tree_entries(dest_root, surface):
            if rel_path not in expected_entries:
                extras.append(
                    Operation(
                        action="remove",
                        surface=surface.name,
                        dest_path=dest_path,
                        reason="prune_extra_path",
                    )
                )
        operations.extend(sorted(extras, key=lambda item: len(item.dest_path.parts), reverse=True))

    return operations


def _iter_tree_entries(root: Path, surface: SurfaceSpec, rel_root: Path | None = None):
    rel_root = rel_root or Path()
    for child in sorted(root.iterdir(), key=lambda path: path.name):
        rel_path = rel_root / child.name
        if _should_exclude(surface, rel_path):
            continue
        if child.is_symlink():
            yield "symlink", rel_path, child
            continue
        if child.is_dir():
            yield "dir", rel_path, child
            yield from _iter_tree_entries(child, surface, rel_path)
            continue
        if child.is_file():
            yield "file", rel_path, child


def _should_exclude(surface: SurfaceSpec, rel_path: Path) -> bool:
    parts = rel_path.parts
    if parts and parts[0] in surface.exclude_roots:
        return True
    if any(part in surface.exclude_names for part in parts):
        return True
    return rel_path.suffix in surface.exclude_suffixes


def _same_regular_file(source_path: Path, dest_path: Path) -> bool:
    if not dest_path.exists() or dest_path.is_symlink() or not dest_path.is_file():
        return False
    if source_path.read_bytes() != dest_path.read_bytes():
        return False
    return stat.S_IMODE(source_path.stat().st_mode) == stat.S_IMODE(dest_path.stat().st_mode)


def _same_text_file(dest_path: Path, rendered_text: str) -> bool:
    if not dest_path.exists() or dest_path.is_symlink() or not dest_path.is_file():
        return False
    return dest_path.read_text(encoding="utf-8") == rendered_text


def _apply_operation(operation: Operation) -> None:
    if operation.action == "mkdir":
        _replace_if_needed(operation.dest_path, keep_directory=True)
        operation.dest_path.mkdir(parents=True, exist_ok=True)
        return

    _ensure_parent_dir(operation.dest_path)

    if operation.action == "write_text":
        _replace_if_needed(operation.dest_path, keep_file=True)
        operation.dest_path.write_text(operation.rendered_text or "", encoding="utf-8")
        if operation.file_mode is not None:
            operation.dest_path.chmod(operation.file_mode)
        return

    if operation.action == "copy_file":
        _replace_if_needed(operation.dest_path, keep_file=True)
        if operation.source_path is None:
            raise ValueError("copy_file operation missing source_path")
        shutil.copy2(operation.source_path, operation.dest_path)
        return

    if operation.action == "symlink":
        _replace_if_needed(operation.dest_path)
        if operation.symlink_target is None:
            raise ValueError("symlink operation missing symlink_target")
        operation.dest_path.symlink_to(operation.symlink_target)
        return

    if operation.action == "remove":
        _replace_if_needed(operation.dest_path)
        return

    raise ValueError(f"unsupported operation: {operation.action}")


def _ensure_parent_dir(path: Path) -> None:
    if path.parent.exists() and path.parent.is_dir():
        return
    path.parent.mkdir(parents=True, exist_ok=True)


def _replace_if_needed(path: Path, *, keep_directory: bool = False, keep_file: bool = False) -> None:
    if path.is_symlink() or path.is_file():
        if keep_file and path.is_file() and not path.is_symlink():
            return
        path.unlink()
        return
    if path.exists():
        if keep_directory and path.is_dir():
            return
        shutil.rmtree(path)


def _display_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix() or "."
    except ValueError:
        return path.as_posix()


def _path_reason(dest_path: Path) -> str:
    if not dest_path.exists() and not dest_path.is_symlink():
        return "missing_destination"
    return "content_or_type_drift"


def _text_reason(dest_path: Path) -> str:
    if not dest_path.exists() and not dest_path.is_symlink():
        return "missing_destination"
    return "rendered_text_drift"


def _format_text_report(report: dict[str, object]) -> str:
    lines = [
        f"mode: {report['mode']}",
        f"workspace_root: {report['workspace_root']}",
        f"changed: {report['changed']}",
        f"operation_count: {report['operation_count']}",
        f"owner_repo: {report['owner_repo']}",
    ]
    for operation in report["operations"]:
        path = operation["dest_path"]
        reason = operation["reason"]
        suffix = ""
        if "symlink_target" in operation:
            suffix = f" -> {operation['symlink_target']}"
        lines.append(f"{operation['action']}: {path}{suffix} [{reason}]")
    lines.append(f"next_step: {report['next_step']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Project the selected 8Dionysus shared-root install surfaces into a live workspace root.",
    )
    parser.add_argument(
        "--workspace-root",
        type=Path,
        default=REPO_ROOT.parent,
        help="Target live workspace root. Defaults to the parent of this repository.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Apply the projection. Dry-run is the default.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit with status 1 when drift is detected. Does not mutate.",
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="Remove extra managed paths in the destination surfaces.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of text.",
    )
    args = parser.parse_args()

    if args.execute and args.check:
        parser.error("--execute and --check cannot be used together")

    report = project_workspace_root(REPO_ROOT, args.workspace_root, execute=args.execute, prune=args.prune)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(_format_text_report(report))

    if args.check and report["changed"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
