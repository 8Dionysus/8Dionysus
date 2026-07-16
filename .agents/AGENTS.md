# AGENTS.md

## Guidance for `.agents/`

`.agents/` is a shared-root projection source and agent-facing companion surface for the public workspace entrypoint. Treat it as source-owned by `8Dionysus` only when the checked-in file lives in this repository.

This source owns workspace plugin discovery and local agent-install companions.
It does not own a shared `.agents/skills/` projection. Shared AoA bundles install
once through the `aoa-skills` `user-default` profile, while a repository may
project only the bundles admitted from its own top-level `skills/` home.

Do not treat projected live workspace copies as primary truth. Edit the source-owned copy here first, then project or install through the documented workspace path. The workspace projector excludes `.agents/skills/` from copy and prune authority.

Keep this surface public-safe: no secrets, private machine paths, local-only credentials, raw transcripts, or operator-only assumptions. Route layer-specific meaning back to the owning sibling repository.

Memory route: use the workspace root `AGENTS.md` and
`generated/workspace_memory_map.min.json` to decide whether a task needs
`aoa_memo`, `.aoa` session evidence, or a repository-local `memo/` port. This
install surface does not own durable memory truth.

Verify changes with:

```bash
python scripts/validate_nested_agents.py
python scripts/build_workspace_memory_map.py --check
python scripts/audit_agents_map.py --workspace-root <workspace-root> --write generated/agents_map.min.json --markdown docs/AGENTS_MAP.md
```
