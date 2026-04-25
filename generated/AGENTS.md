# AGENTS.md

## Guidance for `generated/`

`generated/` stores derived audit, projection, and compact report surfaces. Generated files are evidence and transport; they are not source-owned doctrine.

Prefer regenerating generated files through the owning script instead of hand-editing them. If a generated surface exposes drift, fix the source, validator, schema, or map logic that produced it.

Keep generated outputs compact, deterministic, and public-safe. Do not place secrets, raw private traces, or local absolute paths here.

Verify with:

```bash
python scripts/audit_agents_map.py --workspace-root <workspace-root> --write generated/agents_map.min.json --markdown docs/AGENTS_MAP.md
python scripts/recon_agents_frontier.py --map generated/agents_map.min.json --write generated/agents_frontier_recon.min.json --markdown generated/agents_frontier_recon.md
python scripts/validate_nested_agents.py
```
