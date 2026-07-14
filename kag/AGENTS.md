# AGENTS.md

## Applies to

This card applies to `8Dionysus/kag/` and every nested path until a nearer card
narrows the lane.

## Role

`kag/` is the local KAG provider home for `8Dionysus`. It exposes compact,
source-linked records over the public ecosystem profile and workspace memory map
for `aoa-kag` registry, composition, and MCP consumers.

## Read before editing

Read the root `AGENTS.md`, this card, `kag/README.md`, `kag/manifest.json`,
`README.md`, `stats/README.md`, `docs/WORKSPACE_MEMORY_MAP.md`, and
`generated/workspace_memory_map.min.json` before changing provider records.

## Boundaries

Keep authored ecosystem meaning with the owning source repositories named by the
profile map. Keep shared KAG schema, registry, composition, and provider
validation with `aoa-kag`. Keep runtime serving state with `abyss-stack` or the
runtime owner named by the consumer.

## Validation

Use the owner validator named in `manifest.json`, then validate this provider
through the `aoa-kag` local subtree validator.

## Closeout

Report provider records changed, source-return route changed, owner validation,
`aoa-kag` validation, and the next MCP consumer route.
