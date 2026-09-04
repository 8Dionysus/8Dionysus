# Distinguish Historical Retirement in the Corpus Audit

## Index Metadata

- Decision ID: 8DION-D-0035
- Original date: 2026-09-04
- Surface classes: workspace audit, schema
- Route anchors: scripts/audit_agents_map.py, manifests/readme_agents_dispositions.v1.json
- Owner lanes: 8Dionysus
- Guard families: owner evidence, historical recovery
- Posture: accepted

## Status

Accepted as the integration consequence of the operator-approved Spark and
historical-tree retirement. Sibling owners retain deletion authority.

## Context

The README/AGENTS ledger previously recognized expected absence only for an
obsolete placeholder. A substantive historical document can also leave the
current checkout after owner review while remaining recoverable in Git.
Calling that document empty would misrepresent the reason for its absence.

## Options Considered

1. Misclassify historical documents as obsolete placeholders.
2. Drop their reviewed dispositions and lose the explanation for their absence.
3. Represent historical retirement separately with exact owner evidence.

## Decision

Add `retire-to-git-history` to the existing disposition vocabulary. A reviewed
record of this kind permits absence only after its evidence names the exact
owner, original file path and full 40-character Git commit, plus an immutable
decision-record reference from the same owner.

Keep `delete-obsolete-placeholder` unchanged. The integration ledger records
owner decisions; it neither authorizes deletions nor becomes an archive. No
archive directory or automatic history fetch is introduced.

The loader checks evidence shape. Actual blob recovery and review of surviving
consumers belong to owner retirement work and must be established separately.
An evidence string or a passing corpus audit alone does not prove recovery,
source validity, CI, or merge readiness.

## Consequences

- Historical README/AGENTS files can leave the active tree without losing their
  reviewed disposition or being described as empty scaffolding.
- The existing ledger retains precise source and rationale references; normal
  tree navigation need not preload their historical contents.
- The schema, corpus loader and absence check evolve together, with focused
  tests for full commit, exact path and same-owner evidence.
- Generated maps remain read models. Sibling decisions, archived content and
  current semantic contracts remain with their respective owners.
