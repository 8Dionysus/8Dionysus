# Validation routes

On-demand checks for the repository root and shared-root route surfaces. Run
only the route relevant to the change; this file is not an automatic preload.

## Skill inspection

```bash
aoa skills inspect <repo_root> --root <workspace-root> --json
aoa skills capability <exact-node-id> --root <workspace-root> --json
```

## Codex plane

For organ-fabric source changes, use the
[local organ-fabric route](config/codex_plane/organ_fabric/VALIDATION.md).

```bash
python scripts/build_workspace_memory_map.py --workspace-root <workspace-root> --owner-repo-root . --check
```

## AGENTS map and workspace audit

```bash
python scripts/audit_agents_map.py --workspace-root <workspace-root> --write generated/agents_map.min.json --markdown docs/AGENTS_MAP.md
```

```bash
python scripts/audit_agents_map.py --public-baseline --write generated/agents_map.min.json --markdown docs/AGENTS_MAP.md
```

```bash
python scripts/validate_nested_agents.py
```

```bash
python scripts/build_workspace_memory_map.py --workspace-root <workspace-root> --owner-repo-root . --write generated/workspace_memory_map.min.json --markdown docs/WORKSPACE_MEMORY_MAP.md
```

```bash
python scripts/build_workspace_memory_map.py --workspace-root <workspace-root> --write generated/workspace_memory_map.min.json --markdown docs/WORKSPACE_MEMORY_MAP.md
```

```bash
python scripts/validate_workspace_memory_map.py
```

```bash
python scripts/recon_agents_frontier.py --map generated/agents_map.min.json --write generated/agents_frontier_recon.min.json --markdown generated/agents_frontier_recon.md
```

## Full repository checks

```bash
python -m unittest discover -s tests
```

## Decisions

```bash
python scripts/generate_decision_indexes.py --check
python scripts/validate_decision_records.py
python -m unittest tests.test_decision_indexes
```
