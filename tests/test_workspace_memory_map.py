from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import build_workspace_memory_map
import validate_workspace_memory_map


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class WorkspaceMemoryMapTests(unittest.TestCase):
    def test_route_only_and_full_port_classification(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._make_root(workspace / "8Dionysus", with_memory_route=True)
            write_text(
                workspace / "8Dionysus" / "docs" / "decisions" / "8DION-D-0001-memory-writeback.md",
                "# Memory writeback\n",
            )
            self._make_root(workspace / "Agents-of-Abyss", with_memory_route=True)
            self._make_full_port(workspace / "Agents-of-Abyss" / "memo", "Agents-of-Abyss")
            self._make_root(workspace / "Tree-of-Sophia", with_memory_route=True)
            self._make_root(workspace / "aoa-memo", with_memory_route=True)
            self._make_root(workspace / ".aoa", with_memory_route=False)

            payload = build_workspace_memory_map.build_workspace_memory_map(workspace)
            by_name = {place["name"]: place for place in payload["places"]}

            self.assertEqual(by_name["8Dionysus"]["current_port_level"], "route_only")
            self.assertEqual(by_name["Agents-of-Abyss"]["current_port_level"], "full_port")
            self.assertIn(
                "PYTHONPATH",
                by_name["Agents-of-Abyss"]["validation_command"],
            )
            self.assertIn("validate-port --repo Agents-of-Abyss", by_name["Agents-of-Abyss"]["validation_command"])
            self.assertEqual(by_name["Tree-of-Sophia"]["recommended_port_level"], "full_port")
            self.assertIn("recommended full memo port not yet present", by_name["Tree-of-Sophia"]["issues"])
            self.assertEqual(by_name["aoa-memo"]["memory_role"], "reviewed-memory-owner")
            self.assertEqual(by_name[".aoa"]["memory_role"], "session-evidence-kernel")
            self.assertEqual(by_name[".aoa"]["memory_route_status"], "session_evidence_route")
            self.assertEqual(by_name[".aoa"]["current_port_level"], "route_only")
            self.assertEqual(by_name["8Dionysus"]["writeback_marker"]["status"], "present")
            self.assertEqual(by_name["8Dionysus"]["writeback_debt"]["status"], "live_check_required")
            self.assertEqual(by_name["aoa-memo"]["writeback_debt"]["status"], "needs_first_marker")
            self.assertEqual(
                by_name["aoa-memo"]["writeback_debt"]["first_marker_route"],
                "route_only_owner_decision",
            )

            validate_workspace_memory_map.validate_payload(payload)
            self.assertEqual(payload["access_plane"]["runtime_status"], "not_asserted_by_workspace_map")
            self.assertEqual(payload["writeback_surface"]["judgment_route"], "aoa-memo-writeback")
            self.assertIn("local_memo_port_activation", payload["taxonomy"]["first_marker_routes"])
            self.assertIn("smoke_aoa_memo_mcp.py", payload["access_plane"]["smoke_check"])
            live_readout = build_workspace_memory_map.build_writeback_debt_readout(workspace)
            live_by_name = {place["name"]: place for place in live_readout["places"]}
            self.assertEqual(live_by_name["aoa-memo"]["status"], "needs_first_marker")
            self.assertGreaterEqual(live_readout["totals"]["needs_first_marker"], 1)
            rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            self.assertNotIn(str(workspace), rendered)

    def test_port_yaml_parser_reads_lists_and_scalars(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            port = Path(tmp) / "PORT.yaml"
            write_text(
                port,
                """schema: aoa_local_memo_port_v1
repo: demo
return_receipts: true
allowed_routes:
  - local_only
  - reviewed_intake
""",
            )

            payload = build_workspace_memory_map.parse_port_yaml(port)

            self.assertEqual(payload["schema"], "aoa_local_memo_port_v1")
            self.assertTrue(payload["return_receipts"])
            self.assertEqual(payload["allowed_routes"], ["local_only", "reviewed_intake"])

    def test_reviewed_landing_receipts_are_writeback_markers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._make_root(workspace / "aoa-memo", with_memory_route=True)
            write_text(
                workspace
                / "aoa-memo"
                / "memo"
                / "intake"
                / "receipts"
                / "20260526T004143Z.demo.demo-memory.landing-receipt.json",
                json.dumps(
                    {
                        "schema": "aoa_memo_reviewed_intake_landing_receipt_v1",
                        "repo": "demo",
                        "result": "landed",
                        "object_ref": "memo.decision.2026-05-26.demo-memory",
                    }
                ),
            )

            payload = build_workspace_memory_map.build_workspace_memory_map(workspace)
            by_name = {place["name"]: place for place in payload["places"]}
            marker = by_name["aoa-memo"]["writeback_marker"]

            self.assertEqual(marker["status"], "present")
            self.assertEqual(marker["marker_kind"], "reviewed_memory_landing_receipt")
            self.assertEqual(marker["decision"], "reviewed_write")
            self.assertEqual(marker["source"], "reviewed_memory_corpus")
            self.assertIn("aoa-memo/memo/intake/receipts/", marker["marker_ref"])
            validate_workspace_memory_map.validate_payload(payload)

    def test_reviewed_landing_receipts_do_not_mark_non_owner_repos(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            root = workspace / "aoa-sdk"
            self._make_root(root, with_memory_route=True)
            write_text(
                root / "memo" / "intake" / "receipts" / "20260526T004143Z.demo.landing-receipt.json",
                json.dumps(
                    {
                        "schema": "aoa_memo_reviewed_intake_landing_receipt_v1",
                        "repo": "demo",
                        "result": "landed",
                        "object_ref": "memo.decision.2026-05-26.demo-memory",
                    }
                ),
            )

            payload = build_workspace_memory_map.build_workspace_memory_map(workspace)
            by_name = {place["name"]: place for place in payload["places"]}
            marker = by_name["aoa-sdk"]["writeback_marker"]

            self.assertEqual(marker["status"], "missing")
            self.assertNotEqual(marker["marker_kind"], "reviewed_memory_landing_receipt")
            self.assertEqual(by_name["aoa-sdk"]["writeback_debt"]["status"], "needs_first_marker")
            validate_workspace_memory_map.validate_payload(payload)

    def test_workspace_memory_map_sync_is_8dionysus_marker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            root = workspace / "8Dionysus"
            self._make_root(root, with_memory_route=True)
            write_text(root / "docs" / "decisions" / "8DION-D-0001-memory-writeback.md", "# Memory writeback\n")
            write_text(root / "docs" / "WORKSPACE_MEMORY_MAP.md", "# Workspace memory map\n")
            write_text(root / "generated" / "workspace_memory_map.min.json", "{}\n")

            payload = build_workspace_memory_map.build_workspace_memory_map(workspace)
            by_name = {place["name"]: place for place in payload["places"]}
            marker = by_name["8Dionysus"]["writeback_marker"]

            self.assertEqual(marker["status"], "present")
            self.assertEqual(marker["marker_kind"], "workspace_memory_map_sync")
            self.assertEqual(marker["decision"], "no_writeback_needed")
            self.assertEqual(marker["source"], "workspace_memory_map_sync")
            self.assertEqual(marker["marker_ref"], "8Dionysus/generated/workspace_memory_map.min.json")
            validate_workspace_memory_map.validate_payload(payload)

    def test_workspace_memory_map_sync_uses_manifest_repo_identity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            root = workspace / "entry-route"
            self._make_root(root, with_memory_route=True)
            write_text(root / "docs" / "WORKSPACE_MEMORY_MAP.md", "# Workspace memory map\n")
            write_text(root / "generated" / "workspace_memory_map.min.json", "{}\n")
            write_text(
                workspace / "aoa-sdk" / ".aoa" / "workspace.toml",
                """[repos.8Dionysus]
preferred = ["{workspace_root}/entry-route"]
""",
            )

            payload = build_workspace_memory_map.build_workspace_memory_map(workspace)
            by_name = {place["name"]: place for place in payload["places"]}
            marker = by_name["8Dionysus"]["writeback_marker"]

            self.assertEqual(by_name["8Dionysus"]["path_hint"], "entry-route")
            self.assertEqual(marker["status"], "present")
            self.assertEqual(marker["marker_kind"], "workspace_memory_map_sync")
            self.assertEqual(marker["marker_ref"], "entry-route/generated/workspace_memory_map.min.json")
            validate_workspace_memory_map.validate_payload(payload)

    def test_aoa_memo_operational_readout_sync_is_marker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            root = workspace / "aoa-memo"
            self._make_root(root, with_memory_route=True)
            write_text(root / "generated" / "memory" / "access_plane_currentness.min.json", "{}\n")
            write_text(root / "generated" / "memory" / "workspace_memo_port_status.min.json", "{}\n")

            payload = build_workspace_memory_map.build_workspace_memory_map(workspace)
            by_name = {place["name"]: place for place in payload["places"]}
            marker = by_name["aoa-memo"]["writeback_marker"]

            self.assertEqual(marker["status"], "present")
            self.assertEqual(marker["marker_kind"], "memo_operational_readout_sync")
            self.assertEqual(marker["decision"], "no_writeback_needed")
            self.assertEqual(marker["source"], "memo_operational_readout_sync")
            self.assertEqual(marker["marker_ref"], "aoa-memo/generated/memory/workspace_memo_port_status.min.json")
            validate_workspace_memory_map.validate_payload(payload)

    @unittest.skipIf(shutil.which("git") is None, "git is required for marker currentness ordering")
    def test_latest_committed_marker_wins_over_lexicographic_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            root = workspace / "aoa-memo"
            self._make_root(root, with_memory_route=True)
            write_text(
                root / "memo" / "intake" / "receipts" / "20260526T004143Z.demo.landing-receipt.json",
                json.dumps(
                    {
                        "schema": "aoa_memo_reviewed_intake_landing_receipt_v1",
                        "repo": "demo",
                        "result": "landed",
                        "object_ref": "memo.decision.2026-05-26.demo-memory",
                    }
                ),
            )
            self._git(root, "init")
            self._git(root, "config", "user.email", "test@example.invalid")
            self._git(root, "config", "user.name", "AoA Test")
            self._git(root, "add", ".")
            self._git(root, "commit", "-m", "land reviewed intake")
            write_text(root / "generated" / "memory" / "workspace_memo_port_status.min.json", "{}\n")
            self._git(root, "add", ".")
            self._git(root, "commit", "-m", "refresh memo readout")

            payload = build_workspace_memory_map.build_workspace_memory_map(workspace)
            by_name = {place["name"]: place for place in payload["places"]}
            marker = by_name["aoa-memo"]["writeback_marker"]

            self.assertEqual(marker["marker_kind"], "memo_operational_readout_sync")
            self.assertEqual(marker["marker_ref"], "aoa-memo/generated/memory/workspace_memo_port_status.min.json")

    def test_markdown_keeps_route_contract_visible(self) -> None:
        payload = build_workspace_memory_map.build_workspace_memory_map(Path(__file__).resolve().parents[2])
        markdown = build_workspace_memory_map.render_markdown(payload)

        self.assertIn("aoa-memo", markdown)
        self.assertIn(".aoa", markdown)
        self.assertIn("MCP", markdown)
        self.assertIn("repo/memo", markdown)
        self.assertIn("runtime_status", markdown)
        self.assertIn("Writeback Currentness", markdown)
        self.assertIn("needs_first_marker", markdown)
        self.assertIn("writeback-debt-json", markdown)

    @unittest.skipIf(shutil.which("git") is None, "git is required for live debt currentness")
    def test_live_writeback_debt_reports_commits_after_marker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            root = workspace / "8Dionysus"
            self._make_root(root, with_memory_route=True)
            write_text(
                root / "docs" / "decisions" / "8DION-D-0001-memory-writeback.md",
                "# Memory writeback\n",
            )
            self._git(root, "init")
            self._git(root, "config", "user.email", "test@example.invalid")
            self._git(root, "config", "user.name", "AoA Test")
            self._git(root, "add", ".")
            self._git(root, "commit", "-m", "add memory writeback marker")
            write_text(root / "README.md", "# Demo\n")
            self._git(root, "add", "README.md")
            self._git(root, "commit", "-m", "land work after marker")

            readout = build_workspace_memory_map.build_writeback_debt_readout(workspace)
            by_name = {place["name"]: place for place in readout["places"]}

            self.assertEqual(by_name["8Dionysus"]["status"], "has_unmarked_changes")
            self.assertEqual(by_name["8Dionysus"]["commits_since_marker"], 1)
            self.assertIn("aoa-memo-writeback", readout["judgment_route"])

    def _make_root(self, root: Path, *, with_memory_route: bool) -> None:
        text = "# AGENTS.md\n\n## Purpose\n\nDemo root.\n"
        if with_memory_route:
            text += "\n## Memory route\n\nUse `aoa_memo` for continuity and `.aoa` for session evidence.\n"
        write_text(root / "AGENTS.md", text)

    def _make_full_port(self, memo: Path, repo: str) -> None:
        write_text(memo / "AGENTS.md", "# AGENTS.md\n\n## Memory route\n")
        write_text(memo / "README.md", "# Memo\n")
        write_text(
            memo / "PORT.yaml",
            f"""schema: aoa_local_memo_port_v1
repo: {repo}
owner: {repo}
stronger_memory_owner: aoa-memo
default_mode: write_candidate_only
port_scope: repo
allowed_routes:
  - local_only
  - reviewed_intake
candidate_dir: candidates
receipt_dir: receipts
export_dir: exports
local_dir: local
return_receipts: true
""",
        )
        write_text(memo / "index.min.json", "{}\n")
        for name in ("candidates", "receipts", "exports", "local"):
            (memo / name).mkdir(parents=True, exist_ok=True)

    def _git(self, root: Path, *args: str) -> None:
        subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True)


if __name__ == "__main__":
    unittest.main()
