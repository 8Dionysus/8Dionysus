from __future__ import annotations

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


if __name__ == "__main__":
    unittest.main()
