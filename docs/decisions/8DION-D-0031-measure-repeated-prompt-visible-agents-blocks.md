# Measure Repeated Prompt-Visible AGENTS Blocks

## Index Metadata

- Decision ID: 8DION-D-0031
- Original date: 2026-08-31
- Surface classes: workspace audit, AGENTS context, local-delta quality
- Route anchors: scripts/readme_agents_corpus.py, scripts/audit_agents_map.py, docs/AGENTS_MAP.md
- Owner lanes: 8Dionysus, sibling owner repositories
- Guard families: repeated prose, inherited context, fenced-example exclusion, owner review
- Posture: accepted measurement; owner disposition remains local

## Status

Accepted.

## Context

The README/AGENTS corpus audit measured inherited chain bytes and mandatory
README reads, but it could not distinguish a genuinely local route card from a
smaller-looking template copied into dozens of sibling cards. During the full
owner pass, several repositories reduced executable fences while increasing
total AGENTS bytes by repeating the same long validation, reading-order, or
closeout paragraph across many files.

A future reader looking only at per-file size or chain percentiles would miss
that prompt-visible duplication and could accept a mechanically transformed
corpus that still violates the local-delta model.

## Options Considered

1. Keep duplicate detection as a one-off session script.
2. Treat any repeated line or short stop-line as an error.
3. Add a conservative exact-block measurement to the existing owner audit,
   excluding fenced examples and leaving semantic disposition with each owner.

## Decision

Choose option 3.

The audit normalizes prose blocks outside fenced examples and reports a block
when the exact normalized text is at least 180 bytes and occurs in at least
four tracked `AGENTS.md` files in one repository. It records group count,
occurrence count, normalized redundant bytes beyond the first copy, exact
fingerprints, paths, and authored-versus-excluded scope.

The threshold is a conservative review signal, not a universal prohibition.
It avoids turning short safety phrases, headings, or example commands into
noise while making systemic copied routers visible. A finding does not grant
`8Dionysus` authority to rewrite sibling meaning; the owner must either lift
shared law to an inherited parent, retain a justified local exception, or
replace the template with real local delta.

## Consequences

- final corpus review can observe template bloat that chain percentiles alone
  hide;
- fenced examples do not create false prompt-prose findings;
- exact fingerprints keep the signal deterministic and reproducible;
- owner-specific semantic exceptions remain possible and must be evidenced;
- generated maps gain a new review dimension without becoming sibling truth.

## Verification

Run the focused corpus tests, validate the generated map schema, regenerate
the clean-worktree matrix map, and inspect every remaining authored repeated
block group before opening the merge barrier.
