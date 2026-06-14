#!/usr/bin/env python3
"""Smoke-check the workspace aoa_memo MCP wrapper over stdio."""
from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
from typing import Sequence


REQUIRED_TOOLS = {
    "aoa_memo_brief",
    "aoa_memo_build_port_index",
    "aoa_memo_create_candidate",
    "aoa_memo_prepare_intake_packet",
    "aoa_memo_review_intake",
    "aoa_memo_search",
    "aoa_memo_validate_candidate",
    "aoa_memo_validate_port",
}


async def run_smoke(workspace_root: Path) -> dict[str, object]:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    env = os.environ.copy()
    env["AOA_WORKSPACE_ROOT"] = str(workspace_root)
    params = StdioServerParameters(
        command="python3",
        args=[str(workspace_root / ".codex" / "bin" / "aoa-memo-mcp-server.py")],
        env=env,
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = {tool.name for tool in (await session.list_tools()).tools}
            missing_tools = sorted(REQUIRED_TOOLS - tools)
            brief = await session.call_tool(
                "aoa_memo_brief",
                {"repo": "aoa-memo", "intent": "workspace MCP smoke check"},
            )
            search = await session.call_tool(
                "aoa_memo_search",
                {"query": "session_evidence_route", "scope": "all", "mode": "contracts"},
            )
            brief_payload = json.loads(brief.content[0].text)
            search_payload = json.loads(search.content[0].text)
    errors: list[str] = []
    if missing_tools:
        errors.append(f"missing tools: {', '.join(missing_tools)}")
    if brief_payload.get("operation_mode") != "read_write_under_review":
        errors.append("aoa-memo brief did not report reviewed authority mode")
    candidate_route = (brief_payload.get("memory_route") or {}).get("candidate")
    return {
        "schema": "8dionysus_aoa_memo_mcp_smoke_v1",
        "ok": not errors,
        "workspace_root": str(workspace_root),
        "tools": sorted(tools),
        "brief_mode": brief_payload.get("operation_mode"),
        "candidate_route": candidate_route,
        "search_hits": len(search_payload.get("hits", [])),
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
