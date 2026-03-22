# AGENTS.md

## Repository purpose

This is the GitHub profile repository for Dionysus.
It is a docs-first coordination surface and public entrypoint for the AoA / ToS ecosystem.
Treat it as orientation, not as the authoritative home of each linked project.

## What owns truth here

- `README.md` is the public landing page for humans.
- `GLOSSARY.md` defines shared ecosystem vocabulary used across the public surface.
- Linked repositories own their own charters, roadmaps, schemas, registries, scripts, and implementation details.

Do not move project-specific doctrine or implementation detail into this repository unless the task is explicitly about profile-level orientation.

## Editing priorities

- Keep the profile concise, legible, and navigation-first.
- Prefer stable descriptions over momentum words such as "bootstrapping" or "preparing" unless a status note is genuinely important.
- Preserve exact repository names, capitalization, and hyphenation.
- Use precise English with low hype.
- Keep AoA / ToS vocabulary aligned with `GLOSSARY.md`.
- Do not invent roadmap claims, maturity claims, or public/private status.

## When editing README.md

- Optimize for fast scanning on a GitHub profile page.
- Prefer descriptions that answer "what this repo owns" or "when to go there".
- Keep the profile repository framed as a coordination surface, not a replacement for the source repositories.
- When a linked repository becomes public, changes role, or gains a clearer description, update the README accordingly.
- Avoid duplicating large blocks of doctrine from `Agents-of-Abyss` or `Tree-of-Sophia`; link outward instead.

## When editing GLOSSARY.md

- Preserve the boundary language around source of truth, coordination repository, layer, federation, provenance, bounded, reviewable, and reproducible.
- Do not casually redefine core terms.
- Keep definitions compact, reusable, and cross-repo friendly.
- Prefer clarity over cleverness.

## Sync rules

- `README.md` and `GLOSSARY.md` are the primary public docs in this repository.
- Keep wording between them compatible, but do not create derivative sync artifacts unless the task explicitly asks for them.

## Commands

This repository has no build step and no formal test suite.
Useful local checks:

- Inspect the main docs: `sed -n '1,260p' README.md && printf '\n---\n' && sed -n '1,260p' GLOSSARY.md`
- Search ecosystem references before renaming or rewording: `grep -RIn "Agents-of-Abyss\|Tree-of-Sophia\|aoa-\|abyss-stack\|ATM10-Agent" README.md GLOSSARY.md`

## Validation checklist

Before finishing, verify that:

- all repository links resolve and use the exact repo name
- README descriptions do not contradict current public repository descriptions
- public/private claims are current
- the profile repo is not presented as the source of truth for specialized layer content
- tone remains compact, clear, and legible to humans and smaller models
