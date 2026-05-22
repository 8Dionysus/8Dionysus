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
- `landed_exports`: 1
- `local_candidates`: 2
- `memory_routes`: 20
- `pending_candidates`: 2
- `pending_exports`: 1
- `places_listed`: 20
- `places_scanned`: 20
- `places_with_issues`: 0
- `ready_exports`: 0
- `recommended_full_ports_missing`: 0
- `root_memory_routes`: 19
- `route_only`: 11
- `session_evidence_routes`: 1

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

## Places

| Place | Role | Current | Recommended | Route | Pending candidates | Pending exports | Ready | Landed | Validator | Issues |
|---|---|---|---|---|---:|---:|---:|---:|---|---|
| 8Dionysus | workspace-route-map-owner | `route_only` | `route_only` | root_memory_route | 0 | 0 | 0 | 0 | `python scripts/build_workspace_memory_map.py --check` | ok |
| Agents-of-Abyss | local-memory-port-candidate | `full_port` | `full_port` | local_port_route | 0 | 0 | 0 | 0 | `PYTHONPATH="${AOA_ABYSS_STACK_ROOT:-$HOME/src/abyss-stack}/mcp/services/aoa-memo-mcp/src" python -m aoa_memo_mcp.cli validate-port --repo Agents-of-Abyss` | ok |
| Tree-of-Sophia | local-memory-port-candidate | `full_port` | `full_port` | local_port_route | 0 | 0 | 0 | 0 | `PYTHONPATH="${AOA_ABYSS_STACK_ROOT:-$HOME/src/abyss-stack}/mcp/services/aoa-memo-mcp/src" python -m aoa_memo_mcp.cli validate-port --repo Tree-of-Sophia` | ok |
| abyss-stack | mcp-access-plane-owner | `full_port` | `full_port` | local_port_route | 2 | 1 | 0 | 1 | `PYTHONPATH="${AOA_ABYSS_STACK_ROOT:-$HOME/src/abyss-stack}/mcp/services/aoa-memo-mcp/src" python -m aoa_memo_mcp.cli validate-port --repo abyss-stack` | ok |
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
