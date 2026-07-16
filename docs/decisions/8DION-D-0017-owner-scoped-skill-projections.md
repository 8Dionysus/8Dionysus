# Owner-Scoped Skill Projections

## Index Metadata

- Decision ID: 8DION-D-0017
- Original date: 2026-07-16
- Surface classes: shared-root projection, skill installation, owner home, Codex context
- Route anchors: .agents, .agents/skills, docs/WORKSPACE_INSTALL.md, scripts/project_workspace_root.py, aoa workspace bootstrap
- Owner lanes: 8Dionysus, aoa-skills, aoa-sdk, sibling repositories, agent host
- Guard families: single projection, owner scope, no hidden activation, context budget, reviewed migration
- Posture: accepted; partially supersedes 8DION-D-0001

## Status

Accepted.

## Context

The original shared-root projection copied a broad AoA skill profile into
`<workspace-root>/.agents/skills/`, while many sibling repositories carried
another copy under their own `.agents/skills/`. The host catalog therefore
loaded stale near-duplicates from whichever directory was nearest, consumed
the prompt discovery budget, and could expose two different `aoa-decision`
bundles at once.

The current `aoa-skills` owner contract has seven shared callable bundles but
advertises only the reviewed `aoa-decision` family for default use. It also
states that repository-specific procedures remain in the owning repository's
top-level `skills/` home. The current `aoa-sdk` can inspect those contracts and
install an exact user profile, but no longer selects, activates, dispatches, or
installs repository projections.

Keeping the older projection topology would preserve a runtime shape that the
skill owner and SDK no longer claim.

## Options Considered

1. Keep copying the shared profile into the workspace root and every sibling
   repository.
2. Keep one shared workspace-root projection and remove only sibling copies.
3. Install the advertised shared profile once at user scope, and allow a
   repository projection only from that repository's admitted home-skill
   source.

## Decision

Choose option 3.

The shared `aoa-skills` `user-default` profile installs once into the
host-selected user skill root, normally `${CODEX_HOME:-$HOME/.codex}/skills`.
`8Dionysus` continues to project root guidance, the workspace marker, plugin
discovery, and the Codex plane, but excludes `.agents/skills/` from both copy
and prune authority.

A sibling repository may introduce top-level `skills/` only after the owner
admits a procedure with an independent trigger, input and output ABI,
composition value, and manual evidence of benefit. Any repo-local
`.agents/skills/` is a derived projection of that owner home, not a copy of the
shared AoA catalog. Deferred shared bundles remain available for explicit
research and comparison without becoming implicitly active.

Semantic retrieval and composition belong to KAG and a task-local execution
DAG. SDK inspection remains exact and passive. Risky mutation remains governed
by the owner contract and explicit host or human confirmation rather than a
skill-runtime gate.

## Consequences

- the normal host catalog carries one advertised shared AoA bundle instead of
  competing workspace and repository copies
- `8Dionysus/.agents/` owns plugin and companion projection surfaces, not
  shared skill truth
- old workspace and repository copies require a reviewed, reversible cleanup;
  their path alone is not permission to delete them
- owner-local procedures can evolve without being copied into `aoa-skills`
- repository projection builders must preserve exact owner provenance and may
  not install an unadmitted shared profile as a shortcut
- cross-host installs select and verify the user skill root explicitly
- prompt visibility, coexistence, and no-skill behavior must be checked in the
  real host; projection validators prove only file and boundary invariants

## Supersession

This decision supersedes the `.agents/skills/` portion of `8DION-D-0001`.
The remaining shared-root projection decision stays active.
