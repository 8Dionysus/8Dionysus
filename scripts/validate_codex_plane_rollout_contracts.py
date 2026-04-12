#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
STABLE_MCP_NAMES = ["aoa_workspace", "aoa_stats", "dionysus"]


def load_json(relative_path: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def validate_example(schema_path: str, example_path: str) -> dict[str, object]:
    schema = load_json(schema_path)
    example = load_json(example_path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(example), key=lambda error: list(error.absolute_path))
    if errors:
        error = errors[0]
        path = "".join(
            f"[{part}]" if isinstance(part, int) else f".{part}" for part in error.absolute_path
        ).lstrip(".")
        location = f"{example_path}:{path}" if path else example_path
        raise ValueError(f"{location}: {error.message}")
    return example


def validate_codex_plane_rollout_contracts() -> None:
    trust = validate_example(
        "schemas/codex_plane_trust_state_v1.json",
        "examples/codex_plane_trust_state.example.json",
    )
    regeneration = validate_example(
        "schemas/codex_plane_regeneration_report_v1.json",
        "examples/codex_plane_regeneration_report.example.json",
    )
    receipt = validate_example(
        "schemas/codex_plane_rollout_receipt_v1.json",
        "examples/codex_plane_rollout_receipt.example.json",
    )

    expected_names = sorted(STABLE_MCP_NAMES)
    if sorted(trust["mcp_server_names_expected"]) != expected_names:
        raise ValueError("trust-state expected MCP names must match the stable AoA server set")
    if sorted(trust["mcp_server_names_detected"]) != expected_names:
        raise ValueError("trust-state detected MCP names must match the stable AoA server set")
    if trust["stable_names_ok"] is not True:
        raise ValueError("trust-state happy-path example must keep stable_names_ok=true")

    if regeneration["target_workspace_root"] != trust["workspace_root"]:
        raise ValueError("regeneration report target_workspace_root must match trust-state workspace_root")
    stable_names = regeneration["stable_names"]
    if any(stable_names[name] is not True for name in STABLE_MCP_NAMES):
        raise ValueError("regeneration report must preserve all stable MCP names")

    rendered_paths = {
        item["relative_path"] for item in regeneration["rendered_files"] if isinstance(item, dict)
    }
    if ".codex/config.toml" not in rendered_paths or ".codex/hooks.json" not in rendered_paths:
        raise ValueError("regeneration report must include both .codex/config.toml and .codex/hooks.json")

    if receipt["trust_state_id"] != trust["trust_state_id"]:
        raise ValueError("rollout receipt must reference the trust-state example id")
    if receipt["regeneration_report_id"] != regeneration["regeneration_report_id"]:
        raise ValueError("rollout receipt must reference the regeneration report example id")
    if receipt["deployment_state"] == "verified" and receipt["doctor_result"] != "pass":
        raise ValueError("verified rollout example must keep doctor_result=pass")


def main() -> int:
    validate_codex_plane_rollout_contracts()
    print("[ok] validated codex plane rollout contracts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
