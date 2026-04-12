# Component Refresh Route

This note explains how the shared workspace root should react when internal AoA
components appear stale, drifting, or repeatedly hand-patched.

Use [CODEX_PLANE_REGENERATION.md](CODEX_PLANE_REGENERATION.md) for the
source-authored rerender path of the shared-root Codex plane.
Use [CODEX_PLANE_ROLLOUT.md](CODEX_PLANE_ROLLOUT.md) for live trust, apply,
doctor, and rollback posture after rerender.
Use [TRUSTED_ROLLOUT_CAMPAIGNS.md](TRUSTED_ROLLOUT_CAMPAIGNS.md) when the route
widens into grouped recurring rollout maintenance.
Use this note when the workspace root notices the drift and must route that
evidence back to the owning repository.

It is a route note, not an ownership transfer.

## Workspace role

The workspace root may notice component drift through:

- repeated doctor warnings
- repeated manual refresh patches
- project-scoped generated or install surfaces drifting from source-owned inputs
- stale summary windows
- rollout or continuity routes blocked by one named component

When that happens, the root should:

1. route the evidence to the owner repo
2. preserve reviewed hints
3. avoid pretending that the workspace root itself owns the component

## First named component at this root

`component:codex-plane:shared-root`

### Source-authored inputs

- `config/codex_plane/runtime_manifest.v1.json`
- `config/codex_plane/profiles/*.json`

### Generated or deployed surfaces

- `.codex/config.toml`
- `.codex/hooks.json`

### Drift examples

- the public workspace root changed but `.codex` was not rerendered
- stable MCP names drifted
- doctor fails after render
- the same path-bound hand patch was repeated instead of rerendering

### Honest route

- notice drift
- create or preserve a reviewed hint
- rerender from manifest or profile
- validate and doctor
- record rollout or rollback outcome

This note does not make `8Dionysus` the owner of skill export truth, subagent
projection truth, or stats truth.
