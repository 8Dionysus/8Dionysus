# Measure Validation Command Ownership

## Index Metadata

- Decision ID: 8DION-D-0032
- Original date: 2026-09-04
- Surface classes: workspace audit, validation procedure, README/AGENTS context
- Route anchors: scripts/readme_agents_corpus.py, scripts/audit_agents_map.py, docs/AGENTS_MAP.md
- Owner lanes: 8Dionysus, sibling owner repositories
- Guard families: command ownership, procedure duplication, authored-surface exclusion, owner review
- Posture: accepted measurement; command disposition and exceptions remain owner-local

## Status

Accepted.

## Context

The README/AGENTS migration reduced inherited command blocks by moving exact
procedure into on-demand validation surfaces. A later census showed that this
could make the prompt lighter while copying one executable invocation into
several parent and child `VALIDATION.md` files. File counts and AGENTS chain
bytes do not expose that ownership drift.

`Agents-of-Abyss` decision `AOA-CENTER-D-0043` establishes the portable design:
one human-authored procedure owner for an exact executable invocation inside a
repository, with other validation surfaces routing to that owner. `8Dionysus`
does not own sibling commands or exceptions, but its integration audit needs a
deterministic signal showing where owner review is still required.

## Options Considered

1. Keep validation-command inspection as a one-off session script.
2. Make `8Dionysus` choose and rewrite the canonical command owner in every
   sibling repository.
3. Extend the existing local-worktree corpus audit with repository-local exact
   command grouping and README/AGENTS overlap signals, while leaving semantic
   disposition with each sibling owner.

## Decision

Choose option 3.

For every scanned repository, the audit reads current tracked and untracked
`VALIDATION.md` candidates from the local Git worktree. It extracts normalized
executable-looking invocations from shell, console, terminal, plain-text, and
unlabelled fences and reports:

- active authored validation-file, invocation, and unique-invocation counts;
- exact command groups occurring more than once inside that repository;
- redundant occurrences beyond the first;
- exact overlaps with executable fences in active authored `AGENTS.md` and
  `README.md` surfaces.

Generated, vendor, fixture, and archive validation surfaces are excluded from
the ownership count. Untracked validation candidates remain explicit so a
prepared migration cannot appear clean merely because it has not been staged.
The boundary is repository-local: identical argv in independent owner
repositories do not imply shared authority.

An AGENTS overlap is an audit issue because inherited route cards must not own
executable procedure. A README overlap is a review signal rather than an
automatic error: public usage examples may be legitimate, while required
verification must route to the owner procedure. Exact grouping is a lower
bound and does not claim that different wrappers or argv are semantically
distinct.

## Consequences

- The generated map can show prompt reduction and procedure-ownership quality
  as separate dimensions.
- Owner review can identify parent/child command copies without storing a
  federation-wide command authority.
- The compact map records only duplicate and overlap groups, not every unique
  command body.
- A zero exact-duplicate count does not replace owner review, command
  conservation, focused tests, CI, or release evidence.
- Labelling a procedural fence as `text` or leaving its language blank does not
  exempt an executable-looking invocation from ownership measurement.
- Sibling owners choose the survivor, route shape, exception, manifest, runner,
  validator, and generated updates for their own repositories.

## Verification

Run the focused corpus and map-audit tests, validate the generated map schema,
regenerate the merge-bound map from the current owner-worktree matrix, and
inspect every remaining duplicate or overlap group before opening the merge
barrier.
