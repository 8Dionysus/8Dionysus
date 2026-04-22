# Titan Runtime Harness Session Example

Operator:

```text
Spawn Atlas, Sentinel, and Mneme using the runtime harness. Keep Forge and Delta locked.
```

Expected Codex posture:

```text
Atlas active: route and owner boundaries
Sentinel active: risks and gates
Mneme active: provenance and receipt posture
Forge locked: mutation gate required
Delta locked: judgment gate required
```

Receipt:

```bash
python /srv/aoa-sdk/scripts/titanctl.py summon --workspace /srv --operator Dionysus --out /srv/.titan/receipts/example.json
```
