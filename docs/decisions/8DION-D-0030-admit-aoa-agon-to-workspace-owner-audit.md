# Admit aoa-agon to the Workspace Owner Audit

## Index Metadata

- Decision ID: 8DION-D-0030
- Original date: 2026-08-31
- Surface classes: workspace audit, owner route, public-entry boundary
- Route anchors: AGENTS.md, scripts/audit_agents_map.py, generated/agents_map.min.json
- Owner lanes: 8Dionysus, aoa-agon, Agents-of-Abyss, aoa-models
- Guard families: owner coverage, audit completeness, publication boundary
- Posture: accepted workspace-owner route; public publication deferred

## Status

Accepted.

## Context

`aoa-agon` now owns governed model-formation lineage, candidate causality,
material governance, and scoped lineage-continuation decisions. The
`8Dionysus` README/AGENTS corpus audit was created before that owner existed and
therefore could report a complete known-owner census while silently omitting
its documents.

The local owner repository currently has no public remote. Treating its
workspace existence as proof of public publication would be as misleading as
omitting it from the local audit.

## Options Considered

1. Leave `aoa-agon` as an extra, unowned checkout until it is published.
2. Add it to every public route and GitHub link immediately.
3. Admit it to the required workspace owner audit and internal route map while
   keeping the dated public-baseline set and public links unchanged until
   publication is separately evidenced.

## Decision

Choose option 3.

Add `aoa-agon` to the required live-workspace owner set used by
`scripts/audit_agents_map.py` and to the root internal owner route. Keep the
dated public-baseline repository set separate and unchanged. Do not add a
GitHub/public README link, required-check contract, or publication claim until
an observable remote and an owner-approved public posture exist.

`aoa-agon` remains narrower than both neighboring owners: `Agents-of-Abyss`
retains center Agon pressure and contest law, while `aoa-models` retains
accepted model identity and realization truth.

## Consequences

- live and merge-bound corpus scans can no longer call themselves complete
  while omitting `aoa-agon`;
- missing `aoa-agon` is a required-owner audit failure, unlike the optional
  deprecated `aoa-routing` checkout;
- the historical public baseline remains comparable at twenty repositories;
- public navigation does not advertise an unobserved repository endpoint;
- generated workspace maps must be rebuilt from the expanded owner source.

## Verification

Regenerate decision indexes, run the agent-map audit tests, scan the final
clean-worktree matrix, and rebuild the generated AGENTS and workspace-memory
maps. Local audit inclusion is not public publication, remote currentness,
release admission, or merge evidence.
