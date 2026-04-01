# QUESTBOOK profile boundary — 8Dionysus

## Purpose

This note shows how `QUESTBOOK.md` can exist inside the GitHub profile repository without turning the profile into a control plane.

## Core boundary

`8Dionysus` is a public orientation surface.
It helps humans and agents find the right repositories, but it does not own the real charters, schemas, validators, workflows, or implementation details of the ecosystem.

The quest layer here is therefore limited to profile reflection debt:
- public repo links
- role descriptions
- glossary compatibility
- orientation drift after already-landed changes elsewhere

## Good uses

Use profile quests for:
- a public repository link that now points to the wrong role or outdated description
- profile wording that starts lying about which repo owns a capability
- glossary or orientation drift that survives a bounded profile docs pass

## Bad uses

Do not use profile quests for:
- live system routing
- implementation work that belongs in linked repositories
- public claims about maturity or roadmap that the source repos do not own
- operational work tracking for AoA, ToS, or abyss-stack

## Good anchors in this repo

Use stable anchors such as:
- `README.md`
- `GLOSSARY.md`
- `AGENTS.md`

## Posture

This layer should stay lightweight.
It is allowed to track reflection debt, but it should not grow into a dashboard-authority repo or a replacement for the repositories it links to.
