# 0010 Workspace Writeback Marker Debt Surface

## Status

Accepted.

## Context

The shared-root route card now tells agents to run a memory writeback check
after meaningful landings. That solves discovery, but it does not yet give an
agent a reproducible surface for seeing whether a place has a visible
writeback marker or whether git currentness needs a live debt check.

The workspace memory map already owns route-level memory status. Adding a
separate static document would split the operational map and make future agents
guess which surface is current.

## Options considered

1. Keep writeback debt as prose in the route card.
2. Store live git `HEAD` and commit counts directly in the checked-in generated
   workspace memory map.
3. Extend the workspace memory map with stable marker routing, and add a live
   debt JSON output for git currentness.

## Decision

Choose option 3.

`8Dionysus` extends `generated/workspace_memory_map.min.json` and
`docs/WORKSPACE_MEMORY_MAP.md` with writeback marker and debt routing fields.
The checked-in map records stable marker sources such as repo-local memo
packets and decision records with `writeback` in the filename. It also records
the live command agents should run when they need git currentness:

```bash
python scripts/build_workspace_memory_map.py \
  --workspace-root <workspace-root> \
  --writeback-debt-json
```

The live output may report `clean`, `has_unmarked_changes`,
`needs_first_marker`, `not_applicable`, or `unknown`. These statuses are
routing signals only.
Memory-worthiness remains a judgment step owned by `aoa-memo-writeback`; durable
memory still lands through local memo ports and reviewed `aoa-memo` intake.

## Consequences

- A distant agent can inspect one existing workspace map and learn both where
  memory routes live and how to run a writeback debt check.
- The checked-in generated map avoids self-invalidating `HEAD` and commit-count
  fields.
- Hooks can later nudge agents toward this surface without becoming memory
  authority.
- `aoa-evals` can test whether agents use the marker/debt route correctly
  without owning capture or durable memory.

## Review Log

### 2026-05-26 - First Marker Activation Is Not Post-Marker Debt

- Previous status language used `needs_marker` for every routed place with no
  marker source.
- New status language uses `needs_first_marker` for that case and preserves
  `has_unmarked_changes` for real post-marker git currentness debt.
- Reason: a missing first marker means the memory route needs activation and
  owner judgment; it does not prove that a local memo candidate, export, or
  route-only decision should be created.
- The live readout now carries `first_marker_route` so distant agents can see
  whether the next honest move is local memo-port activation, route-only owner
  decision, session-evidence review, or workspace-plane route decision.
