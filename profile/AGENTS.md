# AGENTS.md

## Guidance for `profile/`

`profile/` holds public profile orientation and entrypoint-facing presentation material. It may explain the ecosystem arc, but it must not overrule source-owned repository truth.

Keep profile material legible to new humans and agents. Route detailed doctrine, runtime contracts, proof methods, memory semantics, and role definitions to the owning sibling repo.

No private biographical residue, raw chats, secrets, or local-only assumptions belong in this public surface.

Verify with:

```bash
python scripts/validate_nested_agents.py
```
