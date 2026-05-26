# 0012 Reviewed Memory Landing Receipts As Writeback Markers

## Status

Accepted.

## Context

The workspace writeback debt surface originally recognized local memo-port
packets and repo-local decision records with `writeback` in the filename as
stable marker sources.

That was enough for route-only and local-port repos, but it left `aoa-memo`
looking stale immediately after a reviewed intake landing. In that case the
durable memory event has already landed in the reviewed corpus, and the
landing receipt is a stronger marker than an extra decision note that only says
the same landing happened.

## Options considered

1. Keep adding a new `aoa-memo/docs/decisions/*writeback*.md` marker after each
   reviewed landing.
2. Treat any generated object-surface update as a writeback marker.
3. Treat reviewed intake landing receipts with `result: landed` as writeback
   markers for the reviewed memory corpus owner.

## Decision

Choose option 3.

`scripts/build_workspace_memory_map.py` now recognizes
`memo/intake/receipts/*.json` files whose schema is
`aoa_memo_reviewed_intake_landing_receipt_v1` and whose `result` is `landed`.
Those receipts produce `reviewed_memory_landing_receipt` markers with the
`reviewed_write` decision.

The workspace map still does not become memory authority. The receipt points to
the durable reviewed-memory event; `aoa-memo` owns the reviewed corpus, and
`8Dionysus` owns only the workspace route/readout that tells distant agents
where the marker is and how to run the live debt check.

## Consequences

- Reviewed memory landings can close their own writeback-currentness loop
  without an extra marker-only decision note in `aoa-memo`.
- `reviewed_write` becomes an explicit writeback decision value in the
  workspace map taxonomy.
- The map remains reproducible from checked-in owner surfaces instead of
  inferring reviewed-memory currentness from generated object diffs alone.
- Future marker sources should be added only when they are stable evidence of
  an owner-reviewed memory route, not just convenient changed files.
