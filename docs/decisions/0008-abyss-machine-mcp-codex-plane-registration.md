# 0008 Abyss Machine MCP Codex-Plane Registration

## Status

Accepted.

## Context

`abyss-machine` owns local host facts, policies, generated read models,
resource routing, typing state, nervous evidence, heartbeats, and the host
change ledger. `abyss-stack` owns the runnable `abyss-machine-mcp` service
package. Without a stable Codex-plane name, agents can inspect those surfaces
manually but cannot rely on one shared route for compact machine context.

## Decision

Register the host-machine access plane as the stable MCP server name
`abyss_machine` in the shared-root Codex plane.

The checked-in `8Dionysus` manifest renders the project `.codex/config.toml`.
That config points `abyss_machine` at the shared-root launcher
`.codex/bin/abyss-machine-mcp-server.py`. The launcher resolves the stack-owned
service from `AOA_ABYSS_STACK_ROOT`, `ABYSS_MACHINE_MCP_ROOT`,
`ABYSS_MACHINE_MCP_SERVER`, or the default `~/src/abyss-stack` source checkout.

## Consequences

`8Dionysus` owns the Codex-plane name, projection, launcher, smoke check, and
drift validation. `abyss-stack` owns the MCP service implementation.
`abyss-machine` remains the authority for host truth; `abyss_machine` is only a
stdio, read-only access plane for compact briefs, evidence maps, selected
safe-read surfaces, focused recall, and non-mutating route preflight.

Future Codex-plane regeneration must preserve `abyss_machine` with the existing
stable MCP names and verify that the launcher script resolves before rollout.
