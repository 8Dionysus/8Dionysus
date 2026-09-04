# Project a Dedicated Workspace-Root README

## Index Metadata

- Decision ID: 8DION-D-0029
- Original date: 2026-08-30
- Surface classes: shared-root projection, human entrypoint, public profile boundary, README corpus
- Route anchors: docs/WORKSPACE_ROOT_ENTRY.md, README.md, scripts/project_workspace_root.py, scripts/readme_agents_corpus.py
- Owner lanes: 8Dionysus, workspace root, sibling owner repositories
- Guard families: source-first projection, human navigation, prompt-context boundary, owner parity
- Posture: accepted; extends 8DION-D-0001 and partially supersedes the shared-root README observation in 8DION-D-0028

## Status

Accepted.

## Context

The live sibling workspace has a root `README.md` with a real human and
operator orientation function. Removing it would make the workspace less
legible, but its existing copy has no admitted projection source and has
drifted from the current `8Dionysus` public profile.

The repository `8Dionysus/README.md` cannot simply become that source. It is a
GitHub-facing profile page with profile assets, public presentation, and a
different audience. Projecting it would couple local workspace navigation to
profile layout and would erase the distinction between public entry and live
workspace entry.

Future readers need to know why the root README remains while README content
is not moved into automatically inherited `AGENTS.md` guidance, and why the
profile README is still excluded from projection.

## Options Considered

1. Delete the live root README because it is not currently source-owned.
2. Project `8Dionysus/README.md` directly into the workspace root.
3. Keep the live file as an unmanaged local convention and record only its
   audit drift.
4. Add a dedicated authored workspace-entry source and project it to the live
   root while leaving the profile README independent.

## Decision

Choose option 4.

`8Dionysus/docs/WORKSPACE_ROOT_ENTRY.md` is the authored human-entry source.
The workspace projector renders it to `<workspace-root>/README.md`, including
the same `<workspace-root>` substitution used by the root route card.

`8Dionysus/README.md` remains profile-owned, GitHub-facing, and outside the
shared-root projection. The projected workspace README remains on-demand human
orientation; it is not added to mandatory agent reading or used as semantic
authority for sibling repositories.

The README/AGENTS corpus audit must compare the live root README with the
dedicated workspace-entry source and report it as an admitted projection.

## Rationale

- preserves a useful root human entrypoint without making an unmanaged file
  canonical;
- keeps public profile presentation independent from local workspace layout;
- makes root drift reproducible and owner-reviewable;
- preserves the central README/AGENTS role split: human understanding stays in
  README, while AGENTS carries routing and stop-lines only;
- avoids copying sibling doctrine into either root document.

## Consequences

- the shared-root projector gains one small rendered file surface;
- projection source-currentness now includes the dedicated workspace-entry
  source;
- the live root README may be regenerated and checked instead of hand-edited;
- shared-root corpus parity becomes meaningful for both README and AGENTS;
- changes to public profile visuals, stack notes, or GitHub statistics do not
  churn the local workspace entrypoint;
- owner repositories remain authoritative for every concrete route and
  guarantee named by the entrypoint.

## Supersession Boundary

This decision extends the selected surface list in `8DION-D-0001`; it does not
project the profile README. It supersedes only the `8DION-D-0028` observation
that the similarly named live root README is not an admitted projection. The
0028 distinction between human README surfaces and inherited AGENTS context
remains active.

## Source and Follow-up

Owner source surfaces:

- `docs/WORKSPACE_ROOT_ENTRY.md`
- `scripts/project_workspace_root.py`
- `scripts/readme_agents_corpus.py`
- `docs/WORKSPACE_INSTALL.md`

Generated decision indexes and the workspace corpus map must be rebuilt from
these authored surfaces. Live projection is a later deployment action and does
not make an unmerged branch owner-current.
