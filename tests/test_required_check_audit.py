from __future__ import annotations

import contextlib
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from run_required_check_audit import (  # noqa: E402
    build_audit_commands,
    find_trigger_paths,
    main,
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
        contract_repo = Path("/srv/AbyssOS/8Dionysus")

        default_commands = build_audit_commands(contract_repo, include_github_protection=False)
        self.assertEqual(len(default_commands), 2)
        self.assertEqual(default_commands[1][-1], "--remote-workflows")

        protection_commands = build_audit_commands(contract_repo, include_github_protection=True)
        self.assertEqual(len(protection_commands), 3)
        self.assertEqual(protection_commands[-1][-1], "--github-protection")

    def test_main_dry_run_github_protection_does_not_skip_without_trigger_paths(self) -> None:
        stdout = io.StringIO()
        with (
            patch.object(
                sys,
                "argv",
                [
                    "run_required_check_audit.py",
                    "--repo-root",
                    str(REPO_ROOT),
                    "--compare-ref",
                    "none",
                    "--dry-run",
                    "--github-protection",
                ],
            ),
            patch("run_required_check_audit.discover_repo_root", return_value=REPO_ROOT),
            patch("run_required_check_audit.resolve_contract_repo", return_value=REPO_ROOT),
            patch("run_required_check_audit.select_compare_ref", return_value=None),
            patch("run_required_check_audit.collect_changed_paths", return_value=[]),
            contextlib.redirect_stdout(stdout),
        ):
            exit_code = main()

        output = stdout.getvalue()
        self.assertEqual(0, exit_code)
        self.assertNotIn("[skip] required-check audit not triggered", output)
        self.assertIn("[plan] running required-check audit commands:", output)
        self.assertIn("--github-protection", output)


if __name__ == "__main__":
    unittest.main()
