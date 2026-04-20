from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from run_required_check_audit import (  # noqa: E402
    build_audit_commands,
    find_trigger_paths,
    path_triggers_required_check_audit,
)


class RequiredCheckAuditTests(unittest.TestCase):
    def test_workflow_paths_trigger_required_check_audit(self) -> None:
        self.assertTrue(path_triggers_required_check_audit(".github/workflows/repo-validation.yml"))
        self.assertTrue(path_triggers_required_check_audit("config/github_required_check_contracts.json"))
        self.assertFalse(path_triggers_required_check_audit("README.md"))

    def test_find_trigger_paths_filters_non_trigger_changes(self) -> None:
        changed_paths = [
            "README.md",
            ".github/workflows/repo-validation.yml",
            "docs/GITHUB_REQUIRED_CHECK_CONTRACTS.md",
            "src/example.py",
        ]
        self.assertEqual(
            find_trigger_paths(changed_paths),
            [
                ".github/workflows/repo-validation.yml",
                "docs/GITHUB_REQUIRED_CHECK_CONTRACTS.md",
            ],
        )

    def test_build_audit_commands_adds_github_protection_on_request(self) -> None:
        contract_repo = Path("/srv/8Dionysus")

        default_commands = build_audit_commands(contract_repo, include_github_protection=False)
        self.assertEqual(len(default_commands), 2)
        self.assertEqual(default_commands[1][-1], "--remote-workflows")

        protection_commands = build_audit_commands(contract_repo, include_github_protection=True)
        self.assertEqual(len(protection_commands), 3)
        self.assertEqual(protection_commands[-1][-1], "--github-protection")


if __name__ == "__main__":
    unittest.main()
