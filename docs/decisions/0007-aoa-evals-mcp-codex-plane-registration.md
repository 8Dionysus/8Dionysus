# 0007 AoA Evals MCP Codex-Plane Registration

## Status

Accepted.

## Context

`aoa-evals` defines the bounded proof contract for `aoa_evals`, while
`abyss-stack` owns the runnable `aoa-evals-mcp` service package. Without a
stable Codex-plane name, agents can inspect the package manually but cannot
rely on one shared route from arbitrary workspace roots.

## Decision

Register the bounded proof access plane as the stable MCP server name
`aoa_evals` in the shared-root Codex plane.

The checked-in `8Dionysus` manifest renders the project `.codex/config.toml`.
That config points `aoa_evals` at the shared-root launcher
`.codex/bin/aoa-evals-mcp-server.py`. The launcher resolves the stack-owned
service from `AOA_ABYSS_STACK_ROOT`, `AOA_EVALS_MCP_ROOT`,
`AOA_EVALS_MCP_SERVER`, or the default `~/src/abyss-stack` source checkout.

## Consequences

`8Dionysus` owns the Codex-plane name, projection, launcher, and drift
validation. `abyss-stack` owns the MCP service implementation. `aoa-evals`
remains the authority for proof meaning; `aoa_evals` is only an access plane
for selection, inspection, generated-reader context, read-only find-or-propose
eval-need routing, runtime evidence template lookup, candidate validation,
runtime candidate export reads, and candidate-only report skeletons.

Find-or-propose output is route context only. Proposal approval, source bundle
creation, verdicts, receipt publication, bundle promotion, and proof authority
stay outside the shared-root Codex plane.

Future Codex-plane regeneration must preserve `aoa_evals` with the existing
stable MCP names and verify that the launcher script resolves before rollout.
