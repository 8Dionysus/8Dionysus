# Codex Plane Regeneration

This note explains how the shared-root AoA Codex install surfaces remain
explicit and portable.

## Why this note exists

The public workspace root already carries a checked-in `.codex/config.toml`
and `.codex/hooks.json` that are intentionally project-scoped and
deployment-specific. They are useful because they make the current live
workspace legible to Codex and to the AoA control plane.

But a path-bound install surface should not be treated like sacred scripture.
It should be rerenderable.

`docs/WORKSPACE_INSTALL.md` already says that if the public workspace root
changes, the checked-in `.codex/` tree should be regenerated or adapted before
projection. This note turns that sentence into doctrine.
When recurring drift pressure at the workspace root needs one owner-routing
note before rerender or rollout, use `docs/COMPONENT_REFRESH_ROUTE.md`.

## Governing split

`8Dionysus` owns:

- the source-authored shared-root install subset
- the manifest/profile pair for the Codex plane
- the renderer and drift validator
- the checked-in generated `.codex/config.toml` and `.codex/hooks.json` for the
  current chosen public root
- the source templates and bounded installer for AoA-managed repo-local Git
  checkpoint hooks

It does not own:

- role meaning owned by `aoa-agents`
- MCP implementation meaning owned by `aoa-sdk`, `aoa-stats`, and `Dionysus`
- user-global Codex defaults in `~/.codex/config.toml`
- unmanaged custom hooks already present in a checkout's private `.git/hooks/`
  directory

## Primary edit surface

The primary edit surface for path-bound Codex deployment is:

- `config/codex_plane/runtime_manifest.v1.json`
- `config/codex_plane/profiles/*.json`

The checked-in generated surfaces:

- `.codex/config.toml`
- `.codex/hooks.json`

remain source-owned deployment artifacts for the current live root, not the
place where humans should manually invent path changes.

## Portability law

Portability here does not mean hiding paths behind magic. It means:

1. keep the deployment explicit
2. keep the deployment renderable
3. change the root in one place
4. regenerate the checked-in deployment surfaces
5. project them into the live workspace root

This keeps the system legible while still allowing relocation.

## Stable names

The regeneration path must preserve the stable project-facing names that other
AoA surfaces may already depend on:

- project root markers: `AOA_WORKSPACE_ROOT`, `.git`
- MCP server names: `aoa_workspace`, `aoa_stats`, `dionysus`
- hook events: `SessionStart`, `UserPromptSubmit`, `Stop`

## Relation to projection

`project_workspace_root.py` still projects the selected shared-root surfaces
into the live workspace root.

Regeneration happens before projection whenever the checked-in `.codex/`
deployment needs a new live root.

For the live deployment trail that follows rerender, use
`docs/CODEX_PLANE_ROLLOUT.md`.
For owner-routed component drift at the shared workspace root, use
`docs/COMPONENT_REFRESH_ROUTE.md`.

Repo-local Git hooks are adjacent local runtime state, not Codex event hooks.
After a root move or checkout refresh, validate them with
`scripts/manage_workspace_git_hooks.py --check` and reinstall with `--execute`
from the source templates in `config/git_hooks/`.

## Failure mode to avoid

The bad pattern is this:

- a live root changes
- someone hand-edits `.codex/config.toml`
- someone hand-edits `.codex/hooks.json`
- a later change silently drifts away from the install doctrine

The right pattern is this:

- update manifest/profile if needed
- rerender
- validate
- project
