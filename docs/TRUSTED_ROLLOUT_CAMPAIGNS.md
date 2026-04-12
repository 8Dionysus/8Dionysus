# Codex Trusted Rollout Campaigns

This note defines the recurring campaign-cadence companion for the shared-root
Codex plane after checked-in trusted rollout operations already exist.

Use [CODEX_PLANE_ROLLOUT.md](CODEX_PLANE_ROLLOUT.md) for deploy-local trust,
doctor, and rollback posture at the current live root.
Use [CODEX_TRUSTED_ROLLOUT_OPERATIONS.md](CODEX_TRUSTED_ROLLOUT_OPERATIONS.md)
for source-owned rollout campaign history, drift windows, rollback windows,
and the latest trusted rollout summary.
Use this note for one bounded cadence layer above those rollout operations:
campaign windows, drift-review windows, and rollback-followthrough windows.

## Boundary

`8Dionysus` owns the source-authored cadence doctrine and example windows for:

- `rollout_campaign_window`
- `drift_review_window`
- `rollback_followthrough_window`

It does not own:

- live rollout mutation execution
- scheduler authority
- `aoa-playbooks` scenario composition authority
- `aoa-stats` derived cadence summaries
- `aoa-memo` bounded cadence recall objects
- `aoa-sdk` typed control-plane interpretation

## Stable refs

Use bounded ref families:

- `campaign_ref`: `CAMP-YYYYMMDD-<slug>-NN`
- `review_ref`: `DREV-YYYYMMDD-<slug>-NN`
- `rollback_ref`: `RFU-YYYYMMDD-<slug>-NN`

These refs may point back to the underlying trusted rollout refs already kept
under `generated/codex/rollout/`.

## Core objects

### `rollout_campaign_window`

Use this when grouped shared-root rollout or regeneration work should stay
explicit across one bounded review window.

Keep visible:

- the workspace root and plane
- the grouped rollout refs in scope
- cadence policy and next review due time
- whether the campaign is still open, paused, closed, or review-required
- optional lineage refs when a stronger upstream owner chain already exists

### `drift_review_window`

Use this when campaign drift needs one reviewable decision surface rather than
being narrated informally.

Keep visible:

- named drift signals
- evidence refs
- the review decision
- the rollback or reanchor anchor when one matters

### `rollback_followthrough_window`

Use this when rollback remains contingent but the follow-through boundary
should stay explicit before the route widens again.

Keep visible:

- the rollback anchor
- trigger conditions
- bounded path scope
- whether post-rollback review remains required

## Minimal flow

`rollout_campaign_window -> drift_review_window -> rollback_followthrough_window? -> derived summary refresh -> bounded memo writeback`

Rollback remains optional and contingent.

## Stop lines

Stop and return to review when:

- campaign scope stops being bounded
- drift signals are named without evidence
- rollback starts being treated as convenience instead of contingency
- a cadence window starts acting like a scheduler
- stats, memo, or sdk layers are asked to speak stronger than source-owned
  rollout and cadence surfaces

## Precedence

When cadence signals disagree, prefer:

1. deploy-local trust-state and rollout receipt for the current root
2. checked-in trusted rollout history in `generated/codex/rollout/`
3. source-owned cadence windows in `examples/*.example.json`
4. `aoa-sdk` typed pass-through refs
5. `aoa-stats` derived cadence summaries
6. `aoa-memo` lessons or recovery patterns

Cadence windows are source-owned review surfaces.
They do not become a scheduler, hidden runner, or second playbook.
