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

- `agents_md_files`: 1600
- `high_risk_dirs_without_agents`: 28
- `known_repositories`: 16
- `known_repositories_missing`: 0
- `long_root_agents`: 2
- `missing_required_agents`: 0
- `nested_agents_files`: 1581
- `repos_with_issues`: 12
- `repositories_listed`: 19
- `repositories_scanned`: 19
- `root_agents_present`: 19
- `unvalidated_nested_agents`: 1368
- `validator_required_agents`: 213
- `validators_present`: 13

## Repository coverage

| Repository | State | AGENTS.md | Nested | Validator | Issues |
|---|---:|---:|---:|---:|---|
| `8Dionysus` | `scanned` | 17 | 16 | True |  |
| `Agents-of-Abyss` | `scanned` | 63 | 62 | False | nested AGENTS.md files exist without scripts/validate_nested_agents.py |
| `Tree-of-Sophia` | `scanned` | 48 | 47 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `abyss-stack` | `scanned` | 43 | 42 | True | one or more AGENTS.md files do not start with '# AGENTS.md'; root AGENTS.md is long (310 lines; threshold 240) |
| `ATM10-Agent` | `scanned` | 15 | 14 | True |  |
| `Dionysus` | `scanned` | 19 | 18 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-sdk` | `scanned` | 49 | 48 | True |  |
| `aoa-techniques` | `scanned` | 93 | 92 | True |  |
| `aoa-skills` | `scanned` | 67 | 66 | False | nested AGENTS.md files exist without scripts/validate_nested_agents.py; root AGENTS.md is long (315 lines; threshold 240) |
| `aoa-evals` | `scanned` | 86 | 85 | True |  |
| `aoa-stats` | `scanned` | 12 | 11 | True |  |
| `aoa-routing` | `scanned` | 50 | 49 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-memo` | `scanned` | 116 | 115 | False | nested AGENTS.md files exist without scripts/validate_nested_agents.py |
| `aoa-agents` | `scanned` | 62 | 61 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-playbooks` | `scanned` | 36 | 35 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-kag` | `scanned` | 14 | 13 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `.agents` | `scanned` | 1 | 0 | False |  |
| `.aoa` | `scanned` | 278 | 277 | False | nested AGENTS.md files exist without scripts/validate_nested_agents.py; one or more AGENTS.md files do not start with '# AGENTS.md' |
| `.codex` | `scanned` | 531 | 530 | False | nested AGENTS.md files exist without scripts/validate_nested_agents.py; one or more AGENTS.md files do not start with '# AGENTS.md' |

## How to read the signals

- `missing` means the known public repository was not found under the selected workspace root.
- `unvalidated_nested_agents` means a nested `AGENTS.md` exists but is not declared by `scripts/validate_nested_agents.py`.
- `high_risk_dirs_without_agents` marks common contract, generated, test, runtime, or source directories without a direct local instruction file.
- `long_root_agents` marks roots that may be ready for slimming after local instructions are pushed down-tree.

Use this document as a compass before AGENTS refactors: measure first, then move doctrine to the smallest owner surface.
