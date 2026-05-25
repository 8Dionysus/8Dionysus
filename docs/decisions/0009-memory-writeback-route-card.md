# 0009 Memory Writeback Route Card

## Status

Accepted.

## Context

`aoa-memo` and local memo ports can carry reviewed memory, but a distant agent
still needs a simple operational signal for when to consider memory writeback.
Relying only on memo-specific docs makes the path easy to miss after ordinary
landings. Letting hooks decide memory-worthiness would move judgment into a
weak context and risk over-promotion.

## Options considered

1. Keep memory writeback guidance only in memo-owned docs and MCP surfaces.
2. Add hook-driven automatic candidate creation after commits, PRs, or merges.
3. Add a short shared-root route-card rule that points meaningful landings to
   the `aoa-memo-writeback` skill, while keeping durable memory authority in
   repo-local memo ports and reviewed `aoa-memo` intake.

## Decision

Choose option 3.

The shared-root `AGENTS.md` now tells agents to run a memory writeback check
after meaningful landings. Meaningful includes changes to owner boundaries,
route law, MCP or service contracts, eval or proof surfaces, release posture,
workflows, decisions, topology, public contracts, or important failures and
fixes.

The `aoa-memo-writeback` skill remains the judgment-heavy mechanism. MCP
surfaces may help it search, brief, validate, and prepare handoff packets, but
MCP and hooks do not become durable memory authority. Hooks may later provide
fail-open reminders once the route and marker semantics are stable.

## Consequences

- Agents can discover the writeback route from the shared root before they know
  the details of `aoa-memo`.
- The checked-in project-foundation skill install includes
  `aoa-memo-writeback`, so repo-local dispatch can surface the route as
  executable instead of router-only.
- A meaningful landing can end with a local memo candidate/export, a reviewed
  intake route, or an explicit no-writeback closeout.
- Future hook nudges, debt readouts, and `aoa-evals` behavior tests should
  build on this route instead of inventing their own memory capture authority.
