# AGENTS.md

Root route card for the shared AoA / ToS workspace and the `8Dionysus` public entry repository.

## Purpose

`8Dionysus` is the public route map, profile orientation surface, and selected shared-root install source for the AoA / ToS ecosystem.
Use it to choose the owning repository, audit the AGENTS map, and keep workspace projection surfaces legible.
It is not the constitutional center, not a runtime owner, and not a replacement for layer-owned truth.

## Owner lane

This repository owns:

- public entry orientation, glossary alignment, and profile-level route help
- selected shared-root install sources such as `AGENTS.md`, the dedicated
  `docs/WORKSPACE_ROOT_ENTRY.md` human entry, `AOA_WORKSPACE_ROOT`, `.agents/`,
  and the source-owned `.codex/` subset checked in here
- workspace bootstrap notes, Codex-plane regeneration notes, and AGENTS map audit surfaces
- one admitted repo-local procedure for diagnosing concrete workspace capability-delivery disagreements
- owner-local statistical questions over public route and audit evidence

It does not own:

- AoA center doctrine, which belongs in `Agents-of-Abyss`
- ToS authored meaning, which belongs in `Tree-of-Sophia`
- runtime behavior, which belongs in `abyss-stack`
- SDK helpers, shared skills, sibling home skills, techniques, evals, routing,
  memory, KAG, playbooks, shared stats grammar, agent, or seed canon owned by
  sibling repos

## Conditional routes

Choose the primary owner before editing; do not preload the documentation set.

- public/profile orientation: `README.md`, then `docs/START_HERE.md`
- live workspace-root human orientation: `docs/WORKSPACE_ROOT_ENTRY.md`
- repository posture or glossary work: `docs/PUBLIC_ENTRY_POSTURE.md` or
  `GLOSSARY.md`
- concrete owner work: target source plus its nearest `AGENTS.md`; target
  `README.md` only when human use or topology is relevant
- workspace bootstrap or projection: `docs/WORKSPACE_INSTALL.md`,
  `docs/CODEX_PLANE_REGENERATION.md`, then the affected `.agents/` or
  `.codex/` source
- historical depth: `docs/AGENTS_ROOT_REFERENCE.md`


## AGENTS stack law

- Start with this root card, then follow the nearest nested `AGENTS.md` for every touched path.
- Root guidance owns repository identity, owner boundaries, route choice, and the shortest honest verification path.
- Nested guidance owns local contracts, local risk, exact files, and local checks.
- Authored source surfaces own meaning. Generated, exported, compact, derived, runtime, and adapter surfaces summarize, transport, or support meaning.
- Self-agency, recurrence, quest, progression, checkpoint, or growth language must stay bounded, reviewable, evidence-linked, and reversible.
- Report what changed, what was verified, what was not verified, and where the next agent should resume.

## Decision memory

After a meaningful structural, ownership, workflow, route-law, validator-authority,
public-contract, or topology change, perform a decision review in the owning
repository.

If future agents will need to know why this path was chosen, add or update the
repo-local decision record surface, usually `docs/decisions/`. If no record is
needed, say so in closeout.

## Route by intent

- `Agents-of-Abyss`: ecosystem identity, charter, layer map, federation rules, program direction.
- `Tree-of-Sophia`: source-linked knowledge, texts, concepts, lineages, interpretation architecture.
- `Dionysus`: voice-first interview protocols, evidence-grounded claims, human review, and purpose-bounded personal portrait projections.
- `abyss-stack`: runtime, deployment, storage, lifecycle, infrastructure posture.
- `ATM10-Agent`: local companion behavior, perception, retrieval, KAG-in-project, safe operator automation.
- `aoa-sdk`: typed workspace integration, canonical routing and dispatch,
  discovery, compatibility, passive skill inspection, and explicit
  user-profile bootstrap.
- `aoa-dashboard`: owner-bounded Goal Space/operator projections,
  provenance/freshness/missingness, correlation, actor activity, and
  non-executing annotations or deferred action intents.
- `aoa-techniques`: reusable engineering practice.
- `aoa-skills`: the shared portable bundle family and common owner-home compatibility contract.
- `aoa-evals`: portable proof and evaluation surfaces.
- `aoa-memo`: explicit memory and recall objects.
- `aoa-kag`: derived provenance-aware knowledge substrates.
- `aoa-playbooks`: recurring scenario composition, questlines, campaigns, handoffs.
- `aoa-agents`: role contracts, handoff posture, progression and checkpoint contract surfaces.
- `aoa-stats`: shared measurement grammar, owner-local stats federation, and
  derived non-sovereign read models.
- `8Dionysus`: public route map, shared-root projection source, AGENTS map audit, and concrete workspace-delivery diagnosis.

`aoa-routing` is the deprecated maintenance-only predecessor. Keep it visible
only for reversible history and rollback review until a separate operator
decision authorizes archive; do not route new navigation or dispatch work there.

## Memory route

- Use `aoa_memo` for continuity, recall, preservation, local-port status, or
  reviewed memory handoff; owner source remains stronger than memory.
- Use `aoa_session_memory` only for read-only evidence about a stable
  skill, MCP, hook, tool, path, goal, or recurring failure. It does not own
  writeback, repair, reindex, distillation, or promotion; raw authority remains
  in `.aoa`.
- After a meaningful landing, use `aoa-memo-writeback` to decide between one
  reviewed candidate/export and an explicit no-write result. Durable reviewed
  memory lands through `aoa-memo`, not the shared root or MCP plane.
- Use `generated/workspace_memory_map.min.json` and
  `docs/WORKSPACE_MEMORY_MAP.md` for port/status routing; regenerate them
  through `scripts/build_workspace_memory_map.py` rather than guessing.

## Skill inspection and mutation boundary

`aoa skills` is passive and exact:

```bash
aoa skills inspect <repo_root> --root <workspace-root> --json
aoa skills capability <exact-node-id> --root <workspace-root> --json
```

Semantic skill retrieval and composition belong to `aoa-kag`; SDK inspection
and `aoa surfaces detect` remain read-only and never select, activate, or
execute a skill.

For one concrete mismatch among skill, MCP, or tool source, projection,
consumer scope, prompt/catalog visibility, configuration, transport, and owner
service, use the repo-local `aoa-workspace-diagnose` home skill. General
orientation remains in this route card and KAG. Diagnosis is read-only and does
not authorize repair, install, restart, or configuration mutation.

Risky mutation requires the nearest owner contract, applicable runtime
boundary, and explicit host or human confirmation. There is no SDK-owned skill
ingress or mutation-gate command.

## Projection and audit rules

Follow `docs/WORKSPACE_INSTALL.md` for projection and
`docs/CODEX_PLANE_REGENERATION.md` for Codex render/rollout. Hard boundaries:

- edit the source-owned copy under `<workspace-root>/8Dionysus/` first; do not treat the live copies as source
- keep the repository `README.md` profile-owned and GitHub-facing, outside
  shared-root projection; project `docs/WORKSPACE_ROOT_ENTRY.md` separately as
  `<workspace-root>/README.md`
- do not copy or prune `<workspace-root>/.agents/skills/`; shared bundles
  install through `aoa-skills`, and repo projections come from admitted local
  `skills/` homes
- keep live `.codex/config.toml` and `.codex/agents/` outside the generic
  projector; registration and role projection use their dedicated owner routes
- use a clean current owner checkout; the launcher does not fetch and must
  refuse a stale or dirty managed source
- treat non-current live execution as explicit branch-trial evidence, never
  owner-current proof
- keep generated or install drift narrow and route it to the owner repo

Before a broad AGENTS refactor, run:

```bash
python scripts/audit_agents_map.py --workspace-root <workspace-root> --write generated/agents_map.min.json --markdown docs/AGENTS_MAP.md
```

For a public baseline without sibling checkouts:

```bash
python scripts/audit_agents_map.py --public-baseline --write generated/agents_map.min.json --markdown docs/AGENTS_MAP.md
```

## GitHub landing workflow

Root owns the repository-wide merge stop-line; `.github/AGENTS.md` owns
GitHub-native details. Start from current `origin/main`, inventory dirty state,
and keep only the intended diff. A PR must name changed surfaces, validation,
skips, and risk. Merge only after `Repo Validation` and all required checks
are observed green, then fast-forward local `main` and confirm it is clean.
If status or permission cannot be observed, stop instead of guessing.

## Verify

Use the smallest route-safe check for the changed surface. For AGENTS-map or workspace route changes, run one of the audit commands above and report whether it was a public-baseline or sibling-workspace pass.
For `stats/` changes, also run `python scripts/validate_local_stats_port.py`.
If projection, hooks, plugin, convergence, or closeout details are touched, read `docs/AGENTS_ROOT_REFERENCE.md` and run the named narrow helper there before reporting.
For convergence checks, keep `aoa-codex-doctor`, `aoa-codex-status`, and `aoa-codex-bootstrap` discoverable as wrappers, and keep `aoa_codex_convergence_report.{json,md}` as evidence only. The rule is that convergence reports are evidence, not authority.

## Full reference

`docs/AGENTS_ROOT_REFERENCE.md` preserves the previous detailed root guidance, including plugin, hook, convergence, closeout, and projection details.
Use it as a depth layer when the short route card is not enough. If active rules from that reference still govern a local path, prefer moving them to the nearest owner surface rather than bloating this root again.
