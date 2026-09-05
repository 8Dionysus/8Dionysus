# AGENTS frontier reconnaissance

This report ranks remaining high-risk directories that may need local `AGENTS.md` guidance.
It is a reconnaissance surface, not repository doctrine, and it does not overrule the nearest `AGENTS.md`.

## Totals

- `candidate_count`: 30
- `p0_candidates`: 6
- `p1_candidates`: 12
- `p2_candidates`: 12
- `p3_candidates`: 0
- `repos_with_candidates`: 7
- `repositories_listed`: 26

## Top candidates

| Priority | Score | Repository | Path | Decision | Rationale |
|---|---:|---|---|---|---|
| P0 | 108 | `abyss-stack` | `schemas/AGENTS.md` | `add-local-agents` | schema edits are contract edits |
| P0 | 92 | `aoa-instagram-connector` | `scripts/AGENTS.md` | `add-local-agents` | scripts can mutate, generate, validate, or route other surfaces |
| P0 | 92 | `aoa-pinterest-connector` | `scripts/AGENTS.md` | `add-local-agents` | scripts can mutate, generate, validate, or route other surfaces |
| P0 | 92 | `aoa-tiktok-connector` | `scripts/AGENTS.md` | `add-local-agents` | scripts can mutate, generate, validate, or route other surfaces |
| P0 | 92 | `aoa-x-connector` | `scripts/AGENTS.md` | `add-local-agents` | scripts can mutate, generate, validate, or route other surfaces |
| P0 | 92 | `aoa-youtube-connector` | `scripts/AGENTS.md` | `add-local-agents` | scripts can mutate, generate, validate, or route other surfaces |
| P1 | 84 | `aoa-instagram-connector` | `.github/AGENTS.md` | `inspect-then-add` | platform automation and workflow metadata are public contracts |
| P1 | 84 | `aoa-pinterest-connector` | `.github/AGENTS.md` | `inspect-then-add` | platform automation and workflow metadata are public contracts |
| P1 | 84 | `aoa-session-memory` | `.github/AGENTS.md` | `inspect-then-add` | platform automation and workflow metadata are public contracts |
| P1 | 84 | `aoa-tiktok-connector` | `.github/AGENTS.md` | `inspect-then-add` | platform automation and workflow metadata are public contracts |
| P1 | 84 | `aoa-x-connector` | `.github/AGENTS.md` | `inspect-then-add` | platform automation and workflow metadata are public contracts |
| P1 | 84 | `aoa-youtube-connector` | `.github/AGENTS.md` | `inspect-then-add` | platform automation and workflow metadata are public contracts |
| P1 | 80 | `aoa-session-memory` | `generated/AGENTS.md` | `inspect-then-add` | generated outputs should remain evidence, not authority |
| P1 | 74 | `aoa-instagram-connector` | `src/AGENTS.md` | `inspect-then-add` | source modules often encode executable or importable behavior |
| P1 | 74 | `aoa-pinterest-connector` | `src/AGENTS.md` | `inspect-then-add` | source modules often encode executable or importable behavior |
| P1 | 74 | `aoa-tiktok-connector` | `src/AGENTS.md` | `inspect-then-add` | source modules often encode executable or importable behavior |
| P1 | 74 | `aoa-x-connector` | `src/AGENTS.md` | `inspect-then-add` | source modules often encode executable or importable behavior |
| P1 | 74 | `aoa-youtube-connector` | `src/AGENTS.md` | `inspect-then-add` | source modules often encode executable or importable behavior |
| P2 | 70 | `aoa-instagram-connector` | `tests/AGENTS.md` | `inspect-first` | tests define what drift is caught |
| P2 | 70 | `aoa-pinterest-connector` | `tests/AGENTS.md` | `inspect-first` | tests define what drift is caught |
| P2 | 70 | `aoa-tiktok-connector` | `tests/AGENTS.md` | `inspect-first` | tests define what drift is caught |
| P2 | 70 | `aoa-x-connector` | `tests/AGENTS.md` | `inspect-first` | tests define what drift is caught |
| P2 | 70 | `aoa-youtube-connector` | `tests/AGENTS.md` | `inspect-first` | tests define what drift is caught |
| P2 | 58 | `aoa-instagram-connector` | `docs/AGENTS.md` | `inspect-first` | docs may carry doctrine, but many docs do not need local law |
| P2 | 58 | `aoa-pinterest-connector` | `docs/AGENTS.md` | `inspect-first` | docs may carry doctrine, but many docs do not need local law |
| P2 | 58 | `aoa-session-memory` | `docs/AGENTS.md` | `inspect-first` | docs may carry doctrine, but many docs do not need local law |
| P2 | 58 | `aoa-tiktok-connector` | `docs/AGENTS.md` | `inspect-first` | docs may carry doctrine, but many docs do not need local law |
| P2 | 58 | `aoa-x-connector` | `docs/AGENTS.md` | `inspect-first` | docs may carry doctrine, but many docs do not need local law |
| P2 | 58 | `aoa-youtube-connector` | `docs/AGENTS.md` | `inspect-first` | docs may carry doctrine, but many docs do not need local law |
| P2 | 54 | `aoa-session-memory` | `examples/AGENTS.md` | `inspect-first` | examples need public-safety and source-sync boundaries |

## How to use

1. Start with P0 candidates that are both present and genuinely local-risk bearing.
2. Do not add `AGENTS.md` just to quiet a metric; add it only where it prevents a realistic agent mistake.
3. After landing local guidance, promote it into the owning validator map.
4. Regenerate `generated/agents_map.min.json` and this frontier report.
