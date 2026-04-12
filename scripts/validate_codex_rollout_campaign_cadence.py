#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def validate_example(schema_path: str, example_path: str) -> dict[str, object]:
    schema = load_json(schema_path)
    example = load_json(example_path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(example), key=lambda error: list(error.absolute_path))
    if errors:
        first = errors[0]
        path = "".join(
            f"[{part}]" if isinstance(part, int) else f".{part}" for part in first.absolute_path
        ).lstrip(".")
        location = f"{example_path}:{path}" if path else example_path
        raise ValueError(f"{location}: {first.message}")
    return example


def validate_codex_rollout_campaign_cadence() -> None:
    campaign = validate_example(
        "schemas/rollout_campaign_window_v1.json",
        "examples/rollout_campaign_window.example.json",
    )
    review = validate_example(
        "schemas/drift_review_window_v1.json",
        "examples/drift_review_window.example.json",
    )
    rollback = validate_example(
        "schemas/rollback_followthrough_window_v1.json",
        "examples/rollback_followthrough_window.example.json",
    )
    latest = load_json("generated/codex/rollout/rollout_latest.min.json")

    campaign_ref = campaign["campaign_ref"]
    if review["campaign_ref"] != campaign_ref:
        raise ValueError("drift review window must point to the campaign window ref")
    if rollback["campaign_ref"] != campaign_ref:
        raise ValueError("rollback followthrough window must point to the campaign window ref")

    rollout_refs = campaign["rollout_campaign_refs"]
    if campaign["latest_rollout_campaign_ref"] not in rollout_refs:
        raise ValueError("campaign latest_rollout_campaign_ref must be included in rollout_campaign_refs")
    if campaign["latest_stable_rollout_campaign_ref"] not in rollout_refs:
        raise ValueError("campaign latest_stable_rollout_campaign_ref must be included in rollout_campaign_refs")
    if campaign["latest_rollout_campaign_ref"] != latest["latest_rollout_campaign_ref"]:
        raise ValueError("campaign latest_rollout_campaign_ref must match rollout_latest.min.json")
    if campaign["latest_stable_rollout_campaign_ref"] != latest["latest_stable_rollout_campaign_ref"]:
        raise ValueError("campaign latest_stable_rollout_campaign_ref must match rollout_latest.min.json")
    if review["rollback_anchor"] != campaign["latest_stable_rollout_campaign_ref"]:
        raise ValueError("drift review rollback_anchor must point to the last stable rollout campaign")
    if rollback["rollback_anchor"] != campaign["latest_stable_rollout_campaign_ref"]:
        raise ValueError("rollback followthrough anchor must point to the last stable rollout campaign")

    signals = review["signals"]
    if not any(bool(signals[name]) for name in signals):
        raise ValueError("drift review window must name at least one positive drift signal")
    if review["decision"] == "reanchor_then_regenerate" and review["status"] not in {
        "review_required",
        "reanchor",
    }:
        raise ValueError("reanchor_then_regenerate decision requires review_required or reanchor status")
    if rollback["status"] == "ready_if_needed" and rollback["post_rollback_review"] != "required":
        raise ValueError("ready_if_needed rollback windows must keep post_rollback_review=required")
    if campaign["state"] != "open" and review["status"] != "closed":
        raise ValueError("non-open campaign windows should not keep an open drift review posture")


def main() -> int:
    validate_codex_rollout_campaign_cadence()
    print("[ok] validated codex rollout campaign cadence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
