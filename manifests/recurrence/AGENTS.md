# AGENTS.md

## Guidance for `manifests/recurrence/`

`manifests/recurrence/` records public recurrence, route, and revisit hints for the entrypoint. Recurrence here is a scheduling and orientation aid, not proof of completion, agent growth, or sibling repo authority.

Keep manifests bounded, reviewable, and reversible. Any quest, campaign, checkpoint, role, memory, stats, or playbook meaning must route to the owning sibling repository.

When recurrence manifests affect generated maps or reports, rebuild those outputs and report the diff.

Verify with:

```bash
python scripts/validate_nested_agents.py
python scripts/audit_agents_map.py --workspace-root <workspace-root> --write generated/agents_map.min.json --markdown docs/AGENTS_MAP.md
```
