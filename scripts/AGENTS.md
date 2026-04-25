# AGENTS.md

## Guidance for `scripts/`

`scripts/` contains local audit, frontier, validation, projection, and helper tooling for the public entry repository. Scripts should be deterministic, repo-relative, local-only by default, and safe to run from a checked-out workspace.

Do not add hidden network calls, secret reads, uncontrolled sibling mutation, or operator-specific paths. If a script reads sibling repositories, it must treat them as source-owned checkouts and avoid storing absolute paths in generated outputs.

When script behavior changes, update tests, schemas, generated examples, and docs that describe the command.

Verify with:

```bash
python scripts/validate_nested_agents.py
python -m unittest discover -s tests
```
