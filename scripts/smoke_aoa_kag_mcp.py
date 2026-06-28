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

SAMPLE_PROVIDER_REPOS = (
    "aoa-kag",
    "Agents-of-Abyss",
    "aoa-memo",
    "aoa-evals",
    "aoa-skills",
)
SAMPLE_RECORD_PROVIDER = "aoa-kag"
RECORD_CLASSES = ("node", "edge", "index", "projection", "receipt")
REQUIRED_OS_SURFACES = {".codex", "src/abyss-stack"}
REQUIRED_SERVICE_ROUTE = "abyss-stack/mcp/services/aoa-kag-mcp"


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
            provider_lookups = {
                repo: _json_tool_payload(
                    await session.call_tool("aoa_kag_provider_lookup", {"repo": repo})
                )
                for repo in SAMPLE_PROVIDER_REPOS
            }
            freshness = _json_tool_payload(await session.call_tool("aoa_kag_freshness_check", {}))
            source_returns = {
                repo: _json_tool_payload(
                    await session.call_tool("aoa_kag_source_return_lookup", {"repo": repo})
                )
                for repo in SAMPLE_PROVIDER_REPOS
            }
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
            manifests = {
                repo: _json_resource_payload(
                    await session.read_resource(f"aoa-kag://providers/{repo}/manifest")
                )
                for repo in SAMPLE_PROVIDER_REPOS
            }
            provider_records = {
                record_class: _json_resource_payload(
                    await session.read_resource(
                        f"aoa-kag://providers/{SAMPLE_RECORD_PROVIDER}/records/{record_class}"
                    )
                )
                for record_class in RECORD_CLASSES
            }

    status_block = status.get("status") if isinstance(status.get("status"), dict) else {}
    provider_count = int(status_block.get("provider_count") or 0)
    readiness_surfaces = readiness.get("os_surfaces")
    readiness_surface_ids = {
        surface.get("surface_id")
        for surface in readiness_surfaces
        if isinstance(surface, dict)
    } if isinstance(readiness_surfaces, list) else set()
    provider_map_handoff = (
        provider_map.get("mcp_handoff")
        if isinstance(provider_map.get("mcp_handoff"), dict)
        else {}
    )
    service_route = provider_map_handoff.get("service_route")
    provider_lookup_statuses = {
        repo: packet.get("status")
        for repo, packet in provider_lookups.items()
    }
    source_return_route_counts = {
        repo: len(packet.get("owner_return_routes", []))
        for repo, packet in source_returns.items()
    }
    manifest_repos = {
        repo: packet.get("repo")
        for repo, packet in manifests.items()
    }
    record_class_counts = {
        record_class: packet.get("count")
        for record_class, packet in provider_records.items()
    }
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
    for repo, lookup_status in provider_lookup_statuses.items():
        if lookup_status != "provider_ready":
            errors.append(f"aoa_kag_provider_lookup did not return provider_ready for {repo}")
    if freshness.get("ok") is not True:
        errors.append("aoa_kag_freshness_check reported missing freshness handles")
    for repo, route_count in source_return_route_counts.items():
        if route_count < 1:
            errors.append(f"aoa_kag_source_return_lookup returned no owner routes for {repo}")
    if int(registry.get("count") or 0) < 1:
        errors.append("aoa_kag_registry_slice returned no rows")
    if int(composition.get("count") or 0) < 1:
        errors.append("aoa_kag_composition_slice returned no rows for query 'kag'")
    if provider_map.get("schema_version") != "aoa-local-kag-provider-map-v1":
        errors.append("provider-map resource returned unexpected schema_version")
    if service_route != REQUIRED_SERVICE_ROUTE:
        errors.append("provider-map resource returned unexpected aoa-kag-mcp service route")
    if not isinstance(readiness_surfaces, list) or not readiness_surfaces:
        errors.append("readiness resource returned no OS surfaces")
    missing_os_surfaces = sorted(REQUIRED_OS_SURFACES - readiness_surface_ids)
    if missing_os_surfaces:
        errors.append(f"readiness resource is missing OS surfaces: {', '.join(missing_os_surfaces)}")
    for repo, manifest_repo in manifest_repos.items():
        if manifest_repo != repo:
            errors.append(f"{repo} provider manifest did not identify repo={repo}")
    for record_class, count in record_class_counts.items():
        if int(count or 0) < 1:
            errors.append(f"{SAMPLE_RECORD_PROVIDER} {record_class} record resource returned no records")

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
        "service_route": service_route,
        "sample_provider_lookup_statuses": provider_lookup_statuses,
        "freshness_ok": freshness.get("ok"),
        "missing_receipts": freshness.get("missing_receipts", []),
        "sample_source_return_route_counts": source_return_route_counts,
        "registry_count": registry.get("count"),
        "composition_count": composition.get("count"),
        "validation_provider_home_count": len(validation.get("provider_homes", [])),
        "sample_manifest_repos": manifest_repos,
        "record_provider": SAMPLE_RECORD_PROVIDER,
        "record_class_counts": record_class_counts,
        "required_os_surfaces": sorted(REQUIRED_OS_SURFACES),
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
