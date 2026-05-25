# Runtime Example

## Scenario

A live session corrected an owner-route mistake. The final commit only shows a
clean documentation update, but the reason the system should remember the
correction lives in `.aoa` search hits and source refs from the owner repo.

## Why this skill fits

The route needs a writeback decision before the session is lost, but raw
session history is still evidence rather than reviewed memory. The skill keeps
the durable-memory boundary visible while allowing a local memo candidate or
reviewed-intake export to be prepared through the owner repo.

## Expected inputs

- owner repo
- one bounded memory question
- `.aoa` evidence refs
- owner source refs
- local `memo/` port status
- review posture for candidate or export promotion

## Expected outputs

- `memo_writeback_decision=write_candidate`
- one local memo candidate under the owner repo's memo port
- source refs and `.aoa` evidence refs
- review-required guardrails
- local port validation result
- explicit stop before durable reviewed `aoa-memo` landing

## Boundary notes

- Do not write central `aoa-memo` objects directly from the live session.
- Do not use raw transcript text as reviewed memory.
- Do not create a candidate when the task is only `.aoa` hook repair,
  preservation, retrieval, or indexing.

## Verification notes

- Confirm the owner repo and stronger owner route are named.
- Confirm source refs and evidence refs support one bounded claim.
- Confirm the local memo port exists before writing a candidate.
- Confirm the candidate marks durable promotion as review-required.
- Confirm closeout names what stayed local and where durable review would
  happen.
