#!/usr/bin/env python3
"""Smoke-check the workspace abyss_machine MCP wrapper over stdio."""
from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
from typing import Sequence

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


REQUIRED_TOOLS = {
    "abyss_machine_brief",
    "abyss_machine_evidence_map",
    "abyss_machine_recall",
    "abyss_machine_route",
    "abyss_machine_surface",
}


async def run_smoke(workspace_root: Path) -> dict[str, object]:
    env = os.environ.copy()
    env["AOA_WORKSPACE_ROOT"] = str(workspace_root)
    params = StdioServerParameters(
        command="python3",
        args=[str(workspace_root / ".codex" / "bin" / "abyss-machine-mcp-server.py")],
        env=env,
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = {tool.name for tool in (await session.list_tools()).tools}
            missing_tools = sorted(REQUIRED_TOOLS - tools)
            brief = await session.call_tool("abyss_machine_brief", {"profile": "fast", "evidence_limit": 6})
            evidence = await session.call_tool("abyss_machine_evidence_map", {"limit": 8})
            memory = await session.call_tool("abyss_machine_surface", {"name": "memory-pressure"})
            route = await session.call_tool(
                "abyss_machine_route",
                {"intent": "smoke-check machine context route", "work_class": "heavy", "kind": "ai"},
            )
            brief_payload = json.loads(brief.content[0].text)
            evidence_payload = json.loads(evidence.content[0].text)
            memory_payload = json.loads(memory.content[0].text)
            route_payload = json.loads(route.content[0].text)

    errors: list[str] = []
    if missing_tools:
        errors.append(f"missing tools: {', '.join(missing_tools)}")
    if brief_payload.get("schema") != "abyss_machine_mcp_brief_v1":
        errors.append("abyss_machine_brief returned unexpected schema")
    if not brief_payload.get("constraints", {}).get("mutation_gates"):
        errors.append("abyss_machine_brief lost mutation gate refs")
    brief_evidence_count = brief_payload.get("evidence", {}).get("count", 0)
    if not (0 < brief_evidence_count <= 6):
        errors.append("abyss_machine_brief ignored evidence_limit")
    if brief_payload.get("authority_boundary", {}).get("mcp_role") != "stdio read-only access plane over abyss-machine host read models":
        errors.append("abyss_machine_brief did not preserve authority boundary")
    if evidence_payload.get("count", 0) <= 0:
        errors.append("abyss_machine_evidence_map returned no evidence refs")
    if memory_payload.get("ok") is not True:
        errors.append("abyss_machine_surface(memory-pressure) failed")
    if route_payload.get("mutates") is not False or route_payload.get("route_posture") != "preflight_only":
        errors.append("abyss_machine_route drifted from preflight-only posture")
    return {
        "schema": "8dionysus_abyss_machine_mcp_smoke_v1",
        "ok": not errors,
        "workspace_root": str(workspace_root),
        "tools": sorted(tools),
        "bridge_status": brief_payload.get("machine", {}).get("bridge_status"),
        "brief_evidence_count": brief_evidence_count,
        "evidence_count": evidence_payload.get("count"),
        "memory_surface_ok": memory_payload.get("ok"),
        "route_posture": route_payload.get("route_posture"),
        "errors": errors,
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, default=Path(__file__).resolve().parents[2])
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result = asyncio.run(run_smoke(args.workspace_root.resolve()))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
