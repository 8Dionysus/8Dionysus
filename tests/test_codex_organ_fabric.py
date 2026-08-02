from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import render_codex_organ_fabric as organ_fabric
from validate_codex_organ_fabric import validate


MANIFEST_PATH = (
    REPO_ROOT
    / "config"
    / "codex_plane"
    / "organ_fabric"
    / "codex_consumer_manifest.v1.json"
)
OBSERVATION_PATH = (
    REPO_ROOT
    / "config"
    / "codex_plane"
    / "organ_fabric"
    / "current_consumer_observation.public.json"
)


def load_inputs() -> tuple[dict[str, object], dict[str, object]]:
    return (
        organ_fabric.load_json_object(MANIFEST_PATH),
        organ_fabric.load_json_object(OBSERVATION_PATH),
    )


def registration(manifest: dict[str, object], name: str) -> dict[str, object]:
    return next(
        item
        for item in manifest["registrations"]  # type: ignore[index]
        if item["registration_name"] == name
    )


def admit(item: dict[str, object]) -> None:
    item["registry_state"] = "admitted"
    item["expected_schema_digest"] = "sha256:" + "a" * 64
    item["receipts"] = {
        "admission": "receipt://registry/admission",
        "consumer_schema": "receipt://codex/schema",
        "central_proof": "receipt://aoa-evals/central-proof",
        "canary": "receipt://runtime/canary",
        "owner_acceptance": "receipt://owner/acceptance",
        "rollback": "receipt://operator/rollback",
    }


def select_only(
    manifest: dict[str, object],
    name: str,
    profile_name: str,
    policy_family: str,
) -> dict[str, object]:
    manifest["profiles"][profile_name] = {  # type: ignore[index]
        "description": f"Synthetic {name} test profile.",
        "allowed_policy_families": [policy_family],
    }
    item = registration(manifest, name)
    item["profiles"] = [profile_name]
    return item


class CodexOrganFabricTests(unittest.TestCase):
    def test_current_source_posture_is_deterministic_and_deny_by_default(self) -> None:
        manifest, observation = load_inputs()

        first_plan, first_toml = organ_fabric.derive(manifest, observation, "core-read")
        second_plan, second_toml = organ_fabric.derive(manifest, observation, "core-read")

        self.assertEqual(first_plan, second_plan)
        self.assertEqual(first_toml, second_toml)
        self.assertEqual(first_plan["rendered_registration_count"], 0)
        self.assertFalse(first_plan["mutation_allowed"])
        self.assertNotIn("[mcp_servers.", first_toml)
        actions = [item["action"] for item in first_plan["actions"]]
        self.assertEqual(actions.count("retain_legacy_until_replacement_gates"), 10)
        self.assertEqual(actions.count("withhold"), 8)
        self.assertEqual(validate(REPO_ROOT)["rendered_registrations"], 0)

    def test_stack_contours_bind_runtime_owned_credential_classes(self) -> None:
        manifest, _ = load_inputs()

        self.assertEqual(
            registration(manifest, "abyss_stack_read")["credential_class"],
            "abyss-stack-read",
        )
        self.assertEqual(
            registration(manifest, "abyss_stack_candidate")["credential_class"],
            "abyss-stack-candidate",
        )

    def test_fully_admitted_kag_profile_renders_exact_consumer_policy(self) -> None:
        manifest, observation = load_inputs()
        item = select_only(manifest, "aoa_kag", "kag-only", "read")
        admit(item)
        observation["effective_registrations"] = [  # type: ignore[index]
            observed
            for observed in observation["effective_registrations"]  # type: ignore[index]
            if observed["registration_name"] != "aoa_kag"
        ]

        plan, target = organ_fabric.derive(manifest, observation, "kag-only")

        self.assertEqual(plan["rendered_registration_count"], 1)
        self.assertTrue(plan["mutation_allowed"])
        self.assertIn("[mcp_servers.aoa_kag]", target)
        self.assertIn('bearer_token_env_var = "AOA_KAG_MCP_READ_BEARER_TOKEN"', target)
        self.assertIn('enabled_tools = ["kag_discover", "kag_search"', target)
        self.assertIn("startup_timeout_sec = 20", target)
        self.assertIn("tool_timeout_sec = 90", target)
        self.assertIn('default_tools_approval_mode = "writes"', target)
        self.assertNotIn(organ_fabric.LEGACY_SHARED_BEARER_ENV, target)

    def test_admitted_registration_missing_one_receipt_is_rejected(self) -> None:
        manifest, _ = load_inputs()
        item = select_only(manifest, "aoa_kag", "kag-only", "read")
        admit(item)
        item["receipts"]["owner_acceptance"] = None  # type: ignore[index]

        with self.assertRaisesRegex(ValueError, "missing schema or six required receipts"):
            organ_fabric.validate_manifest(manifest)

    def test_candidate_profile_renders_per_tool_prompts(self) -> None:
        manifest, observation = load_inputs()
        item = select_only(
            manifest,
            "aoa_memo_candidate",
            "memo-candidate-only",
            "candidate",
        )
        admit(item)
        observation["effective_registrations"] = []  # type: ignore[index]

        plan, target = organ_fabric.derive(
            manifest,
            observation,
            "memo-candidate-only",
        )

        self.assertEqual(plan["rendered_registration_count"], 1)
        self.assertIn('default_tools_approval_mode = "prompt"', target)
        for tool_name in item["enabled_tools"]:  # type: ignore[union-attr]
            self.assertIn(
                f"[mcp_servers.aoa_memo_candidate.tools.{tool_name}]",
                target,
            )
        self.assertEqual(
            target.count('approval_mode = "prompt"'),
            len(item["enabled_tools"]) + 1,  # type: ignore[arg-type]
        )

    def test_profile_registration_budget_rejects_full_catalog(self) -> None:
        manifest, _ = load_inputs()
        manifest["profiles"]["full-read"] = {  # type: ignore[index]
            "description": "Forbidden full read catalog.",
            "allowed_policy_families": ["read"],
        }
        for item in manifest["registrations"]:  # type: ignore[index]
            if item["policy_family"] == "read":
                item["profiles"].append("full-read")

        with self.assertRaisesRegex(ValueError, "registration budget exceeded"):
            organ_fabric.validate_manifest(manifest)

    def test_observed_shadow_registration_is_retained_until_admission(self) -> None:
        manifest, observation = load_inputs()
        plan = organ_fabric.build_plan(manifest, observation, "core-read")
        kag_action = next(
            item for item in plan["actions"] if item["registration_name"] == "aoa_kag"
        )

        self.assertEqual(kag_action["action"], "retain_legacy_until_replacement_gates")
        self.assertEqual(kag_action["reason_codes"], ["not_admitted_for_selected_profile"])

    def test_suspended_registration_requires_removal_receipt(self) -> None:
        manifest, observation = load_inputs()
        tos = registration(manifest, "tos_corpus")
        observed_tos = copy.deepcopy(observation["effective_registrations"][0])  # type: ignore[index]
        observed_tos.update(
            {
                "registration_name": "tos_corpus",
                "url": tos["url"],
                "source_layers": ["global"],
            }
        )
        observation["effective_registrations"].append(observed_tos)  # type: ignore[index]

        without_receipt = organ_fabric.build_plan(manifest, observation, "corpus-read")
        action = next(
            item
            for item in without_receipt["actions"]
            if item["registration_name"] == "tos_corpus"
        )
        self.assertEqual(action["action"], "retain_legacy_until_replacement_gates")

        tos["removal_receipt"] = "receipt://registry/tos-suspension"
        with_receipt = organ_fabric.build_plan(manifest, observation, "corpus-read")
        action = next(
            item
            for item in with_receipt["actions"]
            if item["registration_name"] == "tos_corpus"
        )
        self.assertEqual(action["action"], "remove_after_receipt")

    def test_renderer_never_embeds_credential_values(self) -> None:
        manifest, observation = load_inputs()
        item = select_only(manifest, "aoa_kag", "kag-only", "read")
        admit(item)
        _, target = organ_fabric.derive(manifest, observation, "kag-only")

        self.assertNotIn("Authorization", target)
        self.assertNotIn("Bearer ", target)
        self.assertNotIn("receipt://", target)
        self.assertIn("bearer_token_env_var", target)


if __name__ == "__main__":
    unittest.main()
