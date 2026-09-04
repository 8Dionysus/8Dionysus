# AGENTS.md

## Guidance for `generated/`

`generated/` stores derived audit, projection, and compact report surfaces. Generated files are evidence and transport; they are not source-owned doctrine.

Prefer regenerating generated files through the owning script instead of hand-editing them. If a generated surface exposes drift, fix the source, validator, schema, or map logic that produced it.

Keep generated outputs compact, deterministic, and public-safe. Do not place secrets, raw private traces, or local absolute paths here.

Run the applicable root routes in `../VALIDATION.md#agents-map-and-workspace-audit`,
including `recon_agents_frontier.py`.
