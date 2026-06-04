# AGENTS.md

## Guidance for `docs/decisions/`

`docs/decisions/` is the canonical rationale lane for decisions owned by the
`8Dionysus` public-entry repository. Use it when a route, projection,
Codex-plane, workspace-map, GitHub coordination, public contract, or validator
authority choice needs durable "why" context.

This lane does not own sibling-repo doctrine. If a decision belongs to
`Agents-of-Abyss`, `Tree-of-Sophia`, `aoa-sdk`, `abyss-stack`, `.aoa`,
`aoa-memo`, or another owner repo, record it there and keep only the
`8Dionysus` routing consequence here.

Canonical records use:

```text
8DION-D-####-short-kebab-title.md
```

Every record must include `## Index Metadata` with:

- `Decision ID`
- `Original date`
- `Surface classes`
- `Route anchors`
- `Owner lanes`
- `Guard families`
- `Posture`

Generated indexes live under `docs/decisions/indexes/` and are read models only.
Do not edit them by hand. Regenerate them from decision metadata.

Verify with:

```bash
python scripts/generate_decision_indexes.py --check
python scripts/validate_decision_records.py
python -m unittest tests.test_decision_indexes
```
