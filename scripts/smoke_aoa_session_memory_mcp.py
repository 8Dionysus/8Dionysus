#!/usr/bin/env python3
"""Smoke-check the workspace aoa_session_memory MCP wrapper over stdio."""
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
    "aoa_session_brief",
    "aoa_session_evidence_packet",
    "aoa_session_entity_inventory",
    "aoa_session_freshness_check",
    "aoa_session_explain_graph_packet",
    "aoa_session_graph_cooccurrence",
    "aoa_session_graph_eval",
    "aoa_session_graph_neighborhood",
    "aoa_session_graph_quality_audit",
    "aoa_session_graph_shortest_path",
    "aoa_session_graph_timeline",
    "aoa_session_graphrag_packet",
    "aoa_session_latest_diagnostics",
    "aoa_session_maintenance_plan",
    "aoa_session_memory_status",
    "aoa_session_pattern_scan",
    "aoa_session_retrieve",
    "aoa_session_route",
    "aoa_session_search",
    "aoa_session_trace",
}


REF_CONTAINER_KEYS = {
    "evidence_ref",
    "evidence_refs",
    "raw",
    "raw_ref",
    "raw_refs",
    "segment",
    "segment_ref",
    "segment_refs",
}


def ref_value_count(value: object) -> int:
    if isinstance(value, str):
        return 1 if value.strip() else 0
    if isinstance(value, list):
        return sum(ref_value_count(item) for item in value)
    if isinstance(value, dict):
        return refs_dict_count(value)
    return 0


def refs_dict_count(refs: object) -> int:
    if not isinstance(refs, dict) or not refs:
        return 0
    count = 0
    for key, value in refs.items():
        if key in REF_CONTAINER_KEYS:
            count += ref_value_count(value) or int(bool(value))
    if count:
        return count
    return sum(ref_value_count(value) for value in refs.values())


def evidence_ref_count(payload: object) -> int:
    if not isinstance(payload, dict):
        return 0
    count = 0
    refs = payload.get("evidence_refs")
    if isinstance(refs, list):
        count += sum(ref_value_count(item) or int(bool(item)) for item in refs)

    lexical = payload.get("lexical")
    if isinstance(lexical, dict):
        results = lexical.get("results")
        if isinstance(results, list):
            count += sum(refs_dict_count(item.get("refs")) for item in results if isinstance(item, dict))

    packet = payload.get("packet")
    if isinstance(packet, dict):
        count += evidence_ref_count(packet)

    return count


def quality_ready_count(payload: object) -> int:
    if not isinstance(payload, dict):
        return 0
    value = payload.get("ready_for_manual_verdict_count")
    if isinstance(value, int):
        return value
    samples = payload.get("sample_overview")
    if not isinstance(samples, list):
        return 0
    return sum(
        1
        for item in samples
        if isinstance(item, dict)
        and item.get("review_status") == "ready_for_manual_verdict"
        and (item.get("has_raw_ref") or item.get("has_segment_ref"))
    )


async def run_smoke(workspace_root: Path) -> dict[str, object]:
    env = os.environ.copy()
    env["AOA_WORKSPACE_ROOT"] = str(workspace_root)
    params = StdioServerParameters(
        command="python3",
        args=[str(workspace_root / ".codex" / "bin" / "aoa-session-memory-mcp-server.py")],
        env=env,
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = {tool.name for tool in (await session.list_tools()).tools}
            missing_tools = sorted(REQUIRED_TOOLS - tools)
            status = await session.call_tool("aoa_session_memory_status", {})
            trace = await session.call_tool(
                "aoa_session_trace",
                {"anchor": "aoa-session-memory-mcp", "limit": 5, "per_route_limit": 3},
            )
            route = await session.call_tool(
                "aoa_session_route",
                {"axis": "by-mcp", "key": "aoa-session-memory-mcp", "limit": 5},
            )
            evidence = await session.call_tool(
                "aoa_session_evidence_packet",
                {
                    "intent": "debug aoa-session-memory-mcp route",
                    "anchors": ["aoa-session-memory-mcp"],
                    "limit": 5,
                },
            )
            brief = await session.call_tool(
                "aoa_session_brief",
                {"session": "latest", "max_segments": 2},
            )
            skill_inventory = await session.call_tool(
                "aoa_session_entity_inventory",
                {"layer": "skill", "session": "latest", "limit": 5, "sample_limit": 0},
            )
            graph = await session.call_tool(
                "aoa_session_graph_neighborhood",
                {"anchor": "aoa-session-memory-mcp", "kind": "mcp", "limit": 20},
            )
            graphrag = await session.call_tool(
                "aoa_session_graphrag_packet",
                {"query": "aoa-session-memory-mcp", "anchor": "aoa-session-memory-mcp", "limit": 5},
            )
            explain = await session.call_tool(
                "aoa_session_explain_graph_packet",
                {"intent": "debug aoa-session-memory-mcp", "anchor": "aoa-session-memory-mcp", "limit": 5},
            )
            quality = await session.call_tool(
                "aoa_session_graph_quality_audit",
                {"anchors": ["mcp:aoa-session-memory-mcp", "tool:apply_patch"], "limit": 3, "sample_ref_limit": 1},
            )
            status_payload = json.loads(status.content[0].text)
            trace_payload = json.loads(trace.content[0].text)
            route_payload = json.loads(route.content[0].text)
            evidence_payload = json.loads(evidence.content[0].text)
            brief_payload = json.loads(brief.content[0].text)
            skill_inventory_payload = json.loads(skill_inventory.content[0].text)
            graph_payload = json.loads(graph.content[0].text)
            graphrag_payload = json.loads(graphrag.content[0].text)
            explain_payload = json.loads(explain.content[0].text)
            quality_payload = json.loads(quality.content[0].text)
    graph_ref_count = evidence_ref_count(graph_payload)
    graphrag_ref_count = evidence_ref_count(graphrag_payload)
    explain_ref_count = evidence_ref_count(explain_payload)
    ready_count = quality_ready_count(quality_payload)
    errors: list[str] = []
    if missing_tools:
        errors.append(f"missing tools: {', '.join(missing_tools)}")
    if status_payload.get("ok") is not True or status_payload.get("mutates") is not False:
        errors.append("aoa_session_memory_status did not report ready read-only posture")
    if status_payload.get("provider", {}).get("ok") is not True:
        errors.append("aoa_session_memory_status provider is not ready")
    if not status_payload.get("atlas", {}).get("root_index_exists"):
        errors.append("aoa_session_memory_status did not find atlas root index")
    mutation_posture = status_payload.get("authority_boundary", {}).get("mutation_posture")
    if not isinstance(mutation_posture, str) or not mutation_posture.startswith("no write"):
        errors.append("aoa_session_memory_status lost no-write authority boundary")
    route_candidates = trace_payload.get("route_candidates") or trace_payload.get("candidates") or []
    if not route_candidates and not trace_payload.get("results"):
        errors.append("aoa_session_trace returned no route candidates or evidence results")
    if int(route_payload.get("match_count") or 0) < 1:
        errors.append("aoa_session_route(by-mcp) returned no MCP route entry")
    if not evidence_payload.get("search_hits") and not evidence_payload.get("route_traces"):
        errors.append("aoa_session_evidence_packet returned no evidence handles")
    if not brief_payload.get("session"):
        errors.append("aoa_session_brief(latest) returned no session brief")
    if skill_inventory_payload.get("ok") is not True:
        errors.append("aoa_session_entity_inventory(skill) did not report ok")
    if skill_inventory_payload.get("layer") != "skill":
        errors.append("aoa_session_entity_inventory(skill) returned the wrong layer")
    if int(skill_inventory_payload.get("entity_count") or 0) < 1:
        errors.append("aoa_session_entity_inventory(skill) returned no skill entities")
    if graph_ref_count < 1:
        errors.append("aoa_session_graph_neighborhood returned no evidence refs")
    if graphrag_ref_count < 1:
        errors.append("aoa_session_graphrag_packet returned no evidence refs")
    if explain_ref_count < 1:
        errors.append("aoa_session_explain_graph_packet returned no evidence refs")
    if quality_payload.get("ok") is not True or ready_count < 1:
        errors.append("aoa_session_graph_quality_audit returned no verdict-ready graph samples")
    return {
        "schema": "8dionysus_aoa_session_memory_mcp_smoke_v1",
        "ok": not errors,
        "workspace_root": str(workspace_root),
        "tools": sorted(tools),
        "provider_ok": status_payload.get("provider", {}).get("ok"),
        "atlas_entry_count": status_payload.get("atlas", {}).get("entry_count"),
        "mutation_posture": mutation_posture,
        "trace_candidate_count": len(route_candidates),
        "route_match_count": route_payload.get("match_count"),
        "evidence_search_hits": len(evidence_payload.get("search_hits", [])),
        "skill_inventory_entity_count": skill_inventory_payload.get("entity_count"),
        "skill_inventory_source": skill_inventory_payload.get("source"),
        "graph_evidence_refs": graph_ref_count,
        "graphrag_evidence_refs": graphrag_ref_count,
        "graph_explain_evidence_refs": explain_ref_count,
        "graph_quality_ready_count": ready_count,
        "latest_session": brief_payload.get("session", {}).get("label")
        or brief_payload.get("session", {}).get("session_label")
        or brief_payload.get("session", {}).get("session_id"),
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
