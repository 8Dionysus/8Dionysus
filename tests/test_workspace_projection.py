from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from project_workspace_root import inspect_source_currentness, project_workspace_root, render_agents_text


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class WorkspaceProjectionTests(unittest.TestCase):
    def test_render_agents_text_substitutes_workspace_root(self) -> None:
        rendered = render_agents_text("use <workspace-root>/foo", Path("/srv/AbyssOS"))
        self.assertEqual(rendered, "use /srv/AbyssOS/foo")

    def test_dry_run_reports_managed_surface_changes_without_runtime_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            repo_root = temp_root / "8Dionysus"
            workspace_root = temp_root / "workspace"
            self._make_repo(repo_root)

            report = project_workspace_root(repo_root, workspace_root, execute=False, prune=True)
            self.assertTrue(report["changed"])
            self.assertEqual(report["owner_repo"], "8Dionysus")
            self.assertTrue(report["projection_contract"]["edit_source_first"])
            self.assertTrue(report["projection_contract"]["do_not_edit_live_workspace_copy_as_source"])
            self.assertFalse(report["projection_contract"]["profile_readme_projected"])
            self.assertFalse(report["projection_contract"]["workspace_skill_projection_managed"])
            self.assertFalse(
                report["projection_contract"]["workspace_codex_deploy_local_roots_managed"]
            )
            self.assertFalse(
                report["projection_contract"]["workspace_codex_deploy_composed_paths_managed"]
            )
            self.assertEqual(
                report["projection_contract"]["workspace_codex_deploy_composed_paths"],
                [
                    (workspace_root / ".codex" / "config.toml").as_posix(),
                    (workspace_root / ".codex" / "agents").as_posix(),
                ],
            )
            self.assertEqual(report["projection_contract"]["shared_skill_install_owner"], "aoa-skills")
            self.assertEqual(report["projection_contract"]["shared_skill_install_scope"], "user")
            self.assertIn("Do not patch the live workspace copy", report["next_step"])
            self.assertIn((repo_root / "AGENTS.md").as_posix(), report["projection_contract"]["source_paths"])
            self.assertIn((workspace_root / "AGENTS.md").as_posix(), report["projection_contract"]["projected_paths"])

            paths = {entry["dest_path"] for entry in report["operations"]}
            self.assertIn("AGENTS.md", paths)
            self.assertIn("AOA_WORKSPACE_ROOT", paths)
            self.assertNotIn(".agents/plugins/marketplace.json", paths)
            self.assertNotIn(".agents/skills/demo-skill", paths)
            self.assertNotIn(".codex/config.toml", paths)
            self.assertNotIn(".codex/agents/architect.toml", paths)
            self.assertIn(".codex/plugins/active.txt", paths)
            self.assertNotIn(".codex/generated/report.json", paths)
            self.assertNotIn(".codex/worktrees/keep/AGENTS.md", paths)
            self.assertNotIn(".codex/tools/__pycache__/ghost.pyc", paths)
            json.dumps(report)

    def test_execute_projects_shared_root_surfaces(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            repo_root = temp_root / "8Dionysus"
            workspace_root = temp_root / "workspace"
            self._make_repo(repo_root)
            write_text(workspace_root / "AGENTS.md", "stale\n")
            write_text(
                workspace_root / ".agents" / "skills" / "workspace-home" / "SKILL.md",
                "# workspace-owned\n",
            )
            write_text(
                workspace_root / ".codex" / "worktrees" / "keep" / "AGENTS.md",
                "# deploy-local worktree\n",
            )
            live_config = '[mcp_servers.aoa_kag]\nurl = "http://127.0.0.1:5425/mcp"\n'
            live_agent = "name = \"architect\"\n[features]\nplugins = false\n"
            write_text(workspace_root / ".codex" / "config.toml", live_config)
            write_text(workspace_root / ".codex" / "agents" / "architect.toml", live_agent)
            write_text(workspace_root / ".codex" / "plugins" / "retired.txt", "retired\n")
            write_text(
                workspace_root / ".agents" / "plugins" / "marketplace.json",
                '{"name": "retired-launchers"}\n',
            )

            report = project_workspace_root(repo_root, workspace_root, execute=True, prune=True)
            self.assertTrue(report["changed"])
            self.assertEqual(report["owner_repo"], "8Dionysus")
            self.assertTrue(report["projection_contract"]["apply_via_projection"])
            self.assertIn("aoa-workspace-project --execute --json", report["projection_contract"]["execute_command"])
            self.assertIn("/workspace", (workspace_root / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertTrue((workspace_root / "AOA_WORKSPACE_ROOT").exists())
            self.assertFalse(
                (workspace_root / ".agents" / "plugins" / "marketplace.json").exists()
            )
            projected_skill = workspace_root / ".agents" / "skills" / "demo-skill"
            self.assertFalse(projected_skill.exists())
            self.assertEqual(
                (workspace_root / ".agents" / "skills" / "workspace-home" / "SKILL.md").read_text(
                    encoding="utf-8"
                ),
                "# workspace-owned\n",
            )
            self.assertEqual(
                (workspace_root / ".codex" / "config.toml").read_text(encoding="utf-8"),
                live_config,
            )
            self.assertEqual(
                (workspace_root / ".codex" / "agents" / "architect.toml").read_text(encoding="utf-8"),
                live_agent,
            )
            self.assertEqual(
                (workspace_root / ".codex" / "plugins" / "active.txt").read_text(encoding="utf-8"),
                "active\n",
            )
            self.assertFalse((workspace_root / ".codex" / "plugins" / "retired.txt").exists())
            self.assertFalse((workspace_root / ".codex" / "generated" / "report.json").exists())
            self.assertEqual(
                (workspace_root / ".codex" / "worktrees" / "keep" / "AGENTS.md").read_text(
                    encoding="utf-8"
                ),
                "# deploy-local worktree\n",
            )
            self.assertFalse((workspace_root / ".codex" / "tools" / "__pycache__" / "ghost.pyc").exists())

    def test_source_currentness_rejects_stale_or_managed_dirty_owner_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "8Dionysus"
            self._make_repo(repo_root)
            self._git(repo_root, "init", "--initial-branch=main")
            self._git(repo_root, "config", "user.name", "Projection Test")
            self._git(repo_root, "config", "user.email", "projection-test@example.invalid")
            self._git(repo_root, "add", ".")
            self._git(repo_root, "commit", "-m", "initial")
            self._git(repo_root, "update-ref", "refs/remotes/origin/main", "HEAD")

            current = inspect_source_currentness(repo_root)
            self.assertTrue(current["current"])
            self.assertEqual(current["managed_dirty_paths"], [])

            write_text(repo_root / ".agents" / "skills" / "demo-skill" / "SKILL.md", "# local projection\n")
            write_text(repo_root / ".codex" / "config.toml", "# deploy-composed\n")
            write_text(repo_root / ".codex" / "agents" / "architect.toml", "# aoa-agents projection\n")
            excluded_only = inspect_source_currentness(repo_root)
            self.assertTrue(excluded_only["current"])
            self.assertEqual(excluded_only["managed_dirty_paths"], [])

            write_text(repo_root / "scripts" / "project_workspace_root.py", "# unreviewed projector\n")
            dirty_control = inspect_source_currentness(repo_root)
            self.assertFalse(dirty_control["current"])
            self.assertEqual(
                dirty_control["managed_dirty_paths"],
                ["scripts/project_workspace_root.py"],
            )
            (repo_root / "scripts" / "project_workspace_root.py").unlink()

            write_text(repo_root / ".codex" / "plugins" / "active.txt", "managed change\n")
            managed_dirty = inspect_source_currentness(repo_root)
            self.assertFalse(managed_dirty["current"])
            self.assertIn("managed_source_dirty", managed_dirty["reasons"])
            self.assertEqual(managed_dirty["managed_dirty_paths"], [".codex/plugins/active.txt"])

            self._git(repo_root, "add", ".")
            self._git(repo_root, "commit", "-m", "advance source")
            stale_ref = inspect_source_currentness(repo_root)
            self.assertFalse(stale_ref["current"])
            self.assertIn("head_differs_from_source_reference", stale_ref["reasons"])
            self.assertFalse(stale_ref["managed_source_dirty"])

    def test_execute_refuses_noncurrent_source_before_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            repo_root = temp_root / "8Dionysus"
            workspace_root = temp_root / "workspace"
            self._make_repo(repo_root)
            self._git(repo_root, "init", "--initial-branch=main")
            self._git(repo_root, "config", "user.name", "Projection Test")
            self._git(repo_root, "config", "user.email", "projection-test@example.invalid")
            self._git(repo_root, "add", ".")
            self._git(repo_root, "commit", "-m", "initial")
            self._git(repo_root, "update-ref", "refs/remotes/origin/main", "HEAD")

            script = Path(__file__).resolve().parents[1] / "scripts" / "project_workspace_root.py"
            first = subprocess.run(
                [
                    sys.executable,
                    script.as_posix(),
                    "--source-root",
                    repo_root.as_posix(),
                    "--workspace-root",
                    workspace_root.as_posix(),
                    "--execute",
                    "--prune",
                    "--json",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            projected_before = (workspace_root / ".codex" / "plugins" / "active.txt").read_text(
                encoding="utf-8"
            )

            write_text(repo_root / ".codex" / "plugins" / "active.txt", "unsafe branch value\n")
            refused = subprocess.run(
                [
                    sys.executable,
                    script.as_posix(),
                    "--source-root",
                    repo_root.as_posix(),
                    "--workspace-root",
                    workspace_root.as_posix(),
                    "--execute",
                    "--prune",
                    "--json",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(refused.returncode, 2)
            report = json.loads(refused.stdout)
            self.assertEqual(report["mode"], "refused")
            self.assertEqual(report["operation_count"], 0)
            self.assertIn("managed_source_dirty", report["source_currentness"]["reasons"])
            self.assertEqual(
                (workspace_root / ".codex" / "plugins" / "active.txt").read_text(encoding="utf-8"),
                projected_before,
            )

    def _make_repo(self, repo_root: Path) -> None:
        write_text(
            repo_root / "AGENTS.md",
            "# AGENTS.md — <workspace-root> workspace\n\nUse <workspace-root>/.codex/config.toml\n",
        )
        write_text(repo_root / "AOA_WORKSPACE_ROOT", "marker\n")
        write_text(repo_root / ".codex" / "config.toml", 'project_root_markers = ["AOA_WORKSPACE_ROOT"]\n')
        write_text(repo_root / ".codex" / "agents" / "architect.toml", 'name = "portable-architect"\n')
        write_text(repo_root / ".codex" / "plugins" / "active.txt", "active\n")
        write_text(repo_root / ".codex" / "generated" / "report.json", "{}\n")
        write_text(repo_root / ".codex" / "worktrees" / "source-only" / "AGENTS.md", "# no projection\n")
        write_text(repo_root / ".codex" / "tools" / "__pycache__" / "ghost.pyc", "nope")
        write_text(repo_root / ".agents" / "skills" / "demo-skill" / "SKILL.md", "# must not project\n")

    def _git(self, repo_root: Path, *args: str) -> None:
        subprocess.run(
            ["git", "-C", repo_root.as_posix(), *args],
            check=True,
            capture_output=True,
            text=True,
        )


if __name__ == "__main__":
    unittest.main()
