#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ROLLOUT_ROOT = REPO_ROOT / "generated" / "codex" / "rollout"
DEPLOY_HISTORY_PATH = ROLLOUT_ROOT / "deploy_history.jsonl"
REGENERATION_PATH = ROLLOUT_ROOT / "regeneration_campaigns.min.json"
ROLLBACK_PATH = ROLLOUT_ROOT / "rollback_windows.min.json"
LATEST_PATH = ROLLOUT_ROOT / "rollout_latest.min.json"
ROLLOUT_REF_RE = re.compile(r"^ROLL-\d{8}-[a-z0-9-]+-\d{2}$")
DEPLOY_REF_RE = re.compile(r"^DEPLOY-\d{8}-[a-z0-9-]+-\d{2}$")
DRIFT_REF_RE = re.compile(r"^DRIFT-\d{8}-[a-z0-9-]+-\d{2}$")
ROLLBACK_REF_RE = re.compile(r"^RBK-\d{8}-[a-z0-9-]+-\d{2}$")
ALLOWED_ROLLOUT_STATES = {
    "prepared",
    "activated",
    "monitoring",
    "stabilized",
    "rollback_open",
    "rolled_back",
    "abandoned",
}
ALLOWED_DRIFT_STATES = {
    "quiet",
    "watch",
    "material",
    "repairing",
    "resolved",
    "rolled_back",
}


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        payload = json.loads(line)
        if not isinstance(payload, dict):
            raise ValueError(f"{path.relative_to(REPO_ROOT).as_posix()}:{line_number} must be a JSON object")
        rows.append(payload)
    return rows


def require_match(pattern: re.Pattern[str], value: object, label: str) -> str:
    if not isinstance(value, str) or not pattern.match(value):
        raise ValueError(f"{label} must match {pattern.pattern}")
    return value


def suffix_after_prefix(value: str) -> str:
    return value.split("-", 1)[1]


def require_string_list(value: object, label: str, pattern: re.Pattern[str]) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} must be a non-empty list")
    normalized: list[str] = []
    for index, item in enumerate(value):
        normalized.append(require_match(pattern, item, f"{label}[{index}]"))
    return normalized


def validate_codex_trusted_rollout_operations() -> None:
    deploy_history = load_jsonl(DEPLOY_HISTORY_PATH)
    regeneration = load_json(REGENERATION_PATH)
    rollback = load_json(ROLLBACK_PATH)
    latest = load_json(LATEST_PATH)

    if not deploy_history:
        raise ValueError("generated/codex/rollout/deploy_history.jsonl must not be empty")

    campaigns_from_history: list[str] = []
    for index, row in enumerate(deploy_history):
        location = f"deploy_history[{index}]"
        if row.get("schema_version") != "8dionysus_codex_trusted_rollout_entry_v1":
            raise ValueError(f"{location}.schema_version must stay 8dionysus_codex_trusted_rollout_entry_v1")
        rollout_campaign_ref = require_match(
            ROLLOUT_REF_RE,
            row.get("rollout_campaign_ref"),
            f"{location}.rollout_campaign_ref",
        )
        deploy_receipt_refs = require_string_list(
            row.get("deploy_receipt_refs"),
            f"{location}.deploy_receipt_refs",
            DEPLOY_REF_RE,
        )
        drift_window_refs = require_string_list(
            row.get("drift_window_refs"),
            f"{location}.drift_window_refs",
            DRIFT_REF_RE,
        )
        rollback_window_refs = row.get("rollback_window_refs")
        if not isinstance(rollback_window_refs, list):
            raise ValueError(f"{location}.rollback_window_refs must be a list")
        normalized_rollback_refs = [
            require_match(ROLLBACK_REF_RE, item, f"{location}.rollback_window_refs[{ref_index}]")
            for ref_index, item in enumerate(rollback_window_refs)
        ]

        state = row.get("state")
        if state not in ALLOWED_ROLLOUT_STATES:
            raise ValueError(f"{location}.state must stay inside the rollout lifecycle vocabulary")
        drift_state = row.get("drift_state")
        if drift_state not in ALLOWED_DRIFT_STATES:
            raise ValueError(f"{location}.drift_state must stay inside the drift lifecycle vocabulary")
        if state in {"rollback_open", "rolled_back"} and not normalized_rollback_refs:
            raise ValueError(
                f"{location}.rollback_window_refs must not be empty for {state} entries"
            )
        if state == "stabilized" and normalized_rollback_refs:
            raise ValueError(f"{location}.rollback_window_refs must stay empty for stabilized entries")

        rollout_suffix = suffix_after_prefix(rollout_campaign_ref)
        for ref in deploy_receipt_refs:
            if suffix_after_prefix(ref) != rollout_suffix:
                raise ValueError(f"{location}.deploy_receipt_refs must keep the rollout suffix {rollout_suffix}")
        for ref in drift_window_refs:
            if suffix_after_prefix(ref) != rollout_suffix:
                raise ValueError(f"{location}.drift_window_refs must keep the rollout suffix {rollout_suffix}")
        for ref in normalized_rollback_refs:
            if suffix_after_prefix(ref) != rollout_suffix:
                raise ValueError(f"{location}.rollback_window_refs must keep the rollout suffix {rollout_suffix}")

        campaigns_from_history.append(rollout_campaign_ref)

    regeneration_campaigns = regeneration.get("campaigns")
    if regeneration.get("schema_version") != "8dionysus_codex_trusted_rollout_campaigns_v1":
        raise ValueError("regeneration_campaigns.min.json must keep its schema_version")
    if regeneration.get("owner_repo") != "8Dionysus":
        raise ValueError("regeneration_campaigns.min.json must stay owned by 8Dionysus")
    if not isinstance(regeneration_campaigns, list) or not regeneration_campaigns:
        raise ValueError("regeneration_campaigns.min.json must expose a non-empty campaigns list")
    normalized_regeneration_campaigns: list[str] = []
    for index, item in enumerate(regeneration_campaigns):
        if not isinstance(item, dict):
            raise ValueError(f"regeneration_campaigns.min.json.campaigns[{index}] must be an object")
        normalized_regeneration_campaigns.append(
            require_match(
                ROLLOUT_REF_RE,
                item.get("rollout_campaign_ref"),
                f"regeneration_campaigns.min.json.campaigns[{index}].rollout_campaign_ref",
            )
        )
    if sorted(normalized_regeneration_campaigns) != sorted(campaigns_from_history):
        raise ValueError("regeneration campaigns must cover exactly the rollout campaign refs from deploy history")

    rollback_windows = rollback.get("rollback_windows")
    if rollback.get("schema_version") != "8dionysus_codex_trusted_rollback_windows_v1":
        raise ValueError("rollback_windows.min.json must keep its schema_version")
    if rollback.get("owner_repo") != "8Dionysus":
        raise ValueError("rollback_windows.min.json must stay owned by 8Dionysus")
    if not isinstance(rollback_windows, list):
        raise ValueError("rollback_windows.min.json must expose a rollback_windows list")
    rollback_refs = {
        require_match(ROLLBACK_REF_RE, item.get("rollback_window_ref"), "rollback.rollback_window_ref")
        for item in rollback_windows
        if isinstance(item, dict)
    }
    history_rollback_refs = {
        ref
        for row in deploy_history
        for ref in row.get("rollback_window_refs", [])
        if isinstance(ref, str)
    }
    if rollback_refs != history_rollback_refs:
        raise ValueError("rollback_windows.min.json must cover exactly the rollback refs named by deploy history")

    if latest.get("schema_version") != "8dionysus_codex_trusted_rollout_latest_v1":
        raise ValueError("rollout_latest.min.json must keep its schema_version")
    if latest.get("owner_repo") != "8Dionysus":
        raise ValueError("rollout_latest.min.json must stay owned by 8Dionysus")
    latest_rollout_campaign_ref = require_match(
        ROLLOUT_REF_RE,
        latest.get("latest_rollout_campaign_ref"),
        "rollout_latest.min.json.latest_rollout_campaign_ref",
    )
    if latest_rollout_campaign_ref != deploy_history[-1]["rollout_campaign_ref"]:
        raise ValueError("rollout_latest.min.json must point to the latest deploy-history entry")
    if latest.get("latest_state") != deploy_history[-1]["state"]:
        raise ValueError("rollout_latest.min.json.latest_state must match the latest deploy-history state")
    latest_stable_ref = require_match(
        ROLLOUT_REF_RE,
        latest.get("latest_stable_rollout_campaign_ref"),
        "rollout_latest.min.json.latest_stable_rollout_campaign_ref",
    )
    stable_refs = {
        str(row["rollout_campaign_ref"])
        for row in deploy_history
        if row.get("state") == "stabilized"
    }
    if latest_stable_ref not in stable_refs:
        raise ValueError("rollout_latest.min.json latest_stable_rollout_campaign_ref must resolve to a stabilized campaign")
    if latest.get("source_refs") != [
        "generated/codex/rollout/deploy_history.jsonl",
        "generated/codex/rollout/regeneration_campaigns.min.json",
        "generated/codex/rollout/rollback_windows.min.json",
    ]:
        raise ValueError("rollout_latest.min.json must keep the canonical source_refs order")


def main() -> int:
    validate_codex_trusted_rollout_operations()
    print("[ok] validated codex trusted rollout operations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
