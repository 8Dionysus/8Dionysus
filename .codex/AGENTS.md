# AGENTS.md

## Guidance for `.codex/`

`.codex/` holds Codex-plane projection, regeneration, wrapper, and local operator-adjacent surfaces for the public entry repository. It may help agents orient in the workspace, but it does not own AoA doctrine, runtime truth, or sibling repo contracts.

Keep projected copies secondary. Source-owned files in this repository may be edited; installed live copies should be treated as evidence of projection drift, not authority.

No secrets, tokens, private hostnames, unreviewed hooks, or hidden local automation may be added here. Any mutating helper must stay bounded, documented, reversible, and route-aware.

Statistical access in the Codex plane uses `aoa_stats` as a read-only access
plane. Use it to inspect the derived catalog, central boundary references,
owner-local `stats/` ports, and measurement-packet compatibility. Statistical
meaning and the public read contract remain in `aoa-stats`; local questions and
evidence remain with their owner repositories; runnable MCP service code
remains in `abyss-stack`.

Memory access in the Codex plane uses `aoa_memo` as an access plane. Use it for
brief, search, local-port status, candidate creation, port indexing, and intake
review when work asks for recall, continuity, preservation, compaction recovery,
or memory handoff. Use `generated/workspace_memory_map.min.json` to inspect
which roots have local ports or route-only status. Durable reviewed memory still
lands through `aoa-memo`.

Session-evidence access in the Codex plane uses `aoa_session_memory` as an
access plane. Use it to inspect `.aoa` search, route maps, session briefs,
retrieval packets, evidence handles, freshness, diagnostics, and non-mutating
maintenance plans when work asks to debug or study a stable skill, MCP, hook,
tool, path, goal, or other recurring agent-process anchor. Raw transcript,
segment indexes, atlas maps, diagnostics, and reviewed distillation authority
remain in `.aoa`; the MCP must return refs and route signals, not become truth.

Bounded proof access in the Codex plane uses `aoa_evals` as an access plane.
Use it to select and inspect eval bundles, generated readers, comparison
records, read-only find-or-propose eval-need routes, runtime evidence templates,
runtime freshness status, candidate evidence packet validation, stack-owned
runtime candidate exports, and candidate-only report skeletons. Candidate
validation, find-or-propose results, and runtime export reads are pre-review
only. Verdicts, proposal approval, source bundle creation, evidence acceptance,
receipt publication, bundle promotion, and proof authority remain in
`aoa-evals`.

KAG access in the Codex plane uses `aoa_kag` as an access plane. Use it to
inspect KAG provider status, provider records, source-return routes, freshness
handles, registry slices, composition slices, validation status, and prompt
routes. KAG schema, readiness, generated provider maps, and provider-home
validation remain in `aoa-kag`; runnable MCP service code remains in
`abyss-stack`; source meaning remains with the provider repositories.

Decision-lane access in the Codex plane uses `aoa_decisions` as an access
plane. Use it to search, inspect, and packetize workspace `docs/decisions/`
records before broad repo reads. The service refreshes its generated graph
cache before reads when the input fingerprint changes. Decision creation,
correction, supersession, and authority still land in the owning repository's
source decision notes and local decision-index validators.

Host-machine context in the Codex plane uses `abyss_machine` as an access plane.
Use it for compact owner-aware machine briefs, evidence maps, safe read surfaces
such as resource/memory/typing/nervous status, focused nervous recall, and
non-mutating route preflight. Host facts, policy, mutation authority, and
change-ledger truth remain in `abyss-machine`; MCP does not run arbitrary shell,
privileged commands, repair, cleanup, service lifecycle, or process mutation.

If an MCP tool handle reports `Transport closed`, do not claim live MCP
availability from registration alone. Run the service CLI or stdio smoke check,
then restart the Codex MCP host/session before relying on live tool calls.

Verify with:

```bash
python scripts/validate_nested_agents.py
python scripts/build_workspace_memory_map.py --check
python /srv/AbyssOS/8Dionysus/scripts/smoke_aoa_stats_mcp.py --workspace-root /srv/AbyssOS
python /srv/AbyssOS/8Dionysus/scripts/smoke_aoa_memo_mcp.py --workspace-root /srv/AbyssOS
python /srv/AbyssOS/8Dionysus/scripts/smoke_aoa_session_memory_mcp.py --workspace-root /srv/AbyssOS
python /srv/AbyssOS/8Dionysus/scripts/smoke_aoa_evals_mcp.py --workspace-root /srv/AbyssOS
python /srv/AbyssOS/8Dionysus/scripts/smoke_aoa_kag_mcp.py --workspace-root /srv/AbyssOS
python /srv/AbyssOS/8Dionysus/scripts/smoke_aoa_decisions_mcp.py --workspace-root /srv/AbyssOS
python /srv/AbyssOS/8Dionysus/scripts/smoke_abyss_machine_mcp.py --workspace-root /srv/AbyssOS
python scripts/audit_agents_map.py --workspace-root <workspace-root> --write generated/agents_map.min.json --markdown docs/AGENTS_MAP.md
```
