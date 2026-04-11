---
name: aoa-config-doctor
description: Diagnose AoA Codex wiring when shared launcher skills or AoA MCP servers are missing, misnamed, or disconnected. Use when /mcp is incomplete, dependencies do not resolve, or a skill should work but does not.
---

# AoA Config Doctor

Diagnose the wiring instead of guessing.

## First checks
1. Confirm the user is inside the intended AoA workspace.
2. Ask Codex to show `/mcp` and `/skills`.
3. Check that the expected MCP names are present:
   - `aoa_workspace`
   - `aoa_stats`
   - `dionysus`

## If local shell access is appropriate
Recommend running the dependency checker script from this pack:

```bash
python tools/check_skill_mcp_dependencies.py           --skills-root ~/.agents/skills           --codex-config /ABSOLUTE/PATH/TO/AOA_WORKSPACE/.codex/config.toml
```

## Output contract
Return:

1. **What is missing**
2. **Whether the problem is skill discovery or MCP wiring**
3. **Exact path to fix first**
4. **Shortest verification step**

## Boundary rules
- Prefer naming mismatches and path mismatches over vague blame.
- Do not recommend duplicating shared skills into every repo unless there is a clear reason.
