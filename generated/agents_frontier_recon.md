# AGENTS frontier reconnaissance

This report ranks remaining high-risk directories that may need local `AGENTS.md` guidance.
It is a reconnaissance surface, not repository doctrine, and it does not overrule the nearest `AGENTS.md`.

## Totals

- `candidate_count`: 42
- `p0_candidates`: 13
- `p1_candidates`: 20
- `p2_candidates`: 9
- `p3_candidates`: 0
- `repos_with_candidates`: 12
- `repositories_listed`: 19

## Top candidates

| Priority | Score | Repository | Path | Decision | Rationale |
|---|---:|---|---|---|---|
| P0 | 108 | `ATM10-Agent` | `.agents/AGENTS.md` | `add-local-agents` | agent-facing projection surfaces can silently steer tools |
| P0 | 106 | `aoa-sdk` | `.agents/AGENTS.md` | `add-local-agents` | agent-facing projection surfaces can silently steer tools |
| P0 | 105 | `Dionysus` | `.agents/AGENTS.md` | `add-local-agents` | agent-facing projection surfaces can silently steer tools |
| P0 | 103 | `Tree-of-Sophia` | `.agents/AGENTS.md` | `add-local-agents` | agent-facing projection surfaces can silently steer tools |
| P0 | 102 | `.codex` | `scripts/AGENTS.md` | `add-local-agents` | scripts can mutate, generate, validate, or route other surfaces |
| P0 | 102 | `aoa-agents` | `.agents/AGENTS.md` | `add-local-agents` | agent-facing projection surfaces can silently steer tools |
| P0 | 102 | `aoa-playbooks` | `.agents/AGENTS.md` | `add-local-agents` | agent-facing projection surfaces can silently steer tools |
| P0 | 102 | `aoa-sdk` | `scripts/AGENTS.md` | `add-local-agents` | scripts can mutate, generate, validate, or route other surfaces |
| P0 | 101 | `aoa-evals` | `.codex/AGENTS.md` | `add-local-agents` | Codex-plane helpers and projections need local source/installed-copy boundaries |
| P0 | 100 | `aoa-kag` | `.agents/AGENTS.md` | `add-local-agents` | agent-facing projection surfaces can silently steer tools |
| P0 | 100 | `aoa-routing` | `.agents/AGENTS.md` | `add-local-agents` | agent-facing projection surfaces can silently steer tools |
| P0 | 99 | `aoa-stats` | `.agents/AGENTS.md` | `add-local-agents` | agent-facing projection surfaces can silently steer tools |
| P0 | 90 | `.codex` | `generated/AGENTS.md` | `add-local-agents` | generated outputs should remain evidence, not authority |
| P1 | 88 | `aoa-sdk` | `config/AGENTS.md` | `inspect-then-add` | configuration can shift policy and generation behavior |
| P1 | 86 | `aoa-sdk` | `manifests/AGENTS.md` | `inspect-then-add` | manifests can become hidden coordination contracts |
| P1 | 85 | `Tree-of-Sophia` | `config/AGENTS.md` | `inspect-then-add` | configuration can shift policy and generation behavior |
| P1 | 84 | `aoa-sdk` | `src/AGENTS.md` | `inspect-then-add` | source modules often encode executable or importable behavior |
| P1 | 83 | `Dionysus` | `src/AGENTS.md` | `inspect-then-add` | source modules often encode executable or importable behavior |
| P1 | 83 | `Tree-of-Sophia` | `manifests/AGENTS.md` | `inspect-then-add` | manifests can become hidden coordination contracts |
| P1 | 82 | `aoa-agents` | `manifests/AGENTS.md` | `inspect-then-add` | manifests can become hidden coordination contracts |
| P1 | 82 | `aoa-playbooks` | `manifests/AGENTS.md` | `inspect-then-add` | manifests can become hidden coordination contracts |
| P1 | 80 | `.codex` | `tests/AGENTS.md` | `inspect-then-add` | tests define what drift is caught |
| P1 | 80 | `aoa-routing` | `manifests/AGENTS.md` | `inspect-then-add` | manifests can become hidden coordination contracts |
| P1 | 80 | `aoa-sdk` | `tests/AGENTS.md` | `inspect-then-add` | tests define what drift is caught |
| P1 | 79 | `Dionysus` | `tests/AGENTS.md` | `inspect-then-add` | tests define what drift is caught |
| P1 | 79 | `aoa-stats` | `manifests/AGENTS.md` | `inspect-then-add` | manifests can become hidden coordination contracts |
| P1 | 77 | `Tree-of-Sophia` | `tests/AGENTS.md` | `inspect-then-add` | tests define what drift is caught |
| P1 | 76 | `aoa-sdk` | `quests/AGENTS.md` | `inspect-first` | quest language must stay evidence-linked and bounded |
| P1 | 75 | `Dionysus` | `quests/AGENTS.md` | `inspect-first` | quest language must stay evidence-linked and bounded |
| P1 | 74 | `.agents` | `skills/AGENTS.md` | `inspect-first` | skill-facing surfaces need bounded execution clarity |
| P1 | 73 | `Tree-of-Sophia` | `quests/AGENTS.md` | `inspect-first` | quest language must stay evidence-linked and bounded |
| P1 | 72 | `aoa-agents` | `quests/AGENTS.md` | `inspect-first` | quest language must stay evidence-linked and bounded |
| P1 | 72 | `aoa-playbooks` | `quests/AGENTS.md` | `inspect-first` | quest language must stay evidence-linked and bounded |
| P2 | 70 | `aoa-kag` | `quests/AGENTS.md` | `inspect-first` | quest language must stay evidence-linked and bounded |
| P2 | 70 | `aoa-routing` | `quests/AGENTS.md` | `inspect-first` | quest language must stay evidence-linked and bounded |
| P2 | 69 | `aoa-stats` | `quests/AGENTS.md` | `inspect-first` | quest language must stay evidence-linked and bounded |
| P2 | 68 | `aoa-sdk` | `docs/AGENTS.md` | `inspect-first` | docs may carry doctrine, but many docs do not need local law |
| P2 | 67 | `Dionysus` | `docs/AGENTS.md` | `inspect-first` | docs may carry doctrine, but many docs do not need local law |
| P2 | 64 | `aoa-playbooks` | `docs/AGENTS.md` | `inspect-first` | docs may carry doctrine, but many docs do not need local law |
| P2 | 64 | `aoa-sdk` | `examples/AGENTS.md` | `inspect-first` | examples need public-safety and source-sync boundaries |

## How to use

1. Start with P0 candidates that are both present and genuinely local-risk bearing.
2. Do not add `AGENTS.md` just to quiet a metric; add it only where it prevents a realistic agent mistake.
3. After landing local guidance, promote it into the owning validator map.
4. Regenerate `generated/agents_map.min.json` and this frontier report.
