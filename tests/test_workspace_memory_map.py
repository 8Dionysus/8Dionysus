from __future__ import annotations

import json
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

            validate_workspace_memory_map.validate_payload(payload)
            self.assertEqual(payload["access_plane"]["runtime_status"], "not_asserted_by_workspace_map")
            self.assertIn("smoke_aoa_memo_mcp.py", payload["access_plane"]["smoke_check"])
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

    def test_markdown_keeps_route_contract_visible(self) -> None:
        payload = build_workspace_memory_map.build_workspace_memory_map(Path(__file__).resolve().parents[2])
        markdown = build_workspace_memory_map.render_markdown(payload)

        self.assertIn("aoa-memo", markdown)
        self.assertIn(".aoa", markdown)
        self.assertIn("MCP", markdown)
        self.assertIn("repo/memo", markdown)
        self.assertIn("runtime_status", markdown)

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


if __name__ == "__main__":
    unittest.main()
