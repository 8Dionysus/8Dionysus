# GitHub Required Check Contracts

This note names the coordination-only source of truth for stable required
GitHub check names across the public AoA / ToS repository family.

It does not make `8Dionysus` the owner of linked repository workflow meaning.
Owner repos still decide what their checks actually prove, how broad they are,
and what release or runtime guarantees they carry.

Decision note: [docs/decisions/0002-repo-family-required-check-contracts.md](decisions/0002-repo-family-required-check-contracts.md)

## Canonical files

- `config/github_required_check_contracts.json`
- `schemas/github_required_check_contracts.schema.json`
- `scripts/validate_github_required_check_contracts.py`

These three files are the bounded coordination surface:

- the JSON contract names which repos are covered
- the schema constrains the contract shape
- the validator checks that the contract stays coherent and can also audit live drift

## Boundary

`8Dionysus` owns here:

- stable required status-check names for the public repo family
- the coordination contract that maps those names to watched workflow files
- the drift-check route that compares the declared contract against GitHub-hosted workflow files

`8Dionysus` does not own here:

- the internal validation semantics of linked repos
- the contents of the tests, audits, smokes, or proofs that a check runs
- cross-repo release policy beyond the named check contract
- runtime or infrastructure guarantees that remain owner-repo work

## Current families

- `repo-validation`: `8Dionysus`, `Agents-of-Abyss`, `Dionysus`,
  `Tree-of-Sophia`, `aoa-agents`, `aoa-evals`, `aoa-kag`, `aoa-memo`,
  `aoa-playbooks`, `aoa-routing`, `aoa-sdk`, `aoa-stats`, `aoa-techniques`
  all require `Repo Validation`
- `ATM10-Agent`: requires `test` and `smoke`
- `abyss-stack`: requires `Repo Validation` and `validate-windows-host-bridge`
- `aoa-skills`: requires `Repo Validation` and `build-validate`
- `abyss-stack_old`: intentionally stays outside this contract and must be
  reviewed manually before any tightening or cleanup work

## Validation routes

Validate contract shape only:

```bash
python scripts/validate_github_required_check_contracts.py
```

Validate tracked workflow names and required jobs against GitHub-hosted files:

```bash
python scripts/validate_github_required_check_contracts.py --remote-workflows
```

Validate live `main` branch protection contexts through the authenticated GitHub CLI:

```bash
python scripts/validate_github_required_check_contracts.py --github-protection
```

Limit either live route to one repo:

```bash
python scripts/validate_github_required_check_contracts.py \
  --remote-workflows \
  --github-protection \
  --repo 8Dionysus/aoa-skills
```

## Watch surface

`.github/workflows/repo-family-drift-check.yml` runs the remote workflow audit
on a schedule and on manual dispatch.

That watch surface is intentionally separate from `Repo Validation` on
`8Dionysus`.
Cross-repo drift should stay visible without turning unrelated `8Dionysus`
changes into merge-gate hostages to external repo state.
