# Route Active Routing Work Through aoa-sdk

## Index Metadata

- Decision ID: 8DION-D-0025
- Original date: 2026-07-28
- Surface classes: public entry, routing succession, repository lifecycle
- Route anchors: AGENTS.md, README.md, GLOSSARY.md, docs/START_HERE.md, generated/workspace_memory_map.min.json
- Owner lanes: 8Dionysus, aoa-sdk, aoa-routing, operator
- Guard families: public route ownership, owner succession, compatibility, rollback, consumer-zero, archive approval
- Posture: accepted

## Status

Accepted for the `8Dionysus` public-entry route.

## Context

The routing producer succession is owned and justified by
`aoa-sdk:docs/decisions/AOA-SDK-D-0071-staged-routing-producer-succession.md`,
its receipt-bound owner switch is authorized by
`aoa-sdk:docs/decisions/AOA-SDK-D-0076-authorize-receipt-bound-routing-g5-owner-switch.md`,
and the predecessor boundary is preserved by
`aoa-routing:docs/decisions/AOA-RT-D-0004-stage-producer-succession-to-aoa-sdk.md`.

Those owner decisions make `aoa-sdk` the canonical routing producer and keep
`aoa-routing` as a maintenance-only rollback source. The public entry still
needs a durable local answer to a narrower question: where should a new agent
route active navigation, dispatch, and routing work, and why does the
predecessor remain visible?

Leaving that answer only in route-card edits would make a future rollback,
consumer-zero review, or archive assessment reconstruct the public-entry
boundary from commit prose.

## Options Considered

1. Keep routing active work pointed at `aoa-routing` until the predecessor is
   archived.
2. Remove `aoa-routing` from public orientation as soon as the owner switch is
   accepted.
3. Route all active routing work through `aoa-sdk` while retaining
   `aoa-routing` as an explicit maintenance-only predecessor until its separate
   exit gates close.

Option 1 would preserve two active public control-plane routes after the
canonical producer changed and would continue the ambiguity and coordination
cost the succession is meant to remove. Option 2 would erase the rollback and
repository-lifecycle boundary before consumer-zero, compatibility exit, and
operator approval exist. Choose option 3.

## Decision

`8Dionysus` routes new navigation, discovery, dispatch, and routing-control
questions to `aoa-sdk`.

`aoa-routing` remains visible only as the deprecated maintenance-only
predecessor for reversible history, compatibility review, and rollback. It is
not an active destination for new routing work.

This record owns only the public-entry consequence. Routing producer and ABI
authority remain with `aoa-sdk`; predecessor lifecycle evidence remains with
`aoa-routing` and the succession proof surfaces; the operator alone may
authorize archive or deletion.

## Consequences

- Public route cards and projected role-agent instructions have one active
  routing destination.
- The predecessor remains legible without competing with the canonical owner.
- Consumer-zero and compatibility evidence may make the repository
  archive-ready, but cannot archive it.
- Archiving, deleting, or renaming `aoa-routing` still requires a separate
  exact operator approval.
- Generated maps and indexes may project this posture, but do not replace the
  three owner-authored decision records.

## Verification

Run:

```bash
python scripts/generate_decision_indexes.py --check
python scripts/validate_decision_records.py
python -m unittest tests.test_decision_indexes
python -m unittest tests.test_codex_plane_regeneration
python scripts/build_workspace_memory_map.py --workspace-root /srv/AbyssOS --owner-repo-root . --check
```

These checks prove the `8Dionysus` source and generated public-entry posture.
They do not prove consumer-zero, compatibility-window exit, runtime health, or
archive authorization.
