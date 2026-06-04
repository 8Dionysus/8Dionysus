# AoA Memo MCP Codex-Plane Registration

## Index Metadata

- Decision ID: 8DION-D-0004
- Original date: 2026-05-20
- Surface classes: codex plane, MCP access, memory route
- Route anchors: .codex/config.toml, .codex/bin/aoa-memo-mcp-server.py, config/codex_plane/runtime_manifest.v1.json
- Owner lanes: 8Dionysus, abyss-stack, aoa-memo
- Guard families: access-plane boundary, projection drift, stable MCP name
- Posture: accepted

## Status

Accepted.

## Context

`aoa-memo-mcp` lives under `abyss-stack` because MCP servers are runtime access
planes, while `aoa-memo` keeps durable reviewed memory authority. Without a
stable Codex-plane name, agents can smoke-test the package manually but cannot
rely on one shared route from arbitrary workspace roots.

## Decision

Register the memory access plane as the stable MCP server name `aoa_memo` in
the shared-root Codex plane.

The checked-in `8Dionysus` manifest renders the project `.codex/config.toml`.
That config points `aoa_memo` at the shared-root launcher
`.codex/bin/aoa-memo-mcp-server.py`. The launcher resolves the stack-owned
service from `AOA_ABYSS_STACK_ROOT`, `AOA_MEMO_MCP_ROOT`, `AOA_MEMO_MCP_SERVER`,
or the default `~/src/abyss-stack` source checkout.

## Consequences

`8Dionysus` owns the Codex-plane name, projection, and drift validation.
`abyss-stack` owns the MCP service implementation. `aoa-memo` remains the
authority for reviewed memory truth; `aoa_memo` is only an access plane for
briefs, search, candidates, validation, and rehydration routes.

Future Codex-plane regeneration must preserve `aoa_memo` with the existing
stable MCP names and verify that the launcher script resolves before rollout.
