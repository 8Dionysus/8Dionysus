#!/usr/bin/env python3
from __future__ import annotations
import json

context = (
    "Titan Memory Loom available. Recall is candidate-grade; verify owner repos "
    "and source seeds before treating memory as truth. Default Titans: Atlas, "
    "Sentinel, Mneme. Gated Titans: Forge requires mutation; Delta requires judgment."
)

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": context,
    }
}, ensure_ascii=False))
