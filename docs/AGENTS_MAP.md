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

- `active_authored_agents_classified_fenced_blocks`: 2
- `active_authored_agents_fenced_blocks`: 7
- `active_authored_agents_fenced_executable_invocations`: 20
- `active_authored_agents_unclassified_fenced_blocks`: 5
- `active_authored_design_agents_classified_fenced_blocks`: 5
- `active_authored_design_agents_fenced_blocks`: 5
- `active_authored_design_agents_fenced_executable_invocations`: 0
- `active_authored_design_agents_unclassified_fenced_blocks`: 0
- `active_authored_unique_validation_invocations`: 351
- `active_authored_validation_bytes`: 128483
- `active_authored_validation_command_owner_files`: 46
- `active_authored_validation_files`: 127
- `active_authored_validation_invocations`: 351
- `active_authored_validation_route_only_files`: 81
- `agents_conditional_readme_reference_lines`: 72
- `agents_fenced_example_readme_reference_lines`: 0
- `agents_files_declaring_mandatory_readme`: 0
- `agents_files_referencing_readme`: 101
- `agents_md_files`: 237
- `agents_navigational_readme_reference_lines`: 64
- `agents_only_directories`: 75
- `agents_readme_reference_lines`: 136
- `agents_validation_command_overlap_groups`: 0
- `archive_document_files`: 1
- `authored_repeated_long_agents_block_groups`: 0
- `authored_unique_chains_over_budget`: 0
- `blocked_files`: 0
- `chain_max_bytes`: 20319
- `chain_p50_bytes`: 9369
- `chain_p95_bytes`: 18584
- `chain_scopes`: 619
- `chain_scopes_over_budget`: 0
- `declared_mandatory_readme_bytes`: 0
- `duplicate_validation_command_groups`: 0
- `duplicate_validation_command_occurrences`: 0
- `excluded_repeated_long_agents_block_groups`: 0
- `excluded_unique_chains_over_budget`: 0
- `fixture_document_files`: 5
- `generated_document_files`: 7
- `high_risk_dirs_without_agents`: 30
- `known_repositories`: 21
- `known_repositories_missing`: 14
- `long_root_agents`: 0
- `mechanics_document_files`: 403
- `missing_required_agents`: 0
- `nested_agents_files`: 226
- `optional_repositories_missing`: 1
- `paired_directories`: 162
- `readme_only_directories`: 382
- `readme_validation_command_overlap_groups`: 0
- `repeated_long_agents_block_groups`: 0
- `repeated_long_agents_block_instances`: 0
- `repeated_long_agents_normalized_redundant_bytes`: 0
- `repos_with_issues`: 19
- `repositories_listed`: 26
- `repositories_scanned`: 11
- `review_items_total`: 785
- `review_items_unreviewed`: 20
- `reviewed_files`: 765
- `root_agents_present`: 11
- `root_document_files`: 22
- `shared_root_blocked_files`: 0
- `shared_root_files`: 0
- `shared_root_files_in_owner_parity`: 0
- `shared_root_reviewed_files`: 0
- `shared_root_unreviewed_files`: 0
- `stale_agents_fenced_block_classifications`: 0
- `stale_design_agents_fenced_block_classifications`: 0
- `tracked_agents_bytes`: 476730
- `tracked_agents_files`: 237
- `tracked_design_agents_bytes`: 49031
- `tracked_design_agents_files`: 4
- `tracked_document_bytes`: 1957637
- `tracked_document_files`: 781
- `tracked_readme_bytes`: 1480907
- `tracked_readme_files`: 544
- `tracked_validation_files`: 127
- `unique_agents_chains`: 237
- `unique_chain_max_bytes`: 20319
- `unique_chain_p50_bytes`: 9113
- `unique_chain_p95_bytes`: 18506
- `unique_chains_over_budget`: 0
- `unreviewed_files`: 20
- `untracked_design_agents_candidates`: 0
- `untracked_document_candidates`: 0
- `untracked_validation_candidates`: 0
- `unvalidated_nested_agents`: 0
- `validation_route_only_claim_conflicts`: 0
- `validator_required_agents`: 86
- `validators_present`: 4
- `vendor_document_files`: 0

## Repository coverage

| Repository | State | AGENTS corpus/active | README | VALIDATION files/cmds/duplicates | Pairs | Unique chain p95/max | Over 32 KiB authored/excluded | Repeated long blocks/redundant bytes | Reviewed/unreviewed | Issues |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `8Dionysus` | `scanned` | 21/21 | 12 | 4/20/0 | 6 | 8312/10715 | 0/0 | 0/0 | 33/0 |  |
| `Agents-of-Abyss` | `scanned` | 52/52 | 182 | 101/102/0 | 43 | 18736/19045 | 0/0 | 0/0 | 235/0 |  |
| `Tree-of-Sophia` | `missing` | 0/0 | 0 | 0/0/0 | 0 | / | / | 0/0 | 0/0 | known repository checkout not found under workspace root |
| `abyss-stack` | `scanned` | 54/54 | 143 | 7/201/0 | 51 | 12212/14444 | 0/0 | 0/0 | 198/0 |  |
| `abyss-machine` | `missing` | 0/0 | 0 | 0/0/0 | 0 | / | / | 0/0 | 0/0 | known repository checkout not found under workspace root |
| `ATM10-Agent` | `scanned` | 14/14 | 9 | 10/16/0 | 3 | 9189/9189 | 0/0 | 0/0 | 23/0 |  |
| `Dionysus` | `missing` | 0/0 | 0 | 0/0/0 | 0 | / | / | 0/0 | 0/0 | known repository checkout not found under workspace root |
| `aoa-sdk` | `missing` | 0/0 | 0 | 0/0/0 | 0 | / | / | 0/0 | 0/0 | known repository checkout not found under workspace root |
| `aoa-dashboard` | `missing` | 0/0 | 0 | 0/0/0 | 0 | / | / | 0/0 | 0/0 | known repository checkout not found under workspace root |
| `aoa-techniques` | `scanned` | 76/76 | 117 | 1/1/0 | 46 | 19153/20319 | 0/0 | 0/0 | 194/0 |  |
| `aoa-skills` | `missing` | 0/0 | 0 | 0/0/0 | 0 | / | / | 0/0 | 0/0 | known repository checkout not found under workspace root |
| `aoa-evals` | `missing` | 0/0 | 0 | 0/0/0 | 0 | / | / | 0/0 | 0/0 | known repository checkout not found under workspace root |
| `aoa-stats` | `missing` | 0/0 | 0 | 0/0/0 | 0 | / | / | 0/0 | 0/0 | known repository checkout not found under workspace root |
| `aoa-routing` | `missing` | 0/0 | 0 | 0/0/0 | 0 | / | / | 0/0 | 0/0 |  |
| `aoa-memo` | `missing` | 0/0 | 0 | 0/0/0 | 0 | / | / | 0/0 | 0/0 | known repository checkout not found under workspace root |
| `aoa-session-memory` | `scanned` | 15/15 | 66 | 4/11/0 | 8 | 9419/9419 | 0/0 | 0/0 | 82/0 |  |
| `aoa-agents` | `missing` | 0/0 | 0 | 0/0/0 | 0 | / | / | 0/0 | 0/0 | known repository checkout not found under workspace root |
| `aoa-models` | `missing` | 0/0 | 0 | 0/0/0 | 0 | / | / | 0/0 | 0/0 | known repository checkout not found under workspace root |
| `aoa-agon` | `missing` | 0/0 | 0 | 0/0/0 | 0 | / | / | 0/0 | 0/0 | known repository checkout not found under workspace root |
| `aoa-playbooks` | `missing` | 0/0 | 0 | 0/0/0 | 0 | / | / | 0/0 | 0/0 | known repository checkout not found under workspace root |
| `aoa-kag` | `missing` | 0/0 | 0 | 0/0/0 | 0 | / | / | 0/0 | 0/0 | known repository checkout not found under workspace root |
| `aoa-instagram-connector` | `scanned` | 1/1 | 3 | 0/0/0 | 1 | 1687/1687 | 0/0 | 0/0 | 0/4 | active AGENTS.md corpus has 1 unclassified fenced block(s); active AGENTS.md fences retain 4 executable invocation(s) |
| `aoa-pinterest-connector` | `scanned` | 1/1 | 3 | 0/0/0 | 1 | 1259/1259 | 0/0 | 0/0 | 0/4 | active AGENTS.md corpus has 1 unclassified fenced block(s); active AGENTS.md fences retain 4 executable invocation(s) |
| `aoa-tiktok-connector` | `scanned` | 1/1 | 3 | 0/0/0 | 1 | 1278/1278 | 0/0 | 0/0 | 0/4 | active AGENTS.md corpus has 1 unclassified fenced block(s); active AGENTS.md fences retain 4 executable invocation(s) |
| `aoa-x-connector` | `scanned` | 1/1 | 3 | 0/0/0 | 1 | 1245/1245 | 0/0 | 0/0 | 0/4 | active AGENTS.md corpus has 1 unclassified fenced block(s); active AGENTS.md fences retain 4 executable invocation(s) |
| `aoa-youtube-connector` | `scanned` | 1/1 | 3 | 0/0/0 | 1 | 1290/1290 | 0/0 | 0/0 | 0/4 | active AGENTS.md corpus has 1 unclassified fenced block(s); active AGENTS.md fences retain 4 executable invocation(s) |

## How to read the signals

- `missing` means the known public repository was not found under the selected workspace root.
- `checkout_requirement: optional` means an absent retained predecessor is valid and does not create an audit issue.
- Corpus counts use Git-tracked `README.md` and `AGENTS.md`; untracked documents are candidates, not canonical corpus members.
- `tracked_design_agents_files` counts the related on-demand `DESIGN.AGENTS.md` corpus separately; these files require review and fenced-block classification but do not inflate inherited AGENTS-chain bytes.
- `chain_scopes` measures unique document directories; `unique_agents_chains` collapses directories that inherit the same AGENTS path signature.
- Chain percentiles use the nearest-rank method; the repository table reports unique chain signatures.
- `Repeated long blocks` counts exact normalized prose blocks of at least 180 bytes appearing in at least four tracked `AGENTS.md` files; fenced examples are excluded and redundant bytes count copies beyond the first.
- `VALIDATION files/cmds/duplicates` counts active authored on-demand files, normalized shell invocations, and exact command groups with more than one human owner inside one repository. Generated, vendor, fixture, and archive surfaces are excluded.
- `readme_validation_command_overlap_groups` is a review signal: a public usage example may be valid, but required validation should route to its one procedure owner.
- Dispositions remain `unreviewed` until an owner-evidenced record is added to the integration manifest.
- `validator_present` reports only the historical `scripts/validate_nested_agents.py` convention; an owner may validate AGENTS through another script, schema, test, or generated contract.
- `not_in_conventional_nested_validator_map` is populated only when a recognized static required-path map can be extracted from that conventional file. It does not mean that other cards are unvalidated.
- Deprecated `unvalidated_nested_agents` stays empty because a filename scan cannot prove absence of owner-local validation; `unvalidated_by_any_agents_validator` likewise requires stronger owner evidence than this audit has.
- `high_risk_dirs_without_agents` marks common contract, generated, test, runtime, or source directories without a direct local instruction file.
- `long_root_agents` marks roots that may be ready for slimming after local instructions are pushed down-tree.

Use this document as a compass before AGENTS refactors: measure first, then move doctrine to the smallest owner surface.
