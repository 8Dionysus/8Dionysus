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

- `agents_files_declaring_mandatory_readme`: 192
- `agents_files_referencing_readme`: 483
- `agents_md_files`: 797
- `agents_only_directories`: 257
- `archive_document_files`: 293
- `authored_unique_chains_over_budget`: 7
- `blocked_files`: 0
- `chain_max_bytes`: 40883
- `chain_p50_bytes`: 18240
- `chain_p95_bytes`: 30341
- `chain_scopes`: 2146
- `chain_scopes_over_budget`: 29
- `declared_mandatory_readme_bytes`: 519926
- `excluded_unique_chains_over_budget`: 0
- `fixture_document_files`: 38
- `generated_document_files`: 27
- `high_risk_dirs_without_agents`: 29
- `known_repositories`: 20
- `known_repositories_missing`: 0
- `long_root_agents`: 4
- `mechanics_document_files`: 1677
- `missing_required_agents`: 0
- `nested_agents_files`: 778
- `optional_repositories_missing`: 1
- `paired_directories`: 625
- `readme_only_directories`: 1264
- `repos_with_issues`: 13
- `repositories_listed`: 20
- `repositories_scanned`: 19
- `review_items_total`: 2773
- `review_items_unreviewed`: 2773
- `reviewed_files`: 0
- `root_agents_present`: 19
- `root_document_files`: 38
- `shared_root_blocked_files`: 0
- `shared_root_files`: 2
- `shared_root_files_in_owner_parity`: 0
- `shared_root_reviewed_files`: 0
- `shared_root_unreviewed_files`: 2
- `tracked_agents_bytes`: 1854656
- `tracked_agents_files`: 882
- `tracked_document_bytes`: 5604716
- `tracked_document_files`: 2771
- `tracked_readme_bytes`: 3750060
- `tracked_readme_files`: 1889
- `unique_agents_chains`: 882
- `unique_chain_max_bytes`: 40883
- `unique_chain_p50_bytes`: 16908
- `unique_chain_p95_bytes`: 28780
- `unique_chains_over_budget`: 7
- `unreviewed_files`: 2771
- `untracked_document_candidates`: 0
- `unvalidated_nested_agents`: 580
- `validator_required_agents`: 202
- `validators_present`: 11
- `vendor_document_files`: 0

## Repository coverage

| Repository | State | AGENTS corpus/active | README | Pairs | Unique chain p95/max | Over 32 KiB authored/excluded | Reviewed/unreviewed | Issues |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `8Dionysus` | `scanned` | 21/21 | 13 | 6 | 15745/22005 | 0/0 | 0/34 |  |
| `Agents-of-Abyss` | `scanned` | 65/57 | 221 | 56 | 34037/40883 | 5/0 | 0/286 | nested AGENTS.md files exist without scripts/validate_nested_agents.py; root AGENTS.md is long (246 lines; threshold 240) |
| `Tree-of-Sophia` | `scanned` | 55/55 | 213 | 32 | 20852/21741 | 0/0 | 0/268 |  |
| `abyss-stack` | `scanned` | 59/55 | 168 | 56 | 30620/34907 | 2/0 | 0/227 | one or more AGENTS.md files do not start with '# AGENTS.md'; root AGENTS.md is long (324 lines; threshold 240) |
| `abyss-machine` | `scanned` | 60/60 | 54 | 27 | 17378/20962 | 0/0 | 0/114 | nested AGENTS.md files exist without scripts/validate_nested_agents.py; one or more AGENTS.md files do not start with '# AGENTS.md' |
| `ATM10-Agent` | `scanned` | 15/15 | 9 | 3 | 9541/9541 | 0/0 | 0/24 |  |
| `Dionysus` | `scanned` | 4/3 | 19 | 4 | 4537/4537 | 0/0 | 0/23 | nested AGENTS.md files exist without scripts/validate_nested_agents.py; one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-sdk` | `scanned` | 50/46 | 137 | 42 | 19485/20642 | 0/0 | 0/187 |  |
| `aoa-dashboard` | `scanned` | 2/2 | 2 | 1 | 1427/1427 | 0/0 | 0/4 | nested AGENTS.md files exist without scripts/validate_nested_agents.py; one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-techniques` | `scanned` | 94/77 | 169 | 64 | 28100/29280 | 0/0 | 0/263 |  |
| `aoa-skills` | `scanned` | 25/25 | 27 | 16 | 6445/7116 | 0/0 | 0/52 | nested AGENTS.md files exist without scripts/validate_nested_agents.py |
| `aoa-evals` | `scanned` | 90/71 | 191 | 81 | 25723/27870 | 0/0 | 0/281 |  |
| `aoa-stats` | `scanned` | 45/44 | 85 | 36 | 20378/21007 | 0/0 | 0/130 | root AGENTS.md is long (276 lines; threshold 240) |
| `aoa-routing` | `missing` | 0/0 | 0 | 0 | / | / | 0/0 |  |
| `aoa-memo` | `scanned` | 118/103 | 164 | 68 | 23014/24287 | 0/0 | 0/282 | nested AGENTS.md files exist without scripts/validate_nested_agents.py |
| `aoa-session-memory` | `scanned` | 15/15 | 66 | 8 | 9525/9525 | 0/0 | 0/81 | nested AGENTS.md files exist without scripts/validate_nested_agents.py; one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-agents` | `scanned` | 66/54 | 209 | 54 | 18565/20281 | 0/0 | 0/275 | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-models` | `scanned` | 2/2 | 3 | 2 | 4443/4443 | 0/0 | 0/5 | nested AGENTS.md files exist without scripts/validate_nested_agents.py; one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-playbooks` | `scanned` | 38/38 | 67 | 30 | 13310/14665 | 0/0 | 0/105 | one or more AGENTS.md files do not start with '# AGENTS.md' |
| `aoa-kag` | `scanned` | 58/54 | 72 | 39 | 19721/19740 | 0/0 | 0/130 | one or more AGENTS.md files do not start with '# AGENTS.md'; root AGENTS.md is long (305 lines; threshold 240) |

## Shared-root projection posture

| File | Declared projection | Owner parity | Review |
|---|---:|---:|---|
| `AGENTS.md` | True | False | `unreviewed` |
| `README.md` | False | False | `unreviewed` |

## How to read the signals

- `missing` means the known public repository was not found under the selected workspace root.
- `checkout_requirement: optional` means an absent retained predecessor is valid and does not create an audit issue.
- Corpus counts use Git-tracked `README.md` and `AGENTS.md`; untracked documents are candidates, not canonical corpus members.
- `chain_scopes` measures unique document directories; `unique_agents_chains` collapses directories that inherit the same AGENTS path signature.
- Chain percentiles use the nearest-rank method; the repository table reports unique chain signatures.
- Dispositions remain `unreviewed` until an owner-evidenced record is added to the integration manifest.
- `unvalidated_nested_agents` means a nested `AGENTS.md` exists but is not declared by `scripts/validate_nested_agents.py`.
- `high_risk_dirs_without_agents` marks common contract, generated, test, runtime, or source directories without a direct local instruction file.
- `long_root_agents` marks roots that may be ready for slimming after local instructions are pushed down-tree.

Use this document as a compass before AGENTS refactors: measure first, then move doctrine to the smallest owner surface.
