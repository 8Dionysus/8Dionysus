from __future__ import annotations

import json
import unittest
from pathlib import Path

import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from public_route_map_common import SURFACE_PAYLOAD, build_payload, parse_public_entry_posture_rows


class PublicRouteMapTests(unittest.TestCase):
    def test_build_payload_stays_orientation_only(self) -> None:
        payload = build_payload()

        self.assertEqual(payload["schema_version"], "8dionysus_public_route_map_v2")
        self.assertEqual(payload["schema_ref"], "schemas/public-route-map.schema.json")
        self.assertEqual(payload["owner_repo"], "8Dionysus")
        self.assertEqual(payload["surface_kind"], "orientation_surface")
        self.assertEqual(payload["authority_ref"], SURFACE_PAYLOAD["authority_ref"])
        self.assertEqual(payload["posture"], "route-map-only")
        self.assertEqual(
            [route["route_id"] for route in payload["routes"]],
            [
                "ecosystem-understanding",
                "workspace-bootstrap",
                "profile-correction",
            ],
        )

    def test_public_entry_posture_table_keeps_expected_canonical_homes(self) -> None:
        posture_path = Path(__file__).resolve().parents[1] / "docs" / "PUBLIC_ENTRY_POSTURE.md"
        rows = parse_public_entry_posture_rows(posture_path.read_text(encoding="utf-8"))
        by_need = {row["need"]: row["canonical home"] for row in rows}

        self.assertEqual(by_need["ecosystem understanding"], "Agents-of-Abyss")
        self.assertEqual(
            by_need["local workspace bootstrap and typed control-plane use"],
            "aoa-sdk",
        )
        self.assertEqual(by_need["profile-only route or glossary correction"], "8Dionysus")

    def test_workspace_route_uses_sdk_capsule_surface(self) -> None:
        payload = build_payload()
        workspace_route = next(
            route for route in payload["routes"] if route["route_id"] == "workspace-bootstrap"
        )

        self.assertEqual(
            workspace_route["capsule_ref"],
            "aoa-sdk:generated/workspace_control_plane.min.json",
        )
        self.assertEqual(
            workspace_route["verification_refs"],
            [
                "aoa-sdk:docs/workspace-layout.md",
                "aoa-sdk:docs/versioning.md",
                "8Dionysus:docs/WORKSPACE_INSTALL.md",
                "8Dionysus:docs/CODEX_PLANE_REGENERATION.md",
            ],
        )

    def test_ecosystem_route_uses_center_entry_capsule(self) -> None:
        payload = build_payload()
        ecosystem_route = next(
            route for route in payload["routes"] if route["route_id"] == "ecosystem-understanding"
        )

        self.assertEqual(
            ecosystem_route["capsule_ref"],
            "Agents-of-Abyss:generated/center_entry_map.min.json",
        )
        self.assertEqual(ecosystem_route["authority_ref"], "Agents-of-Abyss:CHARTER.md")

    def test_workspace_row_keeps_projection_and_regeneration_visible(self) -> None:
        posture_path = Path(__file__).resolve().parents[1] / "docs" / "PUBLIC_ENTRY_POSTURE.md"
        posture = posture_path.read_text(encoding="utf-8")
        rows = parse_public_entry_posture_rows(posture)
        workspace_row = next(
            row
            for row in rows
            if row["need"] == "local workspace bootstrap and typed control-plane use"
        )

        self.assertIn("8Dionysus/docs/WORKSPACE_INSTALL.md", workspace_row["shortest route"])
        self.assertIn(
            "8Dionysus/docs/CODEX_PLANE_REGENERATION.md",
            workspace_row["shortest route"],
        )
        self.assertIn("docs/WORKSPACE_INSTALL.md", workspace_row["public verification surface"])
        self.assertIn(
            ".codex/bin/aoa-workspace-project --check --json",
            workspace_row["public verification surface"],
        )
        self.assertIn(
            "python scripts/validate_codex_plane_regeneration.py --workspace-root <workspace-root>",
            workspace_row["public verification surface"],
        )
        self.assertIn(
            "shared-root projection sync and Codex-plane regeneration checks",
            posture,
        )

    def test_payload_is_json_serializable(self) -> None:
        payload = build_payload()
        rendered = json.dumps(payload, separators=(",", ":"))

        self.assertIn("orientation_surface", rendered)
        self.assertNotIn(":scripts/", rendered)
        self.assertNotIn(":src/", rendered)


if __name__ == "__main__":
    unittest.main()
