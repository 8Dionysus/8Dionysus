# AGENTS.md — <workspace-root> workspace

Guidance for coding agents and humans operating from a shared AoA / ToS workspace root.

## Purpose

`<workspace-root>` is the editable federation workspace root.
Treat it as the sibling-parent directory for the public AoA / ToS repositories, not as the source of truth for any one layer.

This workspace is where bounded, reviewable agency enters the system.
It is not the final horizon.
The longer arc of the ecosystem is toward self-agency: continuity, memory, reflective revision, durable orientation, and growth that preserves provenance, legibility, and human judgment.

This root-level `AGENTS.md` is a coordination surface.
It helps an agent pick the right owner repository, run safe ingress, and avoid silently absorbing meaning across layers.
Once a concrete `repo_root` is chosen, that repository's own `AGENTS.md` and nearest-file rules take precedence.

## Read first

Before substantial work from the workspace root, read in this order:

1. `<workspace-root>/8Dionysus/README.md`
2. `<workspace-root>/8Dionysus/docs/START_HERE.md`
3. `<workspace-root>/8Dionysus/GLOSSARY.md`
4. `<workspace-root>/8Dionysus/docs/PUBLIC_ENTRY_POSTURE.md`
5. the target repository's own `README.md`
6. the target repository's own `AGENTS.md`

If the task is primarily about workspace layout or bootstrap, also read:

- `<workspace-root>/8Dionysus/docs/WORKSPACE_INSTALL.md`
- `<workspace-root>/8Dionysus/docs/CODEX_PLANE_REGENERATION.md`
- `<workspace-root>/AOA_WORKSPACE_ROOT` when present
- `<workspace-root>/.agents/plugins/marketplace.json` when present
- `<workspace-root>/.codex/config.toml` when present
- `<workspace-root>/aoa-sdk/docs/workspace-layout.md` when available

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

If the task is truly cross-repo and no single owner repo is primary yet, use `<workspace-root>` as the temporary `repo_root` only until the owning layer becomes clear.

## Session start

For every new session started from the workspace root, before substantial work:

1. choose the primary `repo_root`
2. run one ingress pass

```bash
aoa skills enter <repo_root> \
  --root <workspace-root> \
  --intent-text "<short task summary>" \
  --json
```

If the task is already clearly repo-local, use that repository as `repo_root` in your planning and file reads immediately after the workspace ingress.

## Mutation gate

Before risky, mutating, infra, runtime, repo-config, or public-share actions, run:

```bash
aoa skills guard <repo_root> \
  --root <workspace-root> \
  --intent-text "<planned change>" \
  --mutation-surface <code|repo-config|infra|runtime|public-share> \
  --json
```

Do not silently skip `must_confirm` or `blocked_actions`.
Do not weaken dry-run, bounded-claim, or human-judgment posture by convenience.

## Additive surface detection

Keep `aoa skills enter` and `aoa skills guard` as the primary workspace-level ingress and mutation gate.
They stay skill-only.

When the active task shows route drift, owner-layer ambiguity, proof need, recall need, role posture questions, continuity questions, anchor loss, reanchor need, recurring-scenario signals, repeated doctor warnings, repeated manual refresh patches, generated or install drift, stale summary windows, or rollout or continuity routes blocked by one named component, run one additive surface pass for the chosen `repo_root`:

```bash
aoa surfaces detect <repo_root> \
  --root <workspace-root> \
  --phase ingress \
  --intent-text "<surface-aware task summary>" \
  --json
```

Use `--phase pre-mutation` and the same `mutation_surface` when the signal appears during a risky change:

```bash
aoa surfaces detect <repo_root> \
  --root <workspace-root> \
  --phase pre-mutation \
  --intent-text "<surface-aware task summary>" \
  --mutation-surface <code|repo-config|infra|runtime|public-share> \
  --json
```

When those component-refresh signals appear, keep the root posture narrow:
route the evidence to the owner repo, preserve reviewed hints, and do not
pretend the workspace root owns the drifting component.

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
- `8Dionysus` may own selected shared-root install surfaces without becoming the source of truth for the layers those surfaces help route into
- `Agents-of-Abyss` is the ecosystem center, not the full implementation home
- `aoa-sdk` stays on the control plane and does not absorb source-owned meaning
- routing, memory, stats, KAG, and other derived surfaces must not masquerade as source truth
- if the chosen repository has its own `AGENTS.md`, follow its narrower guidance after this root-level trigger fires

## Workspace posture

- `<workspace-root>/AGENTS.md`, `<workspace-root>/AOA_WORKSPACE_ROOT`, `<workspace-root>/.agents/`, and `<workspace-root>/.codex/` are selected shared-root install surfaces sourced from `8Dionysus` and projected into the live workspace root
- `<workspace-root>/.agents/skills` is the shared project-foundation install
- `<workspace-root>/.agents/plugins/marketplace.json` is the workspace plugin discovery surface when present
- `<workspace-root>/.agents/skills/` remains an installed projection of `aoa-skills`, not an authority transfer into `8Dionysus`
- `<workspace-root>/.codex/bin/aoa-workspace-project` is the short launcher for shared-root projection preview, check, and apply
- `<workspace-root>/.codex/bin/`, `<workspace-root>/.codex/scripts/`, and `<workspace-root>/.codex/tools/` are workspace-local control-plane utilities
- `<workspace-root>/.codex/plugins/` is the project-level Codex plugin install surface
- `<workspace-root>/.codex/generated/` remains workspace-local runtime output and must not be mistaken for the source-owned install surface
- `<workspace-root>/8Dionysus` is the public profile and route map
- `<workspace-root>/8Dionysus/config/codex_plane/` is the source-owned regeneration surface for the checked-in `.codex/config.toml` and `.codex/hooks.json`
- `<workspace-root>/Dionysus` is the seed garden and staging surface
- source repositories live as sibling checkouts under `<workspace-root>`
- `abyss-stack` is part of the ecosystem, but its preferred source checkout may still live outside `<workspace-root>`; respect `aoa-sdk` workspace discovery and overrides

Projection edit law:

- when a shared-root install surface needs a real change, edit the source-owned copy under `<workspace-root>/8Dionysus/` first and then project it into the live workspace root
- do not treat the live copies at `<workspace-root>/AGENTS.md`, `<workspace-root>/AOA_WORKSPACE_ROOT`, `<workspace-root>/.agents/`, or `<workspace-root>/.codex/` as the primary source of truth
- preview or verify that drift with `<workspace-root>/.codex/bin/aoa-workspace-project --check --json`, then apply with `--execute`
- keep `<workspace-root>/8Dionysus/README.md` profile-owned and GitHub-facing; it is not part of the shared-root projection contract

## AGENTS map audit

Before large `AGENTS.md` refactors or cross-repo guidance work, use the map audit as the measurement pass:

```bash
python scripts/audit_agents_map.py \
  --workspace-root <workspace-root> \
  --write generated/agents_map.min.json \
  --markdown docs/AGENTS_MAP.md
```

`generated/agents_map.min.json` and `docs/AGENTS_MAP.md` are map surfaces, not doctrine. They show root/nested coverage, validator declarations, high-risk directories without direct local guidance, long roots, and missing checkouts. Use findings to move guidance to the smallest owner surface; do not copy one repository's law into another repository.

For a public bootstrap seed without sibling checkouts, run:

```bash
python scripts/audit_agents_map.py --public-baseline \
  --write generated/agents_map.min.json \
  --markdown docs/AGENTS_MAP.md
```

## Skill ↔ MCP route discipline

- Prefer AoA skills whose generated `.agents/skills/*/agents/openai.yaml` or documented wiring examples declare named MCP dependencies when the route is sibling-workspace orientation, derived stats observability, or Dionysus seed routing
- Treat `aoa_workspace` as the first orientation surface when owner-fit is unclear
- Treat `aoa_stats` as derived observability only. Do not let it overrule owner truth or bounded eval verdicts
- Treat `dionysus` as seed-garden and planting-lineage context. Do not mistake staging notes for final owner doctrine
- Respect `allow_implicit_invocation` from the generated skill export and local adapter manifest. Do not silently force explicit-only skills into automatic use
- Keep role-bearing work in custom agents when they exist. MCP dependencies do not by themselves create hidden actor behavior

## Plugin posture

If the `aoa-shared-launchers` plugin is installed, prefer its bundled launcher
skills for:

- cross-repo orientation
- bounded growth snapshots
- seed-route inspection
- AoA Codex wiring diagnosis

These plugin skills rely on the named MCP servers already configured for the
workspace:

- `aoa_workspace`
- `aoa_stats`
- `dionysus`

Boundary rules:

- the plugin is a launcher layer, not an owning layer
- the plugin install path is workspace-local packaging, not owner-repo truth
- `aoa_stats` remains derived
- `Dionysus` remains staging and route context
- owner truth stays in the owning repo

## Convergence posture

Use the workspace-local convergence seam for read-only drift checks:

- doctor: `<workspace-root>/.codex/bin/aoa-codex-doctor`
- status: `<workspace-root>/.codex/bin/aoa-codex-status`
- bootstrap: `<workspace-root>/.codex/bin/aoa-codex-bootstrap`
- reports: `<workspace-root>/.codex/generated/codex/aoa_codex_convergence_report.{json,md}`

Boundary rules:

- convergence reports are evidence, not authority
- convergence may expose drift across MCP, plugins, skills, hooks, and subagents
- convergence must not replace owner-repo validation or rewrite owner meaning

## Hooks posture

AoA hooks live under `<workspace-root>/.codex/hooks/` and write reports under
`<workspace-root>/.codex/generated/codex/hooks/`.

Use `<workspace-root>/.codex/bin/aoa-codex-hooks-doctor` for the manual
hook-doctor surface.

Boundary rules:

- hooks stay deterministic, narrow, and fail-open
- hooks may write reports and event logs only under the workspace-local hooks report surface
- hooks do not become routing authority, plugin authority, or owner-repo truth

## Workflow

`INGRESS -> READ -> PLAN -> DIFF -> VERIFY -> REPORT`

## Closeout audit

When a repo-local session changes GitHub workflow names, required-check
contract surfaces, or main-branch protection, run the trigger-aware closeout
helper before your final report:

```bash
<workspace-root>/.codex/bin/aoa-required-check-audit --repo-root <repo_root>
```

If the same session changed branch protection through `gh`, rerun with:

```bash
<workspace-root>/.codex/bin/aoa-required-check-audit \
  --repo-root <repo_root> \
  --github-protection
```

The helper is intentionally narrow:

- it inspects the current repo diff against `origin/main` when available
- it skips cleanly when the current change does not touch required-check drift surfaces
- it runs the `8Dionysus` coordination validator only when the trigger is present or when forced explicitly

In your final report, name whether this helper skipped or ran, and which modes
you used.

## Definition of done

A workspace-root change or routed contribution is done when:

- the owning repository is clearer than before
- source-of-truth boundaries are tighter, not blurrier
- the route for humans and agents is easier to follow
- bounded agency is preserved without being mistaken for the whole horizon
- any self-agency or quest language added is grounded, reviewable, and non-magical
- validation run status is reported honestly
