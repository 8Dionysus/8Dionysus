# Decision 0006: System Local Memo Port Rollout

## Context

The workspace memory map showed three working full ports and six recommended
full ports still missing across core author, runtime, and agent-layer
repositories. Waiting for every repository to complete a deep topology refactor
would leave memory usable only in pilot places. Creating uncontrolled note
folders would make the memory layer grow without contracts.

## Options considered

1. Keep the remaining repositories route-only until their full refactors land.
2. Add ad hoc `memo/` folders wherever an agent wants continuity.
3. Add thin, contract-backed local memo ports now and let deeper repo topology
   mature later.

## Decision

Choose option 3.

The rollout adds packet-first `memo/` ports to the core recommended repositories
that were still missing them: `Tree-of-Sophia`, `Dionysus`, `aoa-skills`,
`aoa-techniques`, `aoa-agents`, and `aoa-playbooks`.

Each port uses the same minimal topology:

```text
memo/AGENTS.md
memo/README.md
memo/PORT.yaml
memo/INDEX.md
memo/index.min.json
memo/candidates/
memo/receipts/
memo/exports/
memo/local/
```

`PORT.yaml` owns the local contract, packet directories hold local state, and
`INDEX.md` / `index.min.json` are generated read models. Durable reviewed memory
still lands only through `aoa-memo` reviewed intake.

## Consequences

- Agents can now create and validate local memory candidates in the main
  author, runtime, and agent-layer repositories without guessing where memory
  belongs.
- The workspace map can report the full-port layer as present instead of
  listing rollout debt.
- The change does not move existing repository doctrine, schemas, examples,
  scripts, or tests. Deep topology refactors remain repo-owned follow-up work.
- MCP remains an access plane for brief, status, validation, and landing plans;
  it does not become durable memory authority.
