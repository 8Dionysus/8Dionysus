#!/usr/bin/env python3
"""Smoke-check the workspace aoa_evals MCP wrapper over stdio."""
from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
from typing import Sequence

REQUIRED_TOOLS = {
    "aoa_evals_comparison",
    "aoa_evals_expand",
    "aoa_evals_find_or_propose",
    "aoa_evals_inspect",
    "aoa_evals_report_skeleton",
    "aoa_evals_runtime_evidence_template",
    "aoa_evals_runtime_candidate_exports",
    "aoa_evals_runtime_status",
    "aoa_evals_select",
    "aoa_evals_read_runtime_candidate_export",
    "aoa_evals_validate_evidence_candidate",
}


def matched_runtime_export(exports_payload: dict[str, object]) -> dict[str, object] | None:
    candidates = exports_payload.get("candidates")
    if not isinstance(candidates, list):
        return None
    for item in candidates:
        if not isinstance(item, dict):
            continue
        validation = item.get("validation")
        matched_eval_refs = validation.get("matched_eval_refs") if isinstance(validation, dict) else None
        if matched_eval_refs and item.get("record_id"):
            return item
    return None


def runtime_walkthrough_summary(
    runtime_walkthrough_payload: dict[str, object] | None,
    runtime_walkthrough_report_payload: dict[str, object] | None,
) -> dict[str, object]:
    if runtime_walkthrough_payload is None:
        return {
            "skipped": True,
            "reason": "no matched runtime candidate export in listing",
        }
    return {
        "skipped": False,
        "outcome": runtime_walkthrough_payload.get("outcome"),
        "proposal_valid": runtime_walkthrough_payload.get("proposal_validation", {}).get("valid"),
        "source_mutation_allowed": runtime_walkthrough_payload.get("source_mutation_allowed"),
        "report_candidate_only": None
        if runtime_walkthrough_report_payload is None
        else runtime_walkthrough_report_payload.get("candidate_only"),
    }


async def run_smoke(workspace_root: Path) -> dict[str, object]:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

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
            proposal = await session.call_tool(
                "aoa_evals_find_or_propose",
                {
                    "proof_question": "bounded change verification runtime evidence",
                    "proposal": {"category": "workflow"},
                },
            )
            inspection = await session.call_tool("aoa_evals_inspect", {"name": first})
            skeleton = await session.call_tool(
                "aoa_evals_report_skeleton",
                {"name": first, "evidence_refs": ["artifact:smoke"]},
            )
            status = await session.call_tool("aoa_evals_runtime_status", {})
            exports = await session.call_tool("aoa_evals_runtime_candidate_exports", {"limit": 3})
            candidate = {
                "surface_type": "runtime_evidence_selection",
                "selection_id": "aoa-evals-mcp-smoke",
                "source_repo": "abyss-stack",
                "source_schema_ref": "repo:8Dionysus/scripts/smoke_aoa_evals_mcp.py",
                "source_manifests": ["local:aoa-evals-mcp-smoke"],
                "bounded_claim": "Smoke-check that aoa_evals validates candidate packet shape only.",
                "promotion_target": "local-only",
                "comparison_mode": "none",
                "target_eval": first,
                "selected_evidence": [
                    {
                        "artifact_ref": "local:aoa-evals-mcp-smoke",
                        "evidence_role": "summary",
                        "summary_only": True,
                    }
                ],
                "environment_invariants": ["stdio MCP smoke only"],
                "do_not_overread": ["does not prove an eval verdict"],
                "review_posture": {
                    "portable_enough": False,
                    "comparison_hygiene_named": True,
                    "human_review_required": True,
                },
            }
            validation = await session.call_tool(
                "aoa_evals_validate_evidence_candidate",
                {"packet": candidate},
            )
            inspection_payload = json.loads(inspection.content[0].text)
            skeleton_payload = json.loads(skeleton.content[0].text)
            status_payload = json.loads(status.content[0].text)
            exports_payload = json.loads(exports.content[0].text)
            validation_payload = json.loads(validation.content[0].text)
            proposal_payload = json.loads(proposal.content[0].text)
            runtime_walkthrough_payload: dict[str, object] | None = None
            runtime_walkthrough_report_payload: dict[str, object] | None = None
            matched_export = matched_runtime_export(exports_payload)
            if matched_export:
                matched_eval = matched_export["validation"]["matched_eval_refs"][0]
                record_id = matched_export["record_id"]
                runtime_walkthrough = await session.call_tool(
                    "aoa_evals_find_or_propose",
                    {
                        "proof_question": f"{matched_eval} runtime candidate export {record_id}",
                        "proposal": {
                            "authoring_route": "candidate_evidence_packet",
                            "category": "boundary",
                            "related_eval_refs": [matched_eval],
                            "candidate_evidence_refs": [f"runtime-candidate-export:{record_id}"],
                        },
                    },
                )
                runtime_walkthrough_report = await session.call_tool(
                    "aoa_evals_report_skeleton",
                    {
                        "name": matched_eval,
                        "evidence_refs": [f"runtime-candidate-export:{record_id}"],
                    },
                )
                runtime_walkthrough_payload = json.loads(runtime_walkthrough.content[0].text)
                runtime_walkthrough_report_payload = json.loads(runtime_walkthrough_report.content[0].text)
            export_read_payload: dict[str, object] | None = None
            if exports_payload.get("candidates"):
                first_export = exports_payload["candidates"][0]
                export_read = await session.call_tool(
                    "aoa_evals_read_runtime_candidate_export",
                    {"record_id": first_export["record_id"]},
                )
                export_read_payload = json.loads(export_read.content[0].text)
    errors: list[str] = []
    if missing_tools:
        errors.append(f"missing tools: {', '.join(missing_tools)}")
    if not selection_payload.get("matches"):
        errors.append("aoa_evals_select returned no bounded candidates")
    if proposal_payload.get("read_only") is not True:
        errors.append("aoa_evals_find_or_propose did not report read_only=true")
    if proposal_payload.get("source_mutation_allowed") is not False:
        errors.append("aoa_evals_find_or_propose allowed source mutation")
    if proposal_payload.get("proposal_validation", {}).get("valid") is not True:
        errors.append("aoa_evals_find_or_propose returned invalid eval_need_v1 context")
    if proposal_payload.get("proposal_context", {}).get("packet", {}).get("schema_version") != "eval_need_v1":
        errors.append("aoa_evals_find_or_propose did not return eval_need_v1 packet context")
    if inspection_payload.get("authority_boundary", {}).get("stronger_owner") != "bundle-local EVAL.md and eval.yaml":
        errors.append("aoa_evals_inspect did not preserve source authority boundary")
    if skeleton_payload.get("sections", {}).get("verdict") != "UNSET: MCP must not compute verdicts":
        errors.append("aoa_evals_report_skeleton did not leave verdict unset")
    if status_payload.get("freshness", {}).get("mirror_is_authority") is not False:
        errors.append("aoa_evals_runtime_status did not preserve mirror boundary")
    if validation_payload.get("valid") is not True:
        errors.append("aoa_evals_validate_evidence_candidate rejected the smoke candidate")
    if exports_payload.get("private_payloads_included") is not False:
        errors.append("aoa_evals_runtime_candidate_exports leaked private payloads in listing")
    if export_read_payload and export_read_payload.get("candidate_payload_included") is not False:
        errors.append("aoa_evals_read_runtime_candidate_export leaked private payload by default")
    if runtime_walkthrough_payload is not None:
        if runtime_walkthrough_payload.get("source_mutation_allowed") is not False:
            errors.append("runtime-to-eval walkthrough allowed source mutation")
        if runtime_walkthrough_payload.get("proposal_validation", {}).get("valid") is not True:
            errors.append("runtime-to-eval walkthrough returned invalid eval_need_v1 context")
        if not runtime_walkthrough_payload.get("runtime_candidate_export_refs"):
            errors.append("runtime-to-eval walkthrough lost runtime candidate export ref")
    if runtime_walkthrough_report_payload is not None:
        if runtime_walkthrough_report_payload.get("candidate_only") is not True:
            errors.append("runtime-to-eval report skeleton is not candidate-only")
        if runtime_walkthrough_report_payload.get("sections", {}).get("verdict") != "UNSET: MCP must not compute verdicts":
            errors.append("runtime-to-eval report skeleton did not leave verdict unset")
    return {
        "schema": "8dionysus_aoa_evals_mcp_smoke_v1",
        "ok": not errors,
        "workspace_root": str(workspace_root),
        "tools": sorted(tools),
        "selected_eval": first,
        "candidate_only": skeleton_payload.get("candidate_only"),
        "find_or_propose_outcome": proposal_payload.get("outcome"),
        "find_or_propose_valid": proposal_payload.get("proposal_validation", {}).get("valid"),
        "find_or_propose_source_mutation_allowed": proposal_payload.get("source_mutation_allowed"),
        "freshness_status": status_payload.get("freshness", {}).get("status"),
        "candidate_validation": validation_payload.get("valid"),
        "runtime_candidate_export_count": exports_payload.get("count"),
        "runtime_candidate_export_validation": None
        if export_read_payload is None
        else export_read_payload.get("validation", {}).get("valid"),
        "runtime_to_eval_walkthrough": runtime_walkthrough_summary(
            runtime_walkthrough_payload,
            runtime_walkthrough_report_payload,
        ),
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
