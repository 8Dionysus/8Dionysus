---
name: aoa-workspace-diagnose
description: "Diagnose a missing or drifting AoA workspace capability across owner source, projection, host scope, prompt visibility, configuration, transport, and owner service. Use when a fresh session lacks an expected skill, MCP, or tool, or when installed, configured, and live states disagree. Stop at the earliest evidenced break and hand repair to its owner. Do not use for general cross-repo orientation, narrow owner work, or the repair itself."
---

# AoA Workspace Diagnose

## Intent

Locate the earliest evidenced break in workspace capability delivery without
turning an installer, public route, generated report, or access plane into owner
truth.

## Contract

| Field | Value |
| --- | --- |
| identity | `aoa-workspace-diagnose`, version `0.1.0` |
| owner | `8Dionysus` public workspace-delivery lane |
| lifecycle | admitted and advertised only in `8Dionysus` repository scope |
| freedom and effects | choose the narrowest read-only evidence path inside one typed lane; never repair, install, restart, or rewrite |
| tool posture | filesystem, Git, prompt inventory, catalog, and bounded read-only runtime evidence are optional inputs, not fixed dependencies |
| relations | consume owner contracts and delivery evidence; compose with `aoa-decision` `find`; produce one typed failure or `intended_behavior` handoff |
| trust and provenance | authored owner sources and exact consumer evidence outrank KAG, summaries, caches, and reports |
| health | manual failure, negative, no-skill, and coexistence trials support admission; structural parity alone never proves behavior |
| termination | one earliest evidenced break or intended-behavior result, one owner handoff, then stop |

## Trigger boundary

Use when:

- a fresh host session is missing an expected skill, MCP, tool, or capability;
- source, generated, installed, configured, prompt-visible, and live states
  disagree;
- two visible capabilities appear to collide and their scopes must be separated
  from the primary failure.

Do not use for:

- general workspace orientation or owner mapping without a concrete symptom;
- a narrow task already bounded to one clear owner;
- direct repair, restart, installation, or configuration mutation;
- a factual lookup or a derived health report offered as system authority.

If accepted rationale is also required, compose with `aoa-decision` in `find`
mode. Keep the authored rationale and live diagnosis as separate inputs.

## Inputs

- expected capability and observed symptom;
- exact consumer scope or session when known;
- explicit workspace, owner, projection, or config paths already known;
- read-only runtime evidence already available.

Never require a raw transcript, credential, or repair permission to diagnose.

## Evidence gate

1. Accept roots and paths only when supplied explicitly, declared by the SDK or
   route card, or confirmed from the current Git common directory.
2. In a linked worktree, run `git rev-parse --git-common-dir` before path
   discovery. Inspect only the named owner, projection, and consumer scopes.
   Do not recursively search parent worktree directories, `/home`, `/srv`,
   caches, plugin stores, temporary roots, or every sibling repository.
3. For owner-law claims, name the target ref and freshness class. Prefer a
   verified `origin/main`; a dirty checkout is live evidence, not default owner
   meaning. A non-Git fixture proves only its current filesystem state.
4. If the expected capability or consumer scope cannot be established, return
   `blocked_missing_input` instead of widening the search.

## Typed diagnostic chain

First verify the **owner source**: the authored capability or procedure exists
and declares the expected behavior. Then select exactly one delivery lane.

For a **skill**:

1. verify generated or exported projection provenance and byte or contract
   parity where exactness is claimed;
2. verify materialization in the required user, workspace, or repository host
   scope; a healthy sibling projection is not a projection into this consumer;
3. inspect the real prompt inventory or explicit retrieval result; installed on
   disk does not imply model-visible.

For an **MCP or named tool**:

1. verify any required consumer wrapper or projection against its owner;
2. verify consumer configuration, enablement, and the exact stable MCP or tool
   name before interpreting prompt absence;
3. inspect the real tool catalog or prompt-visible handle;
4. use the narrowest read-only transport or process smoke; registration does
   not prove a live endpoint;
5. inspect owner service health and its source/runtime boundary only after the
   earlier layers pass.

If no declared delivery kind fits, return `blocked_missing_input`; do not invent
a generic chain. When one symptom spans skill and MCP delivery, share the owner
evidence, then inspect each typed lane only until its first causal break.

At each layer, record what passed, what failed, and which tempting explanation
that evidence disproves. Do not continue downstream after the earliest causal
break unless one bounded check is needed to disconfirm a materially different
cause.

## Collision side branch

Treat a routing collision separately from the primary delivery chain:

- distinct visible names with overlapping descriptions are a semantic routing
  collision, not a discovery failure;
- an exact-name entry hidden by precedence is a scope or host-policy question,
  not proof that either owner source is absent;
- a collision between two visible skills does not explain why a third skill is
  absent;
- do not create a decision or invoke a competing procedure merely to inspect
  its routing metadata.

## Authority order

Prefer:

1. the named owner's authored contract or procedure;
2. live evidence from the exact consumer scope;
3. deterministic projection or installed-parity evidence;
4. public routes, KAG, stats, and health summaries as navigation or derived
   evidence only.

The repository that installs or projects a capability owns that delivery
behavior. It does not acquire ownership of the projected domain procedure.

## Output ABI

Return:

- expected behavior and observed evidence;
- earliest evidenced failure layer, or `intended_behavior`;
- passed layers and disconfirmed explanations;
- exact owner and scope for the first possible change;
- shortest read-only verification;
- repair handoff or an explicit statement that no repair is justified.

## Verification and termination

Before returning, ensure that:

- owner, projection, installed, configured, prompt-visible, and live states are
  not conflated;
- every owner-law claim has a root, ref, and freshness class;
- no dependency, cache, temporary copy, or generated report became owner truth;
- the diagnosis stopped at the earliest evidenced layer;
- no mutation, restart, install, decision write, or repair was performed.

Stop after one diagnosis and one owner handoff. Any repair is a separate,
owner-authorized workflow.
