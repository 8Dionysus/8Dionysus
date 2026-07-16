# AoA Shared Launchers plugin notes

This plugin is intentionally narrow and provisional.

- It bundles two explicit-only launcher candidates pending separate owner-first
  admission audits.
- It relies on project-scoped named MCP servers already configured in `.codex/config.toml`.
- It does not try to move AoA owner meaning into the plugin layer.
- It does not bundle `.mcp.json` in this first wave.
- It uses `aoa_workspace` only for route context. Workspace orientation remains
  in root route cards and KAG rather than a generic callable skill.
- It treats `aoa_stats` as the read-only statistical access plane for derived
  catalogs, owner-local ports, boundary references, and compatibility checks.
  Statistical meaning remains in `aoa-stats`, owner-local meaning remains in
  each source repository, and runnable service code remains in `abyss-stack`.
- It treats `dionysus` as seed-garden and planting-route context. Staging does
  not become final owner truth.

Bundled skills:
- `aoa-growth-snapshot`
- `aoa-seed-route-inspect`

Each remaining bundle includes `agents/openai.yaml`, is explicit-only, and has
not been admitted as an owner home skill by this repository.

`8DION-D-0018` retired `aoa-workspace-recon` and `aoa-config-doctor` after
manual comparison. Concrete read-only delivery diagnosis now belongs to the
repo home `aoa-workspace-diagnose`; `aoa-codex-doctor`, status, and bootstrap
remain tools and wrappers rather than skills.
