# AGENTS.md

## Guidance for `quests/`

`quests/` may hold public quest, campaign, or direction markers for entrypoint orientation. Treat quest language as bounded navigation, not sovereign proof, runtime authority, or agent identity.

Every quest marker should remain evidence-linked, reversible, and routed to the owning layer. Do not turn inspirational direction into hidden operational requirements.

If a quest becomes a recurring operational scenario, move it toward `aoa-playbooks`; if it becomes a role or progression contract, route it to `aoa-agents`; if it becomes proof, route it to `aoa-evals`.

Verify with:

```bash
python scripts/validate_nested_agents.py
python scripts/audit_agents_map.py --workspace-root <workspace-root> --write generated/agents_map.min.json --markdown docs/AGENTS_MAP.md
```
