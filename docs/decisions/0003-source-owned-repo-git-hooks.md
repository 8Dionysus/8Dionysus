# 0003 Source-Owned Repo Git Hooks

## Status

Accepted.

## Context

AoA checkpoint hooks run from each checkout's private Git hook directory, not
from a tracked working-tree path. After a workspace-root move, this made the
active hook state machine-local and easy to drift away from the source-owned
Codex plane.

## Decision

Keep the hook bodies as public templates under `config/git_hooks/` and manage
active repo-local hooks with `scripts/manage_workspace_git_hooks.py`.

The installer discovers sibling Git checkouts under the workspace root, renders
the templates with the chosen workspace root, and installs these managed hooks:

- `pre-merge-commit`
- `pre-push`
- `post-commit`

It blocks on existing unmanaged hooks by default so local custom automation is
not silently overwritten. Operators may use `--force` only after reviewing that
local state.

## Consequences

`8Dionysus` owns the source templates and validation route, while each
checkout's `.git/hooks/` remains local runtime state. Future root moves can be
checked with `--check` and repaired with `--execute` instead of hand-patching
private Git metadata.
