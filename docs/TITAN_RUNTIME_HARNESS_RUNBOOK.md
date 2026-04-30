# Titan Runtime Harness Runbook

## Start a session

```bash
codex --cd /srv/AbyssOS "$(cat /srv/AbyssOS/8Dionysus/.codex/prompts/titan-summon.runtime-harness.v0.md)"
```

## Create a receipt

```bash
python /srv/AbyssOS/aoa-sdk/scripts/titanctl.py summon   --workspace /srv/AbyssOS   --operator Dionysus   --out /srv/AbyssOS/.titan/receipts/$(date -u +%Y%m%dT%H%M%SZ).json
```

## Activate Forge

Only after mutation intent:

```bash
python /srv/AbyssOS/aoa-sdk/scripts/titanctl.py gate   --receipt /srv/AbyssOS/.titan/receipts/<receipt>.json   --agent Forge   --kind mutation   --intent "Implement bounded change named here."
```

## Activate Delta

Only after judgment intent:

```bash
python /srv/AbyssOS/aoa-sdk/scripts/titanctl.py gate   --receipt /srv/AbyssOS/.titan/receipts/<receipt>.json   --agent Delta   --kind judgment   --intent "Evaluate bounded comparison named here."
```

## Close a session

```bash
codex --cd /srv/AbyssOS "$(cat /srv/AbyssOS/8Dionysus/.codex/prompts/titan-closeout.service-cohort.v0.md)"

python /srv/AbyssOS/aoa-sdk/scripts/titanctl.py closeout   --receipt /srv/AbyssOS/.titan/receipts/<receipt>.json   --summary "Closeout summary here."
```

## Hook posture

Hooks may add context, reminders, and warnings. Hooks must not spawn Titans behind the operator's back.
