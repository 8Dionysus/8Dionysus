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
SCRIPT_PATH = ROOT / "scripts" / "smoke_aoa_kag_mcp.py"


def load_smoke_module():
    spec = importlib.util.spec_from_file_location("smoke_aoa_kag_mcp_under_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SmokeAoaKagMcpTests(unittest.TestCase):
    def test_module_load_does_not_require_mcp_sdk(self) -> None:
        real_import = builtins.__import__

        def guarded_import(name: str, *args: object, **kwargs: object) -> object:
            if name == "mcp" or name.startswith("mcp."):
                raise ModuleNotFoundError("No module named 'mcp'")
            return real_import(name, *args, **kwargs)

        with mock.patch("builtins.__import__", side_effect=guarded_import):
            module = load_smoke_module()

        self.assertEqual(module.parse_args(["--workspace-root", str(ROOT)]).workspace_root, ROOT)

    def test_smoke_accepts_full_provider_access_packet(self) -> None:
        module = load_smoke_module()

        def result(payload: dict[str, object]) -> object:
            return types.SimpleNamespace(content=[types.SimpleNamespace(text=json.dumps(payload))])

        def resource(payload: dict[str, object]) -> object:
            return types.SimpleNamespace(contents=[types.SimpleNamespace(text=json.dumps(payload))])

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
                return types.SimpleNamespace(
                    resources=[types.SimpleNamespace(uri=uri) for uri in module.REQUIRED_RESOURCES]
                )

            async def list_resource_templates(self) -> object:
                return types.SimpleNamespace(
                    resourceTemplates=[
                        types.SimpleNamespace(uriTemplate=uri)
                        for uri in module.REQUIRED_RESOURCE_TEMPLATES
                    ]
                )

            async def list_prompts(self) -> object:
                return types.SimpleNamespace(
                    prompts=[types.SimpleNamespace(name=name) for name in module.REQUIRED_PROMPTS]
                )

            async def call_tool(self, name: str, args: dict[str, object]) -> object:
                payloads: dict[str, dict[str, object]] = {
                    "aoa_kag_provider_status": {
                        "status": {
                            "provider_count": 15,
                            "remaining_route_count": 0,
                            "os_surface_count": 13,
                        }
                    },
                    "aoa_kag_provider_lookup": {"status": "provider_ready"},
                    "aoa_kag_freshness_check": {"ok": True, "missing_receipts": []},
                    "aoa_kag_source_return_lookup": {
                        "owner_return_routes": [{"surface": "kag/README.md"}]
                    },
                    "aoa_kag_registry_slice": {"count": 5},
                    "aoa_kag_composition_slice": {"count": 3},
                    "aoa_kag_validation_status": {"provider_homes": [{"repo": "aoa-kag"}]},
                }
                return result(payloads[name])

            async def read_resource(self, uri: str) -> object:
                payloads: dict[str, dict[str, object]] = {
                    "aoa-kag://registry/provider-map": {
                        "schema_version": "aoa-local-kag-provider-map-v1"
                    },
                    "aoa-kag://readiness/os-surfaces": {
                        "os_surfaces": [{"root_id": "aoa-kag"}]
                    },
                    "aoa-kag://providers/aoa-kag/manifest": {"repo": "aoa-kag"},
                    "aoa-kag://providers/aoa-kag/records/node": {"count": 1},
                }
                return resource(payloads[uri])

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
        self.assertEqual(smoke["provider_count"], 15)
        self.assertEqual(smoke["aoa_kag_lookup_status"], "provider_ready")
        self.assertEqual(smoke["errors"], [])


if __name__ == "__main__":
    unittest.main()
