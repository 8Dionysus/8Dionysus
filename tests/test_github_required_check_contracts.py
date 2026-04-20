from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from validate_github_required_check_contracts import (  # noqa: E402
    load_contract,
    parse_workflow_metadata,
    validate_contract_structure,
    validate_live_github_protection,
    validate_remote_workflow_contracts,
)


class GitHubRequiredCheckContractTests(unittest.TestCase):
    def test_contract_data_stays_coherent(self) -> None:
        contract = load_contract()
        validate_contract_structure(contract)

        self.assertEqual(
            contract["schema_version"],
            "8dionysus_github_required_check_contracts_v1",
        )
        self.assertEqual(contract["tracked_branch"], "main")
        self.assertEqual(contract["authority_scope"], "coordination-only")
        repos = contract["repos"]
        self.assertEqual(len(repos), 17)

    def test_contract_docs_and_decision_note_stay_cross_linked(self) -> None:
        doc = (REPO_ROOT / "docs" / "GITHUB_REQUIRED_CHECK_CONTRACTS.md").read_text(
            encoding="utf-8"
        )
        decision = (
            REPO_ROOT
            / "docs"
            / "decisions"
            / "0002-repo-family-required-check-contracts.md"
        ).read_text(encoding="utf-8")
        workflow = (
            REPO_ROOT / ".github" / "workflows" / "repo-family-drift-check.yml"
        ).read_text(encoding="utf-8")

        self.assertIn("config/github_required_check_contracts.json", doc)
        self.assertIn("schemas/github_required_check_contracts.schema.json", doc)
        self.assertIn("scripts/validate_github_required_check_contracts.py", doc)
        self.assertIn("docs/decisions/0002-repo-family-required-check-contracts.md", doc)
        self.assertIn("docs/GITHUB_REQUIRED_CHECK_CONTRACTS.md", decision)
        self.assertIn("--remote-workflows", workflow)
        self.assertIn("validate_github_required_check_contracts.py", workflow)

    def test_parse_workflow_metadata_reads_workflow_and_job_names(self) -> None:
        workflow_name, job_names = parse_workflow_metadata(
            """name: "Repo Validation"

on:
  pull_request:

jobs:
  release_audit:
    name: Repo Validation
    runs-on: ubuntu-latest
  build_validate:
    runs-on: ubuntu-latest
""",
            "fixture.yml",
        )

        self.assertEqual(workflow_name, "Repo Validation")
        self.assertEqual(job_names, ["Repo Validation", "build_validate"])

    def test_parse_workflow_metadata_accepts_nonstandard_job_indentation(self) -> None:
        workflow_name, job_names = parse_workflow_metadata(
            """name: "Repo Validation"

jobs:
    release_audit:
        name: Repo Validation
        runs-on: ubuntu-latest
    build_validate:
        runs-on: ubuntu-latest
""",
            "fixture-indented.yml",
        )

        self.assertEqual(workflow_name, "Repo Validation")
        self.assertEqual(job_names, ["Repo Validation", "build_validate"])

    def test_parse_workflow_metadata_ignores_block_scalar_contents(self) -> None:
        workflow_name, job_names = parse_workflow_metadata(
            """name: Pytest

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Example
        run: |
          echo "line one"
          smoke:
            should_not_become_a_job

  smoke:
    runs-on: ubuntu-latest
""",
            "fixture-block.yml",
        )

        self.assertEqual(workflow_name, "Pytest")
        self.assertEqual(job_names, ["test", "smoke"])

    def test_parse_workflow_metadata_ignores_nested_step_name_fields(self) -> None:
        workflow_name, job_names = parse_workflow_metadata(
            """name: Pytest

jobs:
  smoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/upload-artifact@v4
        with:
          name: dependency-audit-report
""",
            "fixture-nested-name.yml",
        )

        self.assertEqual(workflow_name, "Pytest")
        self.assertEqual(job_names, ["smoke"])

    def test_parse_workflow_metadata_ignores_nested_step_names_with_nonstandard_indentation(self) -> None:
        workflow_name, job_names = parse_workflow_metadata(
            """name: Pytest

jobs:
    smoke:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/upload-artifact@v4
              with:
                  name: dependency-audit-report
""",
            "fixture-nested-indent.yml",
        )

        self.assertEqual(workflow_name, "Pytest")
        self.assertEqual(job_names, ["smoke"])

    def test_remote_workflow_validation_accepts_matching_contract(self) -> None:
        contract = {
            "schema_version": "8dionysus_github_required_check_contracts_v1",
            "tracked_branch": "main",
            "authority_scope": "coordination-only",
            "authority_note": "fixture",
            "repos": [
                {
                    "repo": "8Dionysus/example",
                    "family": "fixture",
                    "protection_expected": True,
                    "required_status_checks": ["Repo Validation", "build-validate"],
                    "workflow_checks": [
                        {
                            "path": ".github/workflows/repo-validation.yml",
                            "expected_workflow_name": "Repo Validation",
                            "required_job_names": ["Repo Validation"],
                        },
                        {
                            "path": ".github/workflows/export.yml",
                            "expected_workflow_name": "export",
                            "required_job_names": ["build-validate"],
                        },
                    ],
                }
            ],
        }

        payloads = {
            ("8Dionysus/example", "main", ".github/workflows/repo-validation.yml"): """name: Repo Validation
jobs:
  validate:
    name: Repo Validation
    runs-on: ubuntu-latest
""",
            ("8Dionysus/example", "main", ".github/workflows/export.yml"): """name: export
jobs:
  build-validate:
    runs-on: ubuntu-latest
""",
        }

        def fake_fetcher(repo: str, branch: str, path: str) -> str:
            return payloads[(repo, branch, path)]

        validate_contract_structure(contract)
        validate_remote_workflow_contracts(contract, [], fetcher=fake_fetcher)

    def test_live_github_protection_validation_compares_contexts(self) -> None:
        contract = {
            "schema_version": "8dionysus_github_required_check_contracts_v1",
            "tracked_branch": "main",
            "authority_scope": "coordination-only",
            "authority_note": "fixture",
            "repos": [
                {
                    "repo": "8Dionysus/example",
                    "family": "fixture",
                    "protection_expected": True,
                    "required_status_checks": ["Repo Validation"],
                    "workflow_checks": [
                        {
                            "path": ".github/workflows/repo-validation.yml",
                            "expected_workflow_name": "Repo Validation",
                            "required_job_names": ["Repo Validation"],
                        }
                    ],
                },
                {
                    "repo": "8Dionysus/manual",
                    "family": "manual",
                    "protection_expected": False,
                    "required_status_checks": [],
                    "workflow_checks": [],
                },
            ],
        }

        def fake_gh_runner(api_path: str) -> SimpleNamespace:
            if api_path.endswith("8Dionysus/example/branches/main"):
                return SimpleNamespace(
                    returncode=0,
                    stdout='{"protected": true, "protection": {"required_status_checks": {"contexts": ["Repo Validation"]}}}',
                    stderr="",
                )
            self.assertTrue(api_path.endswith("8Dionysus/manual/branches/main"))
            return SimpleNamespace(
                returncode=0,
                stdout='{"protected": false, "protection": {"required_status_checks": {"contexts": []}}}',
                stderr="",
            )

        validate_contract_structure(contract)
        validate_live_github_protection(contract, [], gh_runner=fake_gh_runner)

    def test_live_github_protection_validation_rejects_unprotected_repo_api_failures(self) -> None:
        contract = {
            "schema_version": "8dionysus_github_required_check_contracts_v1",
            "tracked_branch": "main",
            "authority_scope": "coordination-only",
            "authority_note": "fixture",
            "repos": [
                {
                    "repo": "8Dionysus/manual",
                    "family": "manual",
                    "protection_expected": False,
                    "required_status_checks": [],
                    "workflow_checks": [],
                }
            ],
        }

        def fake_gh_runner(api_path: str) -> SimpleNamespace:
            self.assertEqual(
                "repos/8Dionysus/manual/branches/main",
                api_path,
            )
            return SimpleNamespace(
                returncode=1,
                stdout='{"message":"Upgrade to GitHub Pro or make this repository public to enable this feature.","status":"403"}',
                stderr="gh: Upgrade to GitHub Pro or make this repository public to enable this feature. (HTTP 403)",
            )

        validate_contract_structure(contract)
        with self.assertRaisesRegex(
            ValueError,
            r"8Dionysus/manual protection check failed",
        ):
            validate_live_github_protection(contract, [], gh_runner=fake_gh_runner)


if __name__ == "__main__":
    unittest.main()
