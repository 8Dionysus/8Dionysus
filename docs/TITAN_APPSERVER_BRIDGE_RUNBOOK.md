# Titan App-Server Bridge Runbook

```bash
python /srv/aoa-sdk/scripts/titan_appserver_bridge.py init --workspace /srv --out /srv/.titan/bridge/session.json
python /srv/aoa-sdk/scripts/titan_appserver_bridge.py emit initialize
python /srv/aoa-sdk/scripts/titan_appserver_bridge.py emit thread-start --workspace /srv
```
