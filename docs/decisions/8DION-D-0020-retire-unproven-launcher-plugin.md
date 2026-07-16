# Retire Unproven Launcher Plugin

## Index Metadata

- Decision ID: 8DION-D-0020
- Original date: 2026-07-16
- Surface classes: skill retirement, plugin retirement, workspace projection, convergence diagnostics, clean-worktree generation
- Route anchors: .codex/plugins/aoa-shared-launchers, .agents/plugins/marketplace.json, docs/SYSTEM_CAPABILITY_MAP.md, .codex/tools/aoa_codex_converge, scripts/build_workspace_memory_map.py
- Owner lanes: 8Dionysus, aoa-skills, Dionysus, aoa-kag, agent host
- Guard families: manual baseline comparison, held-out coexistence, owner-currentness, source/projection pruning, clean-worktree source override, session-evidence isolation
- Posture: accepted; supersedes the provisional launcher hold in `8DION-D-0018`

## Status

Accepted.

## Context

`8DION-D-0018` admitted `aoa-workspace-diagnose` as the one repo-owned home
skill and left `aoa-growth-snapshot` plus `aoa-seed-route-inspect` in a
temporary explicit-only plugin pending separate owner-first audits. That hold
was intentionally not evidence of admission.

The audits compared real read-only work without a candidate skill, with the
candidate alone, and beside existing owner capabilities. Trial transcripts,
temporary homes, and task-local execution graphs remain session evidence; this
record carries only the durable owner conclusion.

## Decision

Retire both launcher candidates and remove the complete
`aoa-shared-launchers` plugin, its marketplace entry, and convergence checks
that treated the plugin as expected workspace state.

Keep `skills/aoa-workspace-diagnose/` as the only admitted `8Dionysus` home
skill and keep its exact `.agents/skills/` repository projection. General
orientation remains in route cards and KAG. Growth comparison and seed-route
inspection must be assembled from current owner surfaces, typed capabilities,
or an owner-approved playbook instead of being packaged as generic launchers.

Projection with pruning removes the retired marketplace and plugin source from
the live workspace. Do not retain an empty marketplace, plugin shell, or
warning-only convergence surface as scaffolding.

## Rationale

`aoa-seed-route-inspect` produced no material outcome improvement over the
no-skill route and added navigation cost. Its useful operations already belong
to Dionysus lineage, planting contracts, and owner inspection surfaces.

`aoa-growth-snapshot` helped on one familiar comparison but did not generalize.
In a held-out three-way comparison, no-skill, candidate-only, and composition
all trusted an obsolete checkout instead of reconciling the active owner
version. All three therefore reached the same stale lifecycle conclusion. A
single earlier win does not justify admission when the candidate fails the
next owner-currentness case.

The reusable lesson is not a new launcher. It is a shared authority rule:
before a lifecycle or status conclusion, reconcile owner identity, branch or
version, source state, and weaker derived observations. That rule belongs in
the shared authority-map capability and in retrieval/composition, not in a
public-entry plugin.

## Consequences

- `8Dionysus` has one callable home skill and no workspace launcher plugin.
- The workspace projector can prune the old marketplace and plugin tree.
- Convergence no longer warns when the retired plugin is absent.
- Workspace-memory generation accepts an explicit current `8Dionysus` checkout,
  so a clean branch can rebuild owner-derived maps without borrowing a stale or
  dirty canonical checkout; emitted refs remain workspace-relative.
- Historical decision and Git evidence remain intact; active maps no longer
  advertise provisional launchers.
- Reintroducing a plugin requires a new owner decision plus an independent
  trigger, package contract, coexistence evidence, and stable held-out value.
- The owner-currentness failure routes back to `aoa-skills` and KAG work; this
  decision does not smuggle session-local trial artifacts into either owner.

## Verification

Verify source absence, projection pruning, the admitted home-skill parity, and
convergence behavior through the existing owner checks. Then inspect a fresh
Codex prompt from `8Dionysus` and the workspace root: only the repo scope may
advertise `aoa-workspace-diagnose`, and neither retired launcher may appear.
