# Workspace memory map

This generated map is the first OS Abyss memory overlay surface.
It tells agents where memory routes, local ports, session evidence, and reviewed memory handoff currently live.
It is not memory authority; reviewed memory belongs to `aoa-memo`, session evidence belongs to `.aoa`, and MCP is only an access plane.

## Regenerate

```bash
python scripts/build_workspace_memory_map.py \
  --workspace-root <workspace-root> \
  --write generated/workspace_memory_map.min.json \
  --markdown docs/WORKSPACE_MEMORY_MAP.md
python scripts/build_workspace_memory_map.py --check
python scripts/validate_workspace_memory_map.py
```

## Totals

- `full_ports`: 9
- `landed_exports`: 2
- `local_candidates`: 3
- `memory_routes`: 20
- `pending_candidates`: 3
- `pending_exports`: 1
- `places_listed`: 20
- `places_scanned`: 20
- `places_with_issues`: 0
- `ready_exports`: 0
- `recommended_full_ports_missing`: 0
- `root_memory_routes`: 19
- `route_only`: 11
- `session_evidence_routes`: 1
- `writeback_live_checks`: 5
- `writeback_markers`: 5
- `writeback_needs_marker`: 15
- `writeback_not_applicable`: 0
- `writeback_unknown`: 0

## Access Plane

- `name`: `aoa_memo`
- `registration_status`: `registered`
- `runtime_status`: `not_asserted_by_workspace_map`
- `owner`: `abyss-stack`
- `authority`: `aoa-memo`
- `source`: `~/src/abyss-stack/mcp/services/aoa-memo-mcp`
- `smoke_check`: `python scripts/smoke_aoa_memo_mcp.py --workspace-root <workspace-root>`

## Port Levels

| Level | Meaning |
|---|---|
| `none` | no visible local memo route in this place yet |
| `route_only` | root AGENTS.md or owner-local route points to aoa_memo/.aoa/reviewed memory without a local memo port |
| `stub_port` | memo/ exists with route card and PORT.yaml, but is not yet fully indexed |
| `full_port` | memo/ has route card, PORT.yaml, packet dirs, and index |
| `mature_port` | future state: local port is connected to reviewed landing, stats/evals, and repo vocabulary |

## Writeback Debt

The checked-in map records stable marker routes. Git currentness is live-derived so the map does not become stale from its own commit.

```bash
python scripts/build_workspace_memory_map.py \
  --workspace-root <workspace-root> \
  --writeback-debt-json
```

| Place | Debt route | Marker | Decision | Next route |
|---|---|---|---|---|
| 8Dionysus | `live_check_required` | 8Dionysus/docs/decisions/0012-reviewed-memory-landing-receipts-as-writeback-markers.md | `route_only_debt` | run live writeback debt check before closeout |
| Agents-of-Abyss | `needs_marker` | missing | `` | run aoa-memo-writeback and record a candidate/export/no-writeback marker |
| Tree-of-Sophia | `needs_marker` | missing | `` | run aoa-memo-writeback and record a candidate/export/no-writeback marker |
| abyss-stack | `live_check_required` | ~/src/abyss-stack/memo/receipts/20260526T003646Z.export-abyss-stack-20260526t003500z-os-access-pl.forwarding-receipt.json | `write_candidate` | run live writeback debt check before closeout |
| ATM10-Agent | `needs_marker` | missing | `` | run aoa-memo-writeback and record a candidate/export/no-writeback marker |
| Dionysus | `needs_marker` | missing | `` | run aoa-memo-writeback and record a candidate/export/no-writeback marker |
| aoa-sdk | `needs_marker` | missing | `` | run aoa-memo-writeback and record a candidate/export/no-writeback marker |
| aoa-techniques | `needs_marker` | missing | `` | run aoa-memo-writeback and record a candidate/export/no-writeback marker |
| aoa-skills | `live_check_required` | aoa-skills/docs/decisions/2026-05-25-memo-writeback-skill-owner-boundary.md | `route_only_debt` | run live writeback debt check before closeout |
| aoa-evals | `live_check_required` | aoa-evals/docs/decisions/0045-closeout-writeback-ingress-boundary.md | `route_only_debt` | run live writeback debt check before closeout |
| aoa-stats | `needs_marker` | missing | `` | run aoa-memo-writeback and record a candidate/export/no-writeback marker |
| aoa-routing | `needs_marker` | missing | `` | run aoa-memo-writeback and record a candidate/export/no-writeback marker |
| aoa-memo | `live_check_required` | aoa-memo/memo/intake/receipts/20260526T004143Z.abyss-stack.abyss-stack-os-access-plane-mcp-services.landing-receipt.json | `reviewed_write` | run live writeback debt check before closeout |
| aoa-agents | `needs_marker` | missing | `` | run aoa-memo-writeback and record a candidate/export/no-writeback marker |
| aoa-playbooks | `needs_marker` | missing | `` | run aoa-memo-writeback and record a candidate/export/no-writeback marker |
| aoa-kag | `needs_marker` | missing | `` | run aoa-memo-writeback and record a candidate/export/no-writeback marker |
| abyss-machine | `needs_marker` | missing | `` | run aoa-memo-writeback and record a candidate/export/no-writeback marker |
| .aoa | `needs_marker` | missing | `` | run aoa-memo-writeback and record a candidate/export/no-writeback marker |
| .codex | `needs_marker` | missing | `` | run aoa-memo-writeback and record a candidate/export/no-writeback marker |
| .agents | `needs_marker` | missing | `` | run aoa-memo-writeback and record a candidate/export/no-writeback marker |

## Places

| Place | Role | Current | Recommended | Route | Pending candidates | Pending exports | Ready | Landed | Validator | Issues |
|---|---|---|---|---|---:|---:|---:|---:|---|---|
| 8Dionysus | workspace-route-map-owner | `route_only` | `route_only` | root_memory_route | 0 | 0 | 0 | 0 | `python scripts/build_workspace_memory_map.py --check` | ok |
| Agents-of-Abyss | local-memory-port-candidate | `full_port` | `full_port` | local_port_route | 0 | 0 | 0 | 0 | `PYTHONPATH="${AOA_ABYSS_STACK_ROOT:-$HOME/src/abyss-stack}/mcp/services/aoa-memo-mcp/src" python -m aoa_memo_mcp.cli validate-port --repo Agents-of-Abyss` | ok |
| Tree-of-Sophia | local-memory-port-candidate | `full_port` | `full_port` | local_port_route | 0 | 0 | 0 | 0 | `PYTHONPATH="${AOA_ABYSS_STACK_ROOT:-$HOME/src/abyss-stack}/mcp/services/aoa-memo-mcp/src" python -m aoa_memo_mcp.cli validate-port --repo Tree-of-Sophia` | ok |
| abyss-stack | mcp-access-plane-owner | `full_port` | `full_port` | local_port_route | 3 | 1 | 0 | 2 | `PYTHONPATH="${AOA_ABYSS_STACK_ROOT:-$HOME/src/abyss-stack}/mcp/services/aoa-memo-mcp/src" python -m aoa_memo_mcp.cli validate-port --repo abyss-stack` | ok |
| ATM10-Agent | workspace-memory-route | `route_only` | `route_only` | root_memory_route | 0 | 0 | 0 | 0 | `python scripts/build_workspace_memory_map.py --check` | ok |
| Dionysus | local-memory-port-candidate | `full_port` | `full_port` | local_port_route | 0 | 0 | 0 | 0 | `PYTHONPATH="${AOA_ABYSS_STACK_ROOT:-$HOME/src/abyss-stack}/mcp/services/aoa-memo-mcp/src" python -m aoa_memo_mcp.cli validate-port --repo Dionysus` | ok |
| aoa-sdk | workspace-memory-route | `route_only` | `route_only` | root_memory_route | 0 | 0 | 0 | 0 | `python scripts/build_workspace_memory_map.py --check` | ok |
| aoa-techniques | local-memory-port-candidate | `full_port` | `full_port` | local_port_route | 0 | 0 | 0 | 0 | `PYTHONPATH="${AOA_ABYSS_STACK_ROOT:-$HOME/src/abyss-stack}/mcp/services/aoa-memo-mcp/src" python -m aoa_memo_mcp.cli validate-port --repo aoa-techniques` | ok |
| aoa-skills | local-memory-port-candidate | `full_port` | `full_port` | local_port_route | 0 | 0 | 0 | 0 | `PYTHONPATH="${AOA_ABYSS_STACK_ROOT:-$HOME/src/abyss-stack}/mcp/services/aoa-memo-mcp/src" python -m aoa_memo_mcp.cli validate-port --repo aoa-skills` | ok |
| aoa-evals | workspace-memory-route | `route_only` | `route_only` | root_memory_route | 0 | 0 | 0 | 0 | `python scripts/build_workspace_memory_map.py --check` | ok |
| aoa-stats | workspace-memory-route | `route_only` | `route_only` | root_memory_route | 0 | 0 | 0 | 0 | `python scripts/build_workspace_memory_map.py --check` | ok |
| aoa-routing | workspace-memory-route | `route_only` | `route_only` | root_memory_route | 0 | 0 | 0 | 0 | `python scripts/build_workspace_memory_map.py --check` | ok |
| aoa-memo | reviewed-memory-owner | `route_only` | `route_only` | root_memory_route | 0 | 0 | 0 | 0 | `python scripts/build_workspace_memory_map.py --check` | ok |
| aoa-agents | local-memory-port-candidate | `full_port` | `full_port` | local_port_route | 0 | 0 | 0 | 0 | `PYTHONPATH="${AOA_ABYSS_STACK_ROOT:-$HOME/src/abyss-stack}/mcp/services/aoa-memo-mcp/src" python -m aoa_memo_mcp.cli validate-port --repo aoa-agents` | ok |
| aoa-playbooks | local-memory-port-candidate | `full_port` | `full_port` | local_port_route | 0 | 0 | 0 | 0 | `PYTHONPATH="${AOA_ABYSS_STACK_ROOT:-$HOME/src/abyss-stack}/mcp/services/aoa-memo-mcp/src" python -m aoa_memo_mcp.cli validate-port --repo aoa-playbooks` | ok |
| aoa-kag | workspace-memory-route | `route_only` | `route_only` | root_memory_route | 0 | 0 | 0 | 0 | `python scripts/build_workspace_memory_map.py --check` | ok |
| abyss-machine | host-local-memory-port | `full_port` | `full_port` | local_port_route | 0 | 0 | 0 | 0 | `PYTHONPATH="${AOA_ABYSS_STACK_ROOT:-$HOME/src/abyss-stack}/mcp/services/aoa-memo-mcp/src" python -m aoa_memo_mcp.cli validate-port --repo abyss-machine` | ok |
| .aoa | session-evidence-kernel | `route_only` | `route_only` | session_evidence_route | 0 | 0 | 0 | 0 | `python scripts/build_workspace_memory_map.py --check` | ok |
| .codex | workspace-memory-route | `route_only` | `route_only` | root_memory_route | 0 | 0 | 0 | 0 | `python scripts/build_workspace_memory_map.py --check` | ok |
| .agents | workspace-memory-route | `route_only` | `route_only` | root_memory_route | 0 | 0 | 0 | 0 | `python scripts/build_workspace_memory_map.py --check` | ok |

## Route Contract

- Need continuity or reviewed recall: use `aoa_memo` through the Codex MCP plane when available.
- Need session evidence, compaction recovery, or raw transcript grounding: route to `.aoa` retrieval or rehydration packets.
- Need to preserve local memory in a place that has a port: write a candidate under `repo/memo/`, validate it, then export for reviewed intake.
- Need durable cross-system memory: land through `aoa-memo` reviewed intake and validators.
- Need writeback currentness: run the live debt command, then use `aoa-memo-writeback`; debt is a prompt to judge, not proof that a candidate must exist.
