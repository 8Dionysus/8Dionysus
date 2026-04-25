# AGENTS.md

## Guidance for `.agents/`

`.agents/` is a shared-root projection source and agent-facing companion surface for the public workspace entrypoint. Treat it as source-owned by `8Dionysus` only when the checked-in file lives in this repository.

Do not treat projected live workspace copies as primary truth. Edit the source-owned copy here first, then project or install through the documented workspace path.

Keep this surface public-safe: no secrets, private machine paths, local-only credentials, raw transcripts, or operator-only assumptions. Route layer-specific meaning back to the owning sibling repository.

Verify changes with:

```bash
python scripts/validate_nested_agents.py
python scripts/audit_agents_map.py --workspace-root <workspace-root> --write generated/agents_map.min.json --markdown docs/AGENTS_MAP.md
```
