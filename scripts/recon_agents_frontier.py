#!/usr/bin/env python3
"""Rank the next AGENTS.md frontier from an AGENTS map payload.

The script is intentionally local-only. It reads `generated/agents_map.min.json`
or another supplied map file and turns remaining high-risk directories and
validator signals into a prioritized reconnaissance report.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

SCHEMA_VERSION = "8dionysus_agents_frontier_recon_v1"
SCHEMA_REF = "schemas/agents-frontier-recon.schema.json"
DEFAULT_MAP_PATH = Path("generated/agents_map.min.json")


@dataclass(frozen=True)
class DirectoryRule:
    base_score: int
    label: str
    default_decision: str
    rationale: str


DIRECTORY_RULES: dict[str, DirectoryRule] = {
    ".agents": DirectoryRule(96, "P0", "add-local-agents", "agent-facing projection surfaces can silently steer tools"),
    ".codex": DirectoryRule(96, "P0", "add-local-agents", "Codex-plane helpers and projections need local source/installed-copy boundaries"),
    "schemas": DirectoryRule(94, "P0", "add-local-agents", "schema edits are contract edits"),
    "scripts": DirectoryRule(92, "P0", "add-local-agents", "scripts can mutate, generate, validate, or route other surfaces"),
    "systemd": DirectoryRule(90, "P0", "add-local-agents", "service units can affect runtime lifecycle"),
    "githooks": DirectoryRule(88, "P0", "add-local-agents", "hooks can change local developer behavior"),
    ".github": DirectoryRule(84, "P1", "inspect-then-add", "platform automation and workflow metadata are public contracts"),
    "generated": DirectoryRule(80, "P1", "inspect-then-add", "generated outputs should remain evidence, not authority"),
    "config": DirectoryRule(78, "P1", "inspect-then-add", "configuration can shift policy and generation behavior"),
    "manifests": DirectoryRule(76, "P1", "inspect-then-add", "manifests can become hidden coordination contracts"),
    "manifests/recurrence": DirectoryRule(76, "P1", "inspect-then-add", "recurrence hints can overgrow into undeclared obligations"),
    "seed_staging": DirectoryRule(76, "P1", "inspect-then-add", "staging must not overrule opened waves or owner-repo truth"),
    "seed_notes": DirectoryRule(72, "P1", "inspect-then-add", "seed notes need provenance and owner-routing boundaries"),
    "src": DirectoryRule(74, "P1", "inspect-then-add", "source modules often encode executable or importable behavior"),
    "tests": DirectoryRule(70, "P1", "inspect-then-add", "tests define what drift is caught"),
    "quests": DirectoryRule(66, "P2", "inspect-first", "quest language must stay evidence-linked and bounded"),
    "playbooks": DirectoryRule(64, "P2", "inspect-first", "scenario surfaces can blur into execution or proof contracts"),
    "skills": DirectoryRule(64, "P2", "inspect-first", "skill-facing surfaces need bounded execution clarity"),
    "docs": DirectoryRule(58, "P2", "inspect-first", "docs may carry doctrine, but many docs do not need local law"),
    "examples": DirectoryRule(54, "P2", "inspect-first", "examples need public-safety and source-sync boundaries"),
    "templates": DirectoryRule(52, "P2", "inspect-first", "templates can replicate mistakes at scale"),
    "reports": DirectoryRule(50, "P2", "inspect-first", "reports should stay diagnostic and non-sovereign"),
    "profile": DirectoryRule(48, "P3", "watch", "profile surfaces are usually orientation unless they start carrying rules"),
    "env": DirectoryRule(46, "P3", "watch", "env examples matter, but prior packs may already guard them"),
    "compose": DirectoryRule(46, "P3", "watch", "compose usually needs guards only when runtime-owned"),
    "bundles": DirectoryRule(42, "P3", "watch", "bundles are often transport surfaces"),
}

KIND_BOOSTS: dict[str, int] = {
    "runtime-infrastructure": 14,
    "operator-companion": 12,
    "control-plane-sdk": 10,
    "seed-garden": 9,
    "public-route-map": 8,
    "constitutional-center": 8,
    "knowledge-root": 7,
    "agent-role-layer": 6,
    "scenario-composition": 6,
    "evaluation-layer": 5,
    "skill-canon": 5,
    "technique-canon": 5,
    "memory-layer": 4,
    "routing-layer": 4,
    "knowledge-substrate": 4,
    "derived-observability": 3,
}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _dir_key(path: str) -> str:
    cleaned = path.strip("/")
    if cleaned in DIRECTORY_RULES:
        return cleaned
    parts = cleaned.split("/")
    if len(parts) >= 2 and "/".join(parts[:2]) in DIRECTORY_RULES:
        return "/".join(parts[:2])
    return parts[0] if parts else cleaned


def _priority_label(score: int) -> str:
    if score >= 90:
        return "P0"
    if score >= 72:
        return "P1"
    if score >= 52:
        return "P2"
    return "P3"


def _decision(label: str, default: str) -> str:
    if label == "P0":
        return "add-local-agents"
    if label == "P1":
        return default if default != "watch" else "inspect-then-add"
    if label == "P2":
        return "inspect-first"
    return "watch"


def candidate_for(repo: Mapping[str, Any], rel_dir: str) -> dict[str, Any]:
    kind = str(repo.get("kind", ""))
    rule = DIRECTORY_RULES.get(_dir_key(rel_dir), DirectoryRule(40, "P3", "watch", "unclassified high-risk directory"))
    score = rule.base_score + KIND_BOOSTS.get(kind, 0)
    if not repo.get("validator_present"):
        score += 10
    if _as_list(repo.get("missing_required_agents")):
        score += 8
    if _as_list(repo.get("invalid_heading_agents")):
        score += 4
    label = _priority_label(score)
    return {
        "repository": repo.get("name", "unknown"),
        "repository_kind": kind or "unknown",
        "path": rel_dir.rstrip("/") + "/AGENTS.md",
        "directory": rel_dir.rstrip("/"),
        "priority": label,
        "score": score,
        "decision": _decision(label, rule.default_decision),
        "rationale": rule.rationale,
    }


def build_frontier(payload: Mapping[str, Any], *, max_candidates: int | None = None) -> dict[str, Any]:
    repositories = _as_list(payload.get("repositories"))
    repo_reports: list[dict[str, Any]] = []
    all_candidates: list[dict[str, Any]] = []

    for repo in repositories:
        if not isinstance(repo, Mapping):
            continue
        missing_dirs = [str(item) for item in _as_list(repo.get("high_risk_dirs_without_agents"))]
        candidates = [candidate_for(repo, rel_dir) for rel_dir in missing_dirs]
        candidates.sort(key=lambda item: (-int(item["score"]), item["repository"], item["directory"]))
        all_candidates.extend(candidates)
        repo_reports.append(
            {
                "name": repo.get("name", "unknown"),
                "kind": repo.get("kind", "unknown"),
                "checkout_state": repo.get("checkout_state", "unknown"),
                "validator_present": bool(repo.get("validator_present", False)),
                "nested_validators_present": int(repo.get("nested_validators_present", 1 if repo.get("validator_present") else 0) or 0),
                "semantic_validators_present": int(repo.get("semantic_validators_present", 0) or 0),
                "missing_required_agents": _as_list(repo.get("missing_required_agents")),
                "unvalidated_by_any_agents_validator": _as_list(
                    repo.get("unvalidated_by_any_agents_validator", repo.get("unvalidated_nested_agents", []))
                ),
                "not_in_nested_validator_map": _as_list(repo.get("not_in_nested_validator_map", repo.get("unvalidated_nested_agents", []))),
                "invalid_heading_agents": _as_list(repo.get("invalid_heading_agents")),
                "non_canonical_heading_agents": _as_list(repo.get("non_canonical_heading_agents")),
                "candidate_count": len(candidates),
                "top_candidates": candidates[:5],
            }
        )

    all_candidates.sort(key=lambda item: (-int(item["score"]), item["repository"], item["directory"]))
    if max_candidates is not None:
        all_candidates = all_candidates[:max_candidates]

    totals = {
        "repositories_listed": len(repo_reports),
        "candidate_count": sum(report["candidate_count"] for report in repo_reports),
        "p0_candidates": sum(1 for item in all_candidates if item["priority"] == "P0"),
        "p1_candidates": sum(1 for item in all_candidates if item["priority"] == "P1"),
        "p2_candidates": sum(1 for item in all_candidates if item["priority"] == "P2"),
        "p3_candidates": sum(1 for item in all_candidates if item["priority"] == "P3"),
        "repos_with_candidates": sum(1 for report in repo_reports if report["candidate_count"]),
    }

    return {
        "schema_version": SCHEMA_VERSION,
        "schema_ref": SCHEMA_REF,
        "surface_kind": "agents_frontier_recon",
        "generated_by": "scripts/recon_agents_frontier.py",
        "source_map_schema_version": payload.get("schema_version", "unknown"),
        "source_map_audit_mode": payload.get("audit_mode", "unknown"),
        "totals": totals,
        "top_candidates": all_candidates,
        "repositories": repo_reports,
        "reading_notes": [
            "P0 means add or validate a local AGENTS.md before the next broad refactor.",
            "P1 means inspect and usually add local guidance if the directory carries contracts, generation, runtime, or projection behavior.",
            "P2 means inspect first; many docs/examples/templates do not need new AGENTS.md if existing local guidance already routes them well.",
            "P3 means watch unless the directory starts carrying active rules or risky automation.",
        ],
    }


def render_markdown(payload: Mapping[str, Any]) -> str:
    totals = payload.get("totals", {})
    top_candidates = _as_list(payload.get("top_candidates"))
    lines = [
        "# AGENTS frontier reconnaissance",
        "",
        "This report ranks remaining high-risk directories that may need local `AGENTS.md` guidance.",
        "It is a reconnaissance surface, not repository doctrine, and it does not overrule the nearest `AGENTS.md`.",
        "",
        "## Totals",
        "",
    ]
    for key in sorted(totals):
        lines.append(f"- `{key}`: {totals[key]}")
    lines.extend(["", "## Top candidates", ""])
    if not top_candidates:
        lines.append("No frontier candidates were found in the supplied map.")
    else:
        lines.append("| Priority | Score | Repository | Path | Decision | Rationale |")
        lines.append("|---|---:|---|---|---|---|")
        for item in top_candidates[:40]:
            lines.append(
                "| {priority} | {score} | `{repository}` | `{path}` | `{decision}` | {rationale} |".format(
                    priority=item.get("priority", ""),
                    score=item.get("score", ""),
                    repository=item.get("repository", ""),
                    path=item.get("path", ""),
                    decision=item.get("decision", ""),
                    rationale=item.get("rationale", ""),
                )
            )
    lines.extend(
        [
            "",
            "## How to use",
            "",
            "1. Start with P0 candidates that are both present and genuinely local-risk bearing.",
            "2. Do not add `AGENTS.md` just to quiet a metric; add it only where it prevents a realistic agent mistake.",
            "3. After landing local guidance, promote it into the owning validator map.",
            "4. Regenerate `generated/agents_map.min.json` and this frontier report.",
            "",
        ]
    )
    return "\n".join(lines)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")


def write_markdown(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(payload), encoding="utf-8")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map", type=Path, default=DEFAULT_MAP_PATH, help="Path to generated/agents_map.min.json")
    parser.add_argument("--write", type=Path, help="Write compact frontier JSON to this path")
    parser.add_argument("--markdown", type=Path, help="Write a markdown frontier report to this path")
    parser.add_argument("--max-candidates", type=int, help="Limit top candidates in the JSON output")
    parser.add_argument("--pretty", action="store_true", help="Print pretty JSON when not writing files")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    payload = read_json(args.map)
    frontier = build_frontier(payload, max_candidates=args.max_candidates)
    if args.write:
        write_json(args.write, frontier)
    if args.markdown:
        write_markdown(args.markdown, frontier)
    if not args.write and not args.markdown:
        print(json.dumps(frontier, ensure_ascii=False, sort_keys=True, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
