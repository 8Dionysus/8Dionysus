# Titan Memory Loom Runbook

## Initialize

```bash
python /srv/aoa-sdk/scripts/titan_memory_loom.py init --workspace /srv --operator Dionysus --out /srv/.titan/memory/index.json
```

## Ingest a receipt

```bash
python /srv/aoa-sdk/scripts/titan_memory_loom.py ingest --index /srv/.titan/memory/index.json --receipt /srv/.titan/receipts/session.json --source-kind titanctl
```

## Recall

```bash
python /srv/aoa-sdk/scripts/titan_memory_loom.py recall --index /srv/.titan/memory/index.json --query "Forge mutation gate"
```

## Redact

```bash
python /srv/aoa-sdk/scripts/titan_memory_loom.py redact --index /srv/.titan/memory/index.json --record-id <id> --mode mask --reason "operator requested redaction"
```
