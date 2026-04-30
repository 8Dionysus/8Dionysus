# Titan App-Server Bridge Runbook

```bash
python /srv/AbyssOS/aoa-sdk/scripts/titan_appserver_bridge.py init --workspace /srv/AbyssOS --out /srv/AbyssOS/.titan/bridge/session.json
python /srv/AbyssOS/aoa-sdk/scripts/titan_appserver_bridge.py emit initialize
python /srv/AbyssOS/aoa-sdk/scripts/titan_appserver_bridge.py emit thread-start --workspace /srv/AbyssOS
```
