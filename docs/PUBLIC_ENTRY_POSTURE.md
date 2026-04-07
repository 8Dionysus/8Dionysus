# Public Entry Posture

This note defines what the public profile repository does and does not promise.
It keeps `8Dionysus` as a route map, not a hidden center of authority.

## What this repository owns

`8Dionysus` owns:

- public repository routing
- short role descriptions for the current public ecosystem
- glossary-level orientation
- profile-local reflection debt when linked public descriptions drift

It does not own:

- ecosystem charter or federation rules
- source-owned release semantics for AoA layers
- support guarantees for runtime, product, or infrastructure surfaces
- validators, workflows, or implementation truth from linked repositories

## Shortest onboarding paths

Use the smallest route that matches your need:

| need | canonical home | shortest route | public verification surface |
|---|---|---|---|
| ecosystem understanding | `Agents-of-Abyss` | `README` -> `CHARTER` -> `ECOSYSTEM_MAP` -> `docs/FEDERATION_RULES` | `generated/ecosystem_registry.min.json`, `generated/federation_supporting_inventory.min.json`, `python scripts/validate_ecosystem.py`, `python -m pytest -q tests` |
| local workspace bootstrap and typed control-plane use | `aoa-sdk` | `README` -> `docs/boundaries.md` -> `docs/workspace-layout.md` -> `docs/versioning.md` | `aoa workspace inspect /srv/aoa-sdk`, `aoa compatibility check /srv/aoa-sdk`, `python -m pytest -q`, `python -m ruff check .` |
| profile-only route or glossary correction | `8Dionysus` | `README.md`, `GLOSSARY.md`, `docs/QUESTBOOK_PROFILE_BOUNDARY.md` | link review against linked owner repos |

## Support and release semantics

`8Dionysus` does not issue ecosystem releases.
Its changes are honest only when they follow already-landed owner-repo changes and keep route descriptions aligned with those owner surfaces.

The profile may link to product-edge repositories such as `ATM10-Agent`, but their supported profiles, release cadence, and public test tiers remain owned by those repositories.
In the current remediation program, the product-edge tightening still belongs to the later GitHub-only `WS12` track.

## CI and verification posture

This repository is intentionally lightweight.
It does not claim a federation-wide CI tier map of its own.

Use it to route toward the real verification surfaces:

- `Agents-of-Abyss` for ecosystem-center claims
- `aoa-sdk` for control-plane compatibility and workspace validation
- linked owner repos for layer-local or runtime guarantees
