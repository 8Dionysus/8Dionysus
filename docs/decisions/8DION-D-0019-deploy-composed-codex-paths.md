# Deploy-Composed Codex Paths Stay Outside Generic Projection

## Index Metadata

- Decision ID: 8DION-D-0019
- Original date: 2026-07-16
- Surface classes: shared-root projection, Codex deployment, agent projection
- Route anchors: .codex/config.toml, .codex/agents, scripts/project_workspace_root.py, docs/CODEX_PLANE_REGENERATION.md
- Owner lanes: 8Dionysus, aoa-agents, abyss-stack, workspace root
- Guard families: projection source truth, deploy composition, transport safety, owner boundary
- Posture: accepted; partially supersedes 8DION-D-0001

## Status

Accepted.

## Context

`8Dionysus` keeps a rendered project registration and Codex-facing agent
companions inside its checked-in `.codex/` tree. The live workspace also
contains `.codex/config.toml` and `.codex/agents/`, but those two paths are
compositions rather than ordinary byte projections:

- source registration may use portable stdio while the deployed registration
  retains the same stable MCP names over authenticated loopback HTTP;
- agent role meaning and base projection come from `aoa-agents`, while the
  installed TOML may add deployment restrictions for plugins and MCPs.

A manual `--prune` dry-run from a clean `8Dionysus` source proposed replacing
the live HTTP registration and ten live agent files. The source-render
validator was green at the same time because it checked only the checked-in
render, not the live deployment. Applying that plan would have regressed MCP
transport and removed explicit agent restrictions while reporting ordinary
projection drift.

## Options Considered

1. Continue copying both paths byte-for-byte through the generic projector.
2. Teach the generic projector to merge transport and agent-policy overlays.
3. Exclude both paths from generic copy and prune authority and keep their
   dedicated owner and rollout routes explicit.

Option 1 cannot distinguish a source refresh from a deployment regression.
Option 2 would make a public-entry file projector the hidden owner of MCP
transport composition and agent policy. Choose option 3.

## Decision

The generic shared-root projector must neither copy nor prune:

- `<workspace-root>/.codex/config.toml`;
- `<workspace-root>/.codex/agents/`.

`8Dionysus` continues to own the manifest, profiles, renderer, stable names,
and checked-in source registration. Live registration changes follow the
Codex-plane rollout route and must verify transport and authentication against
the deployed runtime.

`aoa-agents` continues to own role profiles, projection wiring, and generated
agent companions. Installing those companions must use an explicit deployment
route that preserves or deliberately regenerates deployment policy.

The generic projector still manages its remaining source-owned `.codex/`
subset and may prune stale files only inside that managed subset. Deploy-local
`.codex/generated/` and `.codex/worktrees/` remain excluded as before.

`validate_codex_plane_regeneration.py` must identify its result as source-render
validation and state that the live deployment was not compared.

## Consequences

- shared-root plugin, hook, tool, script, test, and launcher updates remain
  projectable and reviewable;
- live bearer-enabled MCP registration cannot be silently replaced by a
  portable source form through shared-root projection;
- live agent restrictions cannot be erased by a stale public companion;
- a clean initial install now needs the explicit Codex-plane and `aoa-agents`
  deployment routes for the excluded paths;
- source-render green and live-deployment green remain separate claims.

## Verification

Verify the boundary first through a dry-run against the intended live root.
The operation set must contain no config, agent, skill-projection, or worktree
paths. Then execute against an isolated workspace containing a live HTTP
registration and restricted agent TOML; their hashes must remain unchanged
while a managed source file is copied and a managed extra is pruned.

Focused tests preserve only the file-boundary invariant learned from those
manual trials. Live transport, authentication, prompt visibility, and agent
behavior remain manual rollout checks.

## Supersession

This decision supersedes only the broad `.codex/` copy-and-prune clause in
`8DION-D-0001` for `.codex/config.toml` and `.codex/agents/`. It does not alter
the `.agents/skills/` supersession recorded by `8DION-D-0017` or transfer
runtime and role authority into `8Dionysus`.
