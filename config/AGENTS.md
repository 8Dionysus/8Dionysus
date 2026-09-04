# AGENTS.md

## Guidance for `config/`

`config/` stores public configuration inputs for `8Dionysus` orientation, audit, projection, and shared-root helper behavior. Config may tune how maps, reports, or install surfaces are produced; it does not author sibling repo truth.

Keep config explicit, stable, and public-safe. Avoid machine-local paths, hidden environment assumptions, and policy that only one local checkout understands.

When config changes generated or projected surfaces, rebuild the affected output and inspect the diff for authority drift.

Run the applicable root routes in `../VALIDATION.md#agents-map-and-workspace-audit`
(`validate_nested_agents.py` and `audit_agents_map.py`).
