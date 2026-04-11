# Workspace Codex Agents

This directory is the workspace install surface for the AoA custom-agent
projection.

Source order:

1. `/srv/aoa-agents/profiles/*.profile.json`
2. `/srv/aoa-agents/config/codex_subagent_wiring.v2.json`
3. `/srv/aoa-agents/generated/codex_agents/agents/*.toml`
4. `/srv/.codex/agents/*.toml`

Do not hand-edit these installed agent files as the source of truth.
Regenerate from `aoa-agents`, then copy the published projection forward.

The matching workspace registration lives in `/srv/.codex/config.toml`.
