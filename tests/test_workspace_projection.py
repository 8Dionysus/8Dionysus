from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from project_workspace_root import project_workspace_root, render_agents_text


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class WorkspaceProjectionTests(unittest.TestCase):
    def test_render_agents_text_substitutes_workspace_root(self) -> None:
        rendered = render_agents_text("use <workspace-root>/foo", Path("/srv"))
        self.assertEqual(rendered, "use /srv/foo")

    def test_dry_run_reports_managed_surface_changes_without_runtime_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            repo_root = temp_root / "8Dionysus"
            workspace_root = temp_root / "workspace"
            self._make_repo(repo_root, temp_root)

            report = project_workspace_root(repo_root, workspace_root, execute=False)
            self.assertTrue(report["changed"])
            self.assertEqual(report["owner_repo"], "8Dionysus")
            self.assertTrue(report["projection_contract"]["edit_source_first"])
            self.assertTrue(report["projection_contract"]["do_not_edit_live_workspace_copy_as_source"])
            self.assertFalse(report["projection_contract"]["profile_readme_projected"])
            self.assertIn("Do not patch the live workspace copy", report["next_step"])
            self.assertIn((repo_root / "AGENTS.md").as_posix(), report["projection_contract"]["source_paths"])
            self.assertIn((workspace_root / "AGENTS.md").as_posix(), report["projection_contract"]["projected_paths"])

            paths = {entry["dest_path"] for entry in report["operations"]}
            self.assertIn("AGENTS.md", paths)
            self.assertIn("AOA_WORKSPACE_ROOT", paths)
            self.assertIn(".agents/plugins/marketplace.json", paths)
            self.assertIn(".agents/skills/demo-skill", paths)
            self.assertIn(".codex/config.toml", paths)
            self.assertNotIn(".codex/generated/report.json", paths)
            self.assertNotIn(".codex/tools/__pycache__/ghost.pyc", paths)
            json.dumps(report)

    def test_execute_projects_shared_root_surfaces(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            repo_root = temp_root / "8Dionysus"
            workspace_root = temp_root / "workspace"
            self._make_repo(repo_root, temp_root)
            write_text(workspace_root / "AGENTS.md", "stale\n")

            report = project_workspace_root(repo_root, workspace_root, execute=True)
            self.assertTrue(report["changed"])
            self.assertEqual(report["owner_repo"], "8Dionysus")
            self.assertTrue(report["projection_contract"]["apply_via_projection"])
            self.assertIn("aoa-workspace-project --execute --json", report["projection_contract"]["execute_command"])
            self.assertIn("/workspace", (workspace_root / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertTrue((workspace_root / "AOA_WORKSPACE_ROOT").exists())
            self.assertEqual(
                json.loads((workspace_root / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))["name"],
                "aoa-local-plugins",
            )
            projected_skill = workspace_root / ".agents" / "skills" / "demo-skill"
            self.assertTrue(projected_skill.is_symlink())
            self.assertEqual(os.readlink(projected_skill), os.readlink(repo_root / ".agents" / "skills" / "demo-skill"))
            self.assertTrue((workspace_root / ".codex" / "config.toml").exists())
            self.assertFalse((workspace_root / ".codex" / "generated" / "report.json").exists())
            self.assertFalse((workspace_root / ".codex" / "tools" / "__pycache__" / "ghost.pyc").exists())

    def _make_repo(self, repo_root: Path, temp_root: Path) -> None:
        write_text(
            repo_root / "AGENTS.md",
            "# AGENTS.md — <workspace-root> workspace\n\nUse <workspace-root>/.codex/config.toml\n",
        )
        write_text(repo_root / "AOA_WORKSPACE_ROOT", "marker\n")
        write_text(repo_root / ".codex" / "config.toml", 'project_root_markers = ["AOA_WORKSPACE_ROOT"]\n')
        write_text(repo_root / ".codex" / "generated" / "report.json", "{}\n")
        write_text(repo_root / ".codex" / "tools" / "__pycache__" / "ghost.pyc", "nope")
        write_text(repo_root / ".agents" / "plugins" / "marketplace.json", '{"name": "aoa-local-plugins"}\n')

        skill_target = temp_root / "aoa-skills" / ".agents" / "skills" / "demo-skill"
        skill_target.mkdir(parents=True, exist_ok=True)
        (repo_root / ".agents" / "skills").mkdir(parents=True, exist_ok=True)
        (repo_root / ".agents" / "skills" / "demo-skill").symlink_to(skill_target)


if __name__ == "__main__":
    unittest.main()
