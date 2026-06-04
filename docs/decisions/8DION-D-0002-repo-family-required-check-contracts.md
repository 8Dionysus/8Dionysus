# Repo-Family Required Check Contracts Stay Coordination-Only in 8Dionysus

## Index Metadata

- Decision ID: 8DION-D-0002
- Original date: 2026-04-19
- Surface classes: github required checks, repo-family coordination, public contract
- Route anchors: config/github_required_check_contracts.json, docs/GITHUB_REQUIRED_CHECK_CONTRACTS.md, scripts/validate_github_required_check_contracts.py, scripts/run_required_check_audit.py
- Owner lanes: 8Dionysus, public repo family, owner repositories
- Guard families: branch protection, workflow drift, coordination-only
- Posture: accepted

## Context

The public AoA / ToS repository family now shares a deliberate main-branch
protection posture:

- most repos require `Repo Validation`
- `ATM10-Agent` requires `test` and `smoke`
- `abyss-stack` extends the contract with `validate-windows-host-bridge`
- `aoa-skills` extends the contract with `build-validate`

Before this note, that agreement lived mostly in merged pull requests and
operator memory.
That was workable for one rollout wave, but it left the family vulnerable to
future name drift between:

- owner-repo workflow files
- branch protection contexts
- solo + Codex session assumptions

## Options considered

1. leave the contract informal and re-discover it when drift appears
2. move the contract into `Agents-of-Abyss` as if it were ecosystem charter
3. record a bounded coordination contract in `8Dionysus`, then validate owner
   repo workflow names against it while leaving owner semantics in owner repos

## Decision

Choose option 3.

`8Dionysus` will own one coordination-only contract for stable required GitHub
check names across the public repo family:

- `config/github_required_check_contracts.json`
- `schemas/github_required_check_contracts.schema.json`
- `scripts/validate_github_required_check_contracts.py`
- [docs/GITHUB_REQUIRED_CHECK_CONTRACTS.md](../GITHUB_REQUIRED_CHECK_CONTRACTS.md)

The validator will keep two routes distinct:

- a remote workflow drift check that reads GitHub-hosted workflow files
- a live branch-protection audit that uses authenticated `gh` when an operator
  wants an admin-grade check

The remote workflow drift route stays a watch surface, not a required merge
gate for `8Dionysus` pull requests.

## Consequences

- future contributors get one explicit place to inspect the current contract
- Codex sessions can run one bounded audit command instead of rebuilding the
  family contract from memory
- owner repos still own what their checks mean and prove
- `8Dionysus` gains a coordination artifact without claiming constitutional or
  implementation authority over linked repos
- branch protection drift still requires authenticated live inspection and does
  not become fake certainty inside unauthenticated CI
