# AbyssOS Workspace

This page is the human and operator entrypoint for the sibling workspace at
`<workspace-root>`. The directory is a federation of owner repositories, not a
monorepo and not a source of layer-specific truth.

Agents do not need to preload this page. Agent editing rules start in
`<workspace-root>/AGENTS.md` and continue through the nearest `AGENTS.md` in
the selected owner repository.

## Start with the owner

- ecosystem identity, federation rules, and program direction:
  `Agents-of-Abyss/README.md`
- source-linked knowledge and interpretation architecture:
  `Tree-of-Sophia/README.md`
- runtime, deployment, storage, and lifecycle:
  `abyss-stack/README.md`
- operator-facing companion behavior and safe automation:
  `ATM10-Agent/README.md`
- typed workspace integration and control-plane access: `aoa-sdk/README.md`
- reusable practice, portable skills, proof, and measurement:
  `aoa-techniques/README.md`, `aoa-skills/README.md`, `aoa-evals/README.md`,
  and `aoa-stats/README.md`
- roles, scenarios, memory, and derived knowledge:
  `aoa-agents/README.md`, `aoa-playbooks/README.md`, `aoa-memo/README.md`, and
  `aoa-kag/README.md`
- public profile and the broader route map: `8Dionysus/README.md`

When a question becomes concrete, use that repository's human `README.md`,
nearest agent route card, authored contracts, and validators. Generated maps,
installed projections, runtime receipts, and this page remain derived or
orienting surfaces.

## Workspace surfaces

- `AOA_WORKSPACE_ROOT` marks the sibling workspace for local tooling.
- `AGENTS.md` is the projected workspace route card for agents.
- `.agents/` and the source-owned subset of `.codex/` are selected install
  surfaces with narrower owner and deployment boundaries.
- `8Dionysus/docs/WORKSPACE_INSTALL.md` owns the projection and bootstrap
  procedure.

This file is projected from
`8Dionysus/docs/WORKSPACE_ROOT_ENTRY.md`. Edit the owner source first and use
the `8Dionysus` workspace projector; do not treat the live copy as source.
