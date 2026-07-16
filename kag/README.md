# 8Dionysus Local KAG Provider

`kag/` exposes the current `8Dionysus` KAG provider packet as portable
source-linked records.

## Operating Card

| Field | Route |
| --- | --- |
| role | local KAG provider for public routing, workspace memory-map orientation, and the repo-owned workspace-diagnosis capability |
| records | `nodes/`, `edges/`, `indexes/`, `projections/`, `receipts/` |
| manifest | `manifest.json` |
| source route | `README.md`, `skills/README.md`, `skills/port.manifest.json`, canonical `SKILL.md`, admission decision, and workspace memory-map sources |
| consumer route | `aoa-kag` registry/composition, `abyss-stack`, MCP resources |
| owner return | `README.md` for public routing; `skills/README.md` and canonical `SKILL.md` for the local procedure |

## Record Classes

| Class | Current record |
| --- | --- |
| node | source surface and owner-return route |
| edge | source surface returns to the owner route |
| index | repository source, entity, artifact, and event indexes |
| projection | MCP-readable source-return packet |
| receipt | validation receipt for the current owner route |

Git holds compact provider records and source-return handles. Runtime graph,
vector, embedding, cache, and serving state stay with runtime owners.
The provider may expose typed capability relations for retrieval, but it does
not copy skill truth or persist task-local execution DAGs.

Validate the canonical skill home and its exact repository projection through
the pinned `aoa-skills` home-port contract before rebuilding this provider.
That structural check does not replace the manual admission evidence recorded
by the owner. Then regenerate and validate the provider with the pinned
`aoa-kag` repository-local index route.
