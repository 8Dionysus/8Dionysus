# Audit DESIGN.AGENTS Without Inherited Chain Cost

## Index Metadata

- Decision ID: 8DION-D-0033
- Original date: 2026-09-04
- Surface classes: workspace audit, AGENTS context, design documentation, generated map
- Route anchors: scripts/readme_agents_corpus.py, scripts/audit_agents_map.py, manifests/readme_agents_dispositions.v1.json, DESIGN.AGENTS.md
- Owner lanes: 8Dionysus, sibling owner repositories
- Guard families: tracked corpus, inherited context, owner review, fenced-block classification
- Posture: accepted measurement boundary; design meaning remains owner-local

## Status

Accepted.

## Context

The README/AGENTS audit intentionally distinguishes inherited `AGENTS.md`
guidance from on-demand human `README.md` surfaces. Several repositories also
carry `DESIGN.AGENTS.md`: an authored design reference describing the intended
form of agent-facing guidance. Its name and subject make it relevant to a full
agent-surface review, but Codex does not automatically inherit it as an
`AGENTS.md` route card.

Ignoring these files would leave legitimate design templates and conceptual
sequences outside the owner-review ledger. Counting them as ordinary AGENTS
would instead overstate prompt cost, chain depth, and route-card population.
A code diff alone would not preserve why the audit treats the file as related
but non-inherited.

## Options Considered

1. Treat every `DESIGN.AGENTS.md` as an inherited `AGENTS.md` and include its
   bytes in descendant chains.
2. Exclude `DESIGN.AGENTS.md` entirely because its basename is not exactly
   `AGENTS.md`.
3. Audit tracked `DESIGN.AGENTS.md` as a separate on-demand related corpus:
   require owner disposition and fenced-block review, but exclude it from
   inherited-chain bytes and exact AGENTS counts.

## Decision

Choose option 3.

The corpus scanner keeps the canonical `README.md` and exact `AGENTS.md`
counts unchanged. It separately reports tracked and untracked
`DESIGN.AGENTS.md` files, bytes, review state, and content-addressed fenced
blocks. A design fence must carry an explicit semantic classification and
reason in the owner-evidenced disposition ledger. Executable-looking
invocations and stale or missing classifications remain audit issues.

`DESIGN.AGENTS.md` contributes neither an inherited card nor chain bytes. Its
presence therefore cannot make a repository appear more expensive to enter,
nor can moving prose into it be reported as an AGENTS-chain reduction unless
the exact inherited cards also changed.

## Consequences

- All current design-agent surfaces remain visible to the 100-percent review
  census without falsifying automatic context cost.
- Canonical card templates, operating-contract templates, decision-record
  templates, diagrams, and conceptual sequences can be distinguished from
  executable procedure by content digest.
- A changed fenced block invalidates its prior declaration and requires fresh
  review; filename or language labels alone are not semantic evidence.
- Owner repositories retain design meaning and disposition authority;
  `8Dionysus` owns only the integration ledger and deterministic audit.
- README references inside exact inherited cards remain measured separately;
  design-document references do not become mandatory prompt reads merely by
  appearing in this related corpus.

## Verification

Run the focused corpus and map-audit tests, validate the disposition manifest
against its schema, regenerate the merge-bound map from the current owner
worktrees, and require zero unreviewed related files, zero unclassified or
stale active fenced blocks, and zero executable invocations in active
AGENTS/design fences before opening the merge barrier.
