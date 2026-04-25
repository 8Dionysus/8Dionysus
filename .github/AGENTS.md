# AGENTS.md

## Guidance for `.github/`

`.github/` is a public platform-facing automation and repository-metadata surface. Treat workflow, issue-template, and repository policy edits as public contract edits.

Do not add secrets, private environment assumptions, unreviewed deployment behavior, or workflow steps that mutate sibling repositories without explicit owner routing.

When workflows or policy files change, prefer narrow static checks and report any checks that could not run locally. GitHub-facing automation should support the AGENTS map and repository orientation; it must not become a hidden source of ecosystem doctrine.

Verify with:

```bash
python scripts/validate_nested_agents.py
```
