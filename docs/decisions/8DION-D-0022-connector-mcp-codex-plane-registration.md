# Connector MCP Codex-Plane Registration

## Index Metadata

- Decision ID: 8DION-D-0022
- Original date: 2026-07-22
- Surface classes: codex plane, MCP access, external connector routes
- Route anchors: .codex/config.toml, .codex/bin/aoa-4pda-connector-mcp-server.py, .codex/bin/aoa-telegram-connector-mcp-server.py, .codex/bin/aoa-discord-connector-mcp-server.py, config/codex_plane/runtime_manifest.v1.json
- Owner lanes: 8Dionysus, abyss-stack, aoa-4pda-connector, aoa-telegram-connector, aoa-discord-connector
- Guard families: stable MCP name, deploy-composed transport, connector owner boundary, access-plane boundary
- Posture: accepted

## Status

Accepted.

## Context

`abyss-stack` owns three connector MCP packages and the loopback service
bundle that runs them. The live Codex configuration already named their
authenticated HTTP endpoints, but the shared-root launcher projection did not
contain the corresponding executable files. A fresh Codex process therefore
failed all three MCP initialize requests even though the service packages and
unit topology existed.

`8DION-D-0019` already separates portable source registration from
deploy-composed transport. The missing durable piece is the stable
Codex-plane name and launcher boundary, not a copy of host HTTP state into the
public source render.

## Options Considered

1. Keep the three registrations as user-global, host-local configuration only.
2. Encode the live loopback URLs and bearer-token environment binding in the
   checked-in source render.
3. Register stable portable stdio names and source-owned launchers in
   `8Dionysus`, while leaving authenticated HTTP composition and service
   lifecycle to the live deployment and `abyss-stack`.

## Decision

Choose option 3.

The Codex-plane manifest preserves the stable names
`aoa_4pda_connector`, `aoa_telegram_connector`, and
`aoa_discord_connector`. Their checked-in launchers resolve the corresponding
stack-owned service package through an explicit package override, an
`abyss-stack` root override, the normal source checkout, or the deployed
workspace tree.

The checked-in source registration remains portable stdio. Live deployment may
retain the same names over authenticated loopback HTTP under the
deploy-composed boundary established by `8DION-D-0019`.

## Consequences

- a clean shared-root projection contains every executable named by the three
  connector registrations;
- `8Dionysus` owns only the stable names, launchers, regeneration shape, and
  public route explanation;
- `abyss-stack` continues to own MCP implementation and service lifecycle;
- connector repositories continue to own source policy, packet truth,
  credentials, sessions, and generated storage;
- source-render validation does not claim that live transport, authentication,
  or service health were checked.
