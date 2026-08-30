from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
import sys

from jsonschema import Draft202012Validator

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import readme_agents_corpus


class ReadmeAgentsCorpusTests(unittest.TestCase):
    def test_checked_in_disposition_manifest_matches_schema(self) -> None:
        root = Path(__file__).resolve().parents[1]
        payload = json.loads(
            (root / "manifests" / "readme_agents_dispositions.v1.json").read_text(
                encoding="utf-8"
            )
        )
        schema = json.loads(
            (root / "schemas" / "readme-agents-dispositions.schema.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(list(Draft202012Validator(schema).iter_errors(payload)), [])

    def test_chain_pair_read_fanout_and_review_overlay(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "docs").mkdir()
            (repo / "notes").mkdir()
            (repo / "AGENTS.md").write_text(
                "# AGENTS.md\nRead README.md before editing.\n", encoding="utf-8"
            )
            (repo / "README.md").write_text("# Public entry\n", encoding="utf-8")
            (repo / "docs" / "AGENTS.md").write_text(
                "# AGENTS.md\nlocal delta\n", encoding="utf-8"
            )
            (repo / "docs" / "README.md").write_text("# Docs\n", encoding="utf-8")
            (repo / "notes" / "README.md").write_text("# Notes\n", encoding="utf-8")
            dispositions = {
                ("fixture", "docs/README.md"): {
                    "review_state": "reviewed",
                    "disposition": "keep",
                    "owner_evidence": ["docs/AGENTS.md"],
                    "note": "human route",
                }
            }

            result = readme_agents_corpus.scan_repository_corpus(
                repo, "fixture", dispositions
            )
            records = {
                record["path"]: record
                for record in [*result["agents_files"], *result["readme_files"]]
            }

            self.assertEqual(result["readme_agents_summary"]["paired_directories"], 2)
            self.assertEqual(result["readme_agents_summary"]["readme_only_directories"], 1)
            self.assertEqual(
                records["docs/README.md"]["agents_chain_paths"],
                ["AGENTS.md", "docs/AGENTS.md"],
            )
            self.assertEqual(records["docs/README.md"]["review"]["disposition"], "keep")
            self.assertEqual(
                records["AGENTS.md"]["mandatory_resolved_readme_references"],
                ["README.md"],
            )
            self.assertEqual(
                result["readme_agents_summary"]["agents_files_declaring_mandatory_readme"],
                1,
            )

    def test_git_corpus_separates_tracked_files_from_untracked_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "config", "user.email", "fixture@example.invalid"],
                check=True,
            )
            subprocess.run(
                ["git", "-C", str(repo), "config", "user.name", "Fixture"], check=True
            )
            (repo / "AGENTS.md").write_text("# AGENTS.md\n", encoding="utf-8")
            (repo / "README.md").write_text("# Root\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "AGENTS.md", "README.md"], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "fixture"], check=True)
            (repo / "draft").mkdir()
            (repo / "draft" / "README.md").write_text("# Draft\n", encoding="utf-8")

            result = readme_agents_corpus.scan_repository_corpus(repo, "fixture", {})
            summary = result["readme_agents_summary"]

            self.assertEqual(summary["tracked_document_files"], 2)
            self.assertEqual(summary["untracked_document_candidates"], 1)
            draft = next(record for record in result["readme_files"] if record["path"] == "draft/README.md")
            self.assertFalse(draft["tracked"])
            self.assertEqual(draft["worktree_status"], "??")

    def test_disposition_loader_requires_owner_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "dispositions.json"
            path.write_text(
                json.dumps(
                    {
                        "schema_version": readme_agents_corpus.DISPOSITIONS_SCHEMA_VERSION,
                        "records": [
                            {
                                "repository": "fixture",
                                "path": "README.md",
                                "review_state": "reviewed",
                                "disposition": "keep",
                                "owner_evidence": [],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            records, issues = readme_agents_corpus.load_dispositions(path)

            self.assertEqual(records, {})
            self.assertIn("reviewed record lacks owner_evidence", issues[0])

    def test_shared_root_distinguishes_declared_projection_from_readme(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            owner = root / "owner"
            workspace.mkdir()
            owner.mkdir()
            for name, content in (("AGENTS.md", "agents\n"), ("README.md", "readme\n")):
                (workspace / name).write_text(content, encoding="utf-8")
                (owner / name).write_text(content, encoding="utf-8")

            result = readme_agents_corpus.scan_shared_root(workspace, owner, {})
            records = {record["path"]: record for record in result["files"]}

            self.assertTrue(records["AGENTS.md"]["declared_projection_surface"])
            self.assertFalse(records["README.md"]["declared_projection_surface"])
            self.assertTrue(records["README.md"]["owner_parity"])


if __name__ == "__main__":
    unittest.main()
