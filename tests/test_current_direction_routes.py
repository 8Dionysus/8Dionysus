from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CURRENT_SURFACE = "docs/PUBLIC_ENTRY_POSTURE.md"


class CurrentDirectionRoutesTestCase(unittest.TestCase):
    def test_root_entrypoints_route_to_public_entry_posture(self) -> None:
        posture_path = REPO_ROOT / "docs" / "PUBLIC_ENTRY_POSTURE.md"
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")

        self.assertTrue(posture_path.is_file())
        self.assertIn(CURRENT_SURFACE, readme)
        self.assertIn(CURRENT_SURFACE, agents)


if __name__ == "__main__":
    unittest.main()
