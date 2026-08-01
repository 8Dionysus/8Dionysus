# Defer Project MCP Registration to Explicit Rollout

## Index Metadata

- Decision ID: 8DION-D-0027
- Original date: 2026-08-01
- Surface classes: Codex plane, MCP consumer registration, source render
- Route anchors: .codex/config.toml, config/codex_plane/runtime_manifest.v1.json, config/codex_plane/profiles/linux-python3.json, scripts/render_codex_plane.py
- Owner lanes: 8Dionysus, abyss-stack, operator
- Guard families: config-layer composition, transport safety, explicit rollout, stable MCP names
- Posture: accepted; refines 8DION-D-0019 and 8DION-D-0024

## Status

Accepted for the OS Abyss organ-fabric consumer source.

## Context

The checked-in project render historically emitted portable stdio MCP entries
under the same stable names used by the deploy-composed user-global HTTP
registration. Codex 0.146.0 composes these trusted-project and global server
tables field-by-field. In an actual owner worktree, `aoa_decisions` therefore
acquired both `command` and `url`; Codex rejected the complete configuration
before app-server or any MCP could start.

Disabling the server does not remove the conflicting inherited transport
fields. Renaming the project entries would load duplicate catalogs and break
stable handles. Making the portable source guess a host deployment would move
runtime and credential composition into `8Dionysus`.

## Decision

The default checked-in project profile uses
`project_mcp_registration_mode = defer_to_explicit_rollout` and emits no
`[mcp_servers.*]` tables into `.codex/config.toml`.

The runtime manifest continues to own the stable-name and portable launcher
inventory. The deny-by-default organ-fabric manifest continues to own bounded
profile candidates. Only an explicit operator-selected deployment scope may
compose live registrations and credentials.

An isolated portability test may still render `portable_stdio`, but that mode
is not the checked-in trusted-project posture and cannot be combined with the
same globally registered names.

## Consequences

- entering the repository no longer corrupts a valid global HTTP contour;
- a standalone clone does not gain ambient MCP registrations merely by being
  trusted;
- stable names and launchers remain reviewable without becoming active;
- live registration, schema re-observation, removal, and rollback stay in the
  explicit organ-fabric rollout;
- source-render validation must reject project MCP tables in the default
  profile.

## Verification

Regenerate the project config, run the Codex-plane tests and validators, then
run `codex mcp list` from the owner worktree with the deployed global contour.
The command must load successfully and must not report a mixed stdio/HTTP
transport shape.
