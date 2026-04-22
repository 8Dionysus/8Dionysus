#!/usr/bin/env python3
"""Emit Titan service-cohort context for Codex hooks.

This script does not spawn agents. It only returns additional context.
"""

import json

context = """Titan service cohort names:
- Atlas = architect, read-only, active after explicit summon.
- Sentinel = reviewer, read-only, active after explicit summon.
- Mneme = memory-keeper, read-only, active after explicit summon.
- Forge = coder, workspace-write posture, locked until mutation gate.
- Delta = evaluator, read-only, locked until judgment gate.

Do not autospawn subagents from hook context.
Do not activate Forge without mutation intent.
Do not activate Delta without judgment intent.
Prefer creating or updating a local Titan session receipt through aoa-sdk/scripts/titanctl.py when the operator asks for runtime harness tracking.
"""

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": context
    }
}))
