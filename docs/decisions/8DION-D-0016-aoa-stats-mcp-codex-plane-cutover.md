# AoA Stats MCP Codex-Plane Cutover

## Index Metadata

- Decision ID: 8DION-D-0016
- Original date: 2026-07-14
- Surface classes: codex plane, MCP access, stats route
- Route anchors: .codex/config.toml, .codex/bin/aoa-stats-mcp-server.py, config/codex_plane/runtime_manifest.v1.json, scripts/smoke_aoa_stats_mcp.py
- Owner lanes: 8Dionysus, abyss-stack, aoa-stats
- Guard families: stable MCP name, statistical authority boundary, access-plane separation, single registration
- Posture: accepted

## Status

Accepted.

## Context

The shared Codex plane already exposed the stable name `aoa_stats`, but it
started the repo-local server inside `aoa-stats`. The federated measurement
boundary now keeps statistical meaning and its public read contract in
`aoa-stats` while placing the runnable MCP package and transport lifecycle in
`abyss-stack`.

Without a source-projection decision here, later regeneration could silently
restore the old implementation owner even after the runtime cutover. A commit
message or smoke alone would show the changed path but not preserve why the
stable name crosses three owner lanes.

## Options Considered

1. Keep the repo-local server behind `aoa_stats`.
2. Introduce a second MCP name for the stack-owned service and migrate callers
   gradually.
3. Preserve `aoa_stats` and route it through a shared-root wrapper to the
   stack-owned package.

## Decision

Choose option 3.

The checked-in Codex-plane manifest keeps the stable name `aoa_stats` and
points it at `.codex/bin/aoa-stats-mcp-server.py`. The wrapper resolves only
the runnable `abyss-stack/mcp/services/aoa-stats-mcp/` package; it does not
implement statistical reads or duplicate the `aoa-stats` contract.

The source registration uses the wrapper for portable stdio. A deployed
runtime may replace that source form with the authenticated loopback endpoint
owned by `abyss-stack`, while retaining the same project-facing name and one
active registration.

This record decides only the `8Dionysus` projection consequence. Statistical
semantics remain governed by
`aoa-stats:docs/decisions/AOST-D-0012-federated-measurement-ownership-and-thin-access.md`;
the runnable service remains governed by
`abyss-stack:docs/decisions/ABYSS-STACK-D-0078-federated-stats-mcp-access-plane.md`.

## Consequences

- `8Dionysus` owns the stable Codex-plane name, source wrapper, projection,
  convergence posture, and stdio smoke.
- `abyss-stack` owns service implementation, installation, authenticated
  transport, diagnostics, and lifecycle.
- `aoa-stats` owns statistical grammar, compatibility, owner inventory,
  derived views, and the transport-neutral read contract.
- Owner repositories keep their local questions, measurements, evidence,
  privacy, and freshness meaning.
- The old repo-local server is not a second valid convergence path. It is
  removed after the live consumer cutover proves the stack-owned path.
