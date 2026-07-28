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

- `agents_md_files`: 2839
- `high_risk_dirs_without_agents`: 22
- `known_repositories`: 16
- `known_repositories_missing`: 0
- `long_root_agents`: 5
- `missing_required_agents`: 0
- `nested_agents_files`: 2817
- `optional_repositories_missing`: 0
- `repos_with_issues`: 15
- `repositories_listed`: 22
- `repositories_scanned`: 22
- `root_agents_present`: 22
- `unvalidated_nested_agents`: 2572
- `validator_required_agents`: 245
- `validators_present`: 13

## Repository coverage

| Repository | State | AGENTS.md | Nested | Validator | Issues |
|---|---:|---:|---:|---:|---|
| `8Dionysus` | `scanned` | 21 | 20 | True |  |
| `Agents-of-Abyss` | `scanned` | 65 | 64 | False | nested AGENTS.md files exist without scripts/validate_nested_agents.py; root AGENTS.md is long (246 lines; threshold 240) |
| `Tree-of-Sophia` | `scanned` | 54 | 53 | True |  |
| `abyss-stack` | `scanned` | 47 | 46 | True | one or more AGENTS.md files do not start with '# AGENTS.md'; root AGENTS.md is long (310 lines; threshold 240) |
| `ATM10-Agent` | `scanned` | 15 | 14 | True |  |
| `Dionysus` | `scanned` | 1 | 0 | False | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-sdk` | `scanned` | 50 | 49 | True |  |
| `aoa-techniques` | `scanned` | 94 | 93 | True |  |
| `aoa-skills` | `scanned` | 25 | 24 | False | nested AGENTS.md files exist without scripts/validate_nested_agents.py |
| `aoa-evals` | `scanned` | 89 | 88 | True |  |
| `aoa-stats` | `scanned` | 45 | 44 | True | root AGENTS.md is long (276 lines; threshold 240) |
| `aoa-routing` | `scanned` | 51 | 50 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-memo` | `scanned` | 118 | 117 | False | nested AGENTS.md files exist without scripts/validate_nested_agents.py |
| `aoa-agents` | `scanned` | 64 | 63 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-playbooks` | `scanned` | 38 | 37 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-kag` | `scanned` | 961 | 960 | True | one or more AGENTS.md files do not start with '# AGENTS.md'; root AGENTS.md is long (300 lines; threshold 240) |
| `.agents` | `scanned` | 1 | 0 | False |  |
| `.aoa` | `scanned` | 740 | 739 | False | nested AGENTS.md files exist without scripts/validate_nested_agents.py; one or more AGENTS.md files do not start with '# AGENTS.md' |
| `.codex` | `scanned` | 218 | 217 | False | nested AGENTS.md files exist without scripts/validate_nested_agents.py; one or more AGENTS.md files do not start with '# AGENTS.md' |
| `abyss-machine` | `scanned` | 59 | 58 | False | nested AGENTS.md files exist without scripts/validate_nested_agents.py; one or more AGENTS.md files do not start with '# AGENTS.md' |
| `abyss-stack-source` | `scanned` | 52 | 51 | True | one or more AGENTS.md files do not start with '# AGENTS.md'; root AGENTS.md is long (324 lines; threshold 240) |
| `connectors` | `scanned` | 31 | 30 | False | nested AGENTS.md files exist without scripts/validate_nested_agents.py; one or more AGENTS.md files do not start with '# AGENTS.md' |

## How to read the signals

- `missing` means the known public repository was not found under the selected workspace root.
- `checkout_requirement: optional` means an absent retained predecessor is valid and does not create an audit issue.
- `unvalidated_nested_agents` means a nested `AGENTS.md` exists but is not declared by `scripts/validate_nested_agents.py`.
- `high_risk_dirs_without_agents` marks common contract, generated, test, runtime, or source directories without a direct local instruction file.
- `long_root_agents` marks roots that may be ready for slimming after local instructions are pushed down-tree.

Use this document as a compass before AGENTS refactors: measure first, then move doctrine to the smallest owner surface.
