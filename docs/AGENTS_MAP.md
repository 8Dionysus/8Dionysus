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

- `active_authored_agents_classified_fenced_blocks`: 4
- `active_authored_agents_fenced_blocks`: 4
- `active_authored_agents_fenced_executable_invocations`: 0
- `active_authored_agents_unclassified_fenced_blocks`: 0
- `active_authored_design_agents_classified_fenced_blocks`: 11
- `active_authored_design_agents_fenced_blocks`: 11
- `active_authored_design_agents_fenced_executable_invocations`: 0
- `active_authored_design_agents_unclassified_fenced_blocks`: 0
- `active_authored_unique_validation_invocations`: 1100
- `active_authored_validation_bytes`: 427246
- `active_authored_validation_command_owner_files`: 338
- `active_authored_validation_files`: 592
- `active_authored_validation_invocations`: 1100
- `active_authored_validation_route_only_files`: 254
- `agents_conditional_readme_reference_lines`: 150
- `agents_fenced_example_readme_reference_lines`: 0
- `agents_files_declaring_mandatory_readme`: 0
- `agents_files_referencing_readme`: 307
- `agents_md_files`: 799
- `agents_navigational_readme_reference_lines`: 242
- `agents_only_directories`: 256
- `agents_readme_reference_lines`: 392
- `agents_validation_command_overlap_groups`: 0
- `archive_document_files`: 281
- `authored_repeated_long_agents_block_groups`: 0
- `authored_unique_chains_over_budget`: 0
- `blocked_files`: 0
- `chain_max_bytes`: 20063
- `chain_p50_bytes`: 11063
- `chain_p95_bytes`: 17952
- `chain_scopes`: 2219
- `chain_scopes_over_budget`: 0
- `declared_mandatory_readme_bytes`: 0
- `duplicate_validation_command_groups`: 0
- `duplicate_validation_command_occurrences`: 0
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
- `nested_agents_files`: 779
- `optional_repositories_missing`: 1
- `paired_directories`: 628
- `readme_only_directories`: 1335
- `readme_validation_command_overlap_groups`: 0
- `repeated_long_agents_block_groups`: 0
- `repeated_long_agents_block_instances`: 0
- `repeated_long_agents_normalized_redundant_bytes`: 0
- `repos_with_issues`: 0
- `repositories_listed`: 21
- `repositories_scanned`: 20
- `review_items_total`: 2864
- `review_items_unreviewed`: 0
- `reviewed_files`: 2862
- `root_agents_present`: 20
- `root_document_files`: 40
- `shared_root_blocked_files`: 0
- `shared_root_files`: 2
- `shared_root_files_in_owner_parity`: 2
- `shared_root_reviewed_files`: 2
- `shared_root_unreviewed_files`: 0
- `stale_agents_fenced_block_classifications`: 0
- `stale_design_agents_fenced_block_classifications`: 0
- `tracked_agents_bytes`: 1448257
- `tracked_agents_files`: 884
- `tracked_design_agents_bytes`: 127046
- `tracked_design_agents_files`: 15
- `tracked_document_bytes`: 5309519
- `tracked_document_files`: 2847
- `tracked_readme_bytes`: 3861262
- `tracked_readme_files`: 1963
- `tracked_validation_files`: 636
- `unique_agents_chains`: 884
- `unique_chain_max_bytes`: 20063
- `unique_chain_p50_bytes`: 9849
- `unique_chain_p95_bytes`: 17115
- `unique_chains_over_budget`: 0
- `unreviewed_files`: 0
- `untracked_design_agents_candidates`: 0
- `untracked_document_candidates`: 0
- `untracked_validation_candidates`: 0
- `unvalidated_nested_agents`: 0
- `validation_route_only_claim_conflicts`: 0
- `validator_required_agents`: 206
- `validators_present`: 11
- `vendor_document_files`: 0

## Repository coverage

| Repository | State | AGENTS corpus/active | README | VALIDATION files/cmds/duplicates | Pairs | Unique chain p95/max | Over 32 KiB authored/excluded | Repeated long blocks/redundant bytes | Reviewed/unreviewed | Issues |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `8Dionysus` | `scanned` | 21/21 | 12 | 4/20/0 | 6 | 8312/10715 | 0/0 | 0/0 | 33/0 |  |
| `Agents-of-Abyss` | `scanned` | 65/57 | 221 | 101/103/0 | 56 | 18583/18867 | 0/0 | 0/0 | 287/0 |  |
| `Tree-of-Sophia` | `scanned` | 56/56 | 327 | 12/25/0 | 33 | 17096/18220 | 0/0 | 0/0 | 384/0 |  |
| `abyss-stack` | `scanned` | 59/55 | 168 | 7/202/0 | 56 | 12212/14427 | 0/0 | 0/0 | 228/0 |  |
| `abyss-machine` | `scanned` | 60/60 | 38 | 10/5/0 | 27 | 9944/13417 | 0/0 | 0/0 | 100/0 |  |
| `ATM10-Agent` | `scanned` | 15/15 | 9 | 10/16/0 | 3 | 9189/9189 | 0/0 | 0/0 | 24/0 |  |
| `Dionysus` | `scanned` | 4/3 | 19 | 1/1/0 | 4 | 4548/4548 | 0/0 | 0/0 | 23/0 |  |
| `aoa-sdk` | `scanned` | 50/46 | 137 | 66/213/0 | 42 | 12201/13242 | 0/0 | 0/0 | 188/0 |  |
| `aoa-dashboard` | `scanned` | 2/2 | 2 | 1/5/0 | 1 | 1581/1581 | 0/0 | 0/0 | 4/0 |  |
| `aoa-techniques` | `scanned` | 94/77 | 169 | 1/3/0 | 64 | 18848/20063 | 0/0 | 0/0 | 264/0 |  |
| `aoa-skills` | `scanned` | 25/25 | 24 | 1/7/0 | 16 | 6342/6887 | 0/0 | 0/0 | 50/0 |  |
| `aoa-evals` | `scanned` | 90/71 | 191 | 123/109/0 | 81 | 16892/19354 | 0/0 | 0/0 | 282/0 |  |
| `aoa-stats` | `scanned` | 45/44 | 85 | 45/81/0 | 36 | 12346/12893 | 0/0 | 0/0 | 131/0 |  |
| `aoa-routing` | `missing` | 0/0 | 0 | 0/0/0 | 0 | / | / | 0/0 | 0/0 |  |
| `aoa-memo` | `scanned` | 118/103 | 164 | 152/151/0 | 68 | 16321/16672 | 0/0 | 0/0 | 283/0 |  |
| `aoa-session-memory` | `scanned` | 15/15 | 66 | 4/11/0 | 8 | 9419/9419 | 0/0 | 0/0 | 82/0 |  |
| `aoa-agents` | `scanned` | 66/54 | 185 | 1/79/0 | 55 | 13259/15757 | 0/0 | 0/0 | 252/0 |  |
| `aoa-models` | `scanned` | 2/2 | 3 | 1/7/0 | 2 | 5340/5340 | 0/0 | 0/0 | 5/0 |  |
| `aoa-agon` | `scanned` | 1/1 | 4 | 1/10/0 | 1 | 2602/2602 | 0/0 | 0/0 | 5/0 |  |
| `aoa-playbooks` | `scanned` | 38/38 | 67 | 22/52/0 | 30 | 9938/10187 | 0/0 | 0/0 | 106/0 |  |
| `aoa-kag` | `scanned` | 58/54 | 72 | 29/0/0 | 39 | 10408/10433 | 0/0 | 0/0 | 131/0 |  |

## Shared-root projection posture

| File | Declared projection | Owner parity | Review |
|---|---:|---:|---|
| `AGENTS.md` | True | True | `reviewed` |
| `README.md` | True | True | `reviewed` |

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
