# AoA Shared Launchers plugin notes

This plugin is intentionally narrow.

- It bundles shared launcher skills.
- It relies on project-scoped named MCP servers already configured in `.codex/config.toml`.
- It does not try to move AoA owner meaning into the plugin layer.
- It does not bundle `.mcp.json` in this first wave.
- It treats `aoa_memo` as the memory access plane for brief, search, local-port
  status, candidate creation, port indexing, and reviewed-intake preparation.
  Durable memory truth still lands through `aoa-memo`.
- It treats `aoa_session_memory` as the session-evidence access plane for
  `.aoa` search, route maps, briefs, retrieval packets, evidence handles,
  freshness, diagnostics, and non-mutating maintenance plans. Raw transcript
  and reviewed distillation truth still live in `.aoa`.
- It treats `aoa_evals` as the bounded proof access plane for selection,
  inspection, generated-reader context, read-only find-or-propose eval-need
  routing, runtime evidence templates, and candidate-only report skeletons.
  Verdict authority, proposal approval, and source bundle creation still land
  through `aoa-evals`.
- It treats `aoa_decisions` as the workspace decision graph access plane for
  search, repo packets, decision packets, and graph freshness checks. Source
  decision records, creation, correction, and supersession still land through
  the owning repository's `docs/decisions/` lane.

Bundled skills:
- `aoa-workspace-recon`
- `aoa-growth-snapshot`
- `aoa-seed-route-inspect`
- `aoa-config-doctor`

Each bundled skill includes `agents/openai.yaml` with named MCP dependencies where appropriate.
`aoa-config-doctor` now resolves the real AoA workspace root from either
`/srv/AbyssOS` or a repo-local checkout before it recommends workspace validators.
