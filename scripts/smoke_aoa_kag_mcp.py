#!/usr/bin/env python3
"""Smoke-check the source-owned aoa_kag MCP wrapper over stdio."""
from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
from typing import Any, Sequence


REQUIRED_TOOLS = {
    "aoa_kag_composition_slice",
    "aoa_kag_freshness_check",
    "aoa_kag_provider_lookup",
    "aoa_kag_provider_status",
    "aoa_kag_registry_slice",
    "aoa_kag_source_return_lookup",
    "aoa_kag_validation_status",
}

REQUIRED_PROMPTS = {
    "bounded-provider-query",
    "cross-repo-relation-preview",
    "runtime-handoff-brief",
    "source-return-summary",
}

REQUIRED_RESOURCES = {
    "aoa-kag://registry/provider-map",
    "aoa-kag://readiness/os-surfaces",
}

REQUIRED_RESOURCE_TEMPLATES = {
    "aoa-kag://providers/{repo}/manifest",
    "aoa-kag://providers/{repo}/records/{record_class}",
}


def _json_tool_payload(result: Any) -> dict[str, object]:
    return json.loads(result.content[0].text)


def _json_resource_payload(result: Any) -> dict[str, object]:
    return json.loads(result.contents[0].text)


def _resource_uri(resource: object) -> str:
    return str(getattr(resource, "uri", ""))


def _template_uri(template: object) -> str:
    return str(
        getattr(template, "uriTemplate", "")
        or getattr(template, "uri_template", "")
        or getattr(template, "uri", "")
    )


async def run_smoke(workspace_root: Path) -> dict[str, object]:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    launcher = workspace_root / ".codex" / "bin" / "aoa-kag-mcp-server.py"
    env = os.environ.copy()
    env["AOA_WORKSPACE_ROOT"] = str(workspace_root)
    params = StdioServerParameters(
        command="python3",
        args=[str(launcher)],
        env=env,
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = {tool.name for tool in (await session.list_tools()).tools}
            resources = {_resource_uri(resource) for resource in (await session.list_resources()).resources}
            templates = {
                _template_uri(template)
                for template in (await session.list_resource_templates()).resourceTemplates
            }
            prompts = {prompt.name for prompt in (await session.list_prompts()).prompts}

            status = _json_tool_payload(await session.call_tool("aoa_kag_provider_status", {}))
            lookup = _json_tool_payload(
                await session.call_tool("aoa_kag_provider_lookup", {"repo": "aoa-kag"})
            )
            freshness = _json_tool_payload(await session.call_tool("aoa_kag_freshness_check", {}))
            source_return = _json_tool_payload(
                await session.call_tool("aoa_kag_source_return_lookup", {"repo": "aoa-kag"})
            )
            registry = _json_tool_payload(
                await session.call_tool("aoa_kag_registry_slice", {"limit": 5})
            )
            composition = _json_tool_payload(
                await session.call_tool("aoa_kag_composition_slice", {"query": "kag", "limit": 5})
            )
            validation = _json_tool_payload(
                await session.call_tool(
                    "aoa_kag_validation_status",
                    {"include_provider_homes": True},
                )
            )
            provider_map = _json_resource_payload(
                await session.read_resource("aoa-kag://registry/provider-map")
            )
            readiness = _json_resource_payload(
                await session.read_resource("aoa-kag://readiness/os-surfaces")
            )
            manifest = _json_resource_payload(
                await session.read_resource("aoa-kag://providers/aoa-kag/manifest")
            )
            node_records = _json_resource_payload(
                await session.read_resource("aoa-kag://providers/aoa-kag/records/node")
            )

    status_block = status.get("status") if isinstance(status.get("status"), dict) else {}
    provider_count = int(status_block.get("provider_count") or 0)
    readiness_surfaces = readiness.get("os_surfaces")
    manifest_repo = manifest.get("repo")
    errors: list[str] = []

    missing_tools = sorted(REQUIRED_TOOLS - tools)
    missing_prompts = sorted(REQUIRED_PROMPTS - prompts)
    missing_resources = sorted(REQUIRED_RESOURCES - resources)
    missing_templates = sorted(REQUIRED_RESOURCE_TEMPLATES - templates)
    if missing_tools:
        errors.append(f"missing tools: {', '.join(missing_tools)}")
    if missing_prompts:
        errors.append(f"missing prompts: {', '.join(missing_prompts)}")
    if missing_resources:
        errors.append(f"missing resources: {', '.join(missing_resources)}")
    if missing_templates:
        errors.append(f"missing resource templates: {', '.join(missing_templates)}")
    if provider_count < 1:
        errors.append("aoa_kag_provider_status returned no providers")
    if lookup.get("status") != "provider_ready":
        errors.append("aoa_kag_provider_lookup did not return provider_ready for aoa-kag")
    if freshness.get("ok") is not True:
        errors.append("aoa_kag_freshness_check reported missing freshness handles")
    if not source_return.get("owner_return_routes"):
        errors.append("aoa_kag_source_return_lookup returned no owner routes for aoa-kag")
    if int(registry.get("count") or 0) < 1:
        errors.append("aoa_kag_registry_slice returned no rows")
    if int(composition.get("count") or 0) < 1:
        errors.append("aoa_kag_composition_slice returned no rows for query 'kag'")
    if provider_map.get("schema_version") != "aoa-local-kag-provider-map-v1":
        errors.append("provider-map resource returned unexpected schema_version")
    if not isinstance(readiness_surfaces, list) or not readiness_surfaces:
        errors.append("readiness resource returned no OS surfaces")
    if manifest_repo != "aoa-kag":
        errors.append("aoa-kag provider manifest did not identify repo=aoa-kag")
    if int(node_records.get("count") or 0) < 1:
        errors.append("aoa-kag node record resource returned no records")

    return {
        "schema": "8dionysus_aoa_kag_mcp_smoke_v1",
        "ok": not errors,
        "workspace_root": str(workspace_root),
        "launcher": str(launcher),
        "tools": sorted(tools),
        "resources": sorted(resources),
        "resource_templates": sorted(templates),
        "prompts": sorted(prompts),
        "provider_count": provider_count,
        "remaining_route_count": status_block.get("remaining_route_count"),
        "os_surface_count": status_block.get("os_surface_count"),
        "aoa_kag_lookup_status": lookup.get("status"),
        "freshness_ok": freshness.get("ok"),
        "missing_receipts": freshness.get("missing_receipts", []),
        "owner_return_route_count": len(source_return.get("owner_return_routes", [])),
        "registry_count": registry.get("count"),
        "composition_count": composition.get("count"),
        "validation_provider_home_count": len(validation.get("provider_homes", [])),
        "manifest_repo": manifest_repo,
        "node_record_count": node_records.get("count"),
        "errors": errors,
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, default=Path("/srv/AbyssOS"))
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result = asyncio.run(run_smoke(args.workspace_root.resolve()))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
