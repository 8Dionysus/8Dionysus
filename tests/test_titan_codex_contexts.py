from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_context_tool(relative_path: str) -> dict[str, object]:
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / relative_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    assert isinstance(payload, dict)
    return payload


class TitanCodexContextTests(unittest.TestCase):
    def assert_session_start_context(self, payload: dict[str, object]) -> str:
        self.assertNotIn("additionalContext", payload)
        hook_output = payload.get("hookSpecificOutput")
        self.assertIsInstance(hook_output, dict)
        assert isinstance(hook_output, dict)
        self.assertEqual("SessionStart", hook_output.get("hookEventName"))
        context = hook_output.get("additionalContext")
        self.assertIsInstance(context, str)
        assert isinstance(context, str)
        return context

    def test_titan_bridge_context_uses_hook_specific_output(self) -> None:
        payload = run_context_tool(".codex/tools/aoa_titan_bridge_context.py")
        context = self.assert_session_start_context(payload)

        self.assertIn("Titan App-Server Bridge", context)

    def test_titan_memory_context_uses_plain_hook_specific_context(self) -> None:
        payload = run_context_tool(".codex/tools/aoa_titan_memory_context.py")
        context = self.assert_session_start_context(payload)

        self.assertIn("Titan Memory Loom", context)
        self.assertNotIn('{"hook"', context)

    def test_titan_swarm_report_allows_p0_findings(self) -> None:
        template = (REPO_ROOT / ".codex" / "prompts" / "titan-swarm.report.v0.md").read_text(
            encoding="utf-8"
        )

        self.assertIn('"severity": "P0|P1|P2|P3|note"', template)


if __name__ == "__main__":
    unittest.main()
