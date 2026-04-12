from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import render_codex_plane
from validate_codex_plane_regeneration import validate_codex_plane_regeneration


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class CodexPlaneRegenerationTests(unittest.TestCase):
    def test_renderer_matches_checked_in_current_srv_examples(self) -> None:
        manifest = render_codex_plane.load_json_object(
            REPO_ROOT / "config" / "codex_plane" / "runtime_manifest.v1.json"
        )
        profile = render_codex_plane.load_json_object(
            REPO_ROOT / "config" / "codex_plane" / "profiles" / "linux-python3.json"
        )
        workspace_root = Path("/srv")

        rendered_config = render_codex_plane.render_config_toml(
            manifest=manifest,
            profile=profile,
            workspace_root=workspace_root,
            manifest_rel="config/codex_plane/runtime_manifest.v1.json",
            profile_rel="config/codex_plane/profiles/linux-python3.json",
        )
        rendered_hooks = json.dumps(
            render_codex_plane.render_hooks_json(
                manifest=manifest,
                profile=profile,
                workspace_root=workspace_root,
            ),
            ensure_ascii=False,
            indent=2,
        ) + "\n"
        rendered_paths = json.dumps(
            render_codex_plane.render_paths_report(
                manifest=manifest,
                profile=profile,
                workspace_root=workspace_root,
            ),
            ensure_ascii=False,
            indent=2,
        ) + "\n"

        self.assertEqual(
            rendered_config,
            (REPO_ROOT / "config" / "codex_plane" / "examples" / "current-srv.config.toml").read_text(
                encoding="utf-8"
            ),
        )
        self.assertEqual(
            rendered_hooks,
            (REPO_ROOT / "config" / "codex_plane" / "examples" / "current-srv.hooks.json").read_text(
                encoding="utf-8"
            ),
        )
        self.assertEqual(
            rendered_paths,
            (REPO_ROOT / "config" / "codex_plane" / "examples" / "current-srv.paths.json").read_text(
                encoding="utf-8"
            ),
        )

    def test_validator_accepts_checked_in_srv_render(self) -> None:
        summary = validate_codex_plane_regeneration(REPO_ROOT, Path("/srv"))

        self.assertEqual(summary.repo_root, REPO_ROOT)
        self.assertEqual(summary.workspace_root, Path("/srv"))
        self.assertEqual(summary.profile_id, "linux-python3")

    def test_validator_detects_render_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_json(
                root / "config" / "codex_plane" / "runtime_manifest.v1.json",
                {
                    "version": "1.0",
                    "workspace_marker": "AOA_WORKSPACE_ROOT",
                    "project_root_markers": ["AOA_WORKSPACE_ROOT", ".git"],
                    "features": {"codex_hooks": True},
                    "agents": {"max_threads": 1, "max_depth": 1, "job_max_runtime_seconds": 60, "roles": []},
                    "repos": {"aoa-sdk": "aoa-sdk", "aoa-stats": "aoa-stats", "Dionysus": "Dionysus"},
                    "mcp_servers": [
                        {"name": "aoa_workspace", "repo_key": "aoa-sdk", "script_rel": "scripts/aoa_workspace_mcp_server.py"},
                        {"name": "aoa_stats", "repo_key": "aoa-stats", "script_rel": "scripts/aoa_stats_mcp_server.py"},
                        {"name": "dionysus", "repo_key": "Dionysus", "script_rel": "scripts/dionysus_mcp_server.py"},
                    ],
                    "hooks": {
                        "Stop": [
                            {
                                "script_rel": ".codex/hooks/aoa_stop_doctor.py",
                                "statusMessage": "AoA stop doctor",
                                "timeout": 20,
                            }
                        ]
                    },
                },
            )
            write_json(
                root / "config" / "codex_plane" / "profiles" / "linux-python3.json",
                {"profile_id": "linux-python3", "python_command": "python3", "python_prefix_args": []},
            )
            write_text(root / ".codex" / "config.toml", "drifted\n")
            write_text(root / ".codex" / "hooks.json", "{}\n")

            with self.assertRaisesRegex(ValueError, "config.toml drift detected"):
                validate_codex_plane_regeneration(root, Path("/srv"))


if __name__ == "__main__":
    unittest.main()
