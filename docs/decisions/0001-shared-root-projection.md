# Decision 0001: Shared-Root Projection Lives in 8Dionysus

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
