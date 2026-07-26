# Dionysus Conversational Portrait Route

## Index Metadata

- Decision ID: 8DION-D-0023
- Original date: 2026-07-25
- Surface classes: public entry, workspace route, Codex plane
- Route anchors: AGENTS.md, README.md, GLOSSARY.md, docs/START_HERE.md, docs/SYSTEM_CAPABILITY_MAP.md, config/codex_plane/runtime_manifest.v1.json
- Owner lanes: 8Dionysus, Dionysus
- Guard families: current owner boundary, active-only routing, explicit MCP registration
- Posture: accepted

## Status

Accepted.

## Context

The public route map and shared Codex plane must describe the current owner
contract of every sibling repository. Dionysus now owns voice-first interview
protocols, evidence-grounded claims, human review, and purpose-bounded personal
portrait projections.

The current owner exposes no repository-local MCP service. Keeping a stable
access-plane registration without a current callable contract would turn
historical configuration into active routing authority.

## Options Considered

1. Keep the existing public description and stable MCP registration for
   compatibility.
2. Remove Dionysus from public orientation entirely.
3. Route public readers to the current protocol owner, while removing the
   unsupported MCP registration and any access-plane claims.

## Decision

Choose option 3.

`8Dionysus` describes Dionysus only through its current conversational portrait
boundary. The shared Codex manifest does not register a repository-local server
for Dionysus. Future MCP registration requires a new owner-defined callable
contract and a separate reviewed Codex-plane decision.

## Consequences

- public orientation points to the current repository purpose;
- the checked-in and regenerated Codex plane no longer probes a nonexistent
  repository-local service;
- convergence reporting no longer emits a warning for that unsupported seam;
- a future integration must begin from the current owner contract rather than
  reviving configuration by name alone.
