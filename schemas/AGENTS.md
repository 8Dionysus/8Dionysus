# AGENTS.md

## Guidance for `schemas/`

`schemas/` stores machine-readable contracts for `8Dionysus` audit, route, frontier, and projection surfaces. Schema edits are contract edits.

Keep `$schema`, required fields, enums, and compatibility expectations explicit. When a schema changes, update paired examples, generated outputs, tests, and downstream readers.

Schemas here describe entrypoint-owned surfaces. They do not define sibling repo semantics unless the owner repo explicitly imports that contract.

Verify with:

```bash
python scripts/validate_nested_agents.py
python -m unittest discover -s tests
python scripts/audit_agents_map.py --workspace-root <workspace-root> --write generated/agents_map.min.json --markdown docs/AGENTS_MAP.md
```
