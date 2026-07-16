# AGENTS.md

## Applies to

This card applies to the canonical `8Dionysus/skills/` home.

## Role

This home owns only admitted callable procedures specific to the public
workspace-delivery lane. The current canonical source is
`skills/aoa-workspace-diagnose/SKILL.md`; its `.agents/skills/` copy is a
generated repository projection and never source truth.

## Read before editing

Read root `AGENTS.md`, `skills/README.md`, the target `SKILL.md`, the admission
decision named by `port.manifest.json`, `docs/WORKSPACE_INSTALL.md`, and the
current `aoa-skills` home-port contract.

## Boundaries

- Keep general ecosystem orientation in route cards and KAG, not in a second
  prompt-visible workspace skill.
- Keep diagnosis read-only. Repair, install, restart, projection, configuration,
  and decision mutation remain separate owner-authorized workflows.
- Do not copy shared `aoa-skills` bundles or sibling procedures into this home
  or its projection.
- Do not keep candidates, fixtures, raw trials, task-local DAGs, session notes,
  runtime state, tools, wrappers, tests, or generated read models here.
- Change canonical source first, then rebuild the exact repository projection
  through the pinned `aoa-skills` home-port contract.

## Validation

Manual no-skill, failure, negative, held-out, and coexistence tasks decide
usefulness. The pinned `aoa-skills` contract checks owner, manifest, and
byte/mode projection parity only; green output makes no behavioral claim.

## Closeout

Report the manual cases exercised, projection rebuild, prompt-visible
inspection, checks skipped, and removal of session-only fixtures.
