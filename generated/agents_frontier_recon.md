# AGENTS frontier reconnaissance

This report ranks remaining high-risk directories that may need local `AGENTS.md` guidance.
It is a reconnaissance surface, not repository doctrine, and it does not overrule the nearest `AGENTS.md`.

## Totals

- `candidate_count`: 37
- `p0_candidates`: 8
- `p1_candidates`: 16
- `p2_candidates`: 13
- `p3_candidates`: 0
- `repos_with_candidates`: 12
- `repositories_listed`: 21

## Top candidates

| Priority | Score | Repository | Path | Decision | Rationale |
|---|---:|---|---|---|---|
| P0 | 108 | `abyss-stack` | `schemas/AGENTS.md` | `add-local-agents` | schema edits are contract edits |
| P0 | 94 | `Dionysus` | `schemas/AGENTS.md` | `add-local-agents` | schema edits are contract edits |
| P0 | 94 | `aoa-agon` | `schemas/AGENTS.md` | `add-local-agents` | schema edits are contract edits |
| P0 | 94 | `aoa-models` | `schemas/AGENTS.md` | `add-local-agents` | schema edits are contract edits |
| P0 | 92 | `Dionysus` | `scripts/AGENTS.md` | `add-local-agents` | scripts can mutate, generate, validate, or route other surfaces |
| P0 | 92 | `aoa-agon` | `scripts/AGENTS.md` | `add-local-agents` | scripts can mutate, generate, validate, or route other surfaces |
| P0 | 92 | `aoa-dashboard` | `scripts/AGENTS.md` | `add-local-agents` | scripts can mutate, generate, validate, or route other surfaces |
| P0 | 92 | `aoa-models` | `scripts/AGENTS.md` | `add-local-agents` | scripts can mutate, generate, validate, or route other surfaces |
| P1 | 84 | `Dionysus` | `.github/AGENTS.md` | `inspect-then-add` | platform automation and workflow metadata are public contracts |
| P1 | 84 | `aoa-models` | `.github/AGENTS.md` | `inspect-then-add` | platform automation and workflow metadata are public contracts |
| P1 | 84 | `aoa-sdk` | `src/AGENTS.md` | `inspect-then-add` | source modules often encode executable or importable behavior |
| P1 | 84 | `aoa-session-memory` | `.github/AGENTS.md` | `inspect-then-add` | platform automation and workflow metadata are public contracts |
| P1 | 82 | `aoa-agents` | `manifests/AGENTS.md` | `inspect-then-add` | manifests can become hidden coordination contracts |
| P1 | 80 | `aoa-agon` | `generated/AGENTS.md` | `inspect-then-add` | generated outputs should remain evidence, not authority |
| P1 | 80 | `aoa-models` | `generated/AGENTS.md` | `inspect-then-add` | generated outputs should remain evidence, not authority |
| P1 | 80 | `aoa-session-memory` | `generated/AGENTS.md` | `inspect-then-add` | generated outputs should remain evidence, not authority |
| P1 | 79 | `aoa-stats` | `manifests/AGENTS.md` | `inspect-then-add` | manifests can become hidden coordination contracts |
| P1 | 78 | `aoa-agon` | `config/AGENTS.md` | `inspect-then-add` | configuration can shift policy and generation behavior |
| P1 | 78 | `aoa-dashboard` | `config/AGENTS.md` | `inspect-then-add` | configuration can shift policy and generation behavior |
| P1 | 74 | `abyss-machine` | `src/AGENTS.md` | `inspect-then-add` | source modules often encode executable or importable behavior |
| P1 | 74 | `aoa-agon` | `src/AGENTS.md` | `inspect-then-add` | source modules often encode executable or importable behavior |
| P1 | 74 | `aoa-dashboard` | `src/AGENTS.md` | `inspect-then-add` | source modules often encode executable or importable behavior |
| P1 | 73 | `Tree-of-Sophia` | `quests/AGENTS.md` | `inspect-first` | quest language must stay evidence-linked and bounded |
| P1 | 72 | `aoa-playbooks` | `quests/AGENTS.md` | `inspect-first` | quest language must stay evidence-linked and bounded |
| P2 | 70 | `aoa-agon` | `tests/AGENTS.md` | `inspect-first` | tests define what drift is caught |
| P2 | 70 | `aoa-dashboard` | `tests/AGENTS.md` | `inspect-first` | tests define what drift is caught |
| P2 | 70 | `aoa-models` | `tests/AGENTS.md` | `inspect-first` | tests define what drift is caught |
| P2 | 64 | `aoa-playbooks` | `docs/AGENTS.md` | `inspect-first` | docs may carry doctrine, but many docs do not need local law |
| P2 | 61 | `aoa-stats` | `docs/AGENTS.md` | `inspect-first` | docs may carry doctrine, but many docs do not need local law |
| P2 | 58 | `Dionysus` | `docs/AGENTS.md` | `inspect-first` | docs may carry doctrine, but many docs do not need local law |
| P2 | 58 | `aoa-agon` | `docs/AGENTS.md` | `inspect-first` | docs may carry doctrine, but many docs do not need local law |
| P2 | 58 | `aoa-dashboard` | `docs/AGENTS.md` | `inspect-first` | docs may carry doctrine, but many docs do not need local law |
| P2 | 58 | `aoa-models` | `docs/AGENTS.md` | `inspect-first` | docs may carry doctrine, but many docs do not need local law |
| P2 | 58 | `aoa-session-memory` | `docs/AGENTS.md` | `inspect-first` | docs may carry doctrine, but many docs do not need local law |
| P2 | 54 | `Dionysus` | `examples/AGENTS.md` | `inspect-first` | examples need public-safety and source-sync boundaries |
| P2 | 54 | `aoa-agon` | `examples/AGENTS.md` | `inspect-first` | examples need public-safety and source-sync boundaries |
| P2 | 54 | `aoa-session-memory` | `examples/AGENTS.md` | `inspect-first` | examples need public-safety and source-sync boundaries |

## How to use

1. Start with P0 candidates that are both present and genuinely local-risk bearing.
2. Do not add `AGENTS.md` just to quiet a metric; add it only where it prevents a realistic agent mistake.
3. After landing local guidance, promote it into the owning validator map.
4. Regenerate `generated/agents_map.min.json` and this frontier report.
