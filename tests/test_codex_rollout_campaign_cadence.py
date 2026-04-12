from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import validate_codex_rollout_campaign_cadence as cadence_validator
from validate_codex_rollout_campaign_cadence import validate_codex_rollout_campaign_cadence


def load_json(relative_path: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


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

    def test_validator_accepts_non_open_campaign_with_non_closed_review_status(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for relative_path in (
                "schemas/rollout_campaign_window_v1.json",
                "schemas/drift_review_window_v1.json",
                "schemas/rollback_followthrough_window_v1.json",
                "generated/codex/rollout/rollout_latest.min.json",
            ):
                source = REPO_ROOT / relative_path
                destination = root / relative_path
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

            campaign = load_json("examples/rollout_campaign_window.example.json")
            review = load_json("examples/drift_review_window.example.json")
            rollback = load_json("examples/rollback_followthrough_window.example.json")
            campaign["state"] = "review_required"
            review["status"] = "review_required"

            write_json(root / "examples/rollout_campaign_window.example.json", campaign)
            write_json(root / "examples/drift_review_window.example.json", review)
            write_json(root / "examples/rollback_followthrough_window.example.json", rollback)

            with patch.object(cadence_validator, "REPO_ROOT", root):
                cadence_validator.validate_codex_rollout_campaign_cadence()


if __name__ == "__main__":
    unittest.main()
