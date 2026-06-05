# AoA Decisions MCP Codex-Plane Registration

## Index Metadata

- Decision ID: 8DION-D-0014
- Original date: 2026-06-04
- Surface classes: codex plane, MCP access, decision route
- Route anchors: .codex/config.toml, .codex/bin/aoa-decisions-mcp-server.py, config/codex_plane/runtime_manifest.v1.json
- Owner lanes: 8Dionysus, abyss-stack, aoa-skills
- Guard families: stable MCP name, decision graph freshness, access-plane boundary
- Posture: accepted

## Status

Accepted.

## Context

`abyss-stack` owns the runnable `aoa-decisions-mcp` service and workspace
decision graph builder. `aoa-skills` owns the agent-facing skill chain that
routes decision-lane work through graph lookup before source reads or writes.

Without a stable Codex-plane server name, agents in sibling repositories can see
the skill dependency but cannot rely on one shared MCP handle for decision graph
packets.

## Decision

Register the decision-lane access plane as the stable MCP server name
`aoa_decisions` in the shared-root Codex plane.

The checked-in `8Dionysus` manifest renders the project `.codex/config.toml`.
That config points `aoa_decisions` at the shared-root launcher
`.codex/bin/aoa-decisions-mcp-server.py`. The launcher resolves the stack-owned
service from `AOA_ABYSS_STACK_ROOT`, `AOA_DECISIONS_MCP_ROOT`,
`AOA_DECISIONS_MCP_SERVER`, or the default `~/src/abyss-stack` source checkout.

## Consequences

`8Dionysus` owns the Codex-plane name, projection, launcher, and drift
validation. `abyss-stack` owns the MCP service implementation and generated
workspace graph cache. `aoa-skills` owns the agent-facing router/subskill route.

`aoa_decisions` is an access plane for status, summary, search, repo packets,
decision packets, and explicit refresh. Decision creation, correction,
supersession, and authority remain in the owning repository's source
`docs/decisions/` lane and local decision-index validators.

Future Codex-plane regeneration must preserve `aoa_decisions` with the existing
stable MCP names and verify that the launcher script resolves before rollout.
