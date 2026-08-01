# Project the Tree of Sophia Runtime Wrapper Without Default Registration

## Index Metadata

- Decision ID: 8DION-D-0026
- Original date: 2026-08-01
- Surface classes: Codex plane, MCP runtime projection, Tree of Sophia access
- Route anchors: .codex/bin/tos-corpus-mcp-server.py, config/codex_plane/organ_fabric/codex_consumer_manifest.v1.json, scripts/validate_codex_plane_regeneration.py
- Owner lanes: 8Dionysus, Tree-of-Sophia, abyss-stack, aoa-sdk
- Guard families: progressive discovery, deny by default, owner boundary, no always-loaded registration
- Posture: accepted

## Status

Accepted for the integrated organ-access landing.

## Context

The stack already owns a runnable `tos-corpus-mcp` package, while the public
Codex plane needs a portable source route that can locate that package after a
future admitted deployment. The current Tree of Sophia record is nevertheless
suspended: there is no complete admission, consumer-schema, central-proof,
canary, owner-acceptance, and rollback receipt set.

Treating wrapper presence as registration would bypass progressive discovery,
increase the always-loaded tool catalog, and turn a projection artifact into a
false availability claim. Omitting the wrapper entirely would leave a later
admitted deployment dependent on a host-local launcher with no public source
owner.

## Options Considered

1. Add `tos_corpus` to the stable runtime manifest when its wrapper is added.
2. Keep both the wrapper and registration host-local until all gates close.
3. Check in the bounded wrapper as a source-owned runtime projection, but keep
   `tos_corpus` out of the stable runtime manifest and allow registration only
   through the receipt-gated organ fabric.

Option 1 conflates executable discovery with admission. Option 2 makes the
future launch route irreproducible from owner source. Choose option 3.

## Decision

`8Dionysus` carries `.codex/bin/tos-corpus-mcp-server.py` as the portable
projection route to the stack-owned package.

The wrapper does not own corpus semantics, service implementation, runtime
health, or admission. Those remain with Tree of Sophia, `abyss-stack`, and the
organ-fabric evidence chain. Its presence must not add `tos_corpus` to
`config/codex_plane/runtime_manifest.v1.json`.

Only the deny-by-default organ-fabric rollout may register `tos_corpus`, and
only after the exact receipt set and owner gates for that contour close. Until
then the record remains suspended and the wrapper is non-admitting source.

## Consequences

- A future admitted runtime has a reproducible public source launcher.
- Wrapper existence cannot be cited as live availability or owner acceptance.
- The current stable MCP names and always-loaded catalog remain unchanged.
- Rollback before admission is simply continued withholding; rollback after a
  future admission remains owned by the organ-fabric rollout contract.

## Verification

Run:

```bash
python scripts/generate_decision_indexes.py --check
python scripts/validate_decision_records.py
python scripts/validate_codex_plane_regeneration.py --repo-root . --workspace-root /srv/AbyssOS
python scripts/validate_codex_organ_fabric.py
python -m unittest tests.test_codex_plane_regeneration tests.test_decision_indexes
```

These checks prove the source boundary and deny-by-default projection. They do
not prove live deployment, corpus freshness, canary health, owner acceptance,
or admission.
