#!/usr/bin/env python3
"""Trigger-aware closeout helper for repo-family required-check audits."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_FILE = Path("config/github_required_check_contracts.json")
DEFAULT_COMPARE_REF = "origin/main"
TRIGGER_PREFIXES = (".github/workflows/",)
TRIGGER_PATHS = {
    ".codex/bin/aoa-required-check-audit",
    "config/github_required_check_contracts.json",
    "docs/GITHUB_REQUIRED_CHECK_CONTRACTS.md",
    "docs/decisions/0002-repo-family-required-check-contracts.md",
    "schemas/github_required_check_contracts.schema.json",
    "scripts/run_required_check_audit.py",
    "scripts/validate_github_required_check_contracts.py",
    "tests/test_github_required_check_contracts.py",
    "tests/test_required_check_audit.py",
}


def git_output(repo_root: Path, *args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    if check and proc.returncode != 0:
        message = proc.stderr.strip() or proc.stdout.strip() or "git command failed"
        raise ValueError(f"{repo_root}: git {' '.join(args)} failed: {message}")
    return proc.stdout.strip()


def discover_repo_root(start_path: Path) -> Path:
    candidate = start_path.resolve()
    if candidate.is_file():
        candidate = candidate.parent
    repo_root_text = git_output(candidate, "rev-parse", "--show-toplevel")
    return Path(repo_root_text)


def resolve_contract_repo(target_repo_root: Path, explicit_contract_repo: Path | None) -> Path:
    if explicit_contract_repo is not None:
        contract_repo = explicit_contract_repo.resolve()
    elif (target_repo_root / CONTRACT_FILE).exists():
        contract_repo = target_repo_root
    else:
        sibling = target_repo_root.parent / "8Dionysus"
        contract_repo = sibling if (sibling / CONTRACT_FILE).exists() else REPO_ROOT

    if not (contract_repo / CONTRACT_FILE).exists():
        raise ValueError(
            f"could not locate {CONTRACT_FILE} from target repo {target_repo_root}"
        )
    return contract_repo


def select_compare_ref(repo_root: Path, requested_ref: str | None) -> str | None:
    if requested_ref == "none":
        return None
    compare_ref = requested_ref or DEFAULT_COMPARE_REF
    proc = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", compare_ref],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    return compare_ref if proc.returncode == 0 else None


def collect_changed_paths(repo_root: Path, compare_ref: str | None) -> list[str]:
    changed: set[str] = set()

    if compare_ref is not None:
        merge_base = git_output(repo_root, "merge-base", "HEAD", compare_ref, check=False)
        if merge_base:
            for path in git_output(repo_root, "diff", "--name-only", f"{merge_base}..HEAD").splitlines():
                if path.strip():
                    changed.add(path.strip())

    for diff_args in (("diff", "--name-only"), ("diff", "--name-only", "--cached")):
        for path in git_output(repo_root, *diff_args).splitlines():
            if path.strip():
                changed.add(path.strip())

    for path in git_output(repo_root, "ls-files", "--others", "--exclude-standard").splitlines():
        if path.strip():
            changed.add(path.strip())

    return sorted(changed)


def path_triggers_required_check_audit(path: str) -> bool:
    return path in TRIGGER_PATHS or path.startswith(TRIGGER_PREFIXES)


def find_trigger_paths(changed_paths: list[str]) -> list[str]:
    return [path for path in changed_paths if path_triggers_required_check_audit(path)]


def build_audit_commands(contract_repo: Path, include_github_protection: bool) -> list[list[str]]:
    validator = contract_repo / "scripts" / "validate_github_required_check_contracts.py"
    commands = [
        [sys.executable, str(validator)],
        [sys.executable, str(validator), "--remote-workflows"],
    ]
    if include_github_protection:
        commands.append([sys.executable, str(validator), "--github-protection"])
    return commands


def run_commands(commands: list[list[str]]) -> None:
    for command in commands:
        print(f"[run] {' '.join(command)}")
        subprocess.run(command, check=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the required-check audit only when the current repo diff touches relevant surfaces.",
    )
    parser.add_argument(
        "--repo-root",
        help="Git repo to inspect for trigger paths. Defaults to the current working tree.",
    )
    parser.add_argument(
        "--contract-repo",
        help="Repo that owns config/github_required_check_contracts.json. Defaults to sibling 8Dionysus.",
    )
    parser.add_argument(
        "--compare-ref",
        default=None,
        help="Ref used to detect branch-level changed paths. Defaults to origin/main when available. Use 'none' to disable.",
    )
    parser.add_argument(
        "--github-protection",
        action="store_true",
        help="Also audit live branch protection through gh. Use when this session changed protection settings.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Run the audit even when no trigger paths are present.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the chosen plan without running the validator commands.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    start_path = Path(args.repo_root) if args.repo_root else Path.cwd()
    target_repo_root = discover_repo_root(start_path)
    contract_repo = resolve_contract_repo(
        target_repo_root,
        Path(args.contract_repo) if args.contract_repo else None,
    )
    compare_ref = select_compare_ref(target_repo_root, args.compare_ref)
    changed_paths = collect_changed_paths(target_repo_root, compare_ref)
    trigger_paths = find_trigger_paths(changed_paths)

    print(f"[info] target_repo={target_repo_root}")
    print(f"[info] contract_repo={contract_repo}")
    print(f"[info] compare_ref={compare_ref or 'none'}")

    if trigger_paths:
        print("[info] trigger_paths:")
        for path in trigger_paths:
            print(f"  - {path}")
    elif changed_paths:
        print("[info] changed_paths_present_but_not_triggering_required_check_audit=true")
    else:
        print("[info] no_changed_paths_detected=true")

    if not args.force and not args.github_protection and not trigger_paths:
        print("[skip] required-check audit not triggered")
        return 0

    commands = build_audit_commands(contract_repo, include_github_protection=args.github_protection)
    if args.dry_run:
        print("[plan] running required-check audit commands:")
        for command in commands:
            print(f"  - {' '.join(command)}")
        return 0

    run_commands(commands)
    print("[ok] required-check audit completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
