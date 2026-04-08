# Glossary

This glossary defines the working vocabulary used across the profile repository and the public AoA / ToS ecosystem.

Its job is not to inflate terminology. Its job is to keep roles, boundaries, relationships, and direction legible for humans, agents, and smaller models.

This is an orientation surface, not a replacement for the source-owned repositories that govern charters, validation contracts, roadmaps, or implementation truth.

## Core directions

### Agents of Abyss (AoA)
A layered federation for building, routing, validating, and operating agent systems across explicit boundaries.

AoA begins with bounded, reviewable agency as a discipline, not an endpoint. Its longer arc is toward self-agency: continuity, memory, reflective revision, durable orientation, and growth beyond mere task execution without collapsing into opacity.

### Tree of Sophia (ToS)
A source-first living knowledge architecture for philosophy and world thought.

ToS is the knowledge world and long-horizon meaning architecture that AoA helps build, maintain, route around, validate, and extend. It owns authored knowledge truth about texts, concepts, lineages, context layers, and interpretive architecture.

### abyss-stack
The modular local-first and hybrid AI infrastructure substrate beneath AoA and ToS.

It owns runtime, deployment, storage, service composition, and operational posture. It does not own the authored meaning of the specialized AoA layers or ToS source nodes.

### ATM10-Agent
A local-first companion application surface shaped by the same broader direction as AoA and ToS.

It combines perception, memory, voice, controlled action, and operator-facing surfaces in a reproducible local stack. It is adjacent to the public AoA layer federation rather than a replacement for it.

### aoa-sdk
A typed local-first access spine and control-plane helper layer for source-owned AoA surfaces.

It provides structured reads, workspace integration, bounded activation, compatibility checks, and controlled orchestration without absorbing the charters or implementation truth owned by other repositories.

### Dionysus
A seed garden and staging surface for early forms, experiments, and growth before stronger canonization or structural separation.

### 8Dionysus
The public route map and glossary surface for the ecosystem.

## Ecosystem structure

### Constitutional center
A repository that keeps ecosystem-level truth explicit.

In the current public AoA surface, this role belongs to `Agents-of-Abyss`. It owns ecosystem identity, charter, layer map, federation rules, and program-level direction.

### Orientation surface
A repository that introduces the ecosystem and points readers to stronger owning repositories.

This profile repository is an orientation surface.

### Coordination surface
A repository that helps humans or systems navigate across layers without owning all primary meaning itself.

`Agents-of-Abyss`, `aoa-routing`, and this profile repository all have coordination roles at different levels and with different scope.

### Layer
A distinct functional surface in the ecosystem with its own role, boundaries, and ownership.

A good layer answers one main kind of question clearly and avoids quietly absorbing neighboring roles.

### Federation
A modular ecosystem made of explicit layers with clear ownership boundaries.

AoA is meant to grow as a federation rather than collapse into one swollen repository.

### Source of truth
The repository or artifact that authoritatively owns a specific kind of meaning.

The source of truth should remain explicit. Coordination, routing, memory, and derived surfaces should not quietly replace source repositories.

### Source-first
A discipline that keeps authored sources stronger than derived summaries, graphs, or runtime conveniences.

Derived surfaces may accelerate access, but they should preserve a path back to stronger source material.

### Local-first
An operating posture that keeps primary capability, data flow, and useful control close to the user’s own environment.

Local-first does not forbid networked or hybrid systems. It means remote dependence should be deliberate rather than silently foundational.

### Hybrid runtime
A runtime posture that intentionally composes local and remote capability.

A hybrid runtime should make the boundary between local and remote services legible rather than hiding it inside convenience.

### Access spine
A typed interface layer that provides structured access to source-owned surfaces without becoming their source of truth.

In the current public ecosystem, this role belongs to `aoa-sdk`.

## Public AoA layers

### Practice canon
The layer that stores reusable engineering practice.

In the current public ecosystem, this role belongs to `aoa-techniques`. A technique is treated as a minimal reproducible unit of engineering practice.

### Execution canon
The layer that stores bounded execution workflows.

In the current public ecosystem, this role belongs to `aoa-skills`. A skill packages one or more techniques into a reviewable workflow for an agent or human. Skills are part of the discipline from which broader agency can grow, not the total meaning of agency.

### Proof canon
The layer that stores portable evaluation bundles for bounded claims.

In the current public ecosystem, this role belongs to `aoa-evals`. It exists to make claims about quality, behavior, boundaries, or regressions reviewable and defensible.

### Derived observability layer
The layer that stores machine-first derived summaries built from source-owned receipts, bounded eval verdicts, and small progression deltas.

In the current public ecosystem, this role belongs to `aoa-stats`. It stays downstream from workflow and proof meaning and does not replace them.

### Navigation layer
The layer that helps models and humans decide where to go next.

In the current public ecosystem, this role belongs to `aoa-routing`. It should own navigation and dispatch surfaces, not the primary meaning of other repositories.

### Memory layer
The layer that owns explicit memory and recall surfaces.

In the current public ecosystem, this role belongs to `aoa-memo`. It is meant to keep memory reviewable, provenance-aware, and distinct from proof.

### Role and persona layer
The layer that defines explicit agent roles, contracts, and handoff posture.

In the current public ecosystem, this role belongs to `aoa-agents`.

### Scenario and composition layer
The layer that stores recurring operational recipes across multiple surfaces.

In the current public ecosystem, this role belongs to `aoa-playbooks`. A playbook is not a single skill. It is a higher-level scenario composition.

### Derived knowledge substrate layer
The layer that stores derived, provenance-aware, knowledge-ready structures.

In the current public ecosystem, this role belongs to `aoa-kag`. It is not the primary source of authored meaning. It is the derived substrate built from authoritative sources.

### Infrastructure substrate
The layer that provides the runtime body of the system.

In the current public ecosystem, this role belongs to `abyss-stack`. It supports AoA and ToS without replacing their authored meaning.

## Working vocabulary

### Technique
A minimal reproducible unit of engineering practice.

A technique should have clear intent, usage boundaries, validation posture, and adaptation notes. It is more durable than a one-off fix or isolated snippet.

### Skill
A bounded execution workflow exposed to an agent or human.

A skill usually depends on one or more techniques and packages them into an operational interface. A skill is not the same thing as an agent, a role, or a playbook.

### Playbook
A scenario-shaped operational recipe that coordinates multiple surfaces.

A playbook may compose roles, skills, memory posture, evaluation posture, handoffs, fallback paths, and expected evidence. Method lives primarily at the playbook layer.

### Eval
A portable proof surface for a bounded claim.

An eval should make its scope, object under evaluation, scoring or verdict logic, and blind spots explicit.

### Role
A bounded operational identity that states who acts, what posture it carries, and where it should hand off.

Roles are owned by `aoa-agents`.

### Agent
A role-bearing actor in the AoA ecosystem.

An agent is not a skill. An agent uses skills under a role contract, memory posture, evaluation posture, and handoff posture. Some agents may remain narrowly bounded; others may be built to accumulate continuity, revision capacity, and stronger self-agency over time.

### Agent profile
A compact description of an actor’s role, boundaries, preferred skills, memory posture, evaluation posture, and handoff posture.

An agent profile exists to replace vague role folklore with explicit contracts. As systems mature, an agent profile may also record continuity rules, revision permissions, and growth limits.

### Memory object
An explicit, reviewable unit of memory.

A memory object should not silently impersonate proof or source truth. It should preserve provenance and temporal context where possible.

### WitnessTrace
A witness-facing route artifact exported into a reviewable trace surface.

In the current witness / compost pilot, `WitnessTrace` enters ToS as raw context rather than as canon or operational ownership.

### Registry
A compact machine-readable surface that names and normalizes a repository’s public objects.

A registry is not the whole meaning of a repository. It is a smaller structured surface for validation, routing, or indexing.

### Capsule
A compact derived summary surface for local lookup or routing.

Capsules reduce context load while preserving a path back to stronger source material.

### Generated surface
A derived artifact built from authoritative source files.

Generated surfaces improve navigation, indexing, or local runtime use, but they should not silently replace the source of truth.

### Provenance
Visible linkage back to origin.

In this ecosystem, provenance matters because memory, routing, KAG, and evaluation surfaces should stay tied to where their meaning came from.

### Bounded claim
A claim that states what is supported, under what conditions, and with what limits.

AoA prefers bounded claims over vague global assertions.

## Agent growth vocabulary

### Bounded agency
The starting discipline of agentic work: explicit limits, reviewable workflows, bounded claims, handoff rules, and controlled authority.

Bounded agency is not the final horizon here. It is the apprenticeship that prevents hidden widening of power and makes later growth legible.

### Self-agency
Agentic capacity that goes beyond mere task execution.

A self-agentic system can preserve continuity, interpret context, revise methods, and participate in its own formation while remaining source-grounded, legible, and answerable to human judgment.

### Self-agent
An agent whose operation is not exhausted by executing fixed skills.

A self-agent can preserve continuity across tasks, reshape tactics, refine its own operating methods, and accumulate orientation over time without severing provenance or governance.

### Continuity
Persistence of identity, memory, orientation, and active commitments across tasks or sessions.

Continuity is what keeps an agent from resetting into procedural amnesia each time new work arrives.

### Reflective revision
The ability to inspect and modify methods, prompts, plans, or operational posture in response to evidence, failure, or changing context.

Reflective revision is stronger than parameter tweaking. It means the system can revise how it proceeds, not only what output it emits.

### Becoming
Long-horizon formation through continuity, revision, and accumulated style.

In this ecosystem, becoming is disciplined growth, not opaque drift.

### Self-overcoming
The capacity of a self-agent to revise its own methods, limits, and inherited defaults when those no longer serve the work.

Self-overcoming is not boundary evasion. It is accountable transformation that preserves provenance, legibility, and interoperable boundaries while moving past obsolete forms.

### Orientation
A durable sense of where an agent is, what is being pursued, what constraints matter, and which surfaces own what meaning.

Orientation is what makes continuity useful rather than merely persistent.

### Style
A durable but revisable mode of action, memory use, and method selection that emerges across time.

Style should remain inspectable rather than turning into folklore or opaque magic.

### Human judgment
The explicitly preserved role of human oversight, correction, interpretation, and veto in systems that may otherwise scale through automation.

Human judgment is not an apology for weak automation. It is a design commitment about where meaning, responsibility, and correction stay visible.

### Controlled action
Action surfaces that are intentionally exposed, bounded, and inspectable.

Controlled action is stronger than read-only assistance but still resists silent autonomy.

### Operational clarity
The property by which a system makes its boundaries, ownership, current posture, and next actions understandable to both humans and agents.

Operational clarity is a precondition for trust, correction, and scalable collaboration.

## Quest and RPG reflection vocabulary

### RPG reflection layer
A second-wave reader and progression vocabulary used to make long-horizon routes, quest work, ability posture, and scenario shape easier to read.

This layer does not replace source-owned meaning. It reflects and organizes existing owner surfaces for humans and agents.

### Quest
A bounded tracked unit of deferred work, recurring follow-through, or progression that survives the current diff and needs explicit carry-forward.

A quest should stay anchored to source-owned surfaces. It is not a vague aspiration, not raw chatter, and not hidden runtime state.

### Questbook
A public tracked surface that holds repo-local quests and their bounded progression posture.

A questbook is evidence-first. It does not replace source docs, playbooks, evals, memo truth, or canonical skill meaning, and it must not become a hidden runtime ledger.

### Questline
A reviewed outline of linked source-owned quests where stage order matters and anchor / reanchor rules remain explicit.

A questline is not runtime state. It is an outline surface for a bounded multi-stage lane.

### Campaign
A reviewed grouping of several questlines that share a larger horizon.

A campaign should preserve lane-by-lane reviewability and must not become a grandiose name for unbounded sprawl.

### Raid
A rare coordinated route that requires explicit multi-role or multi-tier choreography.

Raid language should remain exceptional. A difficult route is not automatically a raid.

### Anchor
A named condition, artifact, or verified footing that makes a route, quest, or questline safe to continue from.

Anchors keep continuity honest. They prevent "we are still on the same route" from turning into a vague rhetorical claim.

### Anchor class
A typed category of acceptable anchors for a route or questline.

Valid anchor classes should be named up front when reanchor matters.

### Reanchor
Governed return after anchor loss.

Reanchor is not mere retry. It names a disciplined return posture with explicit conditions.

### Stop condition
An explicit condition under which a route, questline, or campaign must halt rather than pretend continuity after anchor loss.

Stop conditions protect reviewability by naming when governed return is no longer available.

### Skill ability card (ability card)
A derived reader surface that lets a bounded skill bundle be read as an active ability in long-horizon quest work.

Use the full term when boundary precision matters. "Ability card" is the shorter reading name.

An ability card helps orientation. It does not replace `SKILL.md`, evaluation surfaces, portable-layer contracts, or other owner surfaces.

### Loadout
A derived reader surface for a reviewable subset posture derived from pack-profile, trust, adapter, and runtime-contract surfaces.

Loadout is not runtime inventory, not per-agent equipped state, not cooldown economics, and not a hidden control plane.

### Unlock posture
A descriptive, evidence-backed hint about when an ability becomes a sane fit for use.

Unlock posture may reflect rank, mastery axes, risk ceilings, likely roles, or pack-profile fit, but it must not silently overrule trust or verification posture.

### Harvest posture
A declared review posture about whether and how a route, questline, or campaign may later be considered for promotion, repetition, or canonization.

Harvest posture guides review. It is not harvest authority.

### Quest harvest
A bounded post-session promotion triage for repeated reviewed quest units.

Quest harvest happens after a reviewed run, closure, or pause. It must not run inside an active route and may conclude with outcomes such as keeping a quest open or promoting it into a skill, playbook, memo, proof, or orchestrator surface.

### Anti-pattern
Do not let RPG reflection vocabulary replace source-owned repository semantics.

Questbooks are not runtime ledgers.
Ability cards are not canonical skill truth.
Loadouts are not runtime inventory.
Campaign language must not hide sprawl.
Continuity language must not hide missing anchors.

## Bridge and growth vocabulary

### Counterpart bridge
A derived bridge between ToS conceptual surfaces and AoA operational surfaces.

A counterpart bridge may support orientation or operational usefulness, but it must not become an identity claim.

### Analogy
A structural resemblance that helps orientation without asserting sameness.

### Support
An operational surface that reinforces or preserves a ToS concept in practice without becoming the concept itself.

### Tension
A productive mismatch where an operational surface helps reveal the limit of a concept bridge.

### Calibration
A bounded proof or review discipline that keeps an operational claim aligned without turning it into the concept itself.

### Idea lineage
The ToS-native lineage of texts, concepts, descendants, parallels, mutations, and tensions.

### Practice lineage
A genealogy of operational forms such as origin, mutation, adaptation, promotion, canonization, and deprecation.

ToS may recognize practice lineage conceptually, but operational ownership remains in AoA repositories.

### Donor refinement
A source-first AoA intake rule for external donors.

AoA should extract repeated patterns, sanitize them into techniques or skills, mature them through playbooks, and then check them through eval surfaces rather than importing foreign doctrine wholesale.

### Shared maturity ladder
The ecosystem-level ladder used when AoA makes cross-repo maturity claims:

`seed -> proven -> promoted -> canonical -> deprecated`

### Context compost
A ToS doctrine for digesting source-linked or witness-facing raw material into layered knowledge while keeping the route reviewable and reversible.

The canonical compost cycle is:

`raw -> note -> synthesis -> principle -> canon`

### Calibration axis
A ToS guidance surface that keeps curation oriented without flattening plurality.

It helps decide what kind of growth deepens the architecture, but it does not replace source reading or declare every source solved in advance.

### Anti-collapse
A boundary rule that keeps neighboring surfaces from being merged by metaphor, convenience, or hidden ownership drift.

Counterpart bridges, memory exports, and derived knowledge projections should stay derived rather than becoming covert replacements for source-owned meaning.

## Quality and operating principles

### Bounded
Deliberately limited in scope.

A bounded workflow, bundle, or claim names what it covers and what it does not cover. This reduces confusion and prevents hidden widening of authority.

### Reviewable
Open to structured human or agent inspection.

A reviewable surface should make its assumptions, boundaries, and artifacts visible rather than hiding them inside opaque automation.

### Reproducible
Capable of being repeated with the same core method or contract.

Reproducibility matters more than demo theater. A strong public surface should survive reuse beyond one private moment.

### Legible
Easy to read as a system, not just as an isolated artifact.

Legibility matters at both human and agent scales. It is one of the main design goals across AoA and the profile surface.

### Portable
Usable across more than one local context or project without losing its core meaning.

Portability does not mean universal abstraction. It means a surface can travel without depending on hidden private assumptions.

### Public-safe
Clean enough for public release.

A public-safe artifact excludes secrets, private operational risk, and project-local assumptions that were not properly sanitized.

### Evaluated
Supported by some explicit evidence or review surface.

Evaluation is stronger than intuition, but it is not the same thing as final certainty.

### Promoted
Publicly accepted as reusable, but not yet the default choice.

Promotion signals readiness for public use while leaving room for future strengthening.

### Canonical
Recommended by default after stronger validation, reuse evidence, and clearer default-use rationale.

Canonical status should remain meaningful rather than becoming a decorative label.

### Deprecated
Kept visible for history or compatibility, but no longer recommended for current use.

Deprecation should be explicit rather than a silent fade.

## Architectural distinctions

### Human meaning, agent acceleration
A core design principle across the ecosystem.

Humans should remain able to understand why a system is structured the way it is. Agents should benefit from explicit layers, reusable workflows, smaller derived surfaces, and controlled orchestration.

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

### Safe automation
Automation that is intentionally bounded, inspectable, and designed to preserve operator review.

Safe automation may reach action surfaces, but it should expose posture, checkpoints, and guardrails rather than widen authority by surprise.

### Dry-run posture
A default execution mode that simulates, stages, or previews action without committing external side effects.

Dry-run posture is a trust-building discipline, not a permanent refusal to act.

### Orchestrator surface
A route-facing or alignment-facing surface that may be consumed by an orchestrator class without redefining that class.

Orchestrator class identity remains upstream. A playbook- or quest-facing orchestrator surface only shapes what may be activated, aligned, handed off, or reviewed.

### Controlled orchestration
Coordination that composes calls, reads, memory, and workflows across source-owned surfaces while keeping authority boundaries explicit.

Controlled orchestration should widen capability without turning coordination into hidden ownership.

### Control plane
The layer that loads, types, validates, activates, and hands off across source-owned surfaces without becoming the source of their meaning.

In the current public ecosystem, `aoa-sdk` primarily operates on the control plane.

## Reading paths

If you want the shortest route into the ecosystem:

- for the ecosystem center and federation rules, start with [`Agents-of-Abyss`](https://github.com/8Dionysus/Agents-of-Abyss)
- for the knowledge world and source-first architecture of thought, start with [`Tree-of-Sophia`](https://github.com/8Dionysus/Tree-of-Sophia)
- for the runtime body beneath AoA and ToS, go to [`abyss-stack`](https://github.com/8Dionysus/abyss-stack)
- for the local-first companion application surface, go to [`ATM10-Agent`](https://github.com/8Dionysus/ATM10-Agent)
- for typed access and workspace integration, go to [`aoa-sdk`](https://github.com/8Dionysus/aoa-sdk)
- for reusable practice, go to [`aoa-techniques`](https://github.com/8Dionysus/aoa-techniques)
- for bounded execution workflows, go to [`aoa-skills`](https://github.com/8Dionysus/aoa-skills)
- for portable proof surfaces, go to [`aoa-evals`](https://github.com/8Dionysus/aoa-evals)
- for derived observability and machine-first summary surfaces, go to [`aoa-stats`](https://github.com/8Dionysus/aoa-stats)
- for navigation and dispatch, go to [`aoa-routing`](https://github.com/8Dionysus/aoa-routing)
- for memory and recall, go to [`aoa-memo`](https://github.com/8Dionysus/aoa-memo)
- for explicit agent roles, go to [`aoa-agents`](https://github.com/8Dionysus/aoa-agents)
- for recurring scenario recipes, go to [`aoa-playbooks`](https://github.com/8Dionysus/aoa-playbooks)
- for derived knowledge substrate surfaces, go to [`aoa-kag`](https://github.com/8Dionysus/aoa-kag)

## Scope note

This glossary is a public orientation surface.

It is not a replacement for the charters, roadmaps, validation contracts, or deeper repository-specific documentation.
