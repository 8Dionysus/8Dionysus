# Treat the Conventional AGENTS Validator as Inventory

## Index Metadata

- Decision ID: 8DION-D-0034
- Original date: 2026-09-04
- Surface classes: workspace audit, AGENTS context, validator discovery, generated map
- Route anchors: scripts/audit_agents_map.py, scripts/recon_agents_frontier.py, docs/AGENTS_MAP.md
- Owner lanes: 8Dionysus, sibling owner repositories
- Guard families: owner boundary, validator coverage, compatibility telemetry, false-positive prevention
- Posture: accepted integration measurement; validator authority and implementation remain owner-local

## Status

Accepted.

## Context

The workspace audit historically looked only for
`scripts/validate_nested_agents.py` and treated its absence as an issue whenever
a repository had nested `AGENTS.md` files. That filename is useful in several
repositories, but it is not a federation contract. Other owners validate their
agent surfaces through differently located scripts, schemas, generated maps,
package tests, or broader source validators.

Equating one filename with all owner validation created false integration
failures and inflated the `unvalidated_nested_agents` count. It also pressured
sibling owners to copy a file layout chosen by `8Dionysus`, even when their
existing validation architecture expressed the boundary more accurately.

## Options Considered

1. Require every owner repository to add `scripts/validate_nested_agents.py`.
2. Maintain a central list of alternative validator paths and infer equivalent
   authority from filenames or source mentions.
3. Retain the conventional filename as compatibility inventory, validate its
   declared paths when present, and make no positive or negative coverage claim
   when it is absent.

## Decision

Choose option 3.

`validator_present` remains as a compatibility field for consumers of the
existing map, but it means only that the conventional file exists. The audit
also emits `validator_discovery_state` and
`not_in_conventional_nested_validator_map`. The latter is populated only when
a recognized static required-path map can be extracted. The older
`unvalidated_nested_agents` field remains present but empty: this integration
scan has no basis for claiming that a card is unvalidated by every owner-local
script, schema, test, or builder.

Absence of the conventional file is inventory, not an audit issue and not a
frontier-priority boost. When the file does exist, a declared nested card that
is absent remains an issue. Independent failures such as a missing root card,
invalid headings, unreviewed surfaces, executable AGENTS fences, validation
command duplication, or route-only claim conflicts remain unchanged.

## Consequences

- Sibling owners keep authority over validator layout and validation meaning.
- The integration audit stops claiming that one repository's filename is a
  portable contract.
- The generated map remains backward-compatible while making the claim limit
  explicit.
- `not_in_conventional_nested_validator_map` is an exact set difference, not a
  completeness or quality verdict; `unvalidated_by_any_agents_validator`
  requires stronger owner evidence and remains empty here.
- `validator_present: false` does not prove that an owner lacks validation;
  `validator_present: true` does not prove that its validator is sufficient or
  green.
- Full owner validation and CI evidence remain required outside this inventory
  signal before the merge barrier can open.
- If the federation later needs portable validator discovery, that requires an
  explicit owner-authored manifest or typed contract, not filename heuristics.

## Verification

Run the focused map/frontier tests, rebuild and validate the decision indexes,
regenerate the merge-bound map from the exact clean owner-worktree matrix, and
confirm that only substantive audit issues contribute to `repos_with_issues`.
