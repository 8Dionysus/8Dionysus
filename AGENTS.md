# AGENTS.md — /srv workspace

Guidance for coding agents and humans operating from the shared `/srv` AoA / ToS workspace.

## Purpose

`/srv` is the editable federation workspace root.
Treat it as the sibling-parent directory for the public AoA / ToS repositories, not as the source of truth for any one layer.

This workspace is where bounded, reviewable agency enters the system.
It is not the final horizon.
The longer arc of the ecosystem is toward self-agency: continuity, memory, reflective revision, durable orientation, and growth that preserves provenance, legibility, and human judgment.

This root-level `AGENTS.md` is a coordination surface.
It helps an agent pick the right owner repository, run safe ingress, and avoid silently absorbing meaning across layers.
Once a concrete `repo_root` is chosen, that repository's own `AGENTS.md` and nearest-file rules take precedence.

## Read first

Before substantial work from `/srv`, read in this order:

1. `/srv/8Dionysus/README.md`
2. `/srv/8Dionysus/GLOSSARY.md`
3. `/srv/8Dionysus/docs/PUBLIC_ENTRY_POSTURE.md`
4. the target repository's own `README.md`
5. the target repository's own `AGENTS.md`

If the task is primarily about workspace layout or bootstrap, also read:

- `/srv/8Dionysus/docs/WORKSPACE_INSTALL.md`
- `/srv/aoa-sdk/docs/workspace-layout.md` when available

## Core arc

Keep this ecosystem-level direction explicit while you work:

- knowledge should deepen with provenance as it grows
- agency should grow beyond tools into self-agency
- bounded, reviewable agency is the starting discipline, not the destination
- growth must remain legible, source-grounded, and answerable to human judgment

Do not write as if every repository owns this whole arc equally.
Route the meaning back to the owner repository that actually governs it.

## Route by intent

When choosing a primary `repo_root`, route by the question being asked:

- `Agents-of-Abyss` for ecosystem identity, charter, layer map, federation rules, and program-level direction
- `Tree-of-Sophia` for source-linked knowledge, texts, concepts, lineages, and interpretive architecture
- `abyss-stack` for runtime, deployment, storage, and infrastructure posture
- `ATM10-Agent` for local-first companion behavior, perception, memory, voice, and safe automation surfaces
- `aoa-sdk` for typed workspace integration, compatibility checks, bounded activation, and controlled orchestration
- `aoa-techniques` for reusable engineering practice
- `aoa-skills` for bounded execution workflows
- `aoa-evals` for portable proof and evaluation surfaces
- `aoa-stats` for derived observability
- `aoa-routing` for navigation and dispatch
- `aoa-memo` for explicit memory and recall
- `aoa-agents` for role contracts and handoff posture
- `aoa-playbooks` for recurring scenario composition, questlines, and campaign-shaped routes
- `aoa-kag` for derived provenance-aware knowledge substrates
- `Dionysus` for seed-garden experiments, staging, and early forms
- `8Dionysus` for public routing, glossary alignment, and profile-level orientation

If the task is truly cross-repo and no single owner repo is primary yet, use `/srv` as the temporary `repo_root` only until the owning layer becomes clear.

## Session start

For every new session started from `/srv`, before substantial work:

1. choose the primary `repo_root`
2. run one ingress pass

```bash
aoa skills enter <repo_root> \
  --root /srv \
  --intent-text "<short task summary>" \
  --json
```

If the task is already clearly repo-local, use that repository as `repo_root` in your planning and file reads immediately after the workspace ingress.

## Mutation gate

Before risky, mutating, infra, runtime, repo-config, or public-share actions, run:

```bash
aoa skills guard <repo_root> \
  --root /srv \
  --intent-text "<planned change>" \
  --mutation-surface <code|repo-config|infra|runtime|public-share> \
  --json
```

Do not silently skip `must_confirm` or `blocked_actions`.
Do not weaken dry-run, bounded-claim, or human-judgment posture by convenience.

## Additive surface detection

Keep `aoa skills enter` and `aoa skills guard` as the primary workspace-level ingress and mutation gate.
They stay skill-only.

When the active task shows route drift, owner-layer ambiguity, proof need, recall need, role posture questions, continuity questions, anchor loss, reanchor need, or recurring-scenario signals, run one additive surface pass for the chosen `repo_root`:

```bash
aoa surfaces detect <repo_root> \
  --root /srv \
  --phase ingress \
  --intent-text "<surface-aware task summary>" \
  --json
```

Use `--phase pre-mutation` and the same `mutation_surface` when the signal appears during a risky change:

```bash
aoa surfaces detect <repo_root> \
  --root /srv \
  --phase pre-mutation \
  --intent-text "<surface-aware task summary>" \
  --mutation-surface <code|repo-config|infra|runtime|public-share> \
  --json
```

## Quest and growth posture

Quest and RPG vocabulary is a reflection layer for long-horizon routes.
Use it to improve readability, progression sense, continuity, and reanchor discipline.
Do not let it replace source-owned repository semantics.

Remember:

- questbooks are not runtime ledgers
- ability cards are not canonical skill truth
- loadouts are not runtime inventory
- campaign language must not hide sprawl
- continuity language must not hide missing anchors

## Truth rules

- `aoa skills ...` remains skill-only
- `aoa surfaces detect` is additive and read-only
- non-skill surfaces are hints, candidates, or reviewed closeout handoffs, not executable-now runtime objects
- `8Dionysus` is the public route map, not the constitutional center
- `Agents-of-Abyss` is the ecosystem center, not the full implementation home
- `aoa-sdk` stays on the control plane and does not absorb source-owned meaning
- routing, memory, stats, KAG, and other derived surfaces must not masquerade as source truth
- if the chosen repository has its own `AGENTS.md`, follow its narrower guidance after this root-level trigger fires

## Workspace posture

- `/srv/.agents/skills` is the shared project-foundation install
- `/srv/8Dionysus` is the public profile and route map
- `/srv/Dionysus` is the seed garden and staging surface
- source repositories live as sibling checkouts under `/srv`
- `abyss-stack` is part of the ecosystem, but its preferred source checkout may still live outside `/srv`; respect `aoa-sdk` workspace discovery and overrides

## Workflow

`INGRESS -> READ -> PLAN -> DIFF -> VERIFY -> REPORT`

## Definition of done

A workspace-root change or routed contribution is done when:

- the owning repository is clearer than before
- source-of-truth boundaries are tighter, not blurrier
- the route for humans and agents is easier to follow
- bounded agency is preserved without being mistaken for the whole horizon
- any self-agency or quest language added is grounded, reviewable, and non-magical
- validation run status is reported honestly
