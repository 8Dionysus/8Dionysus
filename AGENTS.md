# AGENTS.md — /srv workspace

## Purpose

`/srv` is the editable federation workspace root.
Treat it as the sibling-parent directory for the public AoA / ToS repositories, not as the source of truth for any one layer.

## Read first

1. `/srv/8Dionysus/README.md`
2. `/srv/8Dionysus/GLOSSARY.md`
3. the target repository's own `README.md` and `AGENTS.md`

## Session start

For every new session started from `/srv`, before substantial work:

1. choose the primary `repo_root`
2. run one ingress pass

```bash
aoa skills enter <repo_root> --root /srv --intent-text "<short task summary>" --json
```

If the task is truly cross-repo and no single owner repo is primary yet, use `/srv` as `repo_root`.

## Mutation gate

Before risky, mutating, infra, runtime, repo-config, or public-share actions, run:

```bash
aoa skills guard <repo_root> --root /srv --intent-text "<planned change>" --mutation-surface <code|repo-config|infra|runtime|public-share> --json
```

Do not silently skip `must_confirm` or `blocked_actions`.

## Additive surface detection

Keep `aoa skills enter` and `aoa skills guard` as the primary workspace-level
ingress and mutation gate. They stay skill-only.

When the active task shows route drift, owner-layer ambiguity, proof need,
recall need, role posture questions, or recurring-scenario signals, run one
additive surface pass for the chosen `repo_root`:

```bash
aoa surfaces detect <repo_root> --root /srv --phase ingress --intent-text "<surface-aware task summary>" --json
```

Use `--phase pre-mutation` and the same `mutation_surface` when the signal
appears during a risky change:

```bash
aoa surfaces detect <repo_root> --root /srv --phase pre-mutation --intent-text "<surface-aware task summary>" --mutation-surface <code|repo-config|infra|runtime|public-share> --json
```

Truth rules:

- `aoa skills ...` remains skill-only
- `aoa surfaces detect` is additive and read-only
- non-skill surfaces are hints, candidates, or reviewed closeout handoffs, not
  executable-now runtime objects
- if the chosen repository has its own `AGENTS.md`, follow its narrower
  surface-detection guidance after this root-level trigger fires

## Workspace posture

- `/srv/.agents/skills` is the shared project-foundation install.
- `/srv/8Dionysus` is the public profile and route map.
- `/srv/Dionysus` is the seed garden and staging surface.
- source repositories live as sibling checkouts under `/srv`.
- `abyss-stack` is part of the ecosystem, but its preferred source checkout may still live outside `/srv`; respect `aoa-sdk` workspace discovery and overrides.

## Workflow

`INGRESS -> READ -> DIFF -> VERIFY -> REPORT`
