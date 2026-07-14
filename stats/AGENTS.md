# AGENTS.md

Route card for public-entry statistical questions in `8Dionysus`.

## Applies to

Everything under `stats/`.

## Role

This directory owns statistical questions whose meaning belongs to the public
entry and workspace-audit surfaces. Shared measurement grammar and cross-owner
composition remain owned by `aoa-stats`.

## Read before editing

1. Root `AGENTS.md`, `README.md`, and `docs/PUBLIC_ENTRY_POSTURE.md`.
2. `stats/README.md` and `stats/port.manifest.json`.
3. `generated/agents_map.min.json`, `schemas/agents-map.schema.json`, and
   `scripts/audit_agents_map.py`.
4. The central measurement and packet contracts under `aoa-stats/stats/`.

## Boundaries

- The known public repository inventory defines the denominator; a missing
  known repository remains in that denominator as uncovered.
- Extra workspace records never enter the known-repository ratio.
- A `public-baseline` map is a synthetic lower-bound seed, not an observation.
- Duplicate, incomplete, or malformed known-repository records are unknown,
  not zero.
- Root `AGENTS.md` presence does not establish guidance quality, nested route
  coverage, repository health, remote freshness, or public onboarding quality.
- The reference packet stays weaker than its named committed AGENTS-map
  evidence and must not copy live workspace or session state.

## Validation

Inspect the committed evidence and reference packet first, then run:

```bash
python scripts/validate_local_stats_port.py
python -m unittest discover -s tests -p 'test_local_stats_port.py'
```

Use the root route for repository-wide validation.

## Closeout

Report the local question, evidence revision, manual positive and negative
cases, packet posture, central validation, and repository validation.
