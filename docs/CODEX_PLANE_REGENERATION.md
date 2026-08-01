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
- the checked-in generated `.codex/config.toml` and `.codex/hooks.json` as
  source render artifacts for the current chosen public root; the project
  config deliberately contains no MCP server tables
- the source templates and bounded installer for AoA-managed repo-local Git
  checkpoint hooks

It does not own:

- role meaning owned by `aoa-agents`
- MCP implementation owned by `aoa-sdk` for `aoa_workspace` and `abyss-stack`
  for stack-owned access planes such as
  `aoa-stats-mcp`, `aoa-memo-mcp`, `aoa-session-memory-mcp`, `aoa-evals-mcp`,
  `aoa-kag-mcp`, `aoa-decisions-mcp`, `abyss-machine-mcp`,
  `tos-corpus-mcp`,
  `aoa-4pda-connector-mcp`, `aoa-telegram-connector-mcp`, and
  `aoa-discord-connector-mcp`; `aoa-stats`
  owns the statistical meaning exposed through `aoa_stats`, `.aoa` owns raw
  session evidence exposed by `aoa_session_memory`, `aoa-evals` owns the proof
  contract exposed by `aoa_evals`, `aoa-kag` owns KAG meaning exposed by
  `aoa_kag`, `aoa-skills` owns the decision-lane route exposed through
  `aoa_decisions`, and `abyss-machine` owns the host truth exposed by
  `abyss_machine`; Tree of Sophia owns corpus meaning exposed by any admitted
  `tos_corpus` contour
- user-global Codex defaults in `~/.codex/config.toml`
- unmanaged custom hooks already present in a checkout's private `.git/hooks/`
  directory

## Primary edit surface

The primary edit surface for path-bound Codex deployment is:

- `config/codex_plane/runtime_manifest.v1.json`
- `config/codex_plane/profiles/*.json`

The future HTTP organ-fabric consumer has a separate, receipt-gated source
surface:

- `config/codex_plane/organ_fabric/codex_consumer_manifest.v1.json`
- `config/codex_plane/organ_fabric/current_consumer_observation.public.json`

It is rendered with `scripts/render_codex_organ_fabric.py` and governed by
`docs/CODEX_ORGAN_FABRIC_CONSUMER.md`. It does not replace the portable source
registration until the integrated rollout closes its registry, runtime,
consumer-schema, owner-acceptance, and rollback gates.

The source tree may carry a wrapper for an organ before admission so the
stack-owned runtime package has one portable projection route. In particular,
`tos-corpus-mcp-server.py` does not add `tos_corpus` to the stable names below:
the contour remains suspended and unregistered until the organ-fabric receipt
gates pass.

The checked-in generated surfaces:

- `.codex/config.toml`
- `.codex/hooks.json`

remain source-owned deployment artifacts for the current live root, not the
place where humans should manually invent path changes.

Codex merges user-global and trusted-project MCP tables field-by-field. A
portable project `command` combined with a deploy-composed global `url` under
the same stable name is an invalid transport shape. The current project render
therefore retains stable-name and launcher inventory in the manifest but emits
no `[mcp_servers.*]` tables. MCP registration is composed only through the
explicit organ-fabric rollout or another isolated operator-selected scope.

That source ownership does not make the generic shared-root projector the
live deployment composer. A deployed `.codex/config.toml` may replace portable
stdio registrations with authenticated loopback endpoints while retaining the
stable names. The live form is verified through rollout evidence, not by
forcing byte parity with the source render.

## Portability law

Portability here does not mean hiding paths behind magic. It means:

1. keep the deployment explicit
2. keep the deployment renderable
3. change the root in one place
4. regenerate the checked-in deployment surfaces
5. roll out the rendered registration through the explicit deployment route

This keeps the system legible while still allowing relocation.

## Stable names

The regeneration path must preserve the stable project-facing names that other
AoA surfaces may already depend on:

- project root markers: `AOA_WORKSPACE_ROOT`, `.git`
- MCP server inventory names: `aoa_workspace`, `aoa_stats`, `aoa_memo`, `aoa_session_memory`, `aoa_evals`, `aoa_kag`, `aoa_decisions`, `abyss_machine`, `aoa_4pda_connector`, `aoa_telegram_connector`, `aoa_discord_connector`; these are not automatically emitted into the project layer
- hook events: `SessionStart`, `UserPromptSubmit`, `Stop`

## Relation to projection

`project_workspace_root.py` still projects the source-owned shared-root subset
into the live workspace root. It deliberately excludes `.codex/config.toml`
from copy and prune authority. It also excludes `.codex/agents/`, whose source
projection belongs to `aoa-agents` and whose installed form may include
deployment policy.

Regeneration happens before the dedicated Codex-plane rollout whenever the
checked-in source registration needs a new live root. Agent regeneration and
installation follow the `aoa-agents` projection and refresh route.

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
- compare the intended deployment composition
- roll out and verify the live registration without routing it through the
  generic shared-root projector

`validate_codex_plane_regeneration.py` validates only the checked-in source
render. Its output states `live_deployment_compared=false`; live transport,
authentication, and agent restrictions require the rollout and owner routes.
`validate_codex_organ_fabric.py` adds source validation for the fail-closed
future consumer projection without treating it as part of the existing stable
portable registration.
