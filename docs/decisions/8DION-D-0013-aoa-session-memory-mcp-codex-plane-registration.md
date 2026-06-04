# AoA Session Memory MCP Codex-Plane Registration

## Index Metadata

- Decision ID: 8DION-D-0013
- Original date: 2026-06-04
- Surface classes: codex plane, MCP access, session evidence route
- Route anchors: .codex/config.toml, .codex/bin/aoa-session-memory-mcp-server.py, config/codex_plane/runtime_manifest.v1.json, scripts/smoke_aoa_session_memory_mcp.py
- Owner lanes: 8Dionysus, abyss-stack, .aoa
- Guard families: access-plane boundary, read-only session evidence, stable MCP name
- Posture: accepted

## Status

Accepted.

## Context

`.aoa` owns raw session transcripts, segment indexes, generated atlas maps,
search surfaces, route-readiness diagnostics, and reviewed distillation
boundaries. Agents can inspect those surfaces manually, but recurring work like
debugging a skill, MCP, hook, tool, path, goal, or repeated failure needs one
stable Codex-plane route that returns evidence refs instead of flattened
summaries.

`abyss-stack` owns the runnable `aoa-session-memory-mcp` service package. The
service is intentionally read-only: it routes through `.aoa` search, maps,
session briefs, retrieval packets, evidence packets, freshness checks, latest
diagnostics, and maintenance planning without running write, repair, reindex,
distillation, export, or promotion commands.

## Decision

Register the session-evidence access plane as the stable MCP server name
`aoa_session_memory` in the shared-root Codex plane.

The checked-in `8Dionysus` manifest renders the project `.codex/config.toml`.
That config points `aoa_session_memory` at the shared-root launcher
`.codex/bin/aoa-session-memory-mcp-server.py`. The launcher resolves the
stack-owned service from `AOA_ABYSS_STACK_ROOT`, `AOA_SESSION_MEMORY_MCP_ROOT`,
`AOA_SESSION_MEMORY_MCP_SERVER`, or the default `~/src/abyss-stack` source
checkout.

## Consequences

`8Dionysus` owns the Codex-plane name, projection, launcher, smoke check, and
drift validation. `abyss-stack` owns the MCP service implementation. `.aoa`
remains the authority for raw evidence, generated route surfaces, freshness,
and reviewed distillation boundaries.

Agents may use `aoa_session_memory` as the first compact route for
session-evidence investigation, but MCP output remains a ref-bearing access
packet, not reviewed truth. Future Codex-plane regeneration must preserve
`aoa_session_memory` with the existing stable MCP names and verify that the
launcher script resolves before rollout.
