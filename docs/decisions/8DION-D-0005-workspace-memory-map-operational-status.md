# Workspace Memory Map Tracks Operational Memory Status

## Index Metadata

- Decision ID: 8DION-D-0005
- Original date: 2026-05-22
- Surface classes: workspace memory map, generated read model, memory route
- Route anchors: generated/workspace_memory_map.min.json, docs/WORKSPACE_MEMORY_MAP.md, scripts/build_workspace_memory_map.py
- Owner lanes: 8Dionysus, aoa-memo, local memo ports
- Guard families: generated route, memory authority boundary, operational status
- Posture: accepted

## Context

The workspace memory overlay has pilot full ports, route-only repositories, and
an `aoa-memo` reviewed corpus district. A simple "has `memo/`" map was no
longer enough: agents need to know whether local memory contains pending
candidates, blocked exports, ready exports, or exports already landed in
`aoa-memo`.

## Options considered

1. Keep the map as a coarse route/presence inventory.
2. Treat every `memo/` directory as the same kind of local port.
3. Keep the map route-first, but add operational counts and distinguish
   reviewed corpus districts from local memo ports.

## Decision

Choose option 3.

`8Dionysus` keeps the generated workspace memory map as a shared-root
navigation and status surface. The map now tracks pending candidates, total
exports, blocked exports, ready exports, landed exports, and the validation
command for each place. It treats `aoa-memo/memo/` as a reviewed corpus
district, not as a broken local port.

## Consequences

- Agents can inspect workspace memory status before deciding where to read,
  write, validate, or land memory.
- The map remains a derived navigation surface and does not replace
  `aoa-memo`, local `memo/PORT.yaml`, MCP results, or owner repository truth.
- Repositories awaiting deeper refactor can remain route-only or stub-port
  without pretending to have mature memory topology.
- The map becomes useful for rollout planning because pending and landed
  memory routes are visible at workspace scale.
