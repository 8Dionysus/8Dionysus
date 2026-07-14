#!/usr/bin/env python3
"""Smoke-check the source-owned aoa_stats MCP wrapper over stdio."""
from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
from typing import Any, Sequence


REQUIRED_TOOLS = {
    "stats_boundary_rules",
    "stats_catalog",
    "stats_owner_port_read",
    "stats_packet_check",
    "stats_surface_read",
}
SAMPLE_REPO = "aoa-memo"


def _json_tool_payload(result: Any) -> dict[str, object]:
    payload = json.loads(result.content[0].text)
    if not isinstance(payload, dict):
        raise ValueError("stats MCP tool returned a non-object payload")
    return payload


def _sample_packet(
    workspace_root: Path,
    owner_result: dict[str, object],
) -> tuple[dict[str, object], dict[str, object]]:
    port = owner_result.get("port")
    if not isinstance(port, dict):
        raise ValueError(f"{SAMPLE_REPO} did not return a local stats port")
    measurements = port.get("measurements")
    exports = port.get("exports")
    if (
        not isinstance(measurements, list)
        or not measurements
        or not isinstance(measurements[0], dict)
    ):
        raise ValueError(f"{SAMPLE_REPO} did not return a measurement contract")
    contract = measurements[0]
    measurement_id = contract.get("measurement_id")
    export = (
        next(
            (
                item
                for item in exports
                if isinstance(item, dict)
                and item.get("measurement_id") == measurement_id
            ),
            None,
        )
        if isinstance(exports, list)
        else None
    )
    packet_refs = export.get("packet_refs") if isinstance(export, dict) else None
    if not isinstance(packet_refs, list) or not packet_refs or not isinstance(packet_refs[0], str):
        raise ValueError(f"{SAMPLE_REPO} did not return a packet reference")

    owner_root = (workspace_root / SAMPLE_REPO).resolve()
    packet_path = (owner_root / packet_refs[0]).resolve()
    packet_path.relative_to(owner_root)
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    if not isinstance(packet, dict):
        raise ValueError(f"{SAMPLE_REPO} packet is not a JSON object")
    return contract, packet


async def run_smoke(workspace_root: Path) -> dict[str, object]:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    launcher = workspace_root / ".codex" / "bin" / "aoa-stats-mcp-server.py"
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
            resources = [
                str(resource.uri)
                for resource in (await session.list_resources()).resources
            ]
            resource_templates = [
                str(
                    getattr(template, "uriTemplate", "")
                    or getattr(template, "uri_template", "")
                )
                for template in (await session.list_resource_templates()).resourceTemplates
            ]
            prompts = [prompt.name for prompt in (await session.list_prompts()).prompts]
            boundary = _json_tool_payload(await session.call_tool("stats_boundary_rules", {}))
            catalog = _json_tool_payload(await session.call_tool("stats_catalog", {}))
            owner = _json_tool_payload(
                await session.call_tool("stats_owner_port_read", {"repo": SAMPLE_REPO})
            )
            contract, packet = _sample_packet(workspace_root, owner)
            packet_check = _json_tool_payload(
                await session.call_tool(
                    "stats_packet_check",
                    {"contract": contract, "packet": packet},
                )
            )

    errors: list[str] = []
    missing_tools = sorted(REQUIRED_TOOLS - tools)
    extra_tools = sorted(tools - REQUIRED_TOOLS)
    if missing_tools:
        errors.append(f"missing tools: {', '.join(missing_tools)}")
    if extra_tools:
        errors.append(f"unexpected tools: {', '.join(extra_tools)}")
    if resources or resource_templates or prompts:
        errors.append("aoa_stats must not publish resources, resource templates, or prompts")
    if boundary.get("schema") != "aoa_stats_mcp_boundary_rules_v1":
        errors.append("stats_boundary_rules returned an unexpected schema")
    if (
        boundary.get("source_owner") != "aoa-stats"
        or boundary.get("access_owner") != "abyss-stack"
    ):
        errors.append("stats_boundary_rules returned an unexpected owner split")
    surfaces = catalog.get("surfaces")
    if not isinstance(surfaces, list) or not surfaces:
        errors.append("stats_catalog returned no derived surfaces")
    port = owner.get("port")
    if (
        owner.get("status") != "available"
        or not isinstance(port, dict)
        or port.get("owner_repo") != SAMPLE_REPO
    ):
        errors.append(f"stats_owner_port_read did not return the {SAMPLE_REPO} port")
    if packet_check.get("compatible") is not True:
        errors.append("stats_packet_check rejected the owner packet")
    if packet_check.get("truth_status") != "compatibility_check_only":
        errors.append("stats_packet_check crossed its compatibility-only authority ceiling")
    for identity_name in ("semantic_identity", "evidence_identity"):
        if not isinstance(packet_check.get(identity_name), str) or not packet_check.get(
            identity_name
        ):
            errors.append(f"stats_packet_check returned no {identity_name}")

    return {
        "schema": "8dionysus_aoa_stats_mcp_smoke_v1",
        "ok": not errors,
        "workspace_root": str(workspace_root),
        "launcher": str(launcher),
        "tools": sorted(tools),
        "resources": resources,
        "resource_templates": resource_templates,
        "prompts": prompts,
        "source_owner": boundary.get("source_owner"),
        "access_owner": boundary.get("access_owner"),
        "catalog_surface_count": len(surfaces) if isinstance(surfaces, list) else 0,
        "sample_repo": SAMPLE_REPO,
        "sample_measurement_id": packet_check.get("measurement_id"),
        "semantic_identity": packet_check.get("semantic_identity"),
        "evidence_identity": packet_check.get("evidence_identity"),
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
