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

    def test_checked_in_routes_keep_readmes_on_demand(self) -> None:
        root = Path(__file__).resolve().parents[1]

        result = readme_agents_corpus.scan_repository_corpus(root, "8Dionysus", {})

        self.assertEqual(
            result["readme_agents_summary"]["agents_files_declaring_mandatory_readme"],
            0,
        )
        self.assertEqual(
            result["readme_agents_summary"]["declared_mandatory_readme_bytes"],
            0,
        )

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

    def test_reading_order_section_marks_bare_readme_item_mandatory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "AGENTS.md").write_text(
                "# AGENTS.md\n\n## Reading order\n\n1. `README.md`\n",
                encoding="utf-8",
            )
            (repo / "README.md").write_text("# Human route\n", encoding="utf-8")

            result = readme_agents_corpus.scan_repository_corpus(repo, "fixture", {})
            root_agents = next(
                record
                for record in result["agents_files"]
                if record["path"] == "AGENTS.md"
            )

            self.assertEqual(
                root_agents["mandatory_resolved_readme_references"],
                ["README.md"],
            )
            self.assertEqual(
                result["readme_agents_summary"]["declared_mandatory_readme_bytes"],
                len("# Human route\n".encode()),
            )

    def test_readme_content_requirement_is_not_a_read_requirement(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "AGENTS.md").write_text(
                "# AGENTS.md\n\n## Index contract\n\n"
                "`README.md` is the durable index. It must carry owner links.\n",
                encoding="utf-8",
            )
            (repo / "README.md").write_text("# Human route\n", encoding="utf-8")

            result = readme_agents_corpus.scan_repository_corpus(repo, "fixture", {})
            root_agents = next(
                record
                for record in result["agents_files"]
                if record["path"] == "AGENTS.md"
            )

            self.assertEqual(root_agents["mandatory_resolved_readme_references"], [])
            self.assertEqual(
                result["readme_agents_summary"]["declared_mandatory_readme_bytes"],
                0,
            )

    def test_conditional_readme_route_is_not_an_unconditional_read(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "AGENTS.md").write_text(
                "# AGENTS.md\n\n## Read before editing\n\n"
                "Open `README.md` only when its human explanation is relevant.\n\n"
                "Root orientation remains in `README.md`; none is mandatory merely "
                "because it is nearby.\n",
                encoding="utf-8",
            )
            (repo / "README.md").write_text("# Human route\n", encoding="utf-8")

            result = readme_agents_corpus.scan_repository_corpus(repo, "fixture", {})
            root_agents = next(
                record
                for record in result["agents_files"]
                if record["path"] == "AGENTS.md"
            )

            self.assertEqual(root_agents["mandatory_readme_reference_lines"], [])
            self.assertEqual(
                result["readme_agents_summary"]["agents_files_declaring_mandatory_readme"],
                0,
            )

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

    def test_repeated_long_agents_blocks_are_measured_outside_fences(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            shared = "Shared inherited routing law " + ("owner-delta " * 18)
            for relative in ["AGENTS.md", "a/AGENTS.md", "b/AGENTS.md", "c/AGENTS.md"]:
                path = repo / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"# AGENTS.md\n\n{shared}\n", encoding="utf-8")
            for relative in ["d/AGENTS.md", "e/AGENTS.md", "f/AGENTS.md", "g/AGENTS.md"]:
                path = repo / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    f"# AGENTS.md\n\n```text\n{shared}\n```\n", encoding="utf-8"
                )

            result = readme_agents_corpus.scan_repository_corpus(repo, "fixture", {})
            summary = result["readme_agents_summary"]
            block = result["repeated_long_agents_blocks"][0]

            self.assertEqual(summary["repeated_long_agents_block_groups"], 1)
            self.assertEqual(summary["authored_repeated_long_agents_block_groups"], 1)
            self.assertEqual(summary["repeated_long_agents_block_instances"], 4)
            self.assertEqual(
                block["paths"],
                ["AGENTS.md", "a/AGENTS.md", "b/AGENTS.md", "c/AGENTS.md"],
            )
            self.assertEqual(
                block["normalized_redundant_bytes"],
                block["normalized_bytes"] * 3,
            )

    def test_shared_root_uses_distinct_sources_for_readme_and_agents(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            owner = root / "owner"
            workspace.mkdir()
            owner.mkdir()
            (workspace / "AGENTS.md").write_text("agents\n", encoding="utf-8")
            (workspace / "README.md").write_text("workspace readme\n", encoding="utf-8")
            (owner / "AGENTS.md").write_text("agents\n", encoding="utf-8")
            (owner / "README.md").write_text("public profile\n", encoding="utf-8")
            (owner / "docs").mkdir()
            (owner / "docs" / "WORKSPACE_ROOT_ENTRY.md").write_text(
                "workspace readme\n", encoding="utf-8"
            )

            result = readme_agents_corpus.scan_shared_root(workspace, owner, {})
            records = {record["path"]: record for record in result["files"]}

            self.assertTrue(records["AGENTS.md"]["declared_projection_surface"])
            self.assertTrue(records["README.md"]["declared_projection_surface"])
            self.assertTrue(records["README.md"]["owner_parity"])
            self.assertEqual(
                records["README.md"]["owner_path"],
                "8Dionysus/docs/WORKSPACE_ROOT_ENTRY.md",
            )


if __name__ == "__main__":
    unittest.main()
