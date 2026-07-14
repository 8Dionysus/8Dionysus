from __future__ import annotations

import asyncio
import builtins
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "smoke_aoa_stats_mcp.py"


def load_smoke_module():
    spec = importlib.util.spec_from_file_location("smoke_aoa_stats_mcp_under_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SmokeAoaStatsMcpTests(unittest.TestCase):
    def test_module_load_does_not_require_mcp_sdk(self) -> None:
        real_import = builtins.__import__

        def guarded_import(name: str, *args: object, **kwargs: object) -> object:
            if name == "mcp" or name.startswith("mcp."):
                raise ModuleNotFoundError("No module named 'mcp'")
            return real_import(name, *args, **kwargs)

        with mock.patch("builtins.__import__", side_effect=guarded_import):
            module = load_smoke_module()

        self.assertEqual(
            module.parse_args(["--workspace-root", str(ROOT)]).workspace_root,
            ROOT,
        )

    def test_smoke_accepts_read_only_owner_packet_route(self) -> None:
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

            async def list_resources(self) -> object:
                return types.SimpleNamespace(resources=[])

            async def list_resource_templates(self) -> object:
                return types.SimpleNamespace(resourceTemplates=[])

            async def list_prompts(self) -> object:
                return types.SimpleNamespace(prompts=[])

            async def call_tool(self, name: str, args: dict[str, object]) -> object:
                if name == "stats_boundary_rules":
                    return result(
                        {
                            "schema": "aoa_stats_mcp_boundary_rules_v1",
                            "source_owner": "aoa-stats",
                            "access_owner": "abyss-stack",
                        }
                    )
                if name == "stats_catalog":
                    return result({"surfaces": [{"name": "sample"}]})
                if name == "stats_owner_port_read":
                    return result(
                        {
                            "status": "available",
                            "port": {
                                "owner_repo": "aoa-memo",
                                "measurements": [
                                    {
                                        "measurement_id": "aoa-memo/sample-count",
                                        "contract_version": "1.0.0",
                                    }
                                ],
                                "exports": [
                                    {
                                        "measurement_id": "aoa-memo/sample-count",
                                        "packet_refs": ["stats/packets/sample.reference.json"],
                                    }
                                ],
                            },
                        }
                    )
                if name == "stats_packet_check":
                    if args["packet"] != {"value": 1}:
                        raise AssertionError("stats_packet_check received the wrong packet")
                    return result(
                        {
                            "compatible": True,
                            "truth_status": "compatibility_check_only",
                            "measurement_id": "aoa-memo/sample-count",
                            "semantic_identity": "aoa-stats-statistic:sha256:sample",
                            "evidence_identity": "aoa-stats-evidence:sha256:sample",
                        }
                    )
                raise AssertionError(f"unexpected tool: {name}")

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

        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            packet_path = (
                workspace_root
                / "aoa-memo"
                / "stats"
                / "packets"
                / "sample.reference.json"
            )
            packet_path.parent.mkdir(parents=True)
            packet_path.write_text('{"value": 1}\n', encoding="utf-8")
            with mock.patch.dict(
                sys.modules,
                {
                    "mcp": mcp_module,
                    "mcp.client": client_module,
                    "mcp.client.stdio": stdio_module,
                },
            ):
                smoke = asyncio.run(module.run_smoke(workspace_root))

        self.assertTrue(smoke["ok"])
        self.assertEqual(smoke["tools"], sorted(module.REQUIRED_TOOLS))
        self.assertEqual(smoke["source_owner"], "aoa-stats")
        self.assertEqual(smoke["access_owner"], "abyss-stack")
        self.assertEqual(smoke["catalog_surface_count"], 1)
        self.assertEqual(smoke["errors"], [])


if __name__ == "__main__":
    unittest.main()
