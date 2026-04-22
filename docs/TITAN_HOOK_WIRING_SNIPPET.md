# Titan Hook Wiring Snippet

The Titan hook context is additive. It does not spawn agents. It reminds Codex about names, gates, and receipt posture.

Suggested SessionStart addition after existing AoA hook:

```json
{
  "type": "command",
  "command": "python3 /srv/8Dionysus/.codex/tools/aoa_titan_context.py",
  "statusMessage": "Titan context",
  "timeout": 10
}
```

The hook output uses `additionalContext`, so it behaves as developer context for the session.
