# Deny-by-Default Organ-Fabric Consumer Projection

## Index Metadata

- Decision ID: 8DION-D-0024
- Original date: 2026-07-26
- Surface classes: Codex plane, MCP organ fabric, consumer registration
- Route anchors: config/codex_plane/organ_fabric/codex_consumer_manifest.v1.json, scripts/render_codex_organ_fabric.py, docs/CODEX_ORGAN_FABRIC_CONSUMER.md
- Owner lanes: 8Dionysus, aoa-sdk, abyss-stack, organ repositories, operator
- Guard families: deny by default, profile budget, credential separation, receipt admission, rollback
- Posture: accepted

## Status

Accepted for the integrated OS Abyss MCP landing.

## Context

The existing Codex plane proves that stable organ handles can be made
available, but its portable source render and deploy-composed HTTP form are not
an admission system. The observed legacy shape also loads a broad catalog,
shares one bearer-token environment name across owners, omits explicit tool
allowlists and timeouts, and cannot by itself distinguish registration,
runtime readiness, schema freshness, grounded use, owner acceptance, or safe
removal.

The OS Abyss organ fabric needs a consumer surface that can grow to many organs
without turning every registered capability into ambient authority or paying
for the entire catalog in every agent context.

## Options Considered

1. Continue adding every organ to the portable always-loaded registration.
2. Let `abyss-stack` write live Codex configuration when a service starts.
3. Keep a source-owned, profile-scoped consumer manifest in `8Dionysus`, admit
   records through `aoa-sdk` evidence, consume `abyss-stack` runtime receipts,
   and reserve live apply to the operator.

Option 1 preserves compatibility but compounds catalog and authority debt.
Option 2 makes runtime presence the hidden authority for consumer admission and
crosses the deploy-composed boundary established by `8DION-D-0019`. Choose
option 3.

## Decision

`8Dionysus` owns a deterministic Codex organ-fabric consumer projection with
these rules:

- one bounded profile is rendered at a time;
- the full catalog is forbidden as an always-loaded profile;
- read and candidate contours use separate registrations and credentials;
- read contours default to `writes` approval and candidate contours to
  `prompt`, with explicit per-tool prompts for candidate tools;
- a whole profile renders only after exact schema and five admission receipts
  exist for every selected registration;
- source rendering never reads secret values and has no apply mode;
- observed legacy registrations remain until replacement gates or explicit
  consumer-zero removal evidence close;
- a fresh Codex process and post-change schema observation are mandatory live
  rollout evidence.

`aoa-sdk` remains the registry owner. `abyss-stack` remains the service and
runtime-evidence owner. Organ repositories remain the semantic and acceptance
owners. The operator remains the only live credential and config-apply
authority.

## Consequences

- adding a source record cannot silently activate an organ;
- profile budget and allowlists bound catalog growth;
- a shared legacy credential can be migrated without pretending the old
  registrations disappeared;
- partial admission cannot produce a plausible partial profile;
- source validation can be green while live rollout remains honestly
  incomplete;
- final landing needs cross-repository receipts before any Codex mutation.

## Verification

Run:

```bash
python scripts/render_codex_organ_fabric.py --check
python scripts/validate_codex_organ_fabric.py
python -m unittest tests.test_codex_organ_fabric
python scripts/validate_codex_plane_regeneration.py --workspace-root /srv/AbyssOS
```

These commands validate checked-in source only. They do not inspect or mutate a
live Codex configuration.
