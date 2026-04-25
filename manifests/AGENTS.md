# AGENTS.md

## Guidance for `manifests/`

`manifests/` records public route, recurrence, projection, and revisit hints for the `8Dionysus` entrypoint. Manifests are coordination evidence and routing aids; they are not proof of completion, owner authority, or sibling-repo doctrine.

Keep manifests compact, deterministic, public-safe, and reversible. Do not add private paths, raw transcripts, secrets, or hidden operational obligations.

Route quest, campaign, checkpoint, role, memory, stats, or playbook meaning to the owning sibling repository instead of expanding this entrypoint.

When manifests affect generated maps or reports, rebuild the affected outputs and report the diff.

Verify with:

```bash
python scripts/validate_nested_agents.py
python scripts/audit_agents_map.py --workspace-root <workspace-root> --write generated/agents_map.min.json --markdown docs/AGENTS_MAP.md
python scripts/recon_agents_frontier.py --map generated/agents_map.min.json --write generated/agents_frontier_recon.min.json --markdown generated/agents_frontier_recon.md
```
