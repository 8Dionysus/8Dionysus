from __future__ import annotations

import hashlib
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
    def test_owner_specific_level_one_agents_heading_is_valid(self) -> None:
        self.assertTrue(
            readme_agents_corpus.has_level_one_heading("# Runtime Agent Route\n")
        )
        self.assertFalse(
            readme_agents_corpus.has_level_one_heading("## Runtime Agent Route\n")
        )

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

    def test_read_model_noun_is_not_a_read_directive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "AGENTS.md").write_text(
                "# AGENTS.md\n\n"
                "`README.md` is a human entrypoint. Generated summaries are read "
                "models; neither overrides its owner.\n",
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

    def test_neighboring_sentence_does_not_make_readme_mandatory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "AGENTS.md").write_text(
                "# AGENTS.md\n\n"
                "Use `DESIGN.md` before changing durable topology. `README.md` "
                "is the public atlas for contributors.\n",
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

    def test_when_route_is_conditional(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "AGENTS.md").write_text(
                "# AGENTS.md\n\n"
                "Use `README.md` when public package topology moves.\n",
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

    def test_fenced_readme_argument_is_not_a_read_directive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "AGENTS.md").write_text(
                "# AGENTS.md\n\n```bash\n"
                "tool --evidence-ref README.md --claim 'review before landing'\n"
                "```\n",
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

    def test_validation_command_ownership_and_doc_overlaps_are_measured(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            command = "python scripts/validate_routes.py --check"
            (repo / "local").mkdir()
            (repo / "generated").mkdir()
            (repo / "AGENTS.md").write_text(
                f"# AGENTS.md\n\n```bash\n{command}\n```\n", encoding="utf-8"
            )
            (repo / "README.md").write_text(
                f"# Human route\n\n```bash\n{command}\n```\n", encoding="utf-8"
            )
            for relative in (
                "VALIDATION.md",
                "local/VALIDATION.md",
                "generated/VALIDATION.md",
            ):
                (repo / relative).write_text(
                    f"# Validation\n\n```bash\n{command}\n```\n", encoding="utf-8"
                )

            result = readme_agents_corpus.scan_repository_corpus(
                repo, "fixture", {}
            )
            summary = result["readme_agents_summary"]

            self.assertEqual(summary["tracked_validation_files"], 3)
            self.assertEqual(summary["active_authored_validation_files"], 2)
            self.assertEqual(summary["active_authored_validation_invocations"], 2)
            self.assertEqual(summary["active_authored_unique_validation_invocations"], 1)
            self.assertEqual(summary["duplicate_validation_command_groups"], 1)
            self.assertEqual(summary["duplicate_validation_command_occurrences"], 1)
            self.assertEqual(summary["agents_validation_command_overlap_groups"], 1)
            self.assertEqual(summary["readme_validation_command_overlap_groups"], 1)
            self.assertEqual(
                result["duplicate_validation_commands"][0]["command"], command
            )
            self.assertEqual(
                [
                    location["path"]
                    for location in result["duplicate_validation_commands"][0][
                        "locations"
                    ]
                ],
                ["VALIDATION.md", "local/VALIDATION.md"],
            )

    def test_validation_command_ownership_is_not_hidden_by_text_fences(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            command = "python scripts/validate_routes.py --check"
            (repo / "local").mkdir()
            (repo / "VALIDATION.md").write_text(
                f"# Validation\n\n```text\n{command}\n```\n", encoding="utf-8"
            )
            (repo / "local" / "VALIDATION.md").write_text(
                f"# Validation\n\n```\n{command}\n```\n", encoding="utf-8"
            )

            result = readme_agents_corpus.scan_repository_corpus(
                repo, "fixture", {}
            )
            summary = result["readme_agents_summary"]

            self.assertEqual(summary["active_authored_validation_invocations"], 2)
            self.assertEqual(summary["active_authored_unique_validation_invocations"], 1)
            self.assertEqual(summary["duplicate_validation_command_groups"], 1)
            self.assertEqual(
                result["duplicate_validation_commands"][0]["command"], command
            )

    def test_multiline_environment_prefix_keeps_distinct_command_identity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "VALIDATION.md").write_text(
                """# Validation

```bash
python -m pytest -q tests/test_route.py
ROUTE_CONTOUR=internal_effect \\
  python -m pytest -q tests/test_route.py
```
""",
                encoding="utf-8",
            )

            result = readme_agents_corpus.scan_repository_corpus(
                repo, "fixture", {}
            )
            summary = result["readme_agents_summary"]

            self.assertEqual(summary["active_authored_validation_invocations"], 2)
            self.assertEqual(
                summary["active_authored_unique_validation_invocations"], 2
            )
            self.assertEqual(summary["duplicate_validation_command_groups"], 0)

    def test_runtime_session_validation_is_counted_but_not_authored(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            command = "python scripts/validate_routes.py --check"
            (repo / ".aoa" / "live_receipts").mkdir(parents=True)
            (repo / "VALIDATION.md").write_text(
                f"# Validation\n\n```bash\n{command}\n```\n", encoding="utf-8"
            )
            (repo / ".aoa" / "live_receipts" / "VALIDATION.md").write_text(
                f"# Runtime receipt\n\n```bash\n{command}\n```\n", encoding="utf-8"
            )

            result = readme_agents_corpus.scan_repository_corpus(
                repo, "fixture", {}
            )
            summary = result["readme_agents_summary"]

            self.assertEqual(summary["tracked_validation_files"], 2)
            self.assertEqual(summary["active_authored_validation_files"], 1)
            self.assertEqual(summary["active_authored_validation_invocations"], 1)
            self.assertEqual(summary["duplicate_validation_command_groups"], 0)

    def test_validation_owner_and_route_only_file_metrics_are_measured(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "local").mkdir()
            owner_text = """# Validation

```bash
python scripts/validate_routes.py --check
```
"""
            route_text = "# Validation\n\nUse [the owner](../VALIDATION.md).\n"
            (repo / "VALIDATION.md").write_text(owner_text, encoding="utf-8")
            (repo / "local" / "VALIDATION.md").write_text(
                route_text, encoding="utf-8"
            )

            result = readme_agents_corpus.scan_repository_corpus(
                repo, "fixture", {}
            )
            summary = result["readme_agents_summary"]

            self.assertEqual(summary["active_authored_validation_files"], 2)
            self.assertEqual(
                summary["active_authored_validation_bytes"],
                len(owner_text.encode("utf-8")) + len(route_text.encode("utf-8")),
            )
            self.assertEqual(
                summary["active_authored_validation_command_owner_files"], 1
            )
            self.assertEqual(
                summary["active_authored_validation_route_only_files"], 1
            )

    def test_route_only_claim_conflicts_with_owned_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "VALIDATION.md").write_text(
                """# Validation

This surface owns no distinct executable procedure.

```bash
python scripts/validate_routes.py --check
```
""",
                encoding="utf-8",
            )

            result = readme_agents_corpus.scan_repository_corpus(
                repo, "fixture", {}
            )

            self.assertEqual(
                result["readme_agents_summary"][
                    "validation_route_only_claim_conflicts"
                ],
                1,
            )
            self.assertEqual(
                result["validation_route_only_claim_conflicts"],
                [
                    {
                        "path": "VALIDATION.md",
                        "claim_lines": [3],
                        "executable_invocations": 1,
                    }
                ],
            )

    def test_agents_fences_require_content_addressed_classification(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            block = "# AGENTS.md\n\n## Applies to"
            digest = hashlib.sha256(block.encode("utf-8")).hexdigest()
            (repo / "AGENTS.md").write_text(
                f"# Agent route\n\n```markdown\n{block}\n```\n",
                encoding="utf-8",
            )
            dispositions = {
                ("fixture", "AGENTS.md"): {
                    "review_state": "reviewed",
                    "disposition": "keep",
                    "owner_evidence": ["fixture:AGENTS.md"],
                    "fenced_blocks": [
                        {
                            "sha256": digest,
                            "classification": "agent-card-template",
                            "reason": "Documents the child-card shape without executable procedure.",
                        }
                    ],
                }
            }

            classified = readme_agents_corpus.scan_repository_corpus(
                repo, "fixture", dispositions
            )
            summary = classified["readme_agents_summary"]
            self.assertEqual(summary["active_authored_agents_fenced_blocks"], 1)
            self.assertEqual(
                summary["active_authored_agents_classified_fenced_blocks"], 1
            )
            self.assertEqual(
                summary["active_authored_agents_unclassified_fenced_blocks"], 0
            )
            self.assertEqual(
                summary["active_authored_agents_fenced_executable_invocations"], 0
            )

            unclassified = readme_agents_corpus.scan_repository_corpus(
                repo, "fixture", {}
            )
            self.assertEqual(
                unclassified["readme_agents_summary"][
                    "active_authored_agents_unclassified_fenced_blocks"
                ],
                1,
            )

    def test_design_agents_are_reviewed_without_entering_inherited_chain(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            block = "# AGENTS.md\n\n## Applies to\n\n## Role"
            digest = hashlib.sha256(block.encode("utf-8")).hexdigest()
            (repo / "AGENTS.md").write_text("# Root route\n", encoding="utf-8")
            (repo / "README.md").write_text("# Human route\n", encoding="utf-8")
            (repo / "DESIGN.AGENTS.md").write_text(
                f"# Agent design\n\n```markdown\n{block}\n```\n",
                encoding="utf-8",
            )
            dispositions = {
                ("fixture", "DESIGN.AGENTS.md"): {
                    "review_state": "reviewed",
                    "disposition": "keep",
                    "owner_evidence": ["fixture:DESIGN.AGENTS.md"],
                    "fenced_blocks": [
                        {
                            "sha256": digest,
                            "classification": "agent-card-template",
                            "reason": "The design surface shows card shape without becoming inherited guidance.",
                        }
                    ],
                }
            }

            result = readme_agents_corpus.scan_repository_corpus(
                repo, "fixture", dispositions
            )
            summary = result["readme_agents_summary"]

            self.assertEqual(summary["tracked_agents_files"], 1)
            self.assertEqual(summary["tracked_readme_files"], 1)
            self.assertEqual(summary["tracked_design_agents_files"], 1)
            self.assertEqual(summary["active_authored_agents_fenced_blocks"], 0)
            self.assertEqual(
                summary["active_authored_design_agents_classified_fenced_blocks"],
                1,
            )
            self.assertEqual(summary["reviewed_files"], 1)
            self.assertEqual(
                result["design_agents_files"][0]["review"]["review_state"],
                "reviewed",
            )
            self.assertEqual(
                result["agents_files"][0]["agents_chain_bytes"],
                len("# Root route\n".encode("utf-8")),
            )

    def test_readme_reference_lines_are_classified_by_read_pressure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "README.md").write_text("# Human route\n", encoding="utf-8")
            (repo / "AGENTS.md").write_text(
                """# Agent route

Read README.md before changing anything.

Read README.md only when the public entry surface changes.

README.md is the human entrypoint.
""",
                encoding="utf-8",
            )

            result = readme_agents_corpus.scan_repository_corpus(
                repo, "fixture", {}
            )
            summary = result["readme_agents_summary"]
            self.assertEqual(summary["agents_readme_reference_lines"], 3)
            self.assertEqual(
                summary["agents_files_declaring_mandatory_readme"], 1
            )
            self.assertEqual(
                summary["agents_conditional_readme_reference_lines"], 1
            )
            self.assertEqual(
                summary["agents_navigational_readme_reference_lines"], 1
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

    def test_shared_root_compares_rendered_owner_surfaces(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            owner = root / "owner"
            workspace.mkdir()
            (owner / "docs").mkdir(parents=True)
            rendered_root = workspace.as_posix()
            (workspace / "AGENTS.md").write_text(
                f"agents at {rendered_root}\n", encoding="utf-8"
            )
            (workspace / "README.md").write_text(
                f"workspace at {rendered_root}\n", encoding="utf-8"
            )
            (owner / "AGENTS.md").write_text(
                "agents at <workspace-root>\n", encoding="utf-8"
            )
            (owner / "docs" / "WORKSPACE_ROOT_ENTRY.md").write_text(
                "workspace at <workspace-root>\n", encoding="utf-8"
            )

            result = readme_agents_corpus.scan_shared_root(workspace, owner, {})
            records = {record["path"]: record for record in result["files"]}

            self.assertTrue(records["AGENTS.md"]["owner_parity"])
            self.assertTrue(records["README.md"]["owner_parity"])
            self.assertEqual(
                records["AGENTS.md"]["sha256"], records["AGENTS.md"]["owner_sha256"]
            )


if __name__ == "__main__":
    unittest.main()
