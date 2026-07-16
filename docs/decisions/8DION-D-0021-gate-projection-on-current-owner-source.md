# Gate Projection on Current Owner Source

## Index Metadata

- Decision ID: 8DION-D-0021
- Original date: 2026-07-16
- Surface classes: workspace projection, source selection, owner currentness, mutation guard
- Route anchors: .codex/bin/aoa-workspace-project, scripts/project_workspace_root.py, docs/WORKSPACE_INSTALL.md
- Owner lanes: 8Dionysus, workspace root, agent host
- Guard families: owner identity, local ref alignment, managed source cleanliness, refusal before planning, explicit source override
- Posture: accepted; strengthens 8DION-D-0001 and 8DION-D-0020

## Status

Accepted.

## Context

After `8DION-D-0020` landed, projection from a clean merged checkout correctly
removed the retired launcher plugin and produced zero remaining operations. The
installed workspace launcher then selected the canonical `8Dionysus` checkout,
whose HEAD was behind the merged owner state and whose worktree carried other
ongoing changes. It proposed hundreds of rollback-looking operations, including
restoring the retired skills.

The live destination was not wrong. Source selection was wrong. A projector
that computes an accurate diff against an obsolete owner checkout can still
produce a dangerously false operational conclusion.

Raw command output and temporary worktrees remain session evidence. This record
keeps only the durable owner rule revealed by that manual negative trial.

## Decision

Treat projection source identity and currentness as prerequisites, not metadata
added after diff planning.

The installed `aoa-workspace-project` launcher must refuse before planning when:

- the selected source is not a Git worktree;
- its HEAD does not match the declared local source reference, normally
  `origin/main`;
- the reference is unavailable; or
- projector control code or a source path managed by the projection is dirty.

The launcher remains local-only and does not fetch, reset, checkout, clean, or
otherwise mutate the source. Matching `origin/main` proves alignment only with
the available local ref; the operator or owner workflow remains responsible for
refreshing that ref before making a remote-currentness claim.

Support `--source-root` so a clean merged checkout can be selected explicitly
when the canonical checkout is stale or carrying unrelated work. Excluded
owner surfaces such as `.agents/skills`, `.codex/config.toml`, and
`.codex/agents` do not make the shared-root source dirty, because this projector
does not own them.

Direct dry-run inspection of a branch remains available. Direct execution from
a source that fails the currentness gate requires the visible
`--allow-noncurrent-source` override and is evidence of a reviewed branch trial,
not evidence that the branch is current owner truth.

## Rationale

Currentness cannot be inferred from path convention, repository name, a green
destination check, or a syntactically valid operation plan. Owner identity,
selected checkout, commit/ref alignment, and relevant worktree state must agree
before the system treats a projection plan as actionable.

Refusal before planning is important: showing a large stale-source diff and
merely attaching a warning still invites an agent or operator to apply the
wrong rollback. The safe result is zero planned operations plus an explicit
source-reconciliation route.

## Consequences

- The installed launcher cannot silently restore retired shared-root content
  from a known stale owner checkout.
- A dirty canonical checkout no longer forces destructive cleanup or loss of
  unrelated work; a clean current checkout can be selected explicitly.
- Source-currentness reports expose the selected local ref, both commits,
  relevant dirty paths, and the fact that no network refresh was performed.
- Projection drift and source-currentness failure become distinct outcomes.
- Tests protect the real failure boundary: excluded owner paths remain allowed,
  while managed source drift and stale HEAD/ref alignment refuse before live
  mutation.

## Verification

Manually exercise both sides after landing:

1. invoke the installed launcher against a stale canonical checkout and confirm
   refusal with zero operations;
2. invoke it with `--source-root` pointing at a clean checkout whose HEAD matches
   refreshed `origin/main`, and confirm a clean projection check;
3. make a managed source dirty in an isolated fixture and confirm live execution
   refuses without changing the destination;
4. confirm excluded `.agents/skills`, `.codex/config.toml`, and `.codex/agents`
   changes do not falsely transfer their ownership to this projector.
