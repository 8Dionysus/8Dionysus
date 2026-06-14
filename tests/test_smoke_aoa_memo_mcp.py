from __future__ import annotations

import asyncio
import builtins
import importlib.util
import json
from pathlib import Path
import sys
import types
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "smoke_aoa_memo_mcp.py"


def load_smoke_module():
    spec = importlib.util.spec_from_file_location("smoke_aoa_memo_mcp_under_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SmokeAoaMemoMcpTests(unittest.TestCase):
    def test_module_load_does_not_require_mcp_sdk(self) -> None:
        real_import = builtins.__import__

        def guarded_import(name: str, *args: object, **kwargs: object) -> object:
            if name == "mcp" or name.startswith("mcp."):
                raise ModuleNotFoundError("No module named 'mcp'")
            return real_import(name, *args, **kwargs)

        with mock.patch("builtins.__import__", side_effect=guarded_import):
            module = load_smoke_module()

        self.assertEqual(module.parse_args(["--workspace-root", str(ROOT)]).workspace_root, ROOT)

    def test_smoke_allows_mutable_route_text_and_empty_search_hits(self) -> None:
        module = load_smoke_module()

        def result(payload: dict[str, object]) -> object:
            return types.SimpleNamespace(content=[types.SimpleNamespace(text=json.dumps(payload))])

        class FakeClientSession:
            def __init__(self, read: object, write: object) -> None:
                pass

            async def __aenter__(self) -> "FakeClientSession":
                return self

            async def __aexit__(self, *args: object) -> None:
                return None

            async def initialize(self) -> None:
                return None

            async def list_tools(self) -> object:
                return types.SimpleNamespace(
                    tools=[types.SimpleNamespace(name=name) for name in module.REQUIRED_TOOLS]
                )

            async def call_tool(self, name: str, args: dict[str, object]) -> object:
                payloads: dict[str, dict[str, object]] = {
                    "aoa_memo_brief": {
                        "operation_mode": "read_write_under_review",
                        "memory_route": {
                            "candidate": "reviewed memory authority route wording may evolve",
                        },
                    },
                    "aoa_memo_search": {"hits": []},
                }
                return result(payloads[name])

        class FakeStdioClient:
            async def __aenter__(self) -> tuple[object, object]:
                return object(), object()

            async def __aexit__(self, *args: object) -> None:
                return None

        class FakeStdioServerParameters:
            def __init__(self, *args: object, **kwargs: object) -> None:
                pass

        mcp_module = types.ModuleType("mcp")
        mcp_module.ClientSession = FakeClientSession
        mcp_module.StdioServerParameters = FakeStdioServerParameters
        client_module = types.ModuleType("mcp.client")
        stdio_module = types.ModuleType("mcp.client.stdio")
        stdio_module.stdio_client = lambda params: FakeStdioClient()

        with mock.patch.dict(
            sys.modules,
            {
                "mcp": mcp_module,
                "mcp.client": client_module,
                "mcp.client.stdio": stdio_module,
            },
        ):
            smoke = asyncio.run(module.run_smoke(ROOT))

        self.assertTrue(smoke["ok"])
        self.assertEqual(smoke["candidate_route"], "reviewed memory authority route wording may evolve")
        self.assertEqual(smoke["search_hits"], 0)
        self.assertEqual(smoke["errors"], [])


if __name__ == "__main__":
    unittest.main()
