from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class SystemCapabilityMapTests(unittest.TestCase):
    def test_capability_map_stays_discoverable_and_owner_bounded(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        posture = (REPO_ROOT / "docs" / "PUBLIC_ENTRY_POSTURE.md").read_text(encoding="utf-8")
        capability_map = (REPO_ROOT / "docs" / "SYSTEM_CAPABILITY_MAP.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("docs/SYSTEM_CAPABILITY_MAP.md", readme)
        self.assertIn("SYSTEM_CAPABILITY_MAP.md", posture)
        self.assertIn("routing surface, not a new source of truth", capability_map)
        self.assertIn("aoa skills enter", capability_map)
        self.assertIn("aoa skills guard", capability_map)
        self.assertIn("AOA-P-0025", capability_map)
        self.assertIn("AOA-P-0026", capability_map)
        self.assertIn("AOA-P-0027", capability_map)
        self.assertIn("AOA-P-0028", capability_map)
        self.assertIn("AOA-P-0029", capability_map)
        self.assertIn("AOA-P-0030", capability_map)
        self.assertIn("aoa_workspace", capability_map)
        self.assertIn("aoa_stats", capability_map)
        self.assertIn("dionysus", capability_map)
        self.assertIn("campaign cadence and deployment continuity as companion notes", capability_map)
        self.assertIn("no hidden scheduler", capability_map)

    def test_capability_map_tracks_launcher_and_convergence_surfaces(self) -> None:
        agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        capability_map = (REPO_ROOT / "docs" / "SYSTEM_CAPABILITY_MAP.md").read_text(
            encoding="utf-8"
        )
        marketplace = json.loads(
            (REPO_ROOT / ".agents" / "plugins" / "marketplace.json").read_text(
                encoding="utf-8"
            )
        )

        plugin_names = {plugin["name"] for plugin in marketplace["plugins"]}
        self.assertIn("aoa-shared-launchers", plugin_names)
        self.assertIn("aoa-shared-launchers", capability_map)

        for skill_name in (
            "aoa-workspace-recon",
            "aoa-growth-snapshot",
            "aoa-seed-route-inspect",
            "aoa-config-doctor",
        ):
            self.assertTrue(
                (
                    REPO_ROOT
                    / ".codex"
                    / "plugins"
                    / "aoa-shared-launchers"
                    / "skills"
                    / skill_name
                    / "SKILL.md"
                ).is_file()
            )
            self.assertIn(skill_name, capability_map)

        for wrapper_name in (
            "aoa-codex-doctor",
            "aoa-codex-status",
            "aoa-codex-bootstrap",
        ):
            self.assertTrue((REPO_ROOT / ".codex" / "bin" / wrapper_name).is_file())
            self.assertIn(wrapper_name, capability_map)
            self.assertIn(wrapper_name, agents)

        for report_name in (
            "aoa_codex_convergence_report.json",
            "aoa_codex_convergence_report.md",
        ):
            self.assertTrue(
                (REPO_ROOT / ".codex" / "generated" / "codex" / report_name).is_file()
            )

        self.assertIn("aoa_codex_convergence_report.{json,md}", capability_map)
        self.assertIn("aoa_codex_convergence_report.{json,md}", agents)
        self.assertIn("convergence reports are evidence, not authority", capability_map)
        self.assertIn("convergence reports are evidence, not authority", agents)


if __name__ == "__main__":
    unittest.main()
