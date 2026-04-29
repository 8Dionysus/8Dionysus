# AGENTS frontier reconnaissance

This report ranks remaining high-risk directories that may need local `AGENTS.md` guidance.
It is a reconnaissance surface, not repository doctrine, and it does not overrule the nearest `AGENTS.md`.

## Totals

- `candidate_count`: 75
- `p0_candidates`: 26
- `p1_candidates`: 33
- `p2_candidates`: 16
- `p3_candidates`: 0
- `repos_with_candidates`: 16
- `repositories_listed`: 18

## Top candidates

| Priority | Score | Repository | Path | Decision | Rationale |
|---|---:|---|---|---|---|
| P0 | 110 | `abyss-stack` | `.agents/AGENTS.md` | `add-local-agents` | agent-facing projection surfaces can silently steer tools |
| P0 | 106 | `aoa-sdk` | `.agents/AGENTS.md` | `add-local-agents` | agent-facing projection surfaces can silently steer tools |
| P0 | 105 | `Dionysus` | `.agents/AGENTS.md` | `add-local-agents` | agent-facing projection surfaces can silently steer tools |
| P0 | 104 | `abyss-stack` | `systemd/AGENTS.md` | `add-local-agents` | service units can affect runtime lifecycle |
| P0 | 103 | `Tree-of-Sophia` | `.agents/AGENTS.md` | `add-local-agents` | agent-facing projection surfaces can silently steer tools |
| P0 | 102 | `.codex` | `scripts/AGENTS.md` | `add-local-agents` | scripts can mutate, generate, validate, or route other surfaces |
| P0 | 102 | `aoa-agents` | `.agents/AGENTS.md` | `add-local-agents` | agent-facing projection surfaces can silently steer tools |
| P0 | 102 | `aoa-playbooks` | `.agents/AGENTS.md` | `add-local-agents` | agent-facing projection surfaces can silently steer tools |
| P0 | 102 | `aoa-sdk` | `scripts/AGENTS.md` | `add-local-agents` | scripts can mutate, generate, validate, or route other surfaces |
| P0 | 101 | `aoa-evals` | `.agents/AGENTS.md` | `add-local-agents` | agent-facing projection surfaces can silently steer tools |
| P0 | 101 | `aoa-skills` | `.agents/AGENTS.md` | `add-local-agents` | agent-facing projection surfaces can silently steer tools |
| P0 | 101 | `aoa-techniques` | `.agents/AGENTS.md` | `add-local-agents` | agent-facing projection surfaces can silently steer tools |
| P0 | 100 | `aoa-kag` | `.agents/AGENTS.md` | `add-local-agents` | agent-facing projection surfaces can silently steer tools |
| P0 | 100 | `aoa-memo` | `.agents/AGENTS.md` | `add-local-agents` | agent-facing projection surfaces can silently steer tools |
| P0 | 100 | `aoa-routing` | `.agents/AGENTS.md` | `add-local-agents` | agent-facing projection surfaces can silently steer tools |
| P0 | 99 | `aoa-stats` | `.agents/AGENTS.md` | `add-local-agents` | agent-facing projection surfaces can silently steer tools |
| P0 | 98 | `abyss-stack` | `.github/AGENTS.md` | `add-local-agents` | platform automation and workflow metadata are public contracts |
| P0 | 96 | `ATM10-Agent` | `.github/AGENTS.md` | `add-local-agents` | platform automation and workflow metadata are public contracts |
| P0 | 94 | `aoa-sdk` | `.github/AGENTS.md` | `add-local-agents` | platform automation and workflow metadata are public contracts |
| P0 | 93 | `Dionysus` | `.github/AGENTS.md` | `add-local-agents` | platform automation and workflow metadata are public contracts |
| P0 | 92 | `abyss-stack` | `config/AGENTS.md` | `add-local-agents` | configuration can shift policy and generation behavior |
| P0 | 91 | `Tree-of-Sophia` | `.github/AGENTS.md` | `add-local-agents` | platform automation and workflow metadata are public contracts |
| P0 | 90 | `.codex` | `generated/AGENTS.md` | `add-local-agents` | generated outputs should remain evidence, not authority |
| P0 | 90 | `abyss-stack` | `manifests/AGENTS.md` | `add-local-agents` | manifests can become hidden coordination contracts |
| P0 | 90 | `aoa-agents` | `.github/AGENTS.md` | `add-local-agents` | platform automation and workflow metadata are public contracts |
| P0 | 90 | `aoa-playbooks` | `.github/AGENTS.md` | `add-local-agents` | platform automation and workflow metadata are public contracts |
| P1 | 89 | `aoa-evals` | `.github/AGENTS.md` | `inspect-then-add` | platform automation and workflow metadata are public contracts |
| P1 | 89 | `aoa-skills` | `.github/AGENTS.md` | `inspect-then-add` | platform automation and workflow metadata are public contracts |
| P1 | 89 | `aoa-techniques` | `.github/AGENTS.md` | `inspect-then-add` | platform automation and workflow metadata are public contracts |
| P1 | 88 | `aoa-kag` | `.github/AGENTS.md` | `inspect-then-add` | platform automation and workflow metadata are public contracts |
| P1 | 88 | `aoa-memo` | `.github/AGENTS.md` | `inspect-then-add` | platform automation and workflow metadata are public contracts |
| P1 | 88 | `aoa-routing` | `.github/AGENTS.md` | `inspect-then-add` | platform automation and workflow metadata are public contracts |
| P1 | 88 | `aoa-sdk` | `config/AGENTS.md` | `inspect-then-add` | configuration can shift policy and generation behavior |
| P1 | 87 | `aoa-stats` | `.github/AGENTS.md` | `inspect-then-add` | platform automation and workflow metadata are public contracts |
| P1 | 86 | `aoa-sdk` | `manifests/AGENTS.md` | `inspect-then-add` | manifests can become hidden coordination contracts |
| P1 | 85 | `Tree-of-Sophia` | `config/AGENTS.md` | `inspect-then-add` | configuration can shift policy and generation behavior |
| P1 | 84 | `aoa-sdk` | `src/AGENTS.md` | `inspect-then-add` | source modules often encode executable or importable behavior |
| P1 | 83 | `Dionysus` | `src/AGENTS.md` | `inspect-then-add` | source modules often encode executable or importable behavior |
| P1 | 83 | `Tree-of-Sophia` | `manifests/AGENTS.md` | `inspect-then-add` | manifests can become hidden coordination contracts |
| P1 | 82 | `aoa-agents` | `manifests/AGENTS.md` | `inspect-then-add` | manifests can become hidden coordination contracts |

## How to use

1. Start with P0 candidates that are both present and genuinely local-risk bearing.
2. Do not add `AGENTS.md` just to quiet a metric; add it only where it prevents a realistic agent mistake.
3. After landing local guidance, promote it into the owning validator map.
4. Regenerate `generated/agents_map.min.json` and this frontier report.
