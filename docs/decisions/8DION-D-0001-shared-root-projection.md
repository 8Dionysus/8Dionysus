# Shared-Root Projection Lives in 8Dionysus

## Index Metadata

- Decision ID: 8DION-D-0001
- Original date: 2026-04-11
- Surface classes: shared-root projection, public entry, workspace install
- Route anchors: AGENTS.md, AOA_WORKSPACE_ROOT, .agents, .codex, scripts/project_workspace_root.py
- Owner lanes: 8Dionysus, workspace root, sibling owner repos
- Guard families: projection source truth, owner boundary, drift preview
- Posture: accepted; skill-projection clause superseded by 8DION-D-0017

## Context

The live AoA / ToS workspace root under `/srv/AbyssOS` carries a small set of shared
install surfaces that agents and local tooling rely on directly:

- `AGENTS.md`
- `AOA_WORKSPACE_ROOT`
- `.agents/`
- `.codex/`

Those surfaces are not the source of truth for the meanings owned by
`aoa-skills`, `aoa-agents`, `aoa-sdk`, `Dionysus`, or other owner repositories.
But the live workspace still needs one explicit source-owned place where the
deployed root copies can be reviewed, updated, and projected from.

## Options considered

1. treat the live `/srv/AbyssOS` root as the only authoritative copy
2. keep copying root surfaces back into `8Dionysus` by hand
3. keep source-owned copies in `8Dionysus` and project them into the live workspace root with an explicit tool

## Decision

Choose option 3.

`8Dionysus` owns the selected shared-root install surfaces as deployable source
copies for the current workspace layout, and it ships the projection tool that
syncs them into the live workspace root.

Projection details:

- `AGENTS.md` is rendered from the source file in `8Dionysus` by replacing
  `<workspace-root>` with the target live root
- `AOA_WORKSPACE_ROOT` projects as a direct file copy
- `.agents/` projects as a workspace install surface, while `.agents/skills/`
  still remains an installed projection of `aoa-skills`
- `.codex/` projects as the project-level Codex install surface
- `.codex/generated/`, `__pycache__/`, and compiled Python artifacts stay
  deploy-local and do not project back into `8Dionysus` as source truth

## Consequences

- workspace-root drift can be previewed or checked explicitly before mutation
- the projection path becomes reviewable and repeatable instead of oral lore
- `8Dionysus` still does not absorb owner-layer authority away from the
  repositories whose meanings these install surfaces help route into
- the checked-in `.agents/` and `.codex/` trees are honest for the current live
  workspace deployment and must be adapted if the root path changes

## Partial Supersession

`8DION-D-0017` supersedes only the `.agents/skills/` clause of this decision.
`8Dionysus` still owns the selected root guidance, marker, plugin discovery,
and Codex-plane projection, but shared AoA bundles now install once at user
scope and repository projections come only from admitted owner-local homes.
