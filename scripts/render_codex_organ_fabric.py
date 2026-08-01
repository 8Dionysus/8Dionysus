#!/usr/bin/env python3
"""Derive a fail-closed Codex MCP target fragment and change plan.

This renderer is deliberately source-only. It has no apply mode, never reads
credential values, and emits no registration until the entire selected profile
has registry admission plus consumer-schema, central-proof, canary,
owner-acceptance, and rollback receipts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator, FormatChecker

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = (
    REPO_ROOT
    / "config"
    / "codex_plane"
    / "organ_fabric"
    / "codex_consumer_manifest.v1.json"
)
DEFAULT_OBSERVATION = (
    REPO_ROOT
    / "config"
    / "codex_plane"
    / "organ_fabric"
    / "current_consumer_observation.public.json"
)
MANIFEST_SCHEMA = REPO_ROOT / "schemas" / "codex_organ_fabric_manifest_v1.json"
OBSERVATION_SCHEMA = REPO_ROOT / "schemas" / "codex_organ_fabric_observation_v1.json"
PLAN_SCHEMA = REPO_ROOT / "schemas" / "codex_organ_fabric_plan_v1.json"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "config" / "codex_plane" / "organ_fabric" / "generated"

ADMISSION_RECEIPT_KEYS = (
    "admission",
    "consumer_schema",
    "central_proof",
    "canary",
    "owner_acceptance",
    "rollback",
)
RETIRED_STATES = {"suspended", "deprecated", "retired"}
MUTATING_ACTIONS = {"add", "replace", "remove_after_receipt"}
LEGACY_SHARED_BEARER_ENV = "AOA_MCP_HTTP_BEARER_TOKEN"


def load_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object in {path}")
    return payload


def canonical_json_bytes(payload: Mapping[str, Any]) -> bytes:
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def canonical_digest(payload: Mapping[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def _schema_error(path: Path, error: Any) -> ValueError:
    location = ".".join(str(part) for part in error.absolute_path) or "<root>"
    return ValueError(f"{path.name}:{location}: {error.message}")


def validate_json_schema(payload: Mapping[str, Any], schema_path: Path) -> None:
    schema = load_json_object(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(payload), key=lambda item: list(item.absolute_path))
    if errors:
        raise _schema_error(schema_path, errors[0])


def admission_ready(registration: Mapping[str, Any]) -> bool:
    receipts = registration["receipts"]
    return (
        registration["registry_state"] == "admitted"
        and isinstance(registration["expected_schema_digest"], str)
        and all(isinstance(receipts[key], str) and receipts[key] for key in ADMISSION_RECEIPT_KEYS)
    )


def _duplicates(values: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def validate_manifest(manifest: Mapping[str, Any]) -> None:
    validate_json_schema(manifest, MANIFEST_SCHEMA)
    registrations = manifest["registrations"]
    profiles = manifest["profiles"]
    policy = manifest["catalog_policy"]

    for field in ("registration_name", "url", "bearer_token_env_var", "credential_class"):
        duplicates = _duplicates([str(registration[field]) for registration in registrations])
        if duplicates:
            raise ValueError(f"duplicate {field}: {', '.join(duplicates)}")

    for registration in registrations:
        name = registration["registration_name"]
        if registration["bearer_token_env_var"] == LEGACY_SHARED_BEARER_ENV:
            raise ValueError(f"{name}: shared legacy bearer environment is forbidden")
        if manifest["production_protocol"] not in registration["protocol_versions"]:
            raise ValueError(f"{name}: production protocol is not explicitly supported")
        if registration["policy_family"] == "read":
            if registration["default_tools_approval_mode"] != "writes":
                raise ValueError(f"{name}: read contour must use writes approval mode")
            if registration["effect_ceiling"] == "prepare_candidate":
                raise ValueError(f"{name}: read contour cannot prepare candidates")
        else:
            if registration["default_tools_approval_mode"] != "prompt":
                raise ValueError(f"{name}: candidate contour must use prompt approval mode")
            if registration["effect_ceiling"] != "prepare_candidate":
                raise ValueError(f"{name}: candidate contour has an invalid effect ceiling")
        if registration["registry_state"] == "admitted" and not admission_ready(registration):
            raise ValueError(f"{name}: admitted state is missing schema or six required receipts")
        for profile_name in registration["profiles"]:
            if profile_name not in profiles:
                raise ValueError(f"{name}: unknown profile {profile_name}")
            allowed = profiles[profile_name]["allowed_policy_families"]
            if registration["policy_family"] not in allowed:
                raise ValueError(
                    f"{name}: policy family {registration['policy_family']} is not allowed "
                    f"by profile {profile_name}"
                )

    max_registrations = policy["max_registrations_per_profile"]
    max_tools = policy["max_enabled_tools_per_profile"]
    for profile_name in profiles:
        selected = [
            registration
            for registration in registrations
            if profile_name in registration["profiles"]
        ]
        tool_count = sum(len(registration["enabled_tools"]) for registration in selected)
        if len(selected) > max_registrations:
            raise ValueError(
                f"{profile_name}: registration budget exceeded "
                f"({len(selected)} > {max_registrations})"
            )
        if tool_count > max_tools:
            raise ValueError(f"{profile_name}: tool budget exceeded ({tool_count} > {max_tools})")


def validate_observation(observation: Mapping[str, Any]) -> None:
    validate_json_schema(observation, OBSERVATION_SCHEMA)
    names = [
        str(registration["registration_name"])
        for registration in observation["effective_registrations"]
    ]
    duplicates = _duplicates(names)
    if duplicates:
        raise ValueError(f"duplicate observed registration_name: {', '.join(duplicates)}")
    if observation["observed_at"] >= observation["expires_at"]:
        raise ValueError("observation expires_at must be later than observed_at")


def registration_matches_observation(
    registration: Mapping[str, Any],
    observed: Mapping[str, Any],
) -> bool:
    return (
        registration["url"] == observed["url"]
        and registration["bearer_token_env_var"] == observed["bearer_token_env_var"]
        and registration["enabled_tools"] == observed["enabled_tools"]
        and registration["startup_timeout_sec"] == observed["startup_timeout_sec"]
        and registration["tool_timeout_sec"] == observed["tool_timeout_sec"]
        and registration["expected_schema_digest"] == observed["schema_digest"]
    )


def _action(name: str, action: str, *reason_codes: str) -> dict[str, Any]:
    return {
        "registration_name": name,
        "action": action,
        "reason_codes": list(reason_codes),
    }


def build_plan(
    manifest: Mapping[str, Any],
    observation: Mapping[str, Any],
    profile_name: str,
) -> dict[str, Any]:
    validate_manifest(manifest)
    validate_observation(observation)
    if profile_name not in manifest["profiles"]:
        raise ValueError(f"unknown profile: {profile_name}")

    registrations = manifest["registrations"]
    by_name = {registration["registration_name"]: registration for registration in registrations}
    observed_by_name = {
        registration["registration_name"]: registration
        for registration in observation["effective_registrations"]
    }
    selected = [
        registration
        for registration in registrations
        if profile_name in registration["profiles"]
    ]
    selected_names = {registration["registration_name"] for registration in selected}
    profile_ready = bool(selected) and all(admission_ready(registration) for registration in selected)
    renderable = selected if profile_ready else []

    actions: list[dict[str, Any]] = []
    blockers: list[str] = []
    for registration in registrations:
        name = registration["registration_name"]
        observed = observed_by_name.get(name)
        state = registration["registry_state"]

        if state in RETIRED_STATES:
            if observed is None:
                actions.append(_action(name, "withhold", f"registry_state_{state}"))
            elif registration.get("removal_receipt"):
                actions.append(
                    _action(name, "remove_after_receipt", f"registry_state_{state}", "removal_receipt")
                )
            else:
                actions.append(
                    _action(
                        name,
                        "retain_legacy_until_replacement_gates",
                        f"registry_state_{state}",
                        "removal_receipt_missing",
                    )
                )
                blockers.append(f"{name}: removal receipt missing")
            continue

        if name in selected_names and admission_ready(registration):
            if observed is None:
                actions.append(_action(name, "add", "selected_profile", "admission_gates_complete"))
            elif registration_matches_observation(registration, observed):
                actions.append(
                    _action(name, "retain_exact", "selected_profile", "target_exactly_observed")
                )
            else:
                actions.append(
                    _action(name, "replace", "selected_profile", "observed_target_drift")
                )
            continue

        if observed is not None:
            reason_codes = ["not_admitted_for_selected_profile"]
            if observed.get("bearer_token_env_var") == LEGACY_SHARED_BEARER_ENV:
                reason_codes.append("legacy_shared_bearer_observed")
            if name not in selected_names:
                reason_codes.append("outside_selected_profile")
            actions.append(
                _action(name, "retain_legacy_until_replacement_gates", *reason_codes)
            )
        else:
            reason = (
                "outside_selected_profile"
                if name not in selected_names
                else "admission_gates_incomplete"
            )
            actions.append(_action(name, "withhold", reason))

        if name in selected_names and not admission_ready(registration):
            missing = []
            if registration["registry_state"] != "admitted":
                missing.append("registry_admission")
            if not registration["expected_schema_digest"]:
                missing.append("consumer_schema_digest")
            for receipt_key in ADMISSION_RECEIPT_KEYS:
                if not registration["receipts"][receipt_key]:
                    missing.append(f"{receipt_key}_receipt")
            blockers.append(f"{name}: missing {', '.join(missing)}")

    for name in sorted(set(observed_by_name) - set(by_name)):
        actions.append(_action(name, "investigate_unmanaged", "absent_from_source_manifest"))
        blockers.append(f"{name}: observed registration is unmanaged")

    mutation_actions = [action for action in actions if action["action"] in MUTATING_ACTIONS]
    mutation_authorized = all(
        (
            action["action"] == "remove_after_receipt"
            and bool(by_name[action["registration_name"]].get("removal_receipt"))
        )
        or (
            action["action"] in {"add", "replace"}
            and admission_ready(by_name[action["registration_name"]])
        )
        for action in mutation_actions
    )
    mutation_allowed = bool(mutation_actions) and profile_ready and mutation_authorized

    plan: dict[str, Any] = {
        "schema_version": "8dionysus_codex_organ_fabric_plan_v1",
        "profile": profile_name,
        "generated_at": max(manifest["updated_at"], observation["observed_at"]),
        "manifest_digest": canonical_digest(manifest),
        "observation_digest": canonical_digest(observation),
        "selected_registration_count": len(selected),
        "selected_tool_count": sum(len(registration["enabled_tools"]) for registration in selected),
        "rendered_registration_count": len(renderable),
        "mutation_allowed": mutation_allowed,
        "fresh_client_required": True,
        "actions": actions,
        "blockers": sorted(set(blockers)),
        "claim_limits": [
            "This plan is derived source evidence and does not mutate Codex configuration.",
            "A rendered registration still requires an operator-controlled apply.",
            "A fresh Codex process and post-registration schema observation are required.",
            "Registration does not prove endpoint, authentication, grounded calls, or owner acceptance.",
        ],
    }
    plan["plan_digest"] = canonical_digest(plan)
    validate_json_schema(plan, PLAN_SCHEMA)
    return plan


def _toml_string(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _toml_list(values: Sequence[str]) -> str:
    return "[" + ", ".join(_toml_string(value) for value in values) + "]"


def render_target_toml(
    manifest: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> str:
    profile_name = plan["profile"]
    selected = [
        registration
        for registration in manifest["registrations"]
        if profile_name in registration["profiles"]
    ]
    if plan["rendered_registration_count"] == 0:
        selected = []
    elif len(selected) != plan["rendered_registration_count"]:
        raise ValueError("plan/rendered registration count mismatch")

    lines = [
        "# GENERATED by scripts/render_codex_organ_fabric.py.",
        "# Source fragment only: this file is never applied automatically.",
        f"# profile = {_toml_string(profile_name)}",
        f"# plan_digest = {_toml_string(plan['plan_digest'])}",
        "# A fresh Codex process is required after an operator-controlled apply.",
        "",
    ]
    for registration in selected:
        if not admission_ready(registration):
            raise ValueError(
                f"{registration['registration_name']}: non-admitted registration reached renderer"
            )
        name = registration["registration_name"]
        lines.extend(
            [
                f"[mcp_servers.{name}]",
                f"url = {_toml_string(registration['url'])}",
                f"bearer_token_env_var = {_toml_string(registration['bearer_token_env_var'])}",
                "enabled = true",
                "required = false",
                f"startup_timeout_sec = {registration['startup_timeout_sec']}",
                f"tool_timeout_sec = {registration['tool_timeout_sec']}",
                f"enabled_tools = {_toml_list(registration['enabled_tools'])}",
                (
                    "default_tools_approval_mode = "
                    f"{_toml_string(registration['default_tools_approval_mode'])}"
                ),
                "",
            ]
        )
        if registration["policy_family"] == "candidate":
            for tool_name in registration["enabled_tools"]:
                lines.extend(
                    [
                        f"[mcp_servers.{name}.tools.{tool_name}]",
                        'approval_mode = "prompt"',
                        "",
                    ]
                )
    return "\n".join(lines).rstrip() + "\n"


def derive(
    manifest: Mapping[str, Any],
    observation: Mapping[str, Any],
    profile_name: str,
) -> tuple[dict[str, Any], str]:
    manifest_copy = deepcopy(dict(manifest))
    observation_copy = deepcopy(dict(observation))
    plan = build_plan(manifest_copy, observation_copy, profile_name)
    return plan, render_target_toml(manifest_copy, plan)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--observation", type=Path, default=DEFAULT_OBSERVATION)
    parser.add_argument("--profile", default="core-read")
    parser.add_argument("--dest-config", type=Path, default=None)
    parser.add_argument("--dest-plan", type=Path, default=None)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    manifest = load_json_object(args.manifest)
    observation = load_json_object(args.observation)
    plan, config_text = derive(manifest, observation, args.profile)
    dest_config = args.dest_config or DEFAULT_OUTPUT_DIR / f"{args.profile}.target.toml"
    dest_plan = args.dest_plan or DEFAULT_OUTPUT_DIR / f"{args.profile}.plan.json"
    plan_text = json.dumps(plan, ensure_ascii=False, indent=2) + "\n"

    if args.check:
        actual_config = dest_config.read_text(encoding="utf-8") if dest_config.exists() else None
        actual_plan = dest_plan.read_text(encoding="utf-8") if dest_plan.exists() else None
        return 0 if actual_config == config_text and actual_plan == plan_text else 1

    dest_config.parent.mkdir(parents=True, exist_ok=True)
    dest_plan.parent.mkdir(parents=True, exist_ok=True)
    dest_config.write_text(config_text, encoding="utf-8")
    dest_plan.write_text(plan_text, encoding="utf-8")
    print(f"rendered_profile={args.profile}")
    print(f"rendered_registration_count={plan['rendered_registration_count']}")
    print(f"mutation_allowed={str(plan['mutation_allowed']).lower()}")
    print(f"dest_config={dest_config}")
    print(f"dest_plan={dest_plan}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
