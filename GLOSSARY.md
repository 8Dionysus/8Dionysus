# Glossary

This glossary defines the working vocabulary used across my profile repository and the public AoA/ToS ecosystem.

It exists to make the system easier to read for humans, smaller models, and new contributors.
The goal is not to inflate terminology. The goal is to keep boundaries, roles, and relationships legible.

## Core directions

### Agents of Abyss (AoA)
An evolving operational federation for long-horizon agentic systems.

AoA is the operational and agentic side of the broader system.
It is organized as a federation of explicit layers rather than one monolith.

Its current public layers include practice, execution, proof, routing, memory, agent roles, scenario composition, and derived knowledge substrate work, with `abyss-stack` beneath the system and `Tree-of-Sophia` as the source-first knowledge architecture counterpart.

### Tree of Sophia (ToS)
A source-first living knowledge architecture for philosophy and world thought.

ToS is the knowledge world and long-horizon meaning architecture that AoA helps build, maintain, navigate, validate, and extend.

### abyss-stack
The modular local and hybrid AI infrastructure substrate beneath AoA and ToS.

It owns runtime, deployment, storage, service composition, and operational posture.
It does not own the authored meaning of the specialized AoA layers.

### ATM10-Agent
A private multimodal companion project in development.

It is separate from the public AoA layer repositories, but related in long-horizon direction.

## Ecosystem structure

### Ecosystem center
A repository that keeps ecosystem-level truth clear.

In the current public AoA surface, this role belongs to `Agents-of-Abyss`.
It owns the charter, layer map, federation rules, and program-level direction.

### Layer
A distinct functional surface in the ecosystem with its own role, boundaries, and ownership.

A good layer answers one main kind of question clearly and avoids silently absorbing neighboring roles.

### Federation
A modular ecosystem made of explicit layers with clear ownership boundaries.

AoA is intended to grow as a federation rather than collapse into a single swollen repository.

### Source of truth
The repository or artifact that authoritatively owns a specific kind of meaning.

The source of truth should remain explicit.
Coordination layers should not quietly replace source repositories.

### Coordination repository
A repository that helps readers or systems navigate across layers without owning all primary meaning itself.

`Agents-of-Abyss` and `aoa-routing` are coordination-oriented surfaces, but with different jobs.

## Public AoA layers

### Practice canon
The layer that stores reusable engineering practice.

In the current public ecosystem, this role belongs to `aoa-techniques`.
A technique is treated as a minimal reproducible unit of engineering practice.

### Execution canon
The layer that stores bounded agent-facing workflows.

In the current public ecosystem, this role belongs to `aoa-skills`.
A skill packages one or more techniques into a reviewable execution workflow.

### Proof canon
The layer that stores portable evaluation bundles for bounded claims.

In the current public ecosystem, this role belongs to `aoa-evals`.
It exists to make claims about agent quality, behavior, boundaries, or regressions reviewable and defensible.

### Navigation layer
The layer that helps models and humans decide where to go next.

In the current public ecosystem, this role belongs to `aoa-routing`.
It should own navigation and dispatch surfaces, not the primary meaning of other repositories.

### Memory layer
The layer that owns explicit memory and recall surfaces.

In the current public ecosystem, this role belongs to `aoa-memo`.
It is meant to keep memory reviewable, provenance-aware, and distinct from proof.

### Role and persona layer
The layer that defines explicit agent roles, contracts, and handoff posture.

In the current public ecosystem, this role belongs to `aoa-agents`.
An agent is not a skill. An agent is a role-bearing actor that uses skills.

### Scenario and composition layer
The layer that stores recurring operational recipes across multiple surfaces.

In the current public ecosystem, this role belongs to `aoa-playbooks`.
A playbook is not a single skill. It is a higher-level scenario composition.

### Derived knowledge substrate layer
The layer that stores derived, provenance-aware, knowledge-ready structures.

In the current public ecosystem, this role belongs to `aoa-kag`.
It is not the primary source of authored meaning. It is the derived substrate built from authoritative sources.

### Infrastructure substrate
The layer that provides the runtime body of the system.

In the current public ecosystem, this role belongs to `abyss-stack`.
It supports AoA and ToS without replacing their authored meaning.

## Working vocabulary

### Technique
A minimal reproducible unit of engineering practice.

A technique should have clear intent, usage boundaries, validation posture, and adaptation notes.
It is more durable than a one-off fix or isolated snippet.

### Skill
A bounded agent-facing execution workflow.

A skill usually depends on one or more techniques and packages them into an operational interface for an agent or human.

### Eval
A portable proof surface for a bounded claim.

An eval should make its scope, object under evaluation, scoring or verdict logic, and blind spots explicit.

### Playbook
A scenario-shaped operational recipe that coordinates multiple surfaces.

A playbook may compose agents, skills, memory posture, evaluation posture, and fallback paths.

### Memory object
An explicit, reviewable unit of memory.

A memory object should not silently impersonate proof or source truth.
It should preserve provenance and temporal context where possible.

### Agent profile
A compact description of an actor's role, boundaries, preferred skills, memory posture, and handoff posture.

An agent profile exists to replace vague role folklore with explicit contracts.

### Registry
A compact machine-readable surface that names and normalizes a repository's public objects.

A registry is not the whole meaning of a repo.
It is a smaller structured surface for validation, routing, or indexing.

### Capsule
A compact derived summary surface for local lookup or routing.

Capsules are meant to reduce context load while preserving a path back to authoritative material.

### Generated surface
A derived artifact built from authoritative source files.

Generated surfaces improve navigation, indexing, or local runtime use, but they should not silently replace the source of truth.

### Provenance
Visible linkage back to origin.

In this ecosystem, provenance matters because memory, routing, KAG, and evaluation surfaces should stay tied to where their meaning came from.

## Quality and operating principles

### Bounded
Deliberately limited in scope.

A bounded workflow, bundle, or claim names what it covers and what it does not cover.
This reduces confusion and prevents hidden widening of authority.

### Reviewable
Open to structured human or agent inspection.

A reviewable surface should make its assumptions, boundaries, and artifacts visible rather than hiding them inside opaque automation.

### Reproducible
Capable of being repeated with the same core method or contract.

Reproducibility matters more than demo theater.
A strong public surface should survive reuse beyond one private moment.

### Legible
Easy to read as a system, not just as an isolated artifact.

Legibility matters at both human and agent scales.
It is one of the main design goals across AoA.

### Portable
Usable across more than one local context or project without losing its core meaning.

Portability does not mean universal abstraction.
It means a surface can travel without depending on hidden private assumptions.

### Public-safe
Clean enough for public release.

A public-safe artifact excludes secrets, private operational risk, and project-local assumptions that were not properly sanitized.

### Canonical
Recommended by default after stronger validation, reuse evidence, and clearer default-use rationale.

Canonical status should remain meaningful rather than becoming a decorative label.

### Promoted
Publicly accepted as reusable, but not yet the default choice.

Promotion signals readiness for public use while leaving room for future strengthening.

### Evaluated
Supported by some explicit evidence or review surface.

Evaluation is stronger than intuition, but it is not the same thing as final certainty.

## Architectural distinctions

### Human meaning, agent acceleration
A core design principle across the ecosystem.

Humans should remain able to understand why a system is structured the way it is.
Agents should benefit from explicit layers, reusable workflows, and smaller derived surfaces.

### Modular growth
The practice of adding new capability as a clear layer or module.

This is preferred over brittle fusion, accidental monoliths, or hidden sprawl.

### Handoff
The explicit transfer of work, context, or responsibility between roles or layers.

Good handoff posture reduces ambiguity and keeps authority boundaries visible.

### Memory posture
The declared way an agent or workflow should interact with memory surfaces.

A good memory posture names whether memory is required, optional, bounded, or restricted.

### Evaluation posture
The declared way an agent, workflow, or playbook relates to proof and verification.

A good evaluation posture names what should be checked, how strongly, and under which limits.

## Reading paths

If you want the shortest route into the ecosystem:

- for the ecosystem center and map, start with [`Agents-of-Abyss`](https://github.com/8Dionysus/Agents-of-Abyss)
- for the knowledge world, start with [`Tree-of-Sophia`](https://github.com/8Dionysus/Tree-of-Sophia)
- for reusable practice, go to [`aoa-techniques`](https://github.com/8Dionysus/aoa-techniques)
- for bounded execution workflows, go to [`aoa-skills`](https://github.com/8Dionysus/aoa-skills)
- for portable proof surfaces, go to [`aoa-evals`](https://github.com/8Dionysus/aoa-evals)
- for navigation and dispatch, go to [`aoa-routing`](https://github.com/8Dionysus/aoa-routing)
- for memory and recall, go to [`aoa-memo`](https://github.com/8Dionysus/aoa-memo)
- for explicit agent roles, go to [`aoa-agents`](https://github.com/8Dionysus/aoa-agents)
- for recurring scenario recipes, go to [`aoa-playbooks`](https://github.com/8Dionysus/aoa-playbooks)
- for derived knowledge substrate surfaces, go to [`aoa-kag`](https://github.com/8Dionysus/aoa-kag)
- for the runtime body, go to [`abyss-stack`](https://github.com/8Dionysus/abyss-stack)

## Scope note

This glossary is a public orientation surface.
It is not a replacement for the charters, roadmaps, validation contracts, or deeper repository-specific documentation.
