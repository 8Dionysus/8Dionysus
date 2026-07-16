# AGENTS.md

Root route card for the shared AoA / ToS workspace and the `8Dionysus` public entry repository.

## Purpose

`8Dionysus` is the public route map, profile orientation surface, and selected shared-root install source for the AoA / ToS ecosystem.
Use it to choose the owning repository, audit the AGENTS map, and keep workspace projection surfaces legible.
It is not the constitutional center, not a runtime owner, and not a replacement for layer-owned truth.

## Owner lane

This repository owns:

- public entry orientation, glossary alignment, and profile-level route help
- selected shared-root install sources such as `AGENTS.md`, `AOA_WORKSPACE_ROOT`, `.agents/`, and the source-owned `.codex/` subset checked in here
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

## Start here

1. Choose the primary owner repository before editing.
2. Read `README.md`, `docs/START_HERE.md`, `GLOSSARY.md`, `docs/PUBLIC_ENTRY_POSTURE.md`, and the target repository `README.md` plus `AGENTS.md`.
3. For workspace bootstrap or projection work, also read `docs/WORKSPACE_INSTALL.md`, `docs/CODEX_PLANE_REGENERATION.md`, and the relevant `.agents/` or `.codex/` source surface.
4. For historical detail preserved from the pre-slim root, read `docs/AGENTS_ROOT_REFERENCE.md`.


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
- `Dionysus`: seed garden, staging, replay, planting trace, early forms.
- `abyss-stack`: runtime, deployment, storage, lifecycle, infrastructure posture.
- `ATM10-Agent`: local companion behavior, perception, retrieval, KAG-in-project, safe operator automation.
- `aoa-sdk`: typed workspace integration, discovery, compatibility, passive skill inspection, and explicit user-profile bootstrap.
- `aoa-techniques`: reusable engineering practice.
- `aoa-skills`: the shared portable bundle family and common owner-home compatibility contract.
- `aoa-evals`: portable proof and evaluation surfaces.
- `aoa-routing`: navigation and dispatch hints.
- `aoa-memo`: explicit memory and recall objects.
- `aoa-kag`: derived provenance-aware knowledge substrates.
- `aoa-playbooks`: recurring scenario composition, questlines, campaigns, handoffs.
- `aoa-agents`: role contracts, handoff posture, progression and checkpoint contract surfaces.
- `aoa-stats`: shared measurement grammar, owner-local stats federation, and
  derived non-sovereign read models.
- `8Dionysus`: public route map, shared-root projection source, AGENTS map audit, and concrete workspace-delivery diagnosis.

## Memory route

Use `aoa_memo` when a workspace task asks to recall, continue, preserve, compare
with past work, recover after compaction, create a memory candidate, inspect a
local memo port, or route evidence toward reviewed memory.

- Need session evidence for a stable agent-process anchor such as a skill, MCP,
  hook, tool, path, goal, or recurring failure: use `aoa_session_memory` to
  search `.aoa`, trace route maps, build retrieval/evidence packets, and check
  freshness before drawing conclusions.
- Do not treat `aoa_session_memory` as memory writeback, repair, reindex,
  distillation, or promotion authority. It is a read-only route over `.aoa`
  refs; raw transcript and reviewed session-memory authority remain in `.aoa`.
- After a meaningful landing, run a memory writeback check before closeout.
  Meaningful includes changes to owner boundaries, route law, MCP or service
  contracts, eval or proof surfaces, release posture, workflows, decisions,
  topology, public contracts, or important failures and fixes.
- Prefer `aoa-memo-writeback` for the judgment-heavy path: inspect the
  diff/PR/commits and session evidence, decide whether the event is
  memory-worthy, then create a local candidate/export or an explicit
  no-writeback closeout.
- Need continuity or context: call `aoa_memo_brief` for the owning repository
  and current intent.
- Need to preserve new memory: write through that repository's `memo/` port when
  it exists, then validate and index the port.
- Need durable reviewed memory: export reviewed intake to `aoa-memo`; the shared
  root and MCP plane do not land durable memo truth directly.
- Need owner truth: follow the owning repository first; memo carries recall,
  provenance, local candidates, and reviewed handoff.
- Need workspace memory status: regenerate `generated/workspace_memory_map.min.json`
  and `docs/WORKSPACE_MEMORY_MAP.md` from `scripts/build_workspace_memory_map.py`
  instead of guessing which repos have local ports.

## Skill inspection and mutation boundary

`aoa skills` is passive and exact. Use it only to inspect an owner-scoped
installation or one known capability node:

```bash
aoa skills inspect <repo_root> --root <workspace-root> --json
aoa skills capability <exact-node-id> --root <workspace-root> --json
```

Semantic skill retrieval and composition belong to `aoa-kag`; neither SDK
inspection nor surface detection selects, activates, or executes a skill.
Use `aoa surfaces detect` only as additive read-only routing help.

For one concrete mismatch among skill, MCP, or tool source, projection,
consumer scope, prompt/catalog visibility, configuration, transport, and owner
service, use the repo-local `aoa-workspace-diagnose` home skill. General
orientation remains in this route card and KAG. Diagnosis is read-only and does
not authorize repair, install, restart, or configuration mutation.

Risky mutations remain governed by the nearest owner `AGENTS.md`, explicit
host or human confirmation, and the applicable runtime boundary. There is no
SDK-owned skill ingress or mutation-gate command.

## Projection and audit rules

- When shared-root install surfaces change, edit the source-owned copy under `<workspace-root>/8Dionysus/` first, then project them into the live workspace root.
- Do not treat live projected copies at `/AGENTS.md`, `/AOA_WORKSPACE_ROOT`, `/.agents/`, or `/.codex/` as primary truth; in projection wording, do not treat the live copies as source.
- `8Dionysus` does not project shared bundles into `<workspace-root>/.agents/skills`. Shared AoA bundles install once through the `aoa-skills` `user-default` profile; repository projections come only from admitted owner-local `skills/` homes.
- `skills/aoa-workspace-diagnose/` is this repository's canonical local procedure; `.agents/skills/aoa-workspace-diagnose/` is its exact repo-only projection and remains excluded from workspace-root copy and prune authority.
- The generic shared-root projector neither copies nor prunes live `.codex/config.toml` or `.codex/agents/`. Project registration follows the Codex-plane render and rollout route; role-agent projection follows `aoa-agents` and its deployment policy.
- Treat source selection as part of projection safety. The installed launcher is local-only and never fetches; it refuses unless the selected owner checkout matches its declared local source ref and projector-controlled or managed source paths are clean. Use `--source-root <clean-current-8Dionysus-checkout>` when the canonical checkout is stale or carrying unrelated work.
- A direct Python dry-run may inspect an unmerged branch. Live execution from a non-current source requires the explicit `--allow-noncurrent-source` override and is branch-trial evidence, not proof of owner currentness.
- Keep `8Dionysus/README.md` profile-owned and GitHub-facing.
- Treat generated or install drift as a route signal: keep the evidence narrow, route it to the owner repository, and do not promote derived reports into authority.
- Before large AGENTS refactors, run the map audit:

```bash
python scripts/audit_agents_map.py --workspace-root <workspace-root> --write generated/agents_map.min.json --markdown docs/AGENTS_MAP.md
```

For workspace memory overlay status:

```bash
python scripts/build_workspace_memory_map.py --workspace-root <workspace-root> --owner-repo-root . --write generated/workspace_memory_map.min.json --markdown docs/WORKSPACE_MEMORY_MAP.md
python scripts/validate_workspace_memory_map.py --workspace-root <workspace-root> --owner-repo-root .
```

For public bootstrap without sibling checkouts:

```bash
python scripts/audit_agents_map.py --public-baseline --write generated/agents_map.min.json --markdown docs/AGENTS_MAP.md
```

After local `AGENTS.md` coverage changes, refresh the frontier report:

```bash
python scripts/recon_agents_frontier.py --map generated/agents_map.min.json --write generated/agents_frontier_recon.min.json --markdown generated/agents_frontier_recon.md
```

## GitHub landing workflow

Root `AGENTS.md` owns the repository-wide branch, PR, CI, and merge route.
`.github/AGENTS.md` owns the GitHub-native files that support it.

When the user asks to commit, push, and merge in this repository, use this route:

1. Start from a branch based on the current `origin/main`. If the worktree is already dirty, inventory it first and carry forward only the intended diff.
2. Commit the intended change with a message that names the changed surface.
3. Push the branch and open a pull request that states changed surfaces, validation run, skipped checks, and remaining risk.
4. Wait for GitHub `Repo Validation` and any required GitHub checks. If a check fails, fix the branch and wait for the new result.
5. Merge through GitHub after green validation. Use squash unless repository settings report a different required method; report the method that landed.
6. Return to `main`, fast-forward from `origin/main`, and confirm the worktree is clean before closeout.

If GitHub status or merge permissions cannot be observed, stop the landing route and report the exact blocker instead of guessing.

## Verify

Use the smallest route-safe check for the changed surface. For AGENTS-map or workspace route changes, run one of the audit commands above and report whether it was a public-baseline or sibling-workspace pass.
For `stats/` changes, also run `python scripts/validate_local_stats_port.py`.
If projection, hooks, plugin, convergence, or closeout details are touched, read `docs/AGENTS_ROOT_REFERENCE.md` and run the named narrow helper there before reporting.
For convergence checks, keep `aoa-codex-doctor`, `aoa-codex-status`, and `aoa-codex-bootstrap` discoverable as wrappers, and keep `aoa_codex_convergence_report.{json,md}` as evidence only. The rule is that convergence reports are evidence, not authority.

## Full reference

`docs/AGENTS_ROOT_REFERENCE.md` preserves the previous detailed root guidance, including plugin, hook, convergence, closeout, and projection details.
Use it as a depth layer when the short route card is not enough. If active rules from that reference still govern a local path, prefer moving them to the nearest owner surface rather than bloating this root again.
