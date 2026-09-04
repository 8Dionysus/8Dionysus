# AGENTS.md

## Guidance for `.codex/`

`.codex/` holds Codex-plane projection, regeneration, wrappers, hooks, tests,
and local operator-adjacent surfaces for the public entry repository. It does
not own AoA doctrine, sibling contracts, runtime truth, or domain meaning.

## Source and projection boundary

Source-owned files in this checkout may be edited. Installed workspace copies
are secondary evidence of projection or deployment drift.

The generic shared-root projector manages only its declared source subset. It
excludes live `.codex/config.toml`, whose registration may be deploy-composed;
`.codex/agents/`, whose role projection belongs to `aoa-agents`; and
deploy-local `generated/` and `worktrees/`. Use each excluded path's named
owner route rather than forcing copy or prune parity.

The checked-in project config intentionally emits no MCP tables. Codex composes
global and project tables additively, so portable stdio and deployed HTTP
fields under one stable name would form an invalid transport before startup.
Stable names and launcher sources stay in
`config/codex_plane/runtime_manifest.v1.json`; registration changes use the
explicit rollout in `docs/CODEX_PLANE_REGENERATION.md`.

The installed `aoa-workspace-project` launcher does not fetch. It must refuse
before diff planning unless the selected owner checkout matches its available
local source ref and all managed source paths are clean. Use an explicit clean
current `--source-root`; use the direct Python entrypoint only for a
non-mutating branch preview.

## Organ-fabric consumer

`config/codex_plane/organ_fabric/` is deny-by-default. A bounded profile may
render only with exact admission, consumer-schema, central-proof, canary,
owner-acceptance, and rollback receipts. The render is a review fragment, not
live apply authority. Keep the legacy stable-name route until rollout proves
replacement and consumer-zero.

The `tos-corpus-mcp-server.py` wrapper is only a source projection to the
stack package. It does not admit or register `tos_corpus`; that contour stays
suspended until its organ-fabric receipts close.

## Access-plane routes

Open `docs/CODEX_PLANE_REGENERATION.md` and the matching decision record only
when registration semantics are in scope. For a wrapper or consumer change,
return evidence to the named owner:

- `aoa_stats`: read-only statistical access; meaning stays in `aoa-stats`
  and local questions stay with their repositories
- `aoa_memo`: recall, local-port, candidate, index, and intake access;
  durable reviewed memory stays in `aoa-memo`
- `aoa_session_memory`: read-only `.aoa` refs, packets, freshness, and
  diagnostics; raw and reviewed session authority stays in `.aoa`
- `aoa_evals`: selection, inspection, candidate validation, and candidate
  exports; verdict, acceptance, promotion, and proof stay in `aoa-evals`
- `aoa_kag`: provider, source-return, freshness, composition, and validation
  access; KAG contracts stay in `aoa-kag`
- `aoa_decisions`: search and packetization; authored decisions and local
  index validators stay in their owner repositories
- `abyss_machine`: compact safe host reads and preflight; machine truth,
  policy, mutation, and ledger authority stay in `abyss-machine`
- `aoa_4pda_connector`, `aoa_telegram_connector`, and
  `aoa_discord_connector`: external evidence access; source policy,
  credentials, packets, and generated storage stay with connector owners

Runnable access-plane packages remain with `abyss-stack` unless a named owner
contract says otherwise. No access plane becomes source truth by registration.

## Stop lines

No secrets, tokens, private hostnames, hidden automation, or unreviewed hooks
belong here. Mutating helpers must stay bounded, documented, reversible, and
owner-routed.

If a handle reports `Transport closed`, do not claim availability from
registration. Run its service CLI or stdio smoke check, then restart the Codex
MCP host/session before relying on live calls.

For one concrete mismatch across owner source, projection, host scope,
prompt/catalog, config, transport, and service, route to
`skills/aoa-workspace-diagnose`. It diagnoses read-only and never authorizes
repair, install, restart, or configuration mutation.

## Verify

Run only the checks matching the changed surface:

Run the relevant on-demand route in the repository [VALIDATION](../VALIDATION.md):
`#codex-plane` for organ-fabric and memory-map projection, and
`#agents-map-and-workspace-audit` for the AGENTS-map audit.

For a changed MCP wrapper or registration, run its matching
`scripts/smoke_*_mcp.py` check. Do not run every access-plane smoke test for an
unrelated `.codex/` edit.
