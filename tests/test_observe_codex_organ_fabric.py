from __future__ import annotations

import copy
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import observe_codex_organ_fabric as observer


def registration() -> dict[str, object]:
    return {
        "name": "aoa_kag",
        "enabled": True,
        "disabled_reason": None,
        "transport": {
            "type": "streamable_http",
            "url": "http://127.0.0.1:5425/mcp",
            "bearer_token_env_var": "AOA_KAG_MCP_READ_BEARER_TOKEN",
            "http_headers": None,
            "env_http_headers": None,
        },
        "enabled_tools": None,
        "disabled_tools": None,
        "startup_timeout_sec": None,
        "tool_timeout_sec": None,
    }


def status() -> dict[str, object]:
    return {
        "name": "aoa_kag",
        "authStatus": "bearerToken",
        "serverInfo": {"name": "aoa-kag-mcp", "version": "0.1.0"},
        "tools": {
            "z": {"name": "z_tool", "inputSchema": {"type": "object"}},
            "a": {"name": "a_tool", "inputSchema": {"type": "object"}},
        },
        "resources": [
            {"name": "z", "uri": "kag://z"},
            {"name": "a", "uri": "kag://a"},
        ],
        "resourceTemplates": [
            {"name": "z", "uriTemplate": "kag://z/{id}"},
            {"name": "a", "uriTemplate": "kag://a/{id}"},
        ],
    }


class ObserveCodexOrganFabricTests(unittest.TestCase):
    def test_inventory_is_sorted_and_digest_is_deterministic(self) -> None:
        first = observer.canonical_inventory(status(), "2025-11-25")
        shuffled = status()
        shuffled["tools"] = dict(reversed(list(shuffled["tools"].items())))
        shuffled["resources"] = list(reversed(shuffled["resources"]))
        shuffled["resourceTemplates"] = list(reversed(shuffled["resourceTemplates"]))
        second = observer.canonical_inventory(shuffled, "2025-11-25")

        self.assertEqual(first, second)
        self.assertEqual([item["name"] for item in first["tools"]], ["a_tool", "z_tool"])
        self.assertEqual(observer.canonical_digest(first), observer.canonical_digest(second))

    def test_receipt_is_secret_free_content_addressed_and_valid(self) -> None:
        observed_at = datetime(2026, 8, 1, tzinfo=timezone.utc)
        receipt = observer.build_receipt(
            registration(),
            status(),
            "0.146.0",
            "2025-11-25",
            observed_at,
            observed_at + timedelta(hours=24),
            {
                "tool_name": "a_tool",
                "arguments_digest": "sha256:" + "a" * 64,
                "result_digest": "sha256:" + "b" * 64,
                "is_error": False,
                "content_item_count": 1,
            },
        )

        serialized = observer.canonical_json_bytes(receipt).decode("utf-8")
        self.assertNotIn("Bearer ", serialized)
        self.assertNotIn("example-secret-value", serialized)
        self.assertIn("AOA_KAG_MCP_READ_BEARER_TOKEN", serialized)
        self.assertTrue(receipt["registration_ref"].endswith(receipt["registration_ref"].split("/")[-1]))
        observer.validate_receipt(receipt)

    def test_tampered_receipt_is_rejected(self) -> None:
        observed_at = datetime(2026, 8, 1, tzinfo=timezone.utc)
        receipt = observer.build_receipt(
            registration(),
            status(),
            "0.146.0",
            "2025-11-25",
            observed_at,
            observed_at + timedelta(hours=24),
            None,
        )
        tampered = copy.deepcopy(receipt)
        tampered["registration"]["url"] = "http://127.0.0.1:5426/mcp"

        with self.assertRaisesRegex(ValueError, "receipt_digest"):
            observer.validate_receipt(tampered)

    def test_stack_overlay_preserves_consumer_issuer_and_exact_ref(self) -> None:
        observed_at = datetime(2026, 8, 1, tzinfo=timezone.utc)
        receipt = observer.build_receipt(
            registration(),
            status(),
            "0.146.0",
            "2025-11-25",
            observed_at,
            observed_at + timedelta(hours=24),
            None,
        )

        overlay = observer.build_stack_overlay(receipt, "aoa-kag")
        consumer = overlay["subjects"][0]["consumers"][0]

        self.assertEqual(consumer["registration_ref"], receipt["registration_ref"])
        self.assertEqual(
            consumer["evidence"]["evidence_refs"][0]["owner"],
            "8Dionysus",
        )
        self.assertEqual(
            consumer["evidence"]["evidence_refs"][0]["revision"],
            receipt["receipt_digest"],
        )
        self.assertFalse(overlay["contains_secrets"])

    def test_failed_call_cannot_issue_usable_receipt(self) -> None:
        observed_at = datetime(2026, 8, 1, tzinfo=timezone.utc)
        with self.assertRaisesRegex(ValueError, "is_error"):
            observer.build_receipt(
                registration(),
                status(),
                "0.146.0",
                "2025-11-25",
                observed_at,
                observed_at + timedelta(hours=24),
                {
                    "tool_name": "a_tool",
                    "arguments_digest": "sha256:" + "a" * 64,
                    "result_digest": "sha256:" + "b" * 64,
                    "is_error": True,
                    "content_item_count": 1,
                },
            )


if __name__ == "__main__":
    unittest.main()
