# Retire Unused Profile Outputs and Producer

## Index Metadata

- Decision ID: 8DION-D-0036
- Original date: 2026-09-05
- Surface classes: public profile, GitHub automation, historical recovery
- Route anchors: README.md, profile/, .github/workflows/update-github-stats.yml
- Owner lanes: 8Dionysus
- Guard families: public entry, owner evidence, historical recovery
- Posture: accepted

## Status

Accepted by the repository owner as a bounded retirement of five obsolete
profile outputs and their unused scheduled producer.

## Context

The public README embeds the current v15 profile assets and does not consume
the older papyrus or zigzag maps, nor the generated stats cards. The scheduled
GitHub stats workflow writes those unconsumed cards and auto-commits them,
creating recurring maintenance without serving the public entry. The stats
owner port and its workspace coverage contract are unrelated and remain
unchanged.

## Options Considered

1. Keep the unused producer and stale outputs.
2. Remove the producer but leave stale outputs in the current tree.
3. Remove both producer and outputs while retaining exact recovery through Git.

## Decision

Choose option 3. Delete exactly these current-tree paths:

- `profile/abyss_os_papyrus_tree_v14.svg`
- `profile/abyss_os_zigzag_tree_v11.svg`
- `profile/stats.svg`
- `profile/top-langs.svg`
- `.github/workflows/update-github-stats.yml`

The active v15, quote, and principles assets remain. This decision does not
change the public README contract, the stats owner port, the Codex plane,
workspace projections, sibling repositories, or required Repo Validation.

## Recovery

Each deleted path is recoverable from the exact clean baseline
`3920ffb7889921a1d38f3b767a48a20754fdffd3`:

- `profile/abyss_os_papyrus_tree_v14.svg`
  (`e93ae375b80443e8b7b49bf28c4a02a0625fed25`)
- `profile/abyss_os_zigzag_tree_v11.svg`
  (`46db09d47c68a2d5fb98141445f6470c5f75b21a`)
- `profile/stats.svg` (`d415b4218220c70ea8c884a5b19f952b9a9cf790`)
- `profile/top-langs.svg` (`22d4909a1d5f215348ca0d4bd6de3d4e1d528f80`)
- `.github/workflows/update-github-stats.yml`
  (`31df9087b70613724ab07fa4b9390c93cc22eb08`)

Historical recovery is evidence, not a current-tree route. External bookmarks
or unknown consumers were not proved universally absent; that uncertainty does
not make these superseded outputs part of the active public entry contract.

## Consequences

The old raw paths are no longer current-tree endpoints, and the scheduled
producer no longer creates unconsumed profile cards. No deletion-specific
permanent validator or new archive policy is needed. Historical event records
remain historical, while current source records and decision indexes are
regenerated canonically.
