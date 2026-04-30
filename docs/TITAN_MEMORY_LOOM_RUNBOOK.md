# Titan Memory Loom Runbook

## Initialize

```bash
python /srv/AbyssOS/aoa-sdk/scripts/titan_memory_loom.py init --workspace /srv/AbyssOS --operator Dionysus --out /srv/AbyssOS/.titan/memory/index.json
```

## Ingest a receipt

```bash
python /srv/AbyssOS/aoa-sdk/scripts/titan_memory_loom.py ingest --index /srv/AbyssOS/.titan/memory/index.json --receipt /srv/AbyssOS/.titan/receipts/session.json --source-kind titanctl
```

## Recall

```bash
python /srv/AbyssOS/aoa-sdk/scripts/titan_memory_loom.py recall --index /srv/AbyssOS/.titan/memory/index.json --query "Forge mutation gate"
```

## Redact

```bash
python /srv/AbyssOS/aoa-sdk/scripts/titan_memory_loom.py redact --index /srv/AbyssOS/.titan/memory/index.json --record-id <id> --mode mask --reason "operator requested redaction"
```
