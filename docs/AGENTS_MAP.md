# AGENTS map

This map is the audit and owner-review surface for the tracked `README.md` / `AGENTS.md` corpus across the AoA / ToS workspace.
It is not repository doctrine and it does not replace the nearest `AGENTS.md` rule.

## How to regenerate

For a live sibling-workspace scan:

```bash
python scripts/audit_agents_map.py \
  --workspace-root <workspace-root> \
  --write generated/agents_map.min.json \
  --markdown docs/AGENTS_MAP.md
```

For a merge-bound baseline, scan an isolated matrix of clean owner worktrees and disable workspace-manifest redirection:

```bash
python scripts/audit_agents_map.py \
  --workspace-root <clean-worktree-matrix> \
  --repo-root <clean-worktree-matrix>/8Dionysus \
  --no-extra-repos --ignore-workspace-manifest \
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

- `agents_files_declaring_mandatory_readme`: 6
- `agents_files_referencing_readme`: 307
- `agents_md_files`: 798
- `agents_only_directories`: 256
- `archive_document_files`: 281
- `authored_repeated_long_agents_block_groups`: 0
- `authored_unique_chains_over_budget`: 0
- `blocked_files`: 0
- `chain_max_bytes`: 25189
- `chain_p50_bytes`: 13513
- `chain_p95_bytes`: 22400
- `chain_scopes`: 2105
- `chain_scopes_over_budget`: 0
- `declared_mandatory_readme_bytes`: 23799
- `excluded_repeated_long_agents_block_groups`: 0
- `excluded_unique_chains_over_budget`: 0
- `fixture_document_files`: 38
- `generated_document_files`: 27
- `high_risk_dirs_without_agents`: 37
- `known_repositories`: 21
- `known_repositories_missing`: 0
- `long_root_agents`: 0
- `mechanics_document_files`: 1636
- `missing_required_agents`: 0
- `nested_agents_files`: 778
- `optional_repositories_missing`: 1
- `paired_directories`: 627
- `readme_only_directories`: 1222
- `repeated_long_agents_block_groups`: 0
- `repeated_long_agents_block_instances`: 0
- `repeated_long_agents_normalized_redundant_bytes`: 0
- `repos_with_issues`: 8
- `repositories_listed`: 21
- `repositories_scanned`: 20
- `review_items_total`: 2734
- `review_items_unreviewed`: 0
- `reviewed_files`: 2732
- `root_agents_present`: 20
- `root_document_files`: 40
- `shared_root_blocked_files`: 0
- `shared_root_files`: 2
- `shared_root_files_in_owner_parity`: 2
- `shared_root_reviewed_files`: 2
- `shared_root_unreviewed_files`: 0
- `tracked_agents_bytes`: 1467879
- `tracked_agents_files`: 883
- `tracked_document_bytes`: 5118564
- `tracked_document_files`: 2732
- `tracked_readme_bytes`: 3650685
- `tracked_readme_files`: 1849
- `unique_agents_chains`: 883
- `unique_chain_max_bytes`: 25189
- `unique_chain_p50_bytes`: 11755
- `unique_chain_p95_bytes`: 21629
- `unique_chains_over_budget`: 0
- `unreviewed_files`: 0
- `untracked_document_candidates`: 0
- `unvalidated_nested_agents`: 576
- `validator_required_agents`: 206
- `validators_present`: 11
- `vendor_document_files`: 0

## Repository coverage

| Repository | State | AGENTS corpus/active | README | Pairs | Unique chain p95/max | Over 32 KiB authored/excluded | Repeated long blocks/redundant bytes | Reviewed/unreviewed | Issues |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `8Dionysus` | `scanned` | 21/21 | 12 | 6 | 12324/14854 | 0/0 | 0/0 | 33/0 |  |
| `Agents-of-Abyss` | `scanned` | 65/57 | 221 | 56 | 23296/23406 | 0/0 | 0/0 | 286/0 | nested AGENTS.md files exist without scripts/validate_nested_agents.py |
| `Tree-of-Sophia` | `scanned` | 55/55 | 213 | 32 | 16728/17852 | 0/0 | 0/0 | 268/0 |  |
| `abyss-stack` | `scanned` | 59/55 | 168 | 56 | 12212/14427 | 0/0 | 0/0 | 227/0 |  |
| `abyss-machine` | `scanned` | 60/60 | 38 | 27 | 10473/14106 | 0/0 | 0/0 | 98/0 | nested AGENTS.md files exist without scripts/validate_nested_agents.py |
| `ATM10-Agent` | `scanned` | 15/15 | 9 | 3 | 9537/9537 | 0/0 | 0/0 | 24/0 |  |
| `Dionysus` | `scanned` | 4/3 | 19 | 4 | 4537/4537 | 0/0 | 0/0 | 23/0 | nested AGENTS.md files exist without scripts/validate_nested_agents.py |
| `aoa-sdk` | `scanned` | 50/46 | 137 | 42 | 14495/15536 | 0/0 | 0/0 | 187/0 |  |
| `aoa-dashboard` | `scanned` | 2/2 | 2 | 1 | 1427/1427 | 0/0 | 0/0 | 4/0 | nested AGENTS.md files exist without scripts/validate_nested_agents.py |
| `aoa-techniques` | `scanned` | 94/77 | 169 | 64 | 23974/25189 | 0/0 | 0/0 | 263/0 |  |
| `aoa-skills` | `scanned` | 25/25 | 24 | 16 | 6317/6951 | 0/0 | 0/0 | 49/0 | nested AGENTS.md files exist without scripts/validate_nested_agents.py |
| `aoa-evals` | `scanned` | 90/71 | 191 | 81 | 16648/19053 | 0/0 | 0/0 | 281/0 |  |
| `aoa-stats` | `scanned` | 45/44 | 85 | 36 | 12185/12732 | 0/0 | 0/0 | 130/0 |  |
| `aoa-routing` | `missing` | 0/0 | 0 | 0 | / | / | 0/0 | 0/0 |  |
| `aoa-memo` | `scanned` | 118/103 | 164 | 68 | 21011/21362 | 0/0 | 0/0 | 282/0 | nested AGENTS.md files exist without scripts/validate_nested_agents.py |
| `aoa-session-memory` | `scanned` | 15/15 | 66 | 8 | 9525/9525 | 0/0 | 0/0 | 81/0 | nested AGENTS.md files exist without scripts/validate_nested_agents.py |
| `aoa-agents` | `scanned` | 66/54 | 185 | 55 | 14293/16791 | 0/0 | 0/0 | 251/0 |  |
| `aoa-models` | `scanned` | 2/2 | 3 | 2 | 5029/5029 | 0/0 | 0/0 | 5/0 | nested AGENTS.md files exist without scripts/validate_nested_agents.py |
| `aoa-agon` | `scanned` | 1/1 | 4 | 1 | 2602/2602 | 0/0 | 0/0 | 5/0 |  |
| `aoa-playbooks` | `scanned` | 38/38 | 67 | 30 | 12775/12790 | 0/0 | 0/0 | 105/0 |  |
| `aoa-kag` | `scanned` | 58/54 | 72 | 39 | 10408/10433 | 0/0 | 0/0 | 130/0 |  |

## Shared-root projection posture

| File | Declared projection | Owner parity | Review |
|---|---:|---:|---|
| `AGENTS.md` | True | True | `reviewed` |
| `README.md` | True | True | `reviewed` |

## How to read the signals

- `missing` means the known public repository was not found under the selected workspace root.
- `checkout_requirement: optional` means an absent retained predecessor is valid and does not create an audit issue.
- Corpus counts use Git-tracked `README.md` and `AGENTS.md`; untracked documents are candidates, not canonical corpus members.
- `chain_scopes` measures unique document directories; `unique_agents_chains` collapses directories that inherit the same AGENTS path signature.
- Chain percentiles use the nearest-rank method; the repository table reports unique chain signatures.
- `Repeated long blocks` counts exact normalized prose blocks of at least 180 bytes appearing in at least four tracked `AGENTS.md` files; fenced examples are excluded and redundant bytes count copies beyond the first.
- Dispositions remain `unreviewed` until an owner-evidenced record is added to the integration manifest.
- `unvalidated_nested_agents` means a nested `AGENTS.md` exists but is not declared by `scripts/validate_nested_agents.py`.
- `high_risk_dirs_without_agents` marks common contract, generated, test, runtime, or source directories without a direct local instruction file.
- `long_root_agents` marks roots that may be ready for slimming after local instructions are pushed down-tree.

Use this document as a compass before AGENTS refactors: measure first, then move doctrine to the smallest owner surface.
