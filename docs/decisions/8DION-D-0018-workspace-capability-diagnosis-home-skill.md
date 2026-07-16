# Workspace Capability Diagnosis Home Skill

## Index Metadata

- Decision ID: 8DION-D-0018
- Original date: 2026-07-16
- Surface classes: skill home, workspace delivery, Codex discovery, plugin retirement, owner boundary
- Route anchors: skills/aoa-workspace-diagnose, .agents/skills/aoa-workspace-diagnose, .codex/plugins/aoa-shared-launchers, docs/WORKSPACE_INSTALL.md
- Owner lanes: 8Dionysus, aoa-skills, aoa-sdk, aoa-kag, agent host, capability owner
- Guard families: manual admission, negative applicability, typed delivery, source/projection parity, read-only diagnosis
- Posture: accepted; follows 8DION-D-0017

## Status

Accepted.

## Context

`8DION-D-0017` removed the shared catalog from repository and workspace-root
projections, but left four launcher bundles nested in the `8Dionysus` plugin for
owner and admission review. Two of them attempted broad workspace orientation
and Codex wiring diagnosis. They overlapped root route cards, SDK inspection,
convergence wrappers, and each other; one was explicit-only in its adapter and
carried a fixed MCP-name list that had already drifted.

Manual comparisons covered no-skill orientation, the existing launchers, a
broad combined candidate, a focused diagnosis candidate, concrete missing-skill
and MCP-name failures, a narrow negative task, and coexistence with the shared
`aoa-decision` family. General orientation did not improve on the no-skill route
and once assigned shared skill law to the public entry repository. Focused
diagnosis consistently stopped at the earliest evidenced delivery break,
preserved owner boundaries, rejected unrelated activation, and composed with
accepted rationale without turning it into live-state evidence.

## Options Considered

1. Keep `aoa-workspace-recon` and `aoa-config-doctor` as plugin launchers.
2. Replace them with one broad `aoa-workspace` skill combining orientation and
   diagnosis.
3. Keep general orientation in route cards and KAG, admit one focused
   repository-owned diagnosis skill, and retire the two overlapping launchers.

## Decision

Choose option 3.

Admit `aoa-workspace-diagnose` version `0.1.0` under
`skills/aoa-workspace-diagnose/`. Generate its exact repository-scoped Codex
copy at `.agents/skills/aoa-workspace-diagnose/` through the common
`aoa-skills` home-port contract. The skill diagnoses one concrete disagreement
among owner source, projection, host scope, prompt visibility, configuration,
stable name, transport, or owner service. It selects a typed skill or MCP/tool
lane, remains read-only, and stops at the first evidenced break or
`intended_behavior`.

Keep general workspace orientation as a semantic capability in root route cards
and KAG rather than another callable bundle. Keep `aoa-codex-doctor`,
`aoa-codex-status`, and `aoa-codex-bootstrap` as tools and wrappers, not skills.
Remove `aoa-workspace-recon` and `aoa-config-doctor` from the launcher plugin.
The remaining `aoa-growth-snapshot` and `aoa-seed-route-inspect` launchers stay
available only pending their own owner-first admission audit; this decision
neither admits nor validates them.

Raw prompts, traces, temporary fixtures, and task-local DAGs remain session
evidence. Permanent checks protect only the admitted manifest, source ownership,
projection parity, and packaging inventory demonstrated by the manual work.

## Consequences

- `8Dionysus` gains one local callable procedure without claiming shared or
  sibling skill truth.
- The normal repository catalog loses two semantically overlapping launcher
  descriptions and one stale fixed MCP inventory.
- Route cards remain the cheap first orientation layer; KAG may federate typed
  capability relations without acquiring procedure authority.
- Diagnosis can consume owner contracts, config, prompt/catalog, and bounded
  runtime evidence, then hand repair to the correct owner. It cannot perform the
  repair or authorize mutation.
- Techniques may supply provenance or adaptation knowledge but are not a
  required dependency of this skill.
- A material model, workflow, contract, or host change requires renewed manual
  failure, negative, no-skill, and coexistence work before lifecycle expansion.

## Source Surfaces

- `AGENTS.md`
- `skills/AGENTS.md`
- `skills/README.md`
- `skills/aoa-workspace-diagnose/SKILL.md`
- `skills/port.manifest.json`
- `.agents/skills/aoa-workspace-diagnose/SKILL.md`
- `.codex/plugins/aoa-shared-launchers/`
- `docs/WORKSPACE_INSTALL.md`
- `docs/SYSTEM_CAPABILITY_MAP.md`
- `aoa-skills:docs/HOME_SKILL_PORT.md`
- `aoa-skills:docs/decisions/AOA-SK-D-0040-owner-skill-homes-and-projection-boundaries.md`
- `aoa-skills:docs/decisions/AOA-SK-D-0041-minimal-owner-home-port-contract.md`

## Validation

Use fresh-session manual failure, MCP, negative, and coexistence cases for
behavior. Use the pinned common home-port action and local validator only for
owner/source/projection structure. Regenerate decision indexes, public route
artifacts, and repo-local KAG from their sources. Inspect the final prompt
inventory from `8Dionysus`; no green structural check proves semantic benefit.
