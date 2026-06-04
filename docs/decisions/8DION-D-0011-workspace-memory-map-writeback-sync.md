# Workspace Memory Map Writeback Sync

## Index Metadata

- Decision ID: 8DION-D-0011
- Original date: 2026-05-26
- Surface classes: workspace memory map, generated read model, writeback marker
- Route anchors: generated/workspace_memory_map.min.json, docs/WORKSPACE_MEMORY_MAP.md, scripts/build_workspace_memory_map.py
- Owner lanes: 8Dionysus, aoa-memo
- Guard families: self-debt prevention, generated map marker, owner-routed memory
- Posture: accepted

## Status

Accepted.

## Context

`aoa-memo` landed a reviewed writeback catchup for recent memory-organ work.
That changed the stable marker route that the workspace memory map should show
for the `aoa-memo` place.

If `8Dionysus` only regenerates the map without recording its own marker, the
live writeback debt readout treats the generated sync commit as new unmarked
work in `8Dionysus`. That would leave a self-created debt tail even though the
durable memory event already landed in the owning repository.

## Decision

Use this decision as the `8Dionysus` writeback marker for the generated
workspace memory map sync.

The sync updates `generated/workspace_memory_map.min.json` and
`docs/WORKSPACE_MEMORY_MAP.md` so they point at the current `aoa-memo`
writeback marker. It does not create a separate `8Dionysus` local memo
candidate or export.

Durable memory truth for the underlying event belongs to the reviewed
`aoa-memo` objects. `8Dionysus` owns only the workspace route/readout surface
that helps distant agents discover the current marker and run the live debt
check.

## Consequences

- The workspace memory map can be regenerated after owner-repo writeback
  landings without leaving an artificial `8Dionysus` debt loop.
- The generated readout remains owner-routed: `aoa-memo` owns reviewed memory,
  while `8Dionysus` owns the public workspace map.
- Future agents should still run the live debt command before closeout; this
  marker only closes the generated-map sync itself.

## Review Log

### 2026-05-26 - Generated map sync became the marker source

- Previous assumption: each generated-map sync needed a route-only decision note
  so `8Dionysus` would not create a self-debt tail.
- New reality: the checked-in `generated/workspace_memory_map.min.json` is
  itself the stable marker for routine workspace memory map syncs.
- Reason: the generated map is the owner-owned readout being synchronized; a
  marker-only decision per refresh would add noise without improving memory
  authority or reviewability.
- Source surfaces updated: `scripts/build_workspace_memory_map.py`,
  `tests/test_workspace_memory_map.py`, `generated/workspace_memory_map.min.json`,
  and `docs/WORKSPACE_MEMORY_MAP.md`.
- Validation: `python scripts/build_workspace_memory_map.py --workspace-root
  /srv/AbyssOS --check`, `python scripts/validate_workspace_memory_map.py`,
  `python -m unittest tests.test_workspace_memory_map`, and
  `python -m unittest discover -s tests -p 'test_*.py'`.
