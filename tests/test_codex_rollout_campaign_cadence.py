from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from validate_codex_rollout_campaign_cadence import validate_codex_rollout_campaign_cadence


def load_json(relative_path: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


class CodexRolloutCampaignCadenceTests(unittest.TestCase):
    def test_campaign_cadence_docs_stay_discoverable(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        install = (REPO_ROOT / "docs" / "WORKSPACE_INSTALL.md").read_text(encoding="utf-8")
        rollout = (REPO_ROOT / "docs" / "CODEX_PLANE_ROLLOUT.md").read_text(encoding="utf-8")
        operations = (REPO_ROOT / "docs" / "CODEX_TRUSTED_ROLLOUT_OPERATIONS.md").read_text(
            encoding="utf-8"
        )
        campaigns = (REPO_ROOT / "docs" / "TRUSTED_ROLLOUT_CAMPAIGNS.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("docs/TRUSTED_ROLLOUT_CAMPAIGNS.md", readme)
        self.assertIn("docs/TRUSTED_ROLLOUT_CAMPAIGNS.md", install)
        self.assertIn("TRUSTED_ROLLOUT_CAMPAIGNS.md", rollout)
        self.assertIn("TRUSTED_ROLLOUT_CAMPAIGNS.md", operations)
        self.assertIn("CAMP-YYYYMMDD-<slug>-NN", campaigns)

    def test_campaign_cadence_examples_validate_and_stay_coherent(self) -> None:
        validate_codex_rollout_campaign_cadence()

        campaign = load_json("examples/rollout_campaign_window.example.json")
        review = load_json("examples/drift_review_window.example.json")
        rollback = load_json("examples/rollback_followthrough_window.example.json")

        self.assertEqual(campaign["schema_version"], "8dionysus_rollout_campaign_window_v1")
        self.assertEqual(review["schema_version"], "8dionysus_drift_review_window_v1")
        self.assertEqual(
            rollback["schema_version"],
            "8dionysus_rollback_followthrough_window_v1",
        )
        self.assertEqual(review["campaign_ref"], campaign["campaign_ref"])
        self.assertEqual(rollback["campaign_ref"], campaign["campaign_ref"])
        self.assertEqual(
            rollback["rollback_anchor"],
            campaign["latest_stable_rollout_campaign_ref"],
        )


if __name__ == "__main__":
    unittest.main()
