#!/usr/bin/env python3
import json

context = "Titan App-Server Bridge v0 available. Explicit launch only. Atlas/Sentinel/Mneme visible; Forge mutation-gated; Delta judgment-gated."

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": context,
    }
}))
