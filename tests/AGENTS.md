# AGENTS.md

## Guidance for `tests/`

`tests/` protects the audit, frontier, validator, and projection contracts of the `8Dionysus` entrypoint. Tests should use temporary directories and minimal fixtures instead of depending on a private workspace layout.

Keep tests deterministic, local-only, and public-safe. Do not require network access, real sibling repos, secrets, or a specific operator machine.

When a validator or schema changes, add or update the narrowest test that catches the intended contract drift.

Verify with:

```bash
python -m unittest discover -s tests
python scripts/validate_nested_agents.py
```
