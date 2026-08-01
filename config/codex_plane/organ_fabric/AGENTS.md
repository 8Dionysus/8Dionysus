# AGENTS.md

## Applies to

This card applies to `config/codex_plane/organ_fabric/`.

## Role

This directory is the source-owned Codex consumer projection for the OS Abyss
organ access fabric. It turns reviewed registry and runtime evidence into a
bounded registration candidate. It does not own organ admission, server
runtime, credentials, domain meaning, proof, or acceptance.

## Boundaries

- Deny by default: `shadow`, `suspended`, `deprecated`, and `retired` entries
  never render as active registrations.
- An admitted entry needs exact admission, consumer-schema, central-proof,
  canary, owner-acceptance, and rollback receipts.
- Credential values never appear here; only public environment-variable names
  and credential classes are allowed.
- The full owner catalog is never an always-loaded profile. Each render names
  one bounded profile and enforces registration and tool-count budgets.
- Candidate contours are separate registrations, credentials, profiles, and
  approval modes.
- A suspended route is removed only through an explicit removal receipt; an
  observed legacy route without consumer-zero proof remains a visible
  compatibility blocker, not an implicit delete instruction.
- A config render does not affect a running Codex process. Schema
  re-observation belongs to a fresh client process and its rollout receipt.

## Validation

```bash
python scripts/render_codex_organ_fabric.py --check
python scripts/validate_codex_organ_fabric.py
python -m unittest tests.test_codex_organ_fabric
```
