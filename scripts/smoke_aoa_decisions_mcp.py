#!/usr/bin/env python3
"""Smoke-check the source-owned aoa_decisions MCP wrapper over stdio."""
from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
from typing import Sequence

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_TOOLS = {
    "aoa_decisions_changed_path",
    "aoa_decisions_decision",
    "aoa_decisions_issues",
    "aoa_decisions_owner_surface",
    "aoa_decisions_packet",
    "aoa_decisions_refresh",
    "aoa_decisions_repo",
    "aoa_decisions_repo_symmetry",
    "aoa_decisions_search",
    "aoa_decisions_source_surface",
    "aoa_decisions_status",
    "aoa_decisions_summary",
}


async def run_smoke(workspace_root: Path, launcher: Path) -> dict[str, object]:
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
            missing_tools = sorted(REQUIRED_TOOLS - tools)
            status = await session.call_tool("aoa_decisions_status", {})
            summary = await session.call_tool("aoa_decisions_summary", {})
            search = await session.call_tool(
                "aoa_decisions_search",
                {"query": "decisions", "limit": 5},
            )
            packet = await session.call_tool(
                "aoa_decisions_packet",
                {"query": "decisions", "limit": 5},
            )
            issues = await session.call_tool("aoa_decisions_issues", {})
            symmetry = await session.call_tool("aoa_decisions_repo_symmetry", {})
            status_payload = json.loads(status.content[0].text)
            summary_payload = json.loads(summary.content[0].text)
            search_payload = json.loads(search.content[0].text)
            packet_payload = json.loads(packet.content[0].text)
            issues_payload = json.loads(issues.content[0].text)
            symmetry_payload = json.loads(symmetry.content[0].text)

    errors: list[str] = []
    if missing_tools:
        errors.append(f"missing tools: {', '.join(missing_tools)}")
    if status_payload.get("status") not in {"fresh", "refreshed"}:
        errors.append("aoa_decisions_status did not report a fresh/refreshed graph")
    if int(status_payload.get("issue_count") or 0) != 0:
        errors.append("aoa_decisions_status reported graph issues")
    if int(status_payload.get("decision_count") or 0) < 1:
        errors.append("aoa_decisions_status returned no decisions")
    if int(status_payload.get("decision_surface_count") or 0) < int(status_payload.get("decision_count") or 0):
        errors.append("aoa_decisions_status returned incomplete decision surface coverage")
    if int(summary_payload.get("decision_count") or 0) < 1:
        errors.append("aoa_decisions_summary returned no decisions")
    if not search_payload.get("results"):
        errors.append("aoa_decisions_search returned no results")
    if int(issues_payload.get("summary_issue_count") or 0) != 0:
        errors.append("aoa_decisions_issues reported graph issues")
    if not symmetry_payload.get("repos"):
        errors.append("aoa_decisions_repo_symmetry returned no repos")
    authority_order = packet_payload.get("authority_order") or []
    if not authority_order or authority_order[0] != "repo-local docs/decisions/*.md":
        errors.append("aoa_decisions_packet did not preserve source authority order")

    return {
        "schema": "8dionysus_aoa_decisions_mcp_smoke_v1",
        "ok": not errors,
        "workspace_root": str(workspace_root),
        "launcher": str(launcher),
        "tools": sorted(tools),
        "status": status_payload.get("status"),
        "decision_count": status_payload.get("decision_count"),
        "decision_surface_count": status_payload.get("decision_surface_count"),
        "repo_count": summary_payload.get("repo_count"),
        "search_count": len(search_payload.get("results", [])),
        "packet_decision_count": len(packet_payload.get("decisions", [])),
        "symmetry_repo_count": symmetry_payload.get("repo_count"),
        "input_fingerprint": status_payload.get("input_fingerprint"),
        "errors": errors,
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, default=Path("/srv/AbyssOS"))
    parser.add_argument(
        "--launcher",
        type=Path,
        default=REPO_ROOT / ".codex" / "bin" / "aoa-decisions-mcp-server.py",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result = asyncio.run(run_smoke(args.workspace_root.resolve(), args.launcher.resolve()))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
