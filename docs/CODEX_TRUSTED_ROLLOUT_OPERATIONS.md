# Codex Trusted Rollout Operations

This note defines the checked-in shared-root rollout operations posture for the
Codex plane that `8Dionysus` projects into the live workspace root.

Use [CODEX_PLANE_REGENERATION.md](CODEX_PLANE_REGENERATION.md) for manifest and
profile rerender.
Use [CODEX_PLANE_ROLLOUT.md](CODEX_PLANE_ROLLOUT.md) for deploy-local trust,
doctor, and rollback posture at the current live root.
Use this note for source-owned rollout campaign history that should remain
reviewable after one live deploy-local receipt is no longer enough context.

## Boundary

`8Dionysus` owns the shared-root rollout operations history for:

- bounded rollout campaigns
- checked-in deploy history
- checked-in regeneration campaign summaries
- checked-in rollback windows
- one latest trusted rollout summary

It does not own:

- runtime-only doctor logs
- live sandbox or approval controls
- `aoa-stats` derived summaries
- `aoa-playbooks` recurring route composition
- `aoa-memo` lesson or recovery-pattern writeback
- `aoa-sdk` control-plane decisions

## Source surfaces

The checked-in rollout operations surfaces live under:

- `generated/codex/rollout/deploy_history.jsonl`
- `generated/codex/rollout/regeneration_campaigns.min.json`
- `generated/codex/rollout/rollback_windows.min.json`
- `generated/codex/rollout/rollout_latest.min.json`

These are source-owned shared-root review surfaces.
They are not deploy-local runtime output copied back from
`/.codex/generated/rollout/`.

## Stable refs

Use the compact bounded ref families:

- `rollout_campaign_ref`: `ROLL-YYYYMMDD-<slug>-NN`
- `deploy_receipt_ref`: `DEPLOY-YYYYMMDD-<slug>-NN`
- `drift_window_ref`: `DRIFT-YYYYMMDD-<slug>-NN`
- `rollback_window_ref`: `RBK-YYYYMMDD-<slug>-NN`

The suffix after the prefix should stay aligned across the related refs for one
campaign.

## Rollout lifecycle

Allowed rollout states:

- `prepared`
- `activated`
- `monitoring`
- `stabilized`
- `rollback_open`
- `rolled_back`
- `abandoned`

Allowed drift states:

- `quiet`
- `watch`
- `material`
- `repairing`
- `resolved`
- `rolled_back`

## What a checked-in campaign must keep explicit

Each campaign should keep visible:

- which bounded rollout was activated
- which deploy receipt refs belong to it
- which drift window refs belong to it
- whether bounded repair was attempted
- whether a rollback window opened
- whether the route stabilized, rolled back, or was abandoned

Do not bury drift as noise.
If drift becomes material on startup, hook discovery, MCP wiring, or shared-root
loading, name it, bound it, and either repair it or roll it back.

## Precedence

When rollout signals disagree, prefer:

1. deploy-local trust-state and deploy-local rollout receipt for the current
   root
2. checked-in trusted rollout campaign history in `generated/codex/rollout/`
3. `aoa-sdk` typed deploy status
4. `aoa-stats` derived rollout summaries
5. `aoa-memo` lessons or recovery patterns

Derived layers may summarize this route.
They do not overrule source-owned rollout history.

## Recovery posture

Bounded repair is acceptable only when the route remains reviewable and the
blast radius stays explicit.

Open a rollback window when:

- startup drift becomes material
- stable MCP name posture is no longer trustworthy
- hook or config activation drifts after the rollout move
- doctor and smoke no longer support continued monitoring

Successful rollback or repeated bounded repair may later feed derived summaries
or memoized recovery patterns, but those follow-on layers remain weaker than
the checked-in campaign history kept here.
