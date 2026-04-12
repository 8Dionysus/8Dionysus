# Codex Plane Rollout

This note defines the deployment continuity posture for the selected shared-root
Codex plane that `8Dionysus` projects into the live workspace root.

Use [CODEX_PLANE_REGENERATION.md](CODEX_PLANE_REGENERATION.md) for the
manifest/profile rerender path. Use this note for the live deployment trail
that follows render: trust, apply posture, doctor outcome, rollback posture,
and deploy-local artifacts.
Use [COMPONENT_REFRESH_ROUTE.md](COMPONENT_REFRESH_ROUTE.md) when the same
shared-root component keeps reopening rerender, doctor, or rollback pressure
and the workspace root must route that drift back to the owner repo.
Use [CODEX_TRUSTED_ROLLOUT_OPERATIONS.md](CODEX_TRUSTED_ROLLOUT_OPERATIONS.md)
for the checked-in shared-root rollout campaign history, drift windows,
rollback windows, and latest trusted rollout summary that remain source-owned in
`8Dionysus`.
Use [TRUSTED_ROLLOUT_CAMPAIGNS.md](TRUSTED_ROLLOUT_CAMPAIGNS.md) when the route
widens from one checked-in rollout history line into one recurring campaign
cadence layer with grouped drift review and rollback-followthrough windows.

## Boundary

`8Dionysus` owns the source-authored rollout doctrine and contract shapes for
the selected shared-root install subset:

- `.codex/config.toml`
- `.codex/hooks.json`
- the projected shared-root surfaces already declared in
  [WORKSPACE_INSTALL.md](WORKSPACE_INSTALL.md)

It does not widen `8Dionysus` into the owner of role meaning, MCP
implementation meaning, or deploy-local runtime outputs.

## Live phases

The rollout cycle stays explicit:

1. render
2. trust-check
3. dry-run validation
4. execute apply
5. doctor verify
6. rollback decision
7. stats refresh

Render is not rollout completion. A successful rerender only proves that the
checked-in deployment artifacts were recomputed from the source-owned
manifest/profile pair.

## Deploy-local artifacts

Preferred live outputs under the workspace root:

- `/.codex/generated/rollout/codex_plane_trust_state.current.json`
- `/.codex/generated/rollout/codex_plane_regeneration_report.latest.json`
- `/.codex/generated/rollout/codex_plane_rollout_receipt.latest.json`

These artifacts stay deploy-local. They are evidence for the current live root,
not source truth to copy back into `8Dionysus`.

## Trust state

The trust-state contract answers:

- did the expected project root resolve?
- is project config active at the current root?
- are hooks enabled and discoverable?
- are the stable MCP server names still present?

Allowed `trust_posture` values:

- `unknown`
- `root_mismatch`
- `config_inactive`
- `trusted_ready`
- `rollout_active`
- `rollback_recommended`

## Regeneration report

The regeneration report describes:

- which shared-root deployment artifacts were rendered
- which source-owned regeneration inputs were used
- whether the render posture was `dry_run`, `check`, or `execute`
- whether the stable MCP server names were preserved
- which warnings still matter before rollout

This report describes render provenance. It does not claim that the live
workspace is already healthy.

## Rollout receipt

The rollout receipt ties a live rollout attempt back to the trust-state and the
regeneration report that shaped it.

It records:

- whether apply was only simulated or actually executed
- whether doctor/verify passed, warned, or failed
- whether rollback is recommended
- whether derived stats should refresh afterward

## Precedence

When deployment signals disagree, prefer:

1. live trust-state captured at the workspace root
2. rollout receipt doctor and verify outcome
3. `aoa-sdk` typed deploy-status snapshot
4. `aoa-stats` derived deployment summary

Derived layers may summarize. They do not overrule live deployment evidence.

## Rollback posture

Rollback is recommended when:

- the detected project root is wrong
- project config is inactive after apply
- hooks cannot be discovered after apply
- required MCP server names drift
- doctor returns `fail`

A rollback recommendation should produce a fresh rollout receipt rather than
silently mutating the deployment trail.
