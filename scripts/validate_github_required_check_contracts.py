#!/usr/bin/env python3
"""Validate the cross-repo required-check contract owned by 8Dionysus."""

from __future__ import annotations

import argparse
import ast
import json
import subprocess
from pathlib import Path
from types import SimpleNamespace
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import urlopen

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = REPO_ROOT / "config" / "github_required_check_contracts.json"
SCHEMA_PATH = REPO_ROOT / "schemas" / "github_required_check_contracts.schema.json"


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def format_jsonschema_error(error: object) -> str:
    path = getattr(error, "absolute_path", [])
    location = "".join(f"[{part}]" if isinstance(part, int) else f".{part}" for part in path).lstrip(".")
    prefix = f"{CONTRACT_PATH}:{location}" if location else str(CONTRACT_PATH)
    return f"{prefix}: {error.message}"


def normalize_unique_strings(values: object, label: str) -> list[str]:
    if not isinstance(values, list):
        raise ValueError(f"{label} must be a list")
    normalized: list[str] = []
    seen: set[str] = set()
    for index, value in enumerate(values):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{label}[{index}] must be a non-empty string")
        if value in seen:
            raise ValueError(f"{label} contains duplicate entry {value!r}")
        normalized.append(value)
        seen.add(value)
    return normalized


def load_contract() -> dict[str, object]:
    schema = load_json(SCHEMA_PATH)
    contract = load_json(CONTRACT_PATH)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(contract), key=lambda error: list(error.absolute_path))
    if errors:
        raise ValueError(format_jsonschema_error(errors[0]))
    if not isinstance(contract, dict):
        raise ValueError(f"{CONTRACT_PATH} must be a JSON object")
    return contract


def iter_selected_repos(contract: dict[str, object], repo_filters: list[str]) -> list[dict[str, object]]:
    repos = contract.get("repos")
    if not isinstance(repos, list):
        raise ValueError(f"{CONTRACT_PATH}:repos must be a list")
    selected = [entry for entry in repos if isinstance(entry, dict)]
    if not repo_filters:
        return selected
    allowed = set(repo_filters)
    repo_map = {entry["repo"]: entry for entry in selected if isinstance(entry.get("repo"), str)}
    missing = sorted(allowed - set(repo_map))
    if missing:
        raise ValueError(f"unknown repo filter(s): {', '.join(missing)}")
    return [repo_map[repo] for repo in repo_filters]


def validate_contract_structure(contract: dict[str, object]) -> None:
    tracked_branch = contract.get("tracked_branch")
    if not isinstance(tracked_branch, str) or not tracked_branch:
        raise ValueError("tracked_branch must be a non-empty string")

    repos = iter_selected_repos(contract, [])
    seen_repos: set[str] = set()

    for repo_entry in repos:
        repo = repo_entry.get("repo")
        if not isinstance(repo, str) or not repo:
            raise ValueError("repo entries must have a non-empty repo field")
        if repo in seen_repos:
            raise ValueError(f"duplicate repo entry {repo!r} in {CONTRACT_PATH}")
        seen_repos.add(repo)

        protection_expected = repo_entry.get("protection_expected")
        if not isinstance(protection_expected, bool):
            raise ValueError(f"{repo} protection_expected must be boolean")

        required_status_checks = normalize_unique_strings(
            repo_entry.get("required_status_checks"), f"{repo}.required_status_checks"
        )
        workflow_checks = repo_entry.get("workflow_checks")
        if not isinstance(workflow_checks, list):
            raise ValueError(f"{repo}.workflow_checks must be a list")

        covered_job_names: list[str] = []
        seen_paths: set[str] = set()
        for index, workflow_check in enumerate(workflow_checks):
            if not isinstance(workflow_check, dict):
                raise ValueError(f"{repo}.workflow_checks[{index}] must be an object")
            path = workflow_check.get("path")
            if not isinstance(path, str) or not path:
                raise ValueError(f"{repo}.workflow_checks[{index}].path must be a non-empty string")
            if path in seen_paths:
                raise ValueError(f"{repo}.workflow_checks contains duplicate path {path!r}")
            seen_paths.add(path)
            workflow_name = workflow_check.get("expected_workflow_name")
            if not isinstance(workflow_name, str) or not workflow_name:
                raise ValueError(
                    f"{repo}.workflow_checks[{index}].expected_workflow_name must be a non-empty string"
                )
            required_job_names = normalize_unique_strings(
                workflow_check.get("required_job_names"),
                f"{repo}.workflow_checks[{index}].required_job_names",
            )
            covered_job_names.extend(required_job_names)

        covered_job_names = normalize_unique_strings(
            covered_job_names, f"{repo}.workflow_checks.required_job_names"
        )

        if protection_expected and not required_status_checks:
            raise ValueError(f"{repo} must declare required_status_checks when protection_expected=true")
        if protection_expected and not workflow_checks:
            raise ValueError(f"{repo} must declare workflow_checks when protection_expected=true")
        if not protection_expected and required_status_checks:
            raise ValueError(f"{repo} cannot declare required_status_checks when protection_expected=false")
        if not protection_expected and workflow_checks:
            raise ValueError(f"{repo} cannot declare workflow_checks when protection_expected=false")
        if sorted(required_status_checks) != sorted(covered_job_names):
            raise ValueError(
                f"{repo} required_status_checks must match the union of workflow required_job_names"
            )


def parse_inline_scalar(raw_value: str, source_label: str, lineno: int) -> str:
    value = raw_value.strip()
    if not value:
        raise ValueError(f"{source_label}:{lineno} expected an inline scalar value")
    if value in {"|", "|-", "|+", ">", ">-", ">+"}:
        raise ValueError(f"{source_label}:{lineno} block scalar names are not supported")
    if value[0] in {'"', "'"} and value[-1] == value[0]:
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError) as exc:
            raise ValueError(f"{source_label}:{lineno} invalid quoted scalar {value!r}") from exc
        if not isinstance(parsed, str) or not parsed.strip():
            raise ValueError(f"{source_label}:{lineno} must decode to a non-empty string")
        return parsed
    if " #" in value:
        value = value.split(" #", 1)[0].rstrip()
    if not value:
        raise ValueError(f"{source_label}:{lineno} expected a non-empty scalar value")
    return value


def parse_workflow_metadata(text: str, source_label: str) -> tuple[str, list[str]]:
    workflow_name: str | None = None
    job_names: list[str] = []
    in_jobs = False
    current_job_id: str | None = None
    current_job_name: str | None = None
    block_scalar_indent: int | None = None

    def finalize_job() -> None:
        nonlocal current_job_id, current_job_name
        if current_job_id is None:
            return
        job_names.append(current_job_name or current_job_id)
        current_job_id = None
        current_job_name = None

    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))

        if block_scalar_indent is not None:
            if not stripped:
                continue
            if indent > block_scalar_indent:
                continue
            block_scalar_indent = None

        if not stripped or stripped.startswith("#"):
            continue

        if ":" in stripped:
            raw_value = stripped.split(":", 1)[1].strip()
            if raw_value in {"|", "|-", "|+", ">", ">-", ">+"}:
                block_scalar_indent = indent

        if indent == 0:
            finalize_job()
            in_jobs = stripped.startswith("jobs:")
            if stripped.startswith("name:"):
                workflow_name = parse_inline_scalar(stripped.split(":", 1)[1], source_label, lineno)
            continue

        if not in_jobs:
            continue
        if indent == 2 and stripped.endswith(":") and not stripped.startswith("-"):
            finalize_job()
            current_job_id = stripped[:-1].strip()
            current_job_name = None
            continue
        if current_job_id is not None and indent == 4 and stripped.startswith("name:"):
            current_job_name = parse_inline_scalar(stripped.split(":", 1)[1], source_label, lineno)

    finalize_job()

    if not workflow_name:
        raise ValueError(f"{source_label} is missing top-level workflow name")
    if not job_names:
        raise ValueError(f"{source_label} is missing jobs")
    return workflow_name, normalize_unique_strings(job_names, f"{source_label}.job_names")


def fetch_remote_workflow_text(repo: str, branch: str, path: str, timeout_sec: float = 20.0) -> str:
    quoted_branch = quote(branch, safe="")
    quoted_path = quote(path, safe="/")
    url = f"https://raw.githubusercontent.com/{repo}/{quoted_branch}/{quoted_path}"
    try:
        with urlopen(url, timeout=timeout_sec) as response:
            return response.read().decode("utf-8")
    except HTTPError as exc:
        raise ValueError(f"{repo}@{branch}:{path} fetch failed with HTTP {exc.code}") from exc
    except URLError as exc:
        raise ValueError(f"{repo}@{branch}:{path} fetch failed: {exc.reason}") from exc


def validate_remote_workflow_contracts(
    contract: dict[str, object],
    repo_filters: list[str],
    fetcher=fetch_remote_workflow_text,
) -> None:
    branch = contract["tracked_branch"]
    if not isinstance(branch, str):
        raise ValueError("tracked_branch must be a string")

    for repo_entry in iter_selected_repos(contract, repo_filters):
        repo = repo_entry["repo"]
        workflow_checks = repo_entry["workflow_checks"]
        if not isinstance(workflow_checks, list):
            raise ValueError(f"{repo}.workflow_checks must be a list")
        for workflow_check in workflow_checks:
            path = workflow_check["path"]
            expected_workflow_name = workflow_check["expected_workflow_name"]
            required_job_names = normalize_unique_strings(
                workflow_check["required_job_names"],
                f"{repo}:{path}.required_job_names",
            )
            source_label = f"{repo}@{branch}:{path}"
            text = fetcher(repo, branch, path)
            actual_workflow_name, actual_job_names = parse_workflow_metadata(text, source_label)
            if actual_workflow_name != expected_workflow_name:
                raise ValueError(
                    f"{source_label} workflow name {actual_workflow_name!r} != {expected_workflow_name!r}"
                )
            missing = sorted(set(required_job_names) - set(actual_job_names))
            if missing:
                raise ValueError(
                    f"{source_label} is missing required job name(s): {', '.join(missing)}"
                )
            print(f"[ok] remote workflow contract {source_label}")


def run_gh_api(api_path: str) -> object:
    return subprocess.run(
        ["gh", "api", api_path],
        check=False,
        text=True,
        capture_output=True,
    )


def validate_live_github_protection(
    contract: dict[str, object],
    repo_filters: list[str],
    gh_runner=run_gh_api,
) -> None:
    branch = contract["tracked_branch"]
    if not isinstance(branch, str):
        raise ValueError("tracked_branch must be a string")

    for repo_entry in iter_selected_repos(contract, repo_filters):
        repo = repo_entry["repo"]
        required_status_checks = normalize_unique_strings(
            repo_entry["required_status_checks"],
            f"{repo}.required_status_checks",
        )
        protection_expected = repo_entry["protection_expected"]
        api_path = f"repos/{repo}/branches/{branch}/protection/required_status_checks"
        response = gh_runner(api_path)
        returncode = getattr(response, "returncode", 1)
        stdout = getattr(response, "stdout", "")
        stderr = getattr(response, "stderr", "")

        if protection_expected:
            if returncode != 0:
                raise ValueError(f"{repo} protection check failed: {stderr.strip() or stdout.strip()}")
            payload = json.loads(stdout)
            contexts = normalize_unique_strings(payload.get("contexts", []), f"{repo}.live_contexts")
            if sorted(contexts) != sorted(required_status_checks):
                raise ValueError(
                    f"{repo} live required_status_checks {contexts!r} != {required_status_checks!r}"
                )
            print(f"[ok] live branch protection {repo}@{branch}")
            continue

        if returncode == 0:
            raise ValueError(f"{repo} unexpectedly has live required_status_checks configured")
        print(f"[ok] live branch protection intentionally absent for {repo}@{branch}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate the coordination contract for required GitHub checks.",
    )
    parser.add_argument(
        "--remote-workflows",
        action="store_true",
        help="Fetch tracked workflow files from GitHub raw URLs and validate workflow/job names.",
    )
    parser.add_argument(
        "--github-protection",
        action="store_true",
        help="Use gh api to validate live required_status_checks on the tracked branch.",
    )
    parser.add_argument(
        "--repo",
        action="append",
        default=[],
        help="Limit validation to one or more repo names such as 8Dionysus/aoa-skills.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    contract = load_contract()
    validate_contract_structure(contract)
    print(f"[ok] validated {CONTRACT_PATH.relative_to(REPO_ROOT)}")

    if args.remote_workflows:
        validate_remote_workflow_contracts(contract, args.repo)
    if args.github_protection:
        validate_live_github_protection(contract, args.repo)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
