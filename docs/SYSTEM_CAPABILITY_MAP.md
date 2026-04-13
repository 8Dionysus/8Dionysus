# System Capability Map

This note is the compact route map for the currently planted AoA system as of
April 13, 2026.
It explains what the system can do, which repository owns each capability
family, and which recurring playbook opens when the route is real.
It is a routing surface, not a new source of truth.

Use [WORKSPACE_INSTALL.md](WORKSPACE_INSTALL.md) for shared-root bootstrap and
projection.
Use [PUBLIC_ENTRY_POSTURE.md](PUBLIC_ENTRY_POSTURE.md) for the scope of
`8Dionysus`.
Use `aoa-playbooks:docs/PLAYBOOK_OPERATIONAL_FAMILY.md` when more than one
playbook feels plausible.

When the live need is workspace orientation or Codex wiring diagnosis, the
installed `aoa-shared-launchers` plugin opens launcher-level skills such as
`aoa-workspace-recon`, `aoa-growth-snapshot`, `aoa-seed-route-inspect`, and
`aoa-config-doctor`.
Use `<workspace-root>/.codex/bin/aoa-codex-doctor`,
`<workspace-root>/.codex/bin/aoa-codex-status`, and
`<workspace-root>/.codex/bin/aoa-codex-bootstrap` together with
`<workspace-root>/.codex/generated/codex/aoa_codex_convergence_report.{json,md}`
as convergence evidence only; convergence reports are evidence, not authority,
and they do not transfer authority away from owner repos.

## Core operating loop

At the workspace root, the honest sequence is still:

1. orient with `aoa skills enter <repo_root> --root /srv ...`
2. add route hints with `aoa surfaces detect ...` when ambiguity appears
3. gate risky mutation with `aoa skills guard <repo_root> --root /srv ...`
4. move the real change into the owner repo
5. prove the move with owner validators, evals, or reviewed runs
6. let stats, memo, and Dionysus preserve weaker follow-through

## Capability families

| capability family | what the system can do | owner truth | open when | main supporting layers |
| --- | --- | --- | --- | --- |
| Workspace orientation and Codex plane | discover the workspace root, use shared launcher skills for orientation and wiring diagnosis, project the shared-root Codex install, keep stable MCP names, run convergence doctor or status, rerender, roll out, and repair drift | `8Dionysus` for shared-root projection, launcher packaging, convergence posture, and rollout history; `aoa-sdk` for typed control-plane and `aoa_workspace`; `aoa-skills`, `aoa-agents`, `aoa-stats`, and `Dionysus` for their own projected or repo-local layers | no sovereign playbook by default; widen to `AOA-P-0028` only when a bounded shared-root rollout with drift or rollback is real | `AGENTS.md`, `.agents/plugins/marketplace.json`, `.codex/plugins/aoa-shared-launchers/PLUGIN_NOTES.md`, `.codex/generated/codex/aoa_codex_convergence_report.md`, `docs/WORKSPACE_INSTALL.md`, `docs/CODEX_PLANE_REGENERATION.md`, `docs/CODEX_PLANE_ROLLOUT.md`, `docs/CODEX_TRUSTED_ROLLOUT_OPERATIONS.md`, `docs/TRUSTED_ROLLOUT_CAMPAIGNS.md` |
| Growth refinery and lineage | carry a reviewed session route through checkpoint hints, reviewed donor harvest, `candidate_ref`, `seed_ref`, owner landing, proof, bounded memo, and derived funnel visibility | `Agents-of-Abyss` for doctrine, `aoa-sdk` for carry-only hints, `aoa-skills` for reviewed `candidate_ref`, `Dionysus` for `seed_ref`, owner repos for landed objects | `AOA-P-0025` when the full reviewed cycle is in play; `AOA-P-0026` when a candidate or staged seed already exists and only the next owner move is in scope; `AOA-P-0021` for owner-first landing | `aoa-stats:generated/candidate_lineage_summary.min.json`, `aoa-evals` lineage and owner-fit bundles, `aoa-memo:docs/GROWTH_REFINERY_WRITEBACK.md`, Dionysus seed lineage notes |
| Trusted rollout operations and cadence | run bounded shared-root Codex deployment campaigns with trust, doctor, drift observation, rollback windows, checked-in history, and bounded follow-through | `8Dionysus` for checked-in rollout history; `aoa-sdk` for typed deploy status; `aoa-stats` for derived rollout summaries; `aoa-memo` for bounded recovery patterns | `AOA-P-0028` when rollout, drift, rollback, and checked-in publication are one reviewable route; keep campaign cadence and deployment continuity as companion notes under `AOA-P-0028`, not separate playbooks | `aoa-stats:generated/codex_plane_deployment_summary.min.json`, `aoa-stats:generated/rollout_campaign_summary.min.json`, `aoa-stats:generated/drift_review_summary.min.json`, `aoa-evals:aoa-diagnosis-cause-discipline`, `aoa-evals:aoa-repair-boundedness` |
| Self-agency continuity | preserve a reviewed anchor across revision windows, explicit reanchor, bounded relaunch aids, and proof that continuity stayed subordinate to the anchor | `Agents-of-Abyss` for doctrine, `aoa-agents` for continuity window law, `aoa-playbooks` for the route, `aoa-evals` for proof | `AOA-P-0029` when the live problem is continuity across more than one revision window or a real reanchor decision | `aoa-sdk:examples/closeout_continuity_window.example.json`, `aoa-stats:generated/continuity_window_summary.min.json`, `aoa-memo:docs/SELF_AGENCY_CONTINUITY_WRITEBACK.md`, `aoa-evals` continuity bundles |
| Component refresh | notice reviewed internal component drift, route it to one named owner, take a bounded refresh decision, validate in the owner repo, and publish derived summary closure without scheduler authority | the drifting component's owner repo; `aoa-sdk` for hint-only drift carry; `aoa-playbooks` for the route; `aoa-stats` for derived summary | `AOA-P-0030` when one named component has real owner-law drift and the route is narrower than shared-root rollout or generic remediation | `docs/COMPONENT_REFRESH_ROUTE.md`, `aoa-sdk:docs/COMPONENT_DRIFT_HINTS.md`, `aoa-stats:generated/component_refresh_summary.min.json`, `aoa-memo` component-refresh recovery patterns |
| MCP and access plane | expose project-level workspace orientation plus repo-local observability and seed-routing MCP surfaces, and let launcher skills bind them by stable name, without turning MCP or launcher packaging into authority | `aoa-sdk` owns `aoa_workspace`; `aoa-stats` owns `aoa_stats`; `Dionysus` owns `dionysus`; `aoa-skills` owns skill-to-MCP dependency wiring; `aoa-agents` owns subagent projection affinity; `8Dionysus` owns the shared-root `.codex` install surface, launcher packaging, and convergence wrappers | use whenever orientation, stats observability, seed routing, or Codex launch discipline is the need; MCP stays support infrastructure, not sovereign workflow truth | `AGENTS.md`, `.agents/plugins/marketplace.json`, `.codex/plugins/aoa-shared-launchers/PLUGIN_NOTES.md`, `aoa-sdk:docs/codex-workspace-mcp.md`, `aoa-skills:docs/CODEX_SKILL_MCP_WIRING.md`, `aoa-agents:docs/CODEX_SUBAGENT_PROJECTION.md`, `Dionysus:docs/CODEX_MCP.md` |

## Playbook opener

If the route anchor is:

- one reviewed session spanning checkpoint carry, donor harvest, seed stage,
  owner landing, proof, and bounded writeback, open `AOA-P-0025`
- an existing reviewed candidate or staged seed and only the next honest owner
  move is in scope, open `AOA-P-0026`
- a reviewed automation candidate that still lacks scheduler authority or a
  real-run promotion, open `AOA-P-0027`
- a shared-root Codex rollout with drift, rollback, checked-in publication, and
  bounded follow-through, open `AOA-P-0028`
- a reviewed anchor that now needs revision-window continuity or a bounded
  reanchor, open `AOA-P-0029`
- one named internal component with owner-law drift and a bounded refresh
  target, open `AOA-P-0030`
- a reviewed capability that must land in the owner repo before broader rollout,
  open `AOA-P-0021`
- a failed validator or proof surface that now drives the route, open
  `AOA-P-0018`

When two routes still feel close, fall back to
`aoa-playbooks:docs/PLAYBOOK_OPERATIONAL_FAMILY.md`.

## Derived and preserved layers

The planted system now has a stable weaker-layer split:

- `aoa-evals` proves route claims, but does not become execution authority
- `aoa-stats` publishes derived summaries, but does not become source truth
- `aoa-memo` keeps bounded writeback and recovery patterns, but does not become
  the first record of truth
- `Dionysus` keeps seed packs, lineage notes, and planting reports, but does
  not replace owner repos
- `8Dionysus` routes public and shared-root entry surfaces, but does not become
  the hidden center of the federation

## Non-goals

This planted system still refuses a few tempting shortcuts:

- no hidden scheduler behind cadence, automation, component refresh, or
  continuity routes
- no MCP-owned authority over repository law or playbook truth
- no stats-owned verdicts
- no memo-first truth
- no runtime-autonomy mythology
