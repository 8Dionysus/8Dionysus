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

After changing local `AGENTS.md` coverage, regenerate the frontier reconnaissance report:

```bash
python scripts/recon_agents_frontier.py \
  --map generated/agents_map.min.json \
  --write generated/agents_frontier_recon.min.json \
  --markdown generated/agents_frontier_recon.md
```

For reading guidance, see [AGENTS_FRONTIER_RECON](AGENTS_FRONTIER_RECON.md).

## Current totals

- `agents_md_files`: 208
- `high_risk_dirs_without_agents`: 78
- `known_repositories`: 16
- `known_repositories_missing`: 0
- `long_root_agents`: 0
- `missing_required_agents`: 0
- `nested_agents_files`: 192
- `repos_with_issues`: 13
- `repositories_listed`: 16
- `repositories_scanned`: 16
- `root_agents_present`: 16
- `unvalidated_nested_agents`: 85
- `validator_required_agents`: 107
- `validators_present`: 16

## Repository coverage

| Repository | State | AGENTS.md | Nested | Validator | Issues |
|---|---:|---:|---:|---:|---|
| `8Dionysus` | `scanned` | 15 | 14 | True |  |
| `Agents-of-Abyss` | `scanned` | 16 | 15 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `Tree-of-Sophia` | `scanned` | 19 | 18 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `abyss-stack` | `scanned` | 10 | 9 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `ATM10-Agent` | `scanned` | 12 | 11 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `Dionysus` | `scanned` | 15 | 14 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-sdk` | `scanned` | 7 | 6 | True |  |
| `aoa-techniques` | `scanned` | 18 | 17 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-skills` | `scanned` | 11 | 10 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-evals` | `scanned` | 17 | 16 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-stats` | `scanned` | 9 | 8 | True |  |
| `aoa-routing` | `scanned` | 10 | 9 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-memo` | `scanned` | 10 | 9 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-agents` | `scanned` | 19 | 18 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-playbooks` | `scanned` | 9 | 8 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-kag` | `scanned` | 11 | 10 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |

## How to read the signals

- `missing` means the known public repository was not found under the selected workspace root.
- `unvalidated_nested_agents` means a nested `AGENTS.md` exists but is not declared by `scripts/validate_nested_agents.py`.
- `high_risk_dirs_without_agents` marks common contract, generated, test, runtime, or source directories without a direct local instruction file.
- `long_root_agents` marks roots that may be ready for slimming after local instructions are pushed down-tree.

Use this document as a compass before AGENTS refactors: measure first, then move doctrine to the smallest owner surface.
