# 8Dionysus local stats port

This directory exposes statistical questions whose domain meaning belongs to
the public entry and workspace-audit owner. It uses the shared `aoa-stats`
grammar without moving public route or AGENTS-map authority into the central
organ.

## Current reference measurement

| Measurement | Question | Reference value |
| --- | --- | --- |
| `8Dionysus/known-repository-root-agents-coverage-ratio` | What fraction of known public repositories have an observed root `AGENTS.md` route in the committed live-workspace map? | `16 / 16` at evidence revision `4506bf51ae8c0b1ee8f87d3c7740b3224b75544b` |

The denominator is every name in the map's `known_repositories` inventory.
A known repository whose checkout is missing remains in the denominator as
uncovered. Extra workspace records are excluded. A synthetic
`public-baseline` map, duplicate record, incomplete population, or malformed
root-presence field makes the measurement unknown rather than zero.

## Evidence posture

The packet is a public reference snapshot derived from the already committed
`generated/agents_map.min.json`. It is not a live workspace scan and does not
carry paths, raw guidance, or session state.

## Authority

The ratio reports root route-card presence only. It does not validate guidance
content, nested coverage, repository health, owner availability, current remote
state, projection parity, or onboarding quality.

## Surfaces

- `port.manifest.json` declares the owner-local question and measurement.
- `packets/known-repository-root-agents-coverage-ratio.reference.json` records
  the evidence-linked reference observation.
- `generated/agents_map.min.json` remains the immediate evidence owner.
- `aoa-stats` owns the shared contract validator and cross-owner composition.
