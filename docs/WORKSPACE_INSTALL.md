# Workspace Install

This note explains the public workspace layout for running the AoA / ToS ecosystem as one local project.
It is an orientation surface.
The owning install logic still lives in `aoa-skills` and `aoa-sdk`.

## Canonical shape

Use one parent directory that keeps the public repositories as sibling checkouts:

```text
<workspace-root>/
  .agents/
    skills/
  8Dionysus/
  Agents-of-Abyss/
  Tree-of-Sophia/
  Dionysus/
  aoa-agents/
  aoa-evals/
  aoa-kag/
  aoa-memo/
  aoa-playbooks/
  aoa-routing/
  aoa-sdk/
  aoa-skills/
  aoa-stats/
  aoa-techniques/
```

`8Dionysus` stays the public profile and route map.
It is part of the workspace, but it does not replace the source repositories.

## Foundation install

The safest route is to use the `aoa-sdk` bootstrap command after the sibling checkouts are already present:

```bash
aoa workspace bootstrap <workspace-root> --json
aoa workspace bootstrap <workspace-root> --execute --json
```

That command checks the sibling layout, installs the shared foundation into `<workspace-root>/.agents/skills`, and writes a root-level `AGENTS.md` when one is missing.

Manual install remains available as the lower-level fallback:

Install the shared project foundation into `<workspace-root>/.agents/skills` from `aoa-skills`:

```bash
python <workspace-root>/aoa-skills/scripts/install_skill_pack.py \
  --repo-root <workspace-root>/aoa-skills \
  --profile repo-project-foundation \
  --dest-root <workspace-root>/.agents/skills \
  --mode symlink \
  --execute \
  --overwrite \
  --format json
```

Verify the result:

```bash
python <workspace-root>/aoa-skills/scripts/verify_skill_pack.py \
  --repo-root <workspace-root>/aoa-skills \
  --profile repo-project-foundation \
  --install-root <workspace-root>/.agents/skills \
  --format json
```

## Session start

Use `aoa-sdk` as the control-plane entry surface for session ingress and mutation gates:

```bash
aoa skills enter <workspace-root> --intent-text "plan a cross-repo change" --root <workspace-root> --json
aoa skills guard <repo-root> --intent-text "apply a risky mutation" --mutation-surface infra --root <workspace-root> --json
```

`aoa skills enter` persists one ingress report under `aoa-sdk/.aoa/skill-dispatch/`.
`aoa skills guard` persists one pre-mutation report there too.
When checkpoint-phase surface detection sees a real growth signal, those
commands may also append one local checkpoint note under
`aoa-sdk/.aoa/session-growth/current/`. Use `--no-auto-checkpoint` to suppress
that local note or `--checkpoint-kind` to force one explicit checkpoint event.

## Notes

- `Dionysus` is the seed garden and staging surface in the public workspace.
- `aoa-skills` owns the skill exports, install profiles, and validators.
- `aoa-sdk` owns workspace discovery, typed reads, detector/dispatcher behavior, and closeout helpers.
- `abyss-stack` is part of the ecosystem, but the current preferred source checkout remains separately managed. For its machine-readable path rules, see `aoa-sdk/docs/workspace-layout.md`.
