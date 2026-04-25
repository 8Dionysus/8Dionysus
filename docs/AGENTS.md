# AGENTS.md

## Guidance for `docs/`

`docs/` holds public orientation, audit guides, projection notes, and route explanations for the `8Dionysus` entrypoint. These docs help agents choose the right owner surface; they do not replace the nearest `AGENTS.md` or any sibling repository contract.

Keep docs route-first and evidence-linked. If a document starts to describe layer doctrine, move or route that doctrine to the owning repository instead of expanding this entrypoint.

Do not bury active operational rules in long narrative docs when a small local `AGENTS.md`, schema, validator, or script contract would make the rule easier to follow.

Verify with:

```bash
python scripts/validate_nested_agents.py
python scripts/audit_agents_map.py --workspace-root <workspace-root> --write generated/agents_map.min.json --markdown docs/AGENTS_MAP.md
```
