from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import render_codex_plane


@dataclass(frozen=True)
class CodexPlaneValidationSummary:
    repo_root: Path
    workspace_root: Path
    profile_id: str


def validate_codex_plane_regeneration(
    repo_root: Path,
    workspace_root: Path,
) -> CodexPlaneValidationSummary:
    resolved_repo_root = repo_root.expanduser().resolve()
    resolved_workspace_root = workspace_root.expanduser().resolve()

    manifest_path = resolved_repo_root / "config" / "codex_plane" / "runtime_manifest.v1.json"
    profile_path = resolved_repo_root / "config" / "codex_plane" / "profiles" / "linux-python3.json"
    config_path = resolved_repo_root / ".codex" / "config.toml"
    hooks_path = resolved_repo_root / ".codex" / "hooks.json"

    manifest = render_codex_plane.load_json_object(manifest_path)
    profile = render_codex_plane.load_json_object(profile_path)
    expected_config = render_codex_plane.render_config_toml(
        manifest=manifest,
        profile=profile,
        workspace_root=resolved_workspace_root,
        manifest_rel="config/codex_plane/runtime_manifest.v1.json",
        profile_rel="config/codex_plane/profiles/linux-python3.json",
    )
    expected_hooks = json.dumps(
        render_codex_plane.render_hooks_json(
            manifest=manifest,
            profile=profile,
            workspace_root=resolved_workspace_root,
        ),
        ensure_ascii=False,
        indent=2,
    ) + "\n"

    if not config_path.exists():
        raise ValueError(f"missing rendered config: {config_path}")
    if not hooks_path.exists():
        raise ValueError(f"missing rendered hooks: {hooks_path}")

    actual_config = config_path.read_text(encoding="utf-8")
    actual_hooks = hooks_path.read_text(encoding="utf-8")
    if actual_config != expected_config:
        raise ValueError(".codex/config.toml drift detected; rerender from config/codex_plane/")
    if actual_hooks != expected_hooks:
        raise ValueError(".codex/hooks.json drift detected; rerender from config/codex_plane/")

    expected_server_names = [server["name"] for server in manifest["mcp_servers"]]
    if expected_server_names != ["aoa_workspace", "aoa_stats", "dionysus"]:
        raise ValueError("manifest must preserve the stable AoA MCP server names")

    return CodexPlaneValidationSummary(
        repo_root=resolved_repo_root,
        workspace_root=resolved_workspace_root,
        profile_id=str(profile.get("profile_id") or ""),
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate rendered AoA Codex plane surfaces against the manifest/profile."
    )
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--workspace-root", type=Path, default=Path("/srv"))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    summary = validate_codex_plane_regeneration(args.repo_root, args.workspace_root)
    print("codex plane regeneration: OK")
    print(f"repo_root={summary.repo_root}")
    print(f"workspace_root={summary.workspace_root}")
    print(f"profile_id={summary.profile_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
