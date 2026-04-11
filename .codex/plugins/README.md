# Workspace Plugins

This directory holds workspace-scoped local Codex plugins for `/srv`.

Boundary order:

1. owner-repo skill and role meaning
2. workspace MCP authority in `/srv/.codex/config.toml`
3. plugin discovery in `/srv/.agents/plugins/marketplace.json`
4. plugin packaging in `/srv/.codex/plugins/`

Do not treat installed plugins here as owner truth.
They are launcher packaging that depends on already-landed workspace surfaces.
