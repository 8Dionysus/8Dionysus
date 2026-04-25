# AGENTS frontier reconnaissance

Use this document when the AGENTS map shows high-risk directories without local guidance.

The goal is not to add an `AGENTS.md` to every directory. The goal is to identify places where a future agent can realistically make a harmful or confusing move because the nearest instruction is too far away.

## Command

After regenerating the AGENTS map, run:

```bash
python scripts/recon_agents_frontier.py \
  --map generated/agents_map.min.json \
  --write generated/agents_frontier_recon.min.json \
  --markdown generated/agents_frontier_recon.md
```

## How to read priorities

- `P0`: add or validate local `AGENTS.md` before the next broad refactor.
- `P1`: inspect and usually add local guidance if the directory carries contracts, generation, runtime, or projection behavior.
- `P2`: inspect first; many docs, examples, reports, and templates do not need new local law.
- `P3`: watch unless the directory starts carrying active rules or risky automation.

## Rules of the blade

Do not add a local `AGENTS.md` merely to quiet a metric. Add one when it prevents a concrete mistake: editing generated output by hand, making schemas without examples, treating reports as proof, turning quest language into authority, hiding runtime behavior in scripts, or letting projection copies replace source-owned files.

When a local `AGENTS.md` lands, promote it into the nearest validator map and rerun the audit. A signpost that no validator checks is a painted door on a wall.
