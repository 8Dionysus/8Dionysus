# 8Dionysus Skill Home

This directory is the canonical home for callable procedures owned specifically
by the `8Dionysus` public workspace-delivery lane. It is not a mirror of the
shared AoA catalog.

## Admitted bundle

| Bundle | Capability | Visibility | Admission |
| --- | --- | --- | --- |
| `aoa-workspace-diagnose` | diagnose one concrete skill, MCP, or tool delivery disagreement | repo-advertised | `docs/decisions/8DION-D-0018-workspace-capability-diagnosis-home-skill.md` |

General workspace orientation remains a route-card and KAG capability. It did
not demonstrate independent callable-skill benefit. Repair and convergence
remain separate owner workflows and tools.

`port.manifest.json` declares the admitted source and exact derived Codex
projection. Canonical files live under `skills/aoa-workspace-diagnose/`; files
under `.agents/skills/aoa-workspace-diagnose/` are generated copies.

## Verification posture

Manual work establishes usefulness. Working rules live in `skills/AGENTS.md`.
The pinned common home-port action checks structural ownership and projection
parity; it does not prove triggering, diagnosis quality, safety, or cross-host
behavior.
