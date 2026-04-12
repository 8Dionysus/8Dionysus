from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import validate_codex_trusted_rollout_operations as rollout_validator
from validate_codex_trusted_rollout_operations import validate_codex_trusted_rollout_operations


def load_json(relative_path: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def load_jsonl(relative_path: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for raw_line in (REPO_ROOT / relative_path).read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(row, separators=(",", ":")) for row in rows) + "\n",
        encoding="utf-8",
    )


class CodexTrustedRolloutOperationsTests(unittest.TestCase):
    def test_trusted_rollout_docs_stay_discoverable(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        install = (REPO_ROOT / "docs" / "WORKSPACE_INSTALL.md").read_text(encoding="utf-8")
        rollout = (REPO_ROOT / "docs" / "CODEX_PLANE_ROLLOUT.md").read_text(encoding="utf-8")
        operations = (REPO_ROOT / "docs" / "CODEX_TRUSTED_ROLLOUT_OPERATIONS.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("docs/CODEX_TRUSTED_ROLLOUT_OPERATIONS.md", readme)
        self.assertIn("docs/CODEX_TRUSTED_ROLLOUT_OPERATIONS.md", install)
        self.assertIn("CODEX_TRUSTED_ROLLOUT_OPERATIONS.md", rollout)
        self.assertIn("generated/codex/rollout/deploy_history.jsonl", operations)

    def test_trusted_rollout_surfaces_validate_and_stay_coherent(self) -> None:
        validate_codex_trusted_rollout_operations()

        deploy_history = load_jsonl("generated/codex/rollout/deploy_history.jsonl")
        latest = load_json("generated/codex/rollout/rollout_latest.min.json")
        rollback = load_json("generated/codex/rollout/rollback_windows.min.json")

        self.assertEqual(len(deploy_history), 2)
        self.assertEqual(
            latest["latest_rollout_campaign_ref"],
            "ROLL-20260411-codex-hooks-tighten-02",
        )
        self.assertEqual(latest["latest_state"], "rolled_back")
        self.assertEqual(
            latest["latest_stable_rollout_campaign_ref"],
            "ROLL-20260411-codex-plane-regen-01",
        )
        self.assertEqual(
            rollback["rollback_windows"][0]["rollback_window_ref"],
            "RBK-20260411-codex-hooks-tighten-02",
        )

    def test_validator_requires_rollback_refs_for_rollback_open_entries(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            deploy_history_path = root / "deploy_history.jsonl"
            regeneration_path = root / "regeneration_campaigns.min.json"
            rollback_path = root / "rollback_windows.min.json"
            latest_path = root / "rollout_latest.min.json"

            write_jsonl(
                deploy_history_path,
                [
                    {
                        "schema_version": "8dionysus_codex_trusted_rollout_entry_v1",
                        "rollout_campaign_ref": "ROLL-20260412-codex-plane-regen-03",
                        "state": "rollback_open",
                        "activated_at": "2026-04-12T20:00:00Z",
                        "actor": "codex+review",
                        "scope": "shared-root-codex-plane",
                        "deploy_receipt_refs": ["DEPLOY-20260412-codex-plane-regen-03"],
                        "drift_window_refs": ["DRIFT-20260412-codex-plane-regen-03"],
                        "rollback_window_refs": [],
                        "drift_state": "material",
                        "repair_attempted": True,
                        "summary": "Rollback opened but the rollback ref was omitted.",
                    }
                ],
            )
            write_json(
                regeneration_path,
                {
                    "schema_version": "8dionysus_codex_trusted_rollout_campaigns_v1",
                    "owner_repo": "8Dionysus",
                    "campaigns": [
                        {
                            "rollout_campaign_ref": "ROLL-20260412-codex-plane-regen-03",
                            "state": "rollback_open",
                        }
                    ],
                },
            )
            write_json(
                rollback_path,
                {
                    "schema_version": "8dionysus_codex_trusted_rollback_windows_v1",
                    "owner_repo": "8Dionysus",
                    "rollback_windows": [],
                },
            )
            write_json(
                latest_path,
                {
                    "schema_version": "8dionysus_codex_trusted_rollout_latest_v1",
                    "owner_repo": "8Dionysus",
                    "latest_rollout_campaign_ref": "ROLL-20260412-codex-plane-regen-03",
                    "latest_state": "rollback_open",
                    "active_drift_window_ref": "DRIFT-20260412-codex-plane-regen-03",
                    "active_rollback_window_ref": None,
                    "latest_stable_rollout_campaign_ref": "ROLL-20260411-codex-plane-regen-01",
                    "source_refs": [
                        "generated/codex/rollout/deploy_history.jsonl",
                        "generated/codex/rollout/regeneration_campaigns.min.json",
                        "generated/codex/rollout/rollback_windows.min.json",
                    ],
                },
            )

            with patch.object(rollout_validator, "DEPLOY_HISTORY_PATH", deploy_history_path), patch.object(
                rollout_validator, "REGENERATION_PATH", regeneration_path
            ), patch.object(rollout_validator, "ROLLBACK_PATH", rollback_path), patch.object(
                rollout_validator, "LATEST_PATH", latest_path
            ):
                with self.assertRaisesRegex(
                    ValueError,
                    "rollback_window_refs must not be empty for rollback_open entries",
                ):
                    rollout_validator.validate_codex_trusted_rollout_operations()

    def test_validator_rejects_non_object_campaign_items(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            deploy_history_path = root / "deploy_history.jsonl"
            regeneration_path = root / "regeneration_campaigns.min.json"
            rollback_path = root / "rollback_windows.min.json"
            latest_path = root / "rollout_latest.min.json"

            write_jsonl(
                deploy_history_path,
                [
                    {
                        "schema_version": "8dionysus_codex_trusted_rollout_entry_v1",
                        "rollout_campaign_ref": "ROLL-20260411-codex-plane-regen-01",
                        "state": "stabilized",
                        "activated_at": "2026-04-11T21:10:00Z",
                        "actor": "codex+review",
                        "scope": "shared-root-codex-plane",
                        "deploy_receipt_refs": ["DEPLOY-20260411-codex-plane-regen-01"],
                        "drift_window_refs": ["DRIFT-20260411-codex-plane-regen-01"],
                        "rollback_window_refs": [],
                        "drift_state": "quiet",
                        "repair_attempted": False,
                        "summary": "Stable rollout.",
                    }
                ],
            )
            write_json(
                regeneration_path,
                {
                    "schema_version": "8dionysus_codex_trusted_rollout_campaigns_v1",
                    "owner_repo": "8Dionysus",
                    "campaigns": [
                        "ROLL-20260411-codex-plane-regen-01",
                        {
                            "rollout_campaign_ref": "ROLL-20260411-codex-plane-regen-01",
                            "state": "stabilized",
                        },
                    ],
                },
            )
            write_json(
                rollback_path,
                {
                    "schema_version": "8dionysus_codex_trusted_rollback_windows_v1",
                    "owner_repo": "8Dionysus",
                    "rollback_windows": [],
                },
            )
            write_json(
                latest_path,
                {
                    "schema_version": "8dionysus_codex_trusted_rollout_latest_v1",
                    "owner_repo": "8Dionysus",
                    "latest_rollout_campaign_ref": "ROLL-20260411-codex-plane-regen-01",
                    "latest_state": "stabilized",
                    "active_drift_window_ref": None,
                    "active_rollback_window_ref": None,
                    "latest_stable_rollout_campaign_ref": "ROLL-20260411-codex-plane-regen-01",
                    "source_refs": [
                        "generated/codex/rollout/deploy_history.jsonl",
                        "generated/codex/rollout/regeneration_campaigns.min.json",
                        "generated/codex/rollout/rollback_windows.min.json",
                    ],
                },
            )

            with patch.object(rollout_validator, "DEPLOY_HISTORY_PATH", deploy_history_path), patch.object(
                rollout_validator, "REGENERATION_PATH", regeneration_path
            ), patch.object(rollout_validator, "ROLLBACK_PATH", rollback_path), patch.object(
                rollout_validator, "LATEST_PATH", latest_path
            ):
                with self.assertRaisesRegex(
                    ValueError,
                    "regeneration_campaigns.min.json.campaigns\\[0\\] must be an object",
                ):
                    rollout_validator.validate_codex_trusted_rollout_operations()


if __name__ == "__main__":
    unittest.main()
