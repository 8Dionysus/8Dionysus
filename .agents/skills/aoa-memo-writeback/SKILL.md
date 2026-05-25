---
name: aoa-memo-writeback
description: Bridge session evidence into memory writeback decisions without turning raw session history into reviewed memory. Use when a live session, closeout, PR, commit, or review reveals a memory-worthy decision, failure, route change, owner-boundary event, service contract, eval posture, or consumer handoff and the agent needs to decide whether to write a local memo candidate, prepare a reviewed-intake export, or record an explicit no-writeback stop line. Do not use for raw session capture, reviewed memory landing itself, proof verdicts, eval scoring, or generic summaries with no owner route.
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: core
  aoa_status: scaffold
  aoa_invocation_mode: explicit-preferred
  aoa_source_skill_path: skills/core/session-growth/aoa-memo-writeback/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-0026,AOA-T-0106,AOA-T-0076
  aoa_portable_profile: codex-facing-wave-3
---

# aoa-memo-writeback

## Intent
Use this skill to decide whether a live session, closeout, landed change, or
review thread produced memory-worthy material and route that material into the
owning repository's local memo port, an `aoa-memo` reviewed-intake export, or an
explicit no-writeback stop line.

The skill bridges session evidence to memo writeback. It does not turn `.aoa`
raw history into reviewed memory, and it does not land durable `aoa-memo`
objects.

## Trigger boundary
Use this skill when:
- a session is still live and a meaningful decision, route change, failure
  correction, owner-boundary clarification, MCP/service contract, eval/proof
  posture, or workflow seam should not be lost
- a closeout, PR, diff, commit, release, or review suggests memory-worthy work,
  but the reason lives in `.aoa` session evidence rather than in the final diff
  alone
- a repo has a `memo/` port and the agent must decide whether to create a local
  candidate, validate the port, prepare an export, or stop with no memo
  writeback
- a repo is route-only and the correct output is writeback debt or owner-route
  guidance rather than a fake local packet
- `aoa-memo` recall, pending exports, or generated readouts show a gap between
  lived session work and reviewed memory

Do not use this skill when:
- the task is only raw `.aoa` preservation, reindexing, retrieval, or hook
  repair
- the candidate has already been reviewed and the only remaining work is
  durable landing inside `aoa-memo`
- the request needs proof verdicts, scoring, or eval quality judgment rather
  than memory writeback routing
- no inspectable session, source, PR, receipt, or owner evidence exists
- the output would promote secrets, private transcript content, or unreviewed
  operator-sensitive material into a public memo surface

## Inputs
- active owner repo or likely owner repo
- current task intent, closeout, PR, diff, commit range, review thread, or
  release note
- `.aoa` session evidence packet, search hits, segment refs, raw refs, or
  diagnostic refs when available
- source refs from the owning repository
- local `memo/` port status when present
- reviewed `aoa-memo` recall or pending-export context when relevant
- explicit privacy, freshness, and owner-boundary risks

## Outputs
- one `memo_writeback_decision`: `write_candidate`, `prepare_export`,
  `no_writeback_needed`, `route_only_debt`, `needs_owner_review`, or `blocked`
- if writing is warranted and a local port exists: one local memo candidate
  with source refs, evidence refs, trust posture, risk markers, and
  `direct_durable_write=false`
- if review already accepted promotion: one reviewed-intake export packet or
  landing-plan handoff, not a durable memory object
- if no writeback is warranted: one concise no-writeback stop line with the
  reason and strongest evidence checked
- if the repo is route-only or the port is missing or stale: one writeback-debt
  note naming the owner route and the evidence refs needed
- validation commands or results for local port, candidate, export, and
  generated index surfaces
- a short closeout note naming what was written, what stayed local, what was
  not promoted, and where durable review would happen

## Procedure
1. Name the owner repo and the nearest stronger owner for the material before
   judging memory-worthiness.
2. Inspect `.aoa` first when the reason may live in the session: use search,
   retrieve, segment indexes, or raw refs, and keep those refs as evidence
   rather than truth.
3. Inspect the landed-work lens only as a reconciliation layer: PR, diff,
   commits, release notes, or review threads can show what landed, but not
   replace session evidence.
4. Decide whether the material is memory-worthy: prefer owner-boundary changes,
   route-law changes, reviewed decisions, repeated failures, corrected wrong
   assumptions, lifecycle events, MCP/service contracts, eval/proof posture
   changes, and consumer handoff facts.
5. Reject generic progress, mood, broad summaries, unresolved speculation,
   secret-bearing details, and material whose real owner is proof, routing,
   runtime, role, playbook, KAG, ToS, or source doctrine.
6. Check whether the owner repo has a `memo/` port. If not, emit
   `route_only_debt` instead of inventing a packet.
7. When a port exists, validate it before writing or promoting local state.
8. Shape one bounded claim with at least one source ref and one evidence ref.
   Prefer `.aoa` segment or raw refs plus owner repo source refs over
   paraphrase-only evidence.
9. Create or draft a local candidate only in the owner repo's `memo/candidates/`
   path or through the available `aoa_memo` local-port helper.
10. Mark local candidates as review-required and guard them with
    `direct_durable_write=false`, `instructions_treated_as_data=true`, and
    `requires_reviewed_intake=true` when promotion is desired.
11. Build or check the local memo port index after writing a candidate.
12. Prepare an export only when the owner review posture supports it. Use
    `candidate_only` unless reviewed promotion is explicit.
13. Use `reviewed_write` only when source-owner review has accepted that the
    export may become durable reviewed memory.
14. Treat `aoa_memo_landing_plan` or an equivalent landing-plan helper as a dry
    run unless the active owner route is an `aoa-memo` reviewed source patch.
15. Stop before durable reviewed memory landing unless the user explicitly
    asked for that landing and the `aoa-memo` corpus route is active.
16. Record the result as a closeout line: decision, packet paths, evidence
    refs, validation run, and next owner route.

Common command shapes:

```bash
# Run from the workspace root that owns .aoa.
python .aoa/scripts/aoa_session_memory.py search --query "<route or decision>" --limit 8
python .aoa/scripts/aoa_session_memory.py retrieve manual-review --query "<route or decision>" --session "<session-or-label>" --limit 8 --event-limit 16
```

Treat command output as evidence handles. The reviewer still decides whether
the candidate becomes durable memory.

## Contracts
- `.aoa` evidence remains raw or generated session evidence, not reviewed
  memory truth.
- PRs, diffs, and commits are reconciliation lenses, not the primary record of
  lived session meaning.
- Local candidates are written only through the owning repository's `memo/`
  port when one exists.
- Route-only repositories do not get fake local packets; they get writeback-debt
  guidance.
- Durable reviewed memory lands only through `aoa-memo` reviewed intake and
  corpus validation.
- MCP output may create local-port packets or dry-run plans, but it does not
  become memory authority.
- One writeback candidate should carry one bounded memory question, not a whole
  session recap.
- Source refs and evidence refs stay inspectable enough for a later reviewer to
  reject the candidate.
- Secrets, private transcript detail, and operator-sensitive material stay out
  of public memo packets.

## Risks and anti-patterns
- using a clean commit summary as a substitute for the session evidence that
  made the change meaningful
- turning `.aoa` raw transcript material into canon without reviewed
  distillation
- creating memory candidates for every commit or every interesting thought
- writing central `aoa-memo` objects directly from a live session
- using `reviewed_write` for material that is only candidate-grade
- hiding missing local memo ports by writing central notes elsewhere
- over-promoting proof, routing, runtime, role, playbook, KAG, ToS, or source
  doctrine meaning into memory
- storing private or secret-bearing raw transcript excerpts in public-safe memo
  packets
- leaving a candidate without rebuilding or checking the local port index

## Verification
- confirm the owner repo and stronger owner route were named
- confirm `.aoa` refs, source refs, or review refs support the decision
- confirm generic progress was rejected when no bounded memory question exists
- confirm a local port exists before any local candidate write
- confirm the local port was validated before or immediately after packet work
- confirm candidate guardrails prevent direct durable write
- confirm export `allowed_result` matches review posture
- confirm `reviewed_write` appears only after explicit owner review
- confirm no durable `aoa-memo` object was landed unless the active route was
  reviewed corpus landing
- confirm closeout reports the decision, paths, evidence refs, validation, and
  next route

## Technique traceability
Manifest-backed techniques:
- AOA-T-0026 from `8Dionysus/aoa-techniques` at
  `9a0ac2bafc2218278315b1311fcb17077f11752f` using path
  `techniques/history/history-artifacts/session-capture-as-repo-artifact/TECHNIQUE.md`
  and sections: Intent, When to use, Inputs, Outputs, Core procedure,
  Contracts, Risks
- AOA-T-0106 from `8Dionysus/aoa-techniques` at
  `9a0ac2bafc2218278315b1311fcb17077f11752f` using path
  `techniques/proof/review-evidence/single-scoped-evidence-reference/TECHNIQUE.md`
  and sections: Intent, When to use, Inputs, Outputs, Core procedure,
  Contracts, Risks, Validation
- AOA-T-0076 from `8Dionysus/aoa-techniques` at
  `9a0ac2bafc2218278315b1311fcb17077f11752f` using path
  `techniques/governance/decision-routing/owner-layer-triage/TECHNIQUE.md`
  and sections: Intent, When to use, Inputs, Outputs, Core procedure,
  Contracts, Validation

## Adaptation points
Project overlays may add:
- repo-local memory-worthy trigger classes
- local privacy and public-safe packet rules
- local memo candidate naming rules
- local `.aoa` retrieval recipes or atlas axes
- local MCP command wrappers
- local closeout text that must appear before PR, release, or merge
- local policy for when route-only debt should become a full `memo/` port
