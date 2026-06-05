#!/usr/bin/env python3
from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path


PACKAGE_SCRIPT_REL = Path("mcp/services/aoa-decisions-mcp/scripts/aoa_decisions_mcp_server.py")


def workspace_root() -> Path:
    env_root = os.environ.get("AOA_WORKSPACE_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()

    cwd = Path.cwd().resolve()
    for candidate in [cwd, *cwd.parents]:
        if (candidate / "AOA_WORKSPACE_ROOT").exists():
            return candidate

    script_path = Path(__file__).resolve()
    for candidate in script_path.parents:
        if (candidate / "AOA_WORKSPACE_ROOT").exists():
            return candidate
        if candidate.name == "8Dionysus" and (candidate.parent / "AOA_WORKSPACE_ROOT").exists():
            return candidate.parent

    return Path("/srv/AbyssOS")


def candidate_scripts(root: Path) -> list[Path]:
    paths: list[Path] = []

    direct = os.environ.get("AOA_DECISIONS_MCP_SERVER")
    if direct:
        paths.append(Path(direct).expanduser())

    package_root = os.environ.get("AOA_DECISIONS_MCP_ROOT")
    if package_root:
        paths.append(Path(package_root).expanduser() / "scripts" / "aoa_decisions_mcp_server.py")

    for env_name in ("AOA_ABYSS_STACK_ROOT", "AOA_ABYSS_STACK_SOURCE", "AOA_SOURCE_ROOT"):
        value = os.environ.get(env_name)
        if value:
            paths.append(Path(value).expanduser() / PACKAGE_SCRIPT_REL)

    paths.extend(
        [
            Path.home() / "src" / "abyss-stack" / PACKAGE_SCRIPT_REL,
            root / "abyss-stack" / PACKAGE_SCRIPT_REL,
        ]
    )
    return paths


def main() -> int:
    root = workspace_root()
    os.environ.setdefault("AOA_WORKSPACE_ROOT", str(root))

    for script in candidate_scripts(root):
        resolved = script.resolve()
        if resolved.is_file():
            runpy.run_path(str(resolved), run_name="__main__")
            return 0

    searched = "\n".join(f"- {path}" for path in candidate_scripts(root))
    print(
        "Could not locate aoa-decisions-mcp server. Set AOA_ABYSS_STACK_ROOT, "
        "AOA_DECISIONS_MCP_ROOT, or AOA_DECISIONS_MCP_SERVER.\nSearched:\n" + searched,
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
