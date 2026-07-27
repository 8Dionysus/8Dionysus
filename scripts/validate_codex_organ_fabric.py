#!/usr/bin/env python3
"""Validate the checked-in deny-by-default Codex organ-fabric projection."""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

import render_codex_organ_fabric as organ_fabric


def validate(repo_root: Path) -> dict[str, object]:
    root = repo_root.expanduser().resolve()
    manifest_path = (
        root
        / "config"
        / "codex_plane"
        / "organ_fabric"
        / "codex_consumer_manifest.v1.json"
    )
    observation_path = (
        root
        / "config"
        / "codex_plane"
        / "organ_fabric"
        / "current_consumer_observation.public.json"
    )
    config_path = (
        root / "config" / "codex_plane" / "organ_fabric" / "generated" / "core-read.target.toml"
    )
    plan_path = (
        root / "config" / "codex_plane" / "organ_fabric" / "generated" / "core-read.plan.json"
    )

    manifest = organ_fabric.load_json_object(manifest_path)
    observation = organ_fabric.load_json_object(observation_path)
    plan, rendered = organ_fabric.derive(manifest, observation, "core-read")
    actual_rendered = config_path.read_text(encoding="utf-8")
    actual_plan = organ_fabric.load_json_object(plan_path)

    if rendered != actual_rendered:
        raise ValueError("generated core-read TOML drift; rerun render_codex_organ_fabric.py")
    if plan != actual_plan:
        raise ValueError("generated core-read plan drift; rerun render_codex_organ_fabric.py")
    if plan["rendered_registration_count"] != 0 or plan["mutation_allowed"]:
        raise ValueError("current source posture must render zero registrations and deny mutation")

    action_counts = Counter(action["action"] for action in plan["actions"])
    if action_counts != {
        "retain_legacy_until_replacement_gates": 9,
        "withhold": 9,
    }:
        raise ValueError(f"unexpected current action distribution: {dict(action_counts)}")

    baseline = manifest["catalog_policy"]["legacy_baseline"]
    expected_baseline = {
        "active_server_count": 10,
        "active_tool_count": 118,
        "active_tool_catalog_bytes": 74098,
        "source_digest": (
            "sha256:1caab18801716c002647f32f3c6d48fd"
            "6770d6ed2c1cdfe05832c1b698b59553"
        ),
    }
    for key, expected in expected_baseline.items():
        if baseline[key] != expected:
            raise ValueError(f"legacy baseline drift at {key}")

    registrations = manifest["registrations"]
    for registration in registrations:
        if registration["expected_schema_digest"] is not None:
            raise ValueError("current source manifest must not invent schema admission digests")
        if any(value is not None for value in registration["receipts"].values()):
            raise ValueError("current source manifest must not invent admission receipts")
        if registration.get("removal_receipt") is not None:
            raise ValueError("current source manifest must not invent removal receipts")
        if registration["bearer_token_env_var"] == organ_fabric.LEGACY_SHARED_BEARER_ENV:
            raise ValueError("target manifest reuses the legacy shared bearer environment")

    tos = next(item for item in registrations if item["registration_name"] == "tos_corpus")
    if tos["registry_state"] != "suspended":
        raise ValueError("Tree of Sophia corpus contour must remain suspended")
    observed = observation["effective_registrations"]
    if len(observed) != 9:
        raise ValueError("public observation must retain the nine effective legacy registrations")
    if any(
        item["bearer_token_env_var"] != organ_fabric.LEGACY_SHARED_BEARER_ENV
        for item in observed
    ):
        raise ValueError("legacy observation no longer matches the captured shared-auth baseline")

    return {
        "profile": plan["profile"],
        "registrations_in_manifest": len(registrations),
        "observed_legacy_registrations": len(observed),
        "rendered_registrations": plan["rendered_registration_count"],
        "mutation_allowed": plan["mutation_allowed"],
        "plan_digest": plan["plan_digest"],
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    summary = validate(parse_args(argv).repo_root)
    print("codex organ fabric: OK")
    for key, value in summary.items():
        print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    print("validation_scope=checked_in_source_only")
    print("live_config_compared=false")
    print("live_mutation_performed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
