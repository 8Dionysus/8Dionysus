# Workspace Install

This note explains the public workspace layout for running the AoA / ToS ecosystem as one local project.
It is an orientation and install-source surface.
The shared profile and common repository-home contract live in `aoa-skills`;
passive workspace discovery and explicit user-profile bootstrap live in
`aoa-sdk`. `8Dionysus` owns the selected shared-root surfaces projected from
this repository and its one admitted repo-local diagnosis home.

## Canonical shape

Use one parent directory that keeps the public repositories as sibling checkouts:

```text
<workspace-root>/
  AGENTS.md
  AOA_WORKSPACE_ROOT
  .agents/
    plugins/
      marketplace.json
  .codex/
    config.toml
    hooks.json
    agents/
    hooks/
    plugins/
    scripts/
    tools/
  8Dionysus/
  Agents-of-Abyss/
  Tree-of-Sophia/
  Dionysus/
  aoa-agents/
  aoa-evals/
  aoa-kag/
  aoa-memo/
  aoa-playbooks/
  aoa-routing/
  aoa-sdk/
  aoa-skills/
  aoa-stats/
  aoa-techniques/
```

`8Dionysus` stays the public profile and route map.
It is part of the workspace, but it does not replace the source repositories.
Inside that checkout, `skills/aoa-workspace-diagnose/` is canonical and
`.agents/skills/aoa-workspace-diagnose/` is its exact repo-only Codex
projection. Neither path is a workspace-root projection source.

## Selected shared-root install surfaces

`8Dionysus` is also the source-owned home for a small shared-root install
subset that is projected into the live workspace root:

- `<workspace-root>/AGENTS.md`
- `<workspace-root>/AOA_WORKSPACE_ROOT`
- `<workspace-root>/.agents/`
- `<workspace-root>/.codex/`

Those surfaces exist to make the live workspace legible and usable for Codex
and AoA tooling. They do not make `8Dionysus` the owner of layer-specific
runtime, charter, or implementation truth.

Projection rules:

- keep `README.md` profile-owned and GitHub-facing; it is not part of the shared-root install projection
- keep personal Codex defaults in `~/.codex/config.toml`, not in the project-level `.codex/`
- treat `<workspace-root>/AOA_WORKSPACE_ROOT` as the sibling-workspace marker for Codex and AoA tooling
- treat `<workspace-root>/.agents/plugins/marketplace.json` as the local plugin discovery surface; the `8Dionysus` projector neither copies nor prunes `<workspace-root>/.agents/skills/`
- install the advertised shared AoA profile once into the host-selected user skill root, normally `${CODEX_HOME:-$HOME/.codex}/skills`; do not reproduce it at the workspace root or in every sibling repository
- keep a sibling repository's canonical callable procedures under that owner's admitted top-level `skills/` home and derive any repo-local `.agents/skills/` projection only through its owner builder
- keep `8Dionysus/skills/aoa-workspace-diagnose/` and its exact repo projection inside the `8Dionysus` checkout; the shared-root projector must neither copy nor prune it at `<workspace-root>/.agents/skills/`
- treat `<workspace-root>/.codex/` as the project-level Codex install surface for hooks, agents, plugins, scripts, convergence tooling, tests, and named MCP server wiring such as `aoa_workspace`, `aoa_stats`, `dionysus`, `aoa_memo`, `aoa_session_memory`, `aoa_evals`, `aoa_kag`, `aoa_decisions`, and `abyss_machine`
- treat the checked-in `.codex/` tree as the source-owned install surface for the current live workspace deployment; if the public workspace root changes, regenerate or adapt the path-bound wiring before projecting it
- the checked-in `.codex/config.toml` and `.codex/hooks.json` are source-owned generated deployment artifacts for the current chosen public workspace root; if that root changes, rerender them from `config/codex_plane/runtime_manifest.v1.json` and the selected profile before projection, rather than hand-editing them as the primary change surface
- live rollout evidence for the current workspace root belongs under `<workspace-root>/.codex/generated/rollout/`; keep it deploy-local and use `docs/CODEX_PLANE_ROLLOUT.md` for trust, doctor, and rollback posture
- checked-in trusted rollout campaign history for the shared-root Codex plane belongs under `8Dionysus/generated/codex/rollout/`; keep it source-owned and use `docs/CODEX_TRUSTED_ROLLOUT_OPERATIONS.md` for campaign, drift-window, rollback-window, and summary posture
- recurring campaign cadence windows that group multiple rollout attempts belong in `8Dionysus/examples/` and `docs/TRUSTED_ROLLOUT_CAMPAIGNS.md`; keep them source-owned, reviewable, and companion-only rather than letting them become a scheduler or a second playbook
- keep `<workspace-root>/.codex/generated/` and
  `<workspace-root>/.codex/worktrees/` deploy-local; generated reports, event
  logs, worktree contents, and other runtime output are outside projector copy
  and prune authority and must not be copied back into `8Dionysus` as source
  truth

Decision note:

- `docs/decisions/8DION-D-0001-shared-root-projection.md`
- `docs/decisions/8DION-D-0017-owner-scoped-skill-projections.md`
- `docs/decisions/8DION-D-0018-workspace-capability-diagnosis-home-skill.md`

## Foundation install

After the sibling checkouts are present, use the passive `aoa-sdk` bootstrap
to install the exact `aoa-skills` `user-default` profile into the verified user
skill root:

```bash
aoa workspace bootstrap <workspace-root> --profile user-default --json
aoa workspace bootstrap <workspace-root> --profile user-default --execute --json
aoa skills inspect <workspace-root>/8Dionysus --root <workspace-root> --json
```

The command copies only the advertised shared bundle into the user root. It
does not mutate workspace guidance, install repository profiles, or create a
workspace-wide skill projection. The selected `8Dionysus` shared-root install
surfaces are projected separately.

It also does not install `aoa-workspace-diagnose` at user or workspace scope.
Codex discovers that owner home from `8Dionysus/.agents/skills/` only when the
active repository scope is `8Dionysus`. A session launched from the workspace
root or another sibling should not see it unless that host performs an explicit
owner-approved retrieval.

Manual install remains available as the lower-level fallback:

Install the same user profile directly from `aoa-skills`:

```bash
python <workspace-root>/aoa-skills/scripts/install_skill_pack.py \
  --repo-root <workspace-root>/aoa-skills \
  --profile user-default \
  --dest-root "${CODEX_HOME:-$HOME/.codex}/skills" \
  --mode copy \
  --execute \
  --format json
```

Verify the result:

```bash
python <workspace-root>/aoa-skills/scripts/verify_skill_pack.py \
  --repo-root <workspace-root>/aoa-skills \
  --profile user-default \
  --install-root "${CODEX_HOME:-$HOME/.codex}/skills" \
  --format json
```

The deferred shared bundles are available for explicit research and manual
comparison, not implicit installation. A repository-scoped profile is an
input to that repository's admitted home-skill builder; `aoa workspace
bootstrap` intentionally refuses to install it.

### Legacy workspace projection cleanup

An existing `<workspace-root>/.agents/skills/` may be an older shared-profile
copy. Do not infer that from the path alone. Compare every bundle with the
current `aoa-skills` owner catalog and check for workspace-owned procedures
before removal. Move the reviewed legacy directory to a temporary rollback
location, verify prompt visibility and owner-local home skills, then delete the
temporary copy. The `8Dionysus` projector deliberately excludes this path from
both copy and prune operations.

## Projection sync

Use the repository-local projection tool to preview or apply the selected
shared-root surfaces from `8Dionysus` into the live workspace root:

```bash
<workspace-root>/.codex/bin/aoa-workspace-project --json
<workspace-root>/.codex/bin/aoa-workspace-project --check --json
<workspace-root>/.codex/bin/aoa-workspace-project --execute --json
```

The direct Python entrypoint remains available:

```bash
python <workspace-root>/8Dionysus/scripts/project_workspace_root.py --workspace-root <workspace-root> --json
python <workspace-root>/8Dionysus/scripts/project_workspace_root.py --workspace-root <workspace-root> --check --json
python <workspace-root>/8Dionysus/scripts/project_workspace_root.py --workspace-root <workspace-root> --execute --json
```

Source-first law for these projected surfaces:

- if the change is real, edit the source-owned copy under `<workspace-root>/8Dionysus/` first
- do not hand-edit `<workspace-root>/AGENTS.md`, `<workspace-root>/AOA_WORKSPACE_ROOT`, `<workspace-root>/.agents/`, or `<workspace-root>/.codex/` as if those live copies were the primary source of truth
- treat `<workspace-root>/.agents/skills/` separately: it is excluded from this projector and must be routed to its workspace or repository owner before mutation
- use `--check --json` to see the owner repo, source paths, projected paths, and the next-step guidance before mutation
- after the source edit, rerun the projection with `--execute` and confirm `--check` returns clean
- keep `8Dionysus/README.md` profile-owned and outside this projection path

When the checked-in Codex plane needs a new live root, rerender it before projection:

```bash
python <workspace-root>/8Dionysus/scripts/render_codex_plane.py \
  --manifest <workspace-root>/8Dionysus/config/codex_plane/runtime_manifest.v1.json \
  --profile <workspace-root>/8Dionysus/config/codex_plane/profiles/linux-python3.json \
  --workspace-root <workspace-root> \
  --dest-config <workspace-root>/8Dionysus/.codex/config.toml \
  --dest-hooks <workspace-root>/8Dionysus/.codex/hooks.json \
  --dest-report <workspace-root>/8Dionysus/config/codex_plane/examples/current-srv.paths.json
python <workspace-root>/8Dionysus/scripts/validate_codex_plane_regeneration.py --workspace-root <workspace-root>
```

After rerender, treat rollout as a separate phase: capture trust, apply only as
needed, run doctor/verify, and keep rollout receipts under
`<workspace-root>/.codex/generated/rollout/` instead of treating render success
as rollout success. See `docs/CODEX_PLANE_ROLLOUT.md`.

When the route becomes a bounded campaign rather than one deploy-local apply,
publish the checked-in shared-root campaign history, drift window, rollback
window, and latest-trusted summary in `8Dionysus/generated/codex/rollout/` and
review them through `docs/CODEX_TRUSTED_ROLLOUT_OPERATIONS.md`.

When recurring grouped maintenance needs one cadence layer above those
individual rollout attempts, keep the campaign, drift-review, and
rollback-followthrough windows source-owned in `8Dionysus/examples/` and
review them through `docs/TRUSTED_ROLLOUT_CAMPAIGNS.md`.

When repeated doctor warnings, hand-patched refreshes, stale generated
surfaces, or blocked rollout or continuity routes point at one drifting
component, keep the workspace role narrow and route that evidence through
`docs/COMPONENT_REFRESH_ROUTE.md` back to the owner repo.

Behavior:

- the launcher resolves both the source-owned `8Dionysus/.codex/bin/` copy and the projected live `<workspace-root>/.codex/bin/` copy
- dry-run is the default
- `--check` exits nonzero when drift exists
- `--execute` applies the projection
- `--prune` may be added when you want managed extra paths removed too
- `AGENTS.md` is rendered by replacing `<workspace-root>` with the target live root

## Repo-local Git hooks

Git stores active hooks inside each checkout's private `.git/hooks/` directory,
so they are not normal shared-root projection files. `8Dionysus` keeps the
source templates for AoA checkpoint hooks under `config/git_hooks/` and manages
the active local copies with:

```bash
python <workspace-root>/8Dionysus/scripts/manage_workspace_git_hooks.py \
  --workspace-root <workspace-root> \
  --check \
  --json
python <workspace-root>/8Dionysus/scripts/manage_workspace_git_hooks.py \
  --workspace-root <workspace-root> \
  --execute \
  --json
```

After projection, the same route is available through the workspace launcher:

```bash
<workspace-root>/.codex/bin/aoa-workspace-git-hooks --check --json
<workspace-root>/.codex/bin/aoa-workspace-git-hooks --execute --json
```

The managed hooks are `pre-merge-commit`, `pre-push`, and `post-commit`. The
installer renders their workspace-root default, preserves local overrides via
`AOA_CHECKPOINT_WORKSPACE_ROOT` and `AOA_CHECKPOINT_AOA_BIN`, and refuses to
overwrite unmanaged existing hooks unless `--force` is passed after review.

## Skill inspection

Use `aoa-sdk` only for passive owner-scoped inspection and exact capability
lookup:

```bash
aoa skills inspect <repo-root> --root <workspace-root> --json
aoa skills capability <exact-node-id> --root <workspace-root> --json
```

These commands do not select, activate, execute, or create session state for a
skill. Use KAG for semantic retrieval and task-local composition. Risky
mutations stay governed by the nearest owner contract plus explicit host or
human confirmation.

When one concrete expected skill, MCP, or tool disagrees across owner source,
projection, host scope, prompt/catalog, config, transport, or service state,
the repo-local `aoa-workspace-diagnose` procedure provides the read-only route.
General orientation remains in route cards and KAG; repair remains a separate
owner-authorized workflow.

## Notes

- `8Dionysus` owns the source copies for the selected shared-root install surfaces it projects into the live workspace root.
- `README.md` in `8Dionysus` remains the profile page and should not be treated as the workspace install authority surface.
- `Dionysus` is the seed garden and staging surface in the public workspace.
- `aoa-skills` owns shared portable skill exports, install profiles, the common
  home-port grammar, and its structural validators. Each admitted repository
  owns its local skill meaning and lifecycle.
- `aoa-sdk` owns workspace discovery, typed reads, passive inspection, explicit user-profile bootstrap, and reviewed evidence handoff helpers.
- `docs/COMPONENT_REFRESH_ROUTE.md` names the workspace-root route for owner-owned component drift without transferring component truth into `8Dionysus`.
- `abyss-stack` is part of the ecosystem, but the current preferred source checkout remains separately managed. For its machine-readable path rules, see `aoa-sdk/docs/workspace-layout.md`.
