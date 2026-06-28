# AoA KAG MCP Codex-Plane Registration

## Index Metadata

- Decision ID: 8DION-D-0015
- Original date: 2026-06-28
- Surface classes: codex plane, MCP access, KAG route
- Route anchors: .codex/config.toml, .codex/bin/aoa-kag-mcp-server.py, config/codex_plane/runtime_manifest.v1.json, scripts/smoke_aoa_kag_mcp.py
- Owner lanes: 8Dionysus, abyss-stack, aoa-kag
- Guard families: stable MCP name, KAG provider map freshness, source-return boundary, access-plane boundary
- Posture: accepted

## Status

Accepted.

## Context

`aoa-kag` now publishes a generated provider map over repo-local `kag/`
provider homes. `abyss-stack` owns the runnable `aoa-kag-mcp` service that
turns that map into MCP resources, tools, prompts, freshness diagnostics, and
source-return lookups.

Agents need one stable Codex-plane handle for KAG provider access so repository
work can inspect provider status, records, owner-return routes, and validation
posture without flattening KAG packets into prompt text.

## Options Considered

1. Use ad hoc shell or source-package CLI calls whenever KAG context is needed.
2. Register `aoa-kag-mcp` only inside `abyss-stack`.
3. Register the shared Codex-plane MCP name `aoa_kag` and verify it with the
   same source-owned launcher and smoke pattern as the other AoA MCP access
   planes.

## Decision

Choose option 3.

The checked-in `8Dionysus` Codex-plane manifest renders the stable server name
`aoa_kag` into `.codex/config.toml`. The launcher
`.codex/bin/aoa-kag-mcp-server.py` resolves the stack-owned service from
`AOA_ABYSS_STACK_ROOT`, `AOA_KAG_MCP_ROOT`, `AOA_KAG_MCP_SERVER`, or the
default `~/src/abyss-stack` source checkout.

`scripts/smoke_aoa_kag_mcp.py` verifies the stdio route, tool inventory,
resource inventory, prompt inventory, provider status, provider lookup,
freshness, source-return lookup, registry slice, composition slice, validation
status, provider map resource, readiness resource, provider manifest, and node
records.

## Consequences

`8Dionysus` owns the Codex-plane name, manifest entry, source launcher,
projection shape, smoke, and regeneration validation. `abyss-stack` owns the MCP
service implementation. `aoa-kag` owns schemas, readiness, generated provider
maps, and provider validation. Repo-local `kag/` homes own provider records and
source-return handles.

Future Codex-plane regeneration preserves `aoa_kag` with the existing stable
MCP names, and rollout checks use the smoke result as runtime evidence for the
access route.
