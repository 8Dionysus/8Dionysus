# Audit README and AGENTS as Distinct Owner Surfaces

## Index Metadata

- Decision ID: 8DION-D-0028
- Original date: 2026-08-30
- Surface classes: workspace audit, README corpus, AGENTS context, generated map
- Route anchors: scripts/audit_agents_map.py, scripts/readme_agents_corpus.py, manifests/readme_agents_dispositions.v1.json, docs/AGENTS_MAP.md
- Owner lanes: 8Dionysus, sibling owner repositories, workspace root
- Guard families: tracked corpus, owner evidence, generated-view boundary, local-ref currentness
- Posture: accepted

## Status

Accepted.

## Context

The existing AGENTS map walked the filesystem and measured only the presence of
`AGENTS.md`. In a live sibling workspace that mixed canonical repositories,
runtime projections, embedded checkouts, caches, and generated families. It
could therefore report thousands of apparent agent cards without distinguishing
tracked owner source from an installed or embedded surface.

A workspace-wide README/AGENTS review also needs to preserve two different
roles. `AGENTS.md` contributes automatically inherited local guidance, while
`README.md` normally remains an on-demand human or public route. Treating both
as interchangeable would hide prompt cost and could erase public navigation.

Future readers would not recover this boundary from a code diff alone. They
would see a larger audit payload but not why mass README-to-AGENTS migration is
rejected or why `8Dionysus` cannot decide sibling dispositions by itself.

## Options Considered

1. Move README content into nearby AGENTS files and remove the redundant files.
2. Keep the filesystem-wide AGENTS-only map and perform README review through
   one-off scripts or session notes.
3. Evolve the existing map entrypoint into a Git-tracked README/AGENTS corpus
   audit, while keeping the implementation modular and applying dispositions
   only through an owner-evidenced integration overlay.
4. Replace the AGENTS map with a separate unrelated audit command and force
   consumers to reconcile two repository lists and two checkout resolvers.

## Decision

Choose option 3.

`scripts/audit_agents_map.py` remains the public audit entrypoint and advances
to schema v2. It preserves the existing AGENTS coverage fields for current
consumers, then adds:

- Git-tracked README and AGENTS records plus separate untracked candidates;
- README/AGENTS pair posture, local document links, and declared README-read
  fanout;
- automatic AGENTS chain signatures, byte budgets, and authored versus
  generated/vendor/fixture/archive classification;
- exact local Git snapshot refs without claiming remote currentness;
- shared-root parity against the selected clean `8Dionysus` owner checkout;
- a compact disposition overlay whose reviewed entries require owner evidence.

The generated map is an integration ledger and navigation surface. It does not
decide whether a sibling file is kept, slimmed, moved, generated, or deleted.
That semantic decision remains with the repository that owns the file.

## Consequences

- Workspace counts no longer inflate when runtime or embedded trees exist
  outside the tracked owner corpus.
- README and AGENTS costs can be compared without collapsing their audiences.
- Every tracked file begins as `unreviewed`; a green generator cannot turn an
  observation into an accepted disposition.
- Embedded `.repos`, generated, fixture, and archive surfaces stay visible but
  are separable from authored chain pressure.
- The map records local `HEAD`, available `origin/main`, worktree dirtiness,
  and ahead/behind posture, but a fetch or clean owner worktree remains a
  separate prerequisite for remote-current claims and mutation.
- Existing AGENTS frontier consumers can continue reading their prior fields;
  new consumers should prefer the v2 corpus metrics for README/AGENTS work.
- Shared-root drift becomes explicit. Only surfaces admitted by the projection
  contract may be treated as projections; a similarly named root README does
  not acquire that status by convention.

## Follow-up Boundary

`8Dionysus` owns the integration tool, schema, generated view, and public route
explanation. Each sibling repository owns its file-level dispositions,
content moves, validators, and decisions. Generated indexes must be rebuilt
from this authored record, and no repository merge is implied by a complete
local census.
