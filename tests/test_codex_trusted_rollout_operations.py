from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

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


if __name__ == "__main__":
    unittest.main()
