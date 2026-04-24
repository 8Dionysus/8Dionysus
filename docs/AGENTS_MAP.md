# AGENTS map

This map is the audit surface for `AGENTS.md` coverage across the AoA / ToS workspace.
It is not repository doctrine and it does not replace the nearest `AGENTS.md` rule.

## How to regenerate

For a live sibling-workspace scan:

```bash
python scripts/audit_agents_map.py \
  --workspace-root <workspace-root> \
  --write generated/agents_map.min.json \
  --markdown docs/AGENTS_MAP.md
```

For the public bootstrap baseline:

```bash
python scripts/audit_agents_map.py --public-baseline \
  --write generated/agents_map.min.json \
  --markdown docs/AGENTS_MAP.md
```

## Current totals

- `agents_md_files`: 121
- `high_risk_dirs_without_agents`: 141
- `known_repositories`: 16
- `known_repositories_missing`: 0
- `long_root_agents`: 3
- `missing_required_agents`: 0
- `nested_agents_files`: 105
- `repos_with_issues`: 15
- `repositories_listed`: 16
- `repositories_scanned`: 16
- `root_agents_present`: 16
- `unvalidated_nested_agents`: 39
- `validator_required_agents`: 66
- `validators_present`: 16

## Repository coverage

| Repository | State | AGENTS.md | Nested | Validator | Issues |
|---|---:|---:|---:|---:|---|
| `8Dionysus` | `scanned` | 1 | 0 | True | root AGENTS.md is long (307 lines; threshold 240) |
| `Agents-of-Abyss` | `scanned` | 6 | 5 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `Tree-of-Sophia` | `scanned` | 19 | 18 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `abyss-stack` | `scanned` | 10 | 9 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `ATM10-Agent` | `scanned` | 12 | 11 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `Dionysus` | `scanned` | 7 | 6 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-sdk` | `scanned` | 7 | 6 | True | root AGENTS.md is long (317 lines; threshold 240) |
| `aoa-techniques` | `scanned` | 9 | 8 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-skills` | `scanned` | 6 | 5 | True | one or more AGENTS.md files do not start with '# AGENTS.md'; root AGENTS.md is long (260 lines; threshold 240) |
| `aoa-evals` | `scanned` | 8 | 7 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-stats` | `scanned` | 1 | 0 | True |  |
| `aoa-routing` | `scanned` | 6 | 5 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-memo` | `scanned` | 6 | 5 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-agents` | `scanned` | 13 | 12 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-playbooks` | `scanned` | 4 | 3 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-kag` | `scanned` | 6 | 5 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |

## How to read the signals

- `missing` means the known public repository was not found under the selected workspace root.
- `unvalidated_nested_agents` means a nested `AGENTS.md` exists but is not declared by `scripts/validate_nested_agents.py`.
- `high_risk_dirs_without_agents` marks common contract, generated, test, runtime, or source directories without a direct local instruction file.
- `long_root_agents` marks roots that may be ready for slimming after local instructions are pushed down-tree.

Use this document as a compass before AGENTS refactors: measure first, then move doctrine to the smallest owner surface.
