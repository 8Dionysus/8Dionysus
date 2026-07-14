from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_PATH = REPO_ROOT / "generated" / "agents_map.min.json"
PACKET_PATH = (
    REPO_ROOT
    / "stats"
    / "packets"
    / "known-repository-root-agents-coverage-ratio.reference.json"
)


def derive_known_repository_root_agents_coverage(payload: dict[str, object]) -> dict[str, object]:
    if payload.get("audit_mode") != "live-workspace":
        return {"status": "unknown", "reason": "not_live_workspace_audit"}

    known = payload.get("known_repositories")
    records = payload.get("repositories")
    if (
        not isinstance(known, list)
        or not known
        or not all(isinstance(name, str) and name for name in known)
        or len(set(known)) != len(known)
    ):
        return {"status": "unknown", "reason": "invalid_known_population"}
    if not isinstance(records, list):
        return {"status": "unknown", "reason": "invalid_repository_records"}

    known_set = set(known)
    records_by_name: dict[str, dict[str, object]] = {}
    for record in records:
        if not isinstance(record, dict) or record.get("name") not in known_set:
            continue
        name = str(record["name"])
        if name in records_by_name:
            return {"status": "unknown", "reason": "duplicate_known_repository_record"}
        records_by_name[name] = record

    if set(records_by_name) != known_set:
        return {"status": "unknown", "reason": "incomplete_known_population"}

    numerator = 0
    for name in known:
        record = records_by_name[name]
        checkout_state = record.get("checkout_state")
        root_agents_present = record.get("root_agents_present")
        if checkout_state not in {"scanned", "missing"} or type(root_agents_present) is not bool:
            return {"status": "unknown", "reason": "malformed_known_repository_record"}
        if checkout_state == "missing" and root_agents_present:
            return {"status": "unknown", "reason": "inconsistent_missing_repository_record"}
        numerator += int(checkout_state == "scanned" and root_agents_present)

    denominator = len(known)
    return {
        "status": "observed",
        "reason": "complete",
        "numerator": numerator,
        "denominator": denominator,
        "ratio": numerator / denominator,
    }


class LocalStatsPortTests(unittest.TestCase):
    def test_reference_packet_matches_committed_agents_map(self) -> None:
        evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
        packet = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
        derived = derive_known_repository_root_agents_coverage(evidence)

        self.assertEqual(derived["status"], "observed")
        self.assertEqual(packet["population"]["size"], derived["denominator"])
        self.assertEqual(packet["sample"]["size"], derived["denominator"])
        self.assertEqual(packet["value"]["numerator"], derived["numerator"])
        self.assertEqual(packet["value"]["denominator"], derived["denominator"])
        self.assertEqual(packet["value"]["number"], derived["ratio"])

    def test_missing_known_repository_remains_in_denominator(self) -> None:
        payload = {
            "audit_mode": "live-workspace",
            "known_repositories": ["alpha", "beta", "gamma"],
            "repositories": [
                {"name": "alpha", "checkout_state": "scanned", "root_agents_present": True},
                {"name": "beta", "checkout_state": "missing", "root_agents_present": False},
                {"name": "gamma", "checkout_state": "scanned", "root_agents_present": True},
                {"name": "extra", "checkout_state": "scanned", "root_agents_present": True},
            ],
        }

        derived = derive_known_repository_root_agents_coverage(payload)

        self.assertEqual(derived["numerator"], 2)
        self.assertEqual(derived["denominator"], 3)
        self.assertEqual(derived["ratio"], 2 / 3)

    def test_successful_zero_is_an_observation(self) -> None:
        payload = {
            "audit_mode": "live-workspace",
            "known_repositories": ["alpha", "beta"],
            "repositories": [
                {"name": "alpha", "checkout_state": "scanned", "root_agents_present": False},
                {"name": "beta", "checkout_state": "missing", "root_agents_present": False},
            ],
        }

        derived = derive_known_repository_root_agents_coverage(payload)

        self.assertEqual(derived["status"], "observed")
        self.assertEqual(derived["ratio"], 0.0)

    def test_public_baseline_is_not_an_observation(self) -> None:
        payload = {
            "audit_mode": "public-baseline",
            "known_repositories": ["alpha"],
            "repositories": [{"name": "alpha", "checkout_state": "public-baseline"}],
        }

        self.assertEqual(
            derive_known_repository_root_agents_coverage(payload),
            {"status": "unknown", "reason": "not_live_workspace_audit"},
        )

    def test_duplicate_malformed_incomplete_and_empty_populations_are_unknown(self) -> None:
        valid = {
            "audit_mode": "live-workspace",
            "known_repositories": ["alpha", "beta"],
            "repositories": [
                {"name": "alpha", "checkout_state": "scanned", "root_agents_present": True},
                {"name": "beta", "checkout_state": "scanned", "root_agents_present": True},
            ],
        }
        duplicate = deepcopy(valid)
        duplicate["repositories"].append(deepcopy(duplicate["repositories"][0]))
        malformed = deepcopy(valid)
        del malformed["repositories"][0]["root_agents_present"]
        incomplete = deepcopy(valid)
        incomplete["repositories"].pop()
        empty = {"audit_mode": "live-workspace", "known_repositories": [], "repositories": []}

        for payload in (duplicate, malformed, incomplete, empty):
            with self.subTest(payload=payload):
                self.assertEqual(
                    derive_known_repository_root_agents_coverage(payload)["status"],
                    "unknown",
                )


if __name__ == "__main__":
    unittest.main()
