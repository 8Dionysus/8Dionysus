# AGENTS.md

## Guidance for `examples/`

`examples/` contains public-safe examples for entrypoint orientation, audit usage, projection, or route choice. Examples are teaching surfaces, not hidden sources of truth.

Use fake data, minimal fixtures, and explicit boundaries. No secrets, raw private logs, personal credentials, machine-local paths, or unreviewed runtime instructions belong here.

If an example encodes a sibling repo contract, keep it synchronized with that owner repo and link back to the source-owned surface.

Verify with:

```bash
python scripts/validate_nested_agents.py
```
