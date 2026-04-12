# Public Entry Posture

This note defines what the public profile repository does and does not promise.
It keeps `8Dionysus` as a route map, not a hidden center of authority.

## What this repository owns

`8Dionysus` owns:

- public repository routing
- short role descriptions for the current public ecosystem
- glossary-level orientation
- one compact capability-map route for already-landed cross-repo families
- selected shared-root install surfaces projected into the live workspace root, specifically `AGENTS.md`, `AOA_WORKSPACE_ROOT`, `.agents/`, and the project-level `.codex` source layer
- profile-local reflection debt when linked public descriptions drift

It does not own:

- ecosystem charter or federation rules
- source-owned release semantics for AoA layers
- support guarantees for runtime, product, or infrastructure surfaces
- personal `~/.codex` defaults or deploy-local runtime output under `<workspace-root>/.codex/generated/`
- validators, workflows, or implementation truth from linked repositories

## Shortest onboarding paths

Use the smallest route that matches your need:

| need | canonical home | shortest route | public verification surface |
|---|---|---|---|
| ecosystem understanding | `Agents-of-Abyss` | `generated/center_entry_map.min.json` -> `README.md` -> `CHARTER.md` -> `docs/FEDERATION_RULES.md` | `generated/ecosystem_registry.min.json`, `generated/federation_supporting_inventory.min.json`, `python scripts/build_center_entry_map.py --check`, `python scripts/validate_center_entry_map.py`, `python scripts/validate_ecosystem.py`, `python -m pytest -q tests` |
| local workspace bootstrap and typed control-plane use | `aoa-sdk` | `generated/workspace_control_plane.min.json` -> `docs/boundaries.md` -> `docs/workspace-layout.md` -> `docs/versioning.md` | `python scripts/build_workspace_control_plane.py --check`, `python scripts/validate_workspace_control_plane.py`, `aoa workspace inspect /srv/aoa-sdk`, `aoa compatibility check /srv/aoa-sdk`, `python -m pytest -q`, `python -m ruff check .` |
| profile-only route or glossary correction | `8Dionysus` | `README.md`, `GLOSSARY.md`, `docs/QUESTBOOK_PROFILE_BOUNDARY.md` | link review against linked owner repos |

## Capability overview

For a compact cross-repo map of the currently planted capability families,
owner repos, playbook openings, and MCP lanes, use
[SYSTEM_CAPABILITY_MAP.md](SYSTEM_CAPABILITY_MAP.md).

That note is overview-only.
It routes into owner repositories and does not replace their validators,
playbooks, or implementation truth.

## Support and release semantics

`8Dionysus` does not issue ecosystem releases.
Its changes are honest only when they follow already-landed owner-repo changes and keep route descriptions aligned with those owner surfaces.
That includes the selected shared-root install surfaces it publishes into the
live workspace root: those files may shape orientation and local bootstrap, but
they still do not transfer layer authority away from the owning repositories.

The profile may link to product-edge repositories such as `ATM10-Agent`, but their supported profiles, release cadence, and public test tiers remain owned by those repositories.
In the current remediation program, the product-edge tightening still belongs to the later GitHub-only `WS12` track.

## CI and verification posture

This repository is intentionally lightweight.
It does not claim a federation-wide CI tier map of its own.

Use it to route toward the real verification surfaces:

- `Agents-of-Abyss` for ecosystem-center claims
- `aoa-sdk` for control-plane compatibility and workspace validation
- linked owner repos for layer-local or runtime guarantees
