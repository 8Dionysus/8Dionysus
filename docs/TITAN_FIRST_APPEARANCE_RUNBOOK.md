# Titan First Appearance Runbook

## Purpose

Operate the first Titan wave from the shared Codex workspace surface.

## Names

```text
Atlas    -> architect
Sentinel -> reviewer
Mneme    -> memory-keeper
Forge    -> coder
Delta    -> evaluator
```

## First summon

```bash
codex --cd /srv "$(cat /srv/8Dionysus/.codex/prompts/titan-summon.service-cohort.v0.md)"
```

## Expected result

```text
active_roster: Atlas, Sentinel, Mneme
conditional_absent: Forge, Delta
route_frame: present
risk_gates: present
memory_posture: present
mutation_gate_status: locked
judgment_gate_status: locked
```

## Mutation route

Use this wording before Forge appears:

```text
I authorize Forge to implement a bounded mutation.
Intent: ...
Targets: ...
Prechecks: Atlas route, Sentinel risk, Mneme provenance.
Validation: ...
Rollback or stop condition: ...
```

## Judgment route

Use this wording before Delta appears:

```text
I authorize Delta to evaluate a bounded question.
Question: ...
Evidence: ...
Success criterion: ...
Output form: verdict with uncertainty and cited evidence.
```

## Hook posture

Hooks may add context at SessionStart, UserPromptSubmit, and Stop. Hooks must not silently summon the Titans. The operator summons.

## Closure

After first summon, record:

```text
summon prompt ref
active roster
conditional roster absent
route frame
risk gates
memory posture
mutation gate status
judgment gate status
validation notes
```
