# Decision Records

`docs/decisions/` preserves why `8Dionysus` chose a route, public-entry
contract, shared-root projection, Codex-plane name, workspace-map behavior, or
validator boundary.

This is a rationale surface, not a changelog and not a replacement for owner
repositories. Keep source truth in the owning repo; use this lane for the
bounded `8Dionysus` decision and its consequences.

## Current Surfaces

- Decision records: `8DION-D-####-short-kebab-title.md`
- Template: [TEMPLATE.md](TEMPLATE.md)
- Local route law: [AGENTS.md](AGENTS.md)
- Generated indexes: [indexes](indexes/README.md)
- Index contract: [indexes/index_contract.yaml](indexes/index_contract.yaml)

## When To Add A Record

Add a decision record when future agents need to recover why `8Dionysus` chose
or preserved a path around:

- public-entry route posture
- shared-root projection source truth
- Codex-plane MCP names and launcher boundaries
- workspace memory map marker/debt behavior
- repo-family GitHub coordination contracts
- local validators that define public contract drift

Do not add a record for a routine typo, generated refresh, or implementation
detail whose rationale is already obvious from the diff and tests.

## Update Rule

Decision records are durable rationale snapshots. If a material choice changes,
add a new `8DION-D-####` record with supersession context instead of rewriting
old rationale into a mutable ledger.

Small clarifications, broken links, and metadata repairs may update an existing
record when they do not change the recorded decision.

## Verify

```bash
python scripts/generate_decision_indexes.py --check
python scripts/validate_decision_records.py
python -m unittest tests.test_decision_indexes
```
