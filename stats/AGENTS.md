# AGENTS.md

Route card for public-entry statistical questions in `8Dionysus`.

## Applies to

Everything under `stats/`.

## Role

This directory owns statistical questions whose meaning belongs to the public
entry and workspace-audit surfaces. Shared measurement grammar and cross-owner
composition remain owned by `aoa-stats`.

## Route

Root `AGENTS.md` supplies repository boundaries. Start with
`stats/port.manifest.json`, the touched packet, and its evidence. Open only
the matching route:

- public measurement explanation: `stats/README.md`
- entrypoint denominator or owner-route change: root `README.md` and
  `docs/PUBLIC_ENTRY_POSTURE.md`
- AGENTS-map algorithm or contract:
  `generated/agents_map.min.json`, `schemas/agents-map.schema.json`, and
  `scripts/audit_agents_map.py`
- shared measurement or packet contract: `aoa-stats/stats/`

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
