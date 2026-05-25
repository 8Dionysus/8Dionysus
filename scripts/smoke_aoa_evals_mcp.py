#!/usr/bin/env python3
"""Smoke-check the workspace aoa_evals MCP wrapper over stdio."""
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
    "aoa_evals_comparison",
    "aoa_evals_expand",
    "aoa_evals_inspect",
    "aoa_evals_report_skeleton",
    "aoa_evals_runtime_evidence_template",
    "aoa_evals_select",
}


async def run_smoke(workspace_root: Path) -> dict[str, object]:
    env = os.environ.copy()
    env["AOA_WORKSPACE_ROOT"] = str(workspace_root)
    params = StdioServerParameters(
        command="python3",
        args=[str(workspace_root / ".codex" / "bin" / "aoa-evals-mcp-server.py")],
        env=env,
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = {tool.name for tool in (await session.list_tools()).tools}
            missing_tools = sorted(REQUIRED_TOOLS - tools)
            selection = await session.call_tool(
                "aoa_evals_select",
                {
                    "proof_question": "bounded change verification",
                    "filters": {"category": "workflow", "limit": 3},
                },
            )
            selection_payload = json.loads(selection.content[0].text)
            first = selection_payload["matches"][0]["name"] if selection_payload.get("matches") else ""
            inspection = await session.call_tool("aoa_evals_inspect", {"name": first})
            skeleton = await session.call_tool(
                "aoa_evals_report_skeleton",
                {"name": first, "evidence_refs": ["artifact:smoke"]},
            )
            inspection_payload = json.loads(inspection.content[0].text)
            skeleton_payload = json.loads(skeleton.content[0].text)
    errors: list[str] = []
    if missing_tools:
        errors.append(f"missing tools: {', '.join(missing_tools)}")
    if not selection_payload.get("matches"):
        errors.append("aoa_evals_select returned no bounded candidates")
    if inspection_payload.get("authority_boundary", {}).get("stronger_owner") != "bundle-local EVAL.md and eval.yaml":
        errors.append("aoa_evals_inspect did not preserve source authority boundary")
    if skeleton_payload.get("sections", {}).get("verdict") != "UNSET: MCP must not compute verdicts":
        errors.append("aoa_evals_report_skeleton did not leave verdict unset")
    return {
        "schema": "8dionysus_aoa_evals_mcp_smoke_v1",
        "ok": not errors,
        "workspace_root": str(workspace_root),
        "tools": sorted(tools),
        "selected_eval": first,
        "candidate_only": skeleton_payload.get("candidate_only"),
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
