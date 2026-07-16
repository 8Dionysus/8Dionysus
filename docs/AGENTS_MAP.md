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

- `agents_md_files`: 2414
- `high_risk_dirs_without_agents`: 23
- `known_repositories`: 16
- `known_repositories_missing`: 0
- `long_root_agents`: 5
- `missing_required_agents`: 0
- `nested_agents_files`: 2394
- `repos_with_issues`: 12
- `repositories_listed`: 20
- `repositories_scanned`: 20
- `root_agents_present`: 20
- `unvalidated_nested_agents`: 2176
- `validator_required_agents`: 218
- `validators_present`: 13

## Repository coverage

| Repository | State | AGENTS.md | Nested | Validator | Issues |
|---|---:|---:|---:|---:|---|
| `8Dionysus` | `scanned` | 20 | 19 | True |  |
| `Agents-of-Abyss` | `scanned` | 65 | 64 | False | nested AGENTS.md files exist without scripts/validate_nested_agents.py; root AGENTS.md is long (246 lines; threshold 240) |
| `Tree-of-Sophia` | `scanned` | 54 | 53 | True |  |
| `abyss-stack` | `scanned` | 47 | 46 | True | one or more AGENTS.md files do not start with '# AGENTS.md'; root AGENTS.md is long (310 lines; threshold 240) |
| `ATM10-Agent` | `scanned` | 17 | 16 | True |  |
| `Dionysus` | `scanned` | 21 | 20 | True |  |
| `aoa-sdk` | `scanned` | 49 | 48 | True |  |
| `aoa-techniques` | `scanned` | 95 | 94 | True |  |
| `aoa-skills` | `scanned` | 68 | 67 | False | nested AGENTS.md files exist without scripts/validate_nested_agents.py; root AGENTS.md is long (315 lines; threshold 240) |
| `aoa-evals` | `scanned` | 89 | 88 | True |  |
| `aoa-stats` | `scanned` | 45 | 44 | True | root AGENTS.md is long (276 lines; threshold 240) |
| `aoa-routing` | `scanned` | 52 | 51 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-memo` | `scanned` | 118 | 117 | False | nested AGENTS.md files exist without scripts/validate_nested_agents.py |
| `aoa-agents` | `scanned` | 64 | 63 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-playbooks` | `scanned` | 38 | 37 | True | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-kag` | `scanned` | 834 | 833 | True | one or more AGENTS.md files do not start with '# AGENTS.md'; root AGENTS.md is long (294 lines; threshold 240) |
| `.agents` | `scanned` | 1 | 0 | False |  |
| `.aoa` | `scanned` | 488 | 487 | False | nested AGENTS.md files exist without scripts/validate_nested_agents.py; one or more AGENTS.md files do not start with '# AGENTS.md' |
| `.codex` | `scanned` | 218 | 217 | False | nested AGENTS.md files exist without scripts/validate_nested_agents.py; one or more AGENTS.md files do not start with '# AGENTS.md' |
| `connectors` | `scanned` | 31 | 30 | False | nested AGENTS.md files exist without scripts/validate_nested_agents.py; one or more AGENTS.md files do not start with '# AGENTS.md' |

## How to read the signals

- `missing` means the known public repository was not found under the selected workspace root.
- `unvalidated_nested_agents` means a nested `AGENTS.md` exists but is not declared by `scripts/validate_nested_agents.py`.
- `high_risk_dirs_without_agents` marks common contract, generated, test, runtime, or source directories without a direct local instruction file.
- `long_root_agents` marks roots that may be ready for slimming after local instructions are pushed down-tree.

Use this document as a compass before AGENTS refactors: measure first, then move doctrine to the smallest owner surface.
