#!/usr/bin/env python3
"""Issue a public-safe receipt for one live Codex MCP registration.

The observer uses Codex's app-server protocol so the inventory is seen by a
fresh Codex client.  It never reads bearer-token values and never mutates Codex
configuration.  An optional direct MCP tool call can prove that the same fresh
client can use the initialized registration; only argument and result digests
enter the receipt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import selectors
import subprocess
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator, FormatChecker


REPO_ROOT = Path(__file__).resolve().parents[1]
RECEIPT_SCHEMA = REPO_ROOT / "schemas" / "codex_consumer_registration_receipt_v1.json"
DEFAULT_PROTOCOL_VERSION = "2025-11-25"
ISSUER_OWNER = "8Dionysus"


def canonical_json_bytes(payload: Any) -> bytes:
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def canonical_digest(payload: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def _utc_text(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _json_object(text: str, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label} did not return JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{label} did not return a JSON object")
    return payload


def read_registration(codex_binary: str, registration_name: str, timeout: float) -> dict[str, Any]:
    completed = subprocess.run(
        [codex_binary, "mcp", "get", registration_name, "--json"],
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"codex mcp get failed: {detail}")
    return _json_object(completed.stdout, "codex mcp get")


def read_consumer_version(codex_binary: str, timeout: float) -> str:
    completed = subprocess.run(
        [codex_binary, "--version"],
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"codex --version failed: {completed.stderr.strip()}")
    parts = completed.stdout.strip().split()
    if not parts:
        raise RuntimeError("codex --version returned an empty response")
    return parts[-1]


class AppServerClient:
    """Small bounded JSONL client for `codex app-server --stdio`."""

    def __init__(self, codex_binary: str, timeout: float) -> None:
        self.timeout = timeout
        self.process = subprocess.Popen(
            [codex_binary, "app-server", "--stdio"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self._next_id = 1
        self._stderr_tail: list[str] = []

    def __enter__(self) -> "AppServerClient":
        return self

    def __exit__(self, *_: object) -> None:
        if self.process.stdin is not None:
            self.process.stdin.close()
        try:
            self.process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=2)

    def _send(self, payload: Mapping[str, Any]) -> None:
        if self.process.stdin is None:
            raise RuntimeError("app-server stdin is unavailable")
        self.process.stdin.write(canonical_json_bytes(payload).decode("utf-8") + "\n")
        self.process.stdin.flush()

    def notify(self, method: str, params: Mapping[str, Any]) -> None:
        self._send({"method": method, "params": dict(params)})

    def request(self, method: str, params: Mapping[str, Any]) -> dict[str, Any]:
        request_id = self._next_id
        self._next_id += 1
        self._send({"id": request_id, "method": method, "params": dict(params)})
        deadline = time.monotonic() + self.timeout
        selector = selectors.DefaultSelector()
        assert self.process.stdout is not None
        assert self.process.stderr is not None
        selector.register(self.process.stdout, selectors.EVENT_READ, "stdout")
        selector.register(self.process.stderr, selectors.EVENT_READ, "stderr")
        try:
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    tail = " | ".join(self._stderr_tail[-5:])
                    raise TimeoutError(f"app-server request timed out: {method}; stderr={tail}")
                events = selector.select(remaining)
                if not events and self.process.poll() is not None:
                    raise RuntimeError(
                        f"app-server exited during {method}: "
                        + " | ".join(self._stderr_tail[-5:])
                    )
                for key, _ in events:
                    line = key.fileobj.readline()
                    if not line:
                        continue
                    if key.data == "stderr":
                        self._stderr_tail.append(line.strip())
                        self._stderr_tail = self._stderr_tail[-20:]
                        continue
                    message = _json_object(line, "codex app-server")
                    if message.get("id") != request_id:
                        continue
                    if "error" in message:
                        raise RuntimeError(f"app-server {method} failed: {message['error']}")
                    result = message.get("result")
                    if not isinstance(result, dict):
                        raise RuntimeError(f"app-server {method} returned no object result")
                    return result
        finally:
            selector.close()


def initialize_app_server(client: AppServerClient) -> None:
    client.request(
        "initialize",
        {
            "clientInfo": {
                "name": "8dionysus_codex_mcp_observer",
                "title": "8Dionysus Codex MCP Observer",
                "version": "1.0.0",
            },
            "capabilities": {"experimentalApi": True},
        },
    )
    client.notify("initialized", {})


def list_server_status(client: AppServerClient, registration_name: str) -> dict[str, Any]:
    cursor: str | None = None
    while True:
        params: dict[str, Any] = {"detail": "full", "limit": 100}
        if cursor is not None:
            params["cursor"] = cursor
        result = client.request("mcpServerStatus/list", params)
        data = result.get("data")
        if not isinstance(data, list):
            raise RuntimeError("mcpServerStatus/list returned invalid data")
        for item in data:
            if isinstance(item, dict) and item.get("name") == registration_name:
                return item
        cursor = result.get("nextCursor")
        if not isinstance(cursor, str) or not cursor:
            break
    raise RuntimeError(f"fresh Codex client did not initialize registration {registration_name}")


def canonical_inventory(status: Mapping[str, Any], protocol_version: str) -> dict[str, Any]:
    tools = status.get("tools")
    resources = status.get("resources")
    templates = status.get("resourceTemplates")
    if not isinstance(tools, dict) or not isinstance(resources, list) or not isinstance(templates, list):
        raise ValueError("full MCP status is missing tools, resources, or resource templates")
    tool_values = list(tools.values())
    if any(not isinstance(item, dict) or not isinstance(item.get("name"), str) for item in tool_values):
        raise ValueError("MCP tool inventory contains an invalid tool")
    if any(not isinstance(item, dict) or not isinstance(item.get("uri"), str) for item in resources):
        raise ValueError("MCP resource inventory contains an invalid resource")
    if any(
        not isinstance(item, dict) or not isinstance(item.get("uriTemplate"), str)
        for item in templates
    ):
        raise ValueError("MCP resource-template inventory contains an invalid template")
    return {
        "protocol_version": protocol_version,
        "tools": sorted(tool_values, key=lambda item: item["name"]),
        "resources": sorted(resources, key=lambda item: item["uri"]),
        "resource_templates": sorted(templates, key=lambda item: item["uriTemplate"]),
        "prompts": [],
    }


def run_tool_call(
    client: AppServerClient,
    registration_name: str,
    tool_name: str,
    arguments: Mapping[str, Any],
    cwd: Path,
) -> dict[str, Any]:
    started = client.request(
        "thread/start",
        {"cwd": str(cwd.resolve()), "ephemeral": True},
    )
    thread = started.get("thread")
    if not isinstance(thread, dict) or not isinstance(thread.get("id"), str):
        raise RuntimeError("thread/start did not return a thread id")
    result = client.request(
        "mcpServer/tool/call",
        {
            "server": registration_name,
            "tool": tool_name,
            "arguments": dict(arguments),
            "threadId": thread["id"],
        },
    )
    return {
        "tool_name": tool_name,
        "arguments_digest": canonical_digest(arguments),
        "result_digest": canonical_digest(result),
        "is_error": bool(result.get("isError", False)),
        "content_item_count": len(result.get("content", []))
        if isinstance(result.get("content"), list)
        else 0,
    }


def build_receipt(
    registration: Mapping[str, Any],
    status: Mapping[str, Any],
    consumer_version: str,
    protocol_version: str,
    observed_at: datetime,
    expires_at: datetime,
    call_observation: Mapping[str, Any] | None,
) -> dict[str, Any]:
    transport = registration.get("transport")
    if not isinstance(transport, dict) or transport.get("type") != "streamable_http":
        raise ValueError("only streamable_http Codex registrations are supported")
    if registration.get("name") != status.get("name"):
        raise ValueError("Codex configuration and app-server status name mismatch")
    if registration.get("enabled") is not True:
        raise ValueError("consumer receipt requires an enabled Codex registration")
    if transport.get("http_headers") or transport.get("env_http_headers"):
        raise ValueError("header-bearing registrations are not public-safe for this issuer")
    inventory = canonical_inventory(status, protocol_version)
    schema_digest = canonical_digest(inventory)
    tools = inventory["tools"]
    resources = inventory["resources"]
    templates = inventory["resource_templates"]
    server_info = status.get("serverInfo")
    if server_info is not None and not isinstance(server_info, dict):
        raise ValueError("app-server returned invalid serverInfo")

    body: dict[str, Any] = {
        "schema_version": "8dionysus_codex_consumer_registration_receipt_v1",
        "issuer_owner": ISSUER_OWNER,
        "consumer_id": "codex",
        "consumer_version": consumer_version,
        "app_server_protocol": "v2",
        "observed_at": _utc_text(observed_at),
        "expires_at": _utc_text(expires_at),
        "registration": {
            "registration_name": registration["name"],
            "enabled": True,
            "transport_type": transport["type"],
            "url": transport.get("url"),
            "bearer_token_env_var": transport.get("bearer_token_env_var"),
            "enabled_tools": registration.get("enabled_tools"),
            "disabled_tools": registration.get("disabled_tools"),
            "startup_timeout_sec": registration.get("startup_timeout_sec"),
            "tool_timeout_sec": registration.get("tool_timeout_sec"),
            "auth_status": status.get("authStatus"),
            "server_info": server_info,
        },
        "schema_observation": {
            "method": "mcpServerStatus/list",
            "detail": "full",
            "protocol_versions": [protocol_version],
            "protocol_basis": "explicit_runtime_protocol_bound_into_observed_inventory",
            "schema_digest": schema_digest,
            "tool_count": len(tools),
            "tool_names": [item["name"] for item in tools],
            "resource_count": len(resources),
            "resource_uris": [item["uri"] for item in resources],
            "resource_template_count": len(templates),
            "resource_template_uris": [item["uriTemplate"] for item in templates],
            "prompt_count": 0,
        },
        "call_observation": dict(call_observation) if call_observation is not None else None,
        "secrets_included": False,
        "claim_limits": [
            "The receipt records one fresh Codex client observation and no credential values.",
            "The schema digest covers canonical full inventory plus the explicitly bound runtime protocol.",
            "A successful direct call proves client use of this registration, not semantic owner acceptance.",
            "The receipt does not prove registry admission, central proof, rollback, or live config mutation.",
            "The registration expires as evidence at expires_at and must not be reused as current afterward.",
        ],
    }
    registration_subject = {
        "issuer_owner": body["issuer_owner"],
        "consumer_id": body["consumer_id"],
        "consumer_version": body["consumer_version"],
        "observed_at": body["observed_at"],
        "registration": body["registration"],
        "schema_observation": body["schema_observation"],
        "call_observation": body["call_observation"],
    }
    subject_digest = canonical_digest(registration_subject).removeprefix("sha256:")
    body["registration_ref"] = (
        f"consumer-registration://8Dionysus/codex/{registration['name']}/{subject_digest}"
    )
    body["receipt_digest"] = canonical_digest(body)
    validate_receipt(body)
    return body


def validate_receipt(receipt: Mapping[str, Any]) -> None:
    schema = _json_object(RECEIPT_SCHEMA.read_text(encoding="utf-8"), str(RECEIPT_SCHEMA))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(receipt), key=lambda item: list(item.absolute_path))
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        raise ValueError(f"receipt schema at {location}: {error.message}")
    unsigned = dict(receipt)
    claimed_digest = unsigned.pop("receipt_digest")
    if canonical_digest(unsigned) != claimed_digest:
        raise ValueError("receipt_digest does not match canonical receipt content")
    observed_at = datetime.fromisoformat(str(receipt["observed_at"]).replace("Z", "+00:00"))
    expires_at = datetime.fromisoformat(str(receipt["expires_at"]).replace("Z", "+00:00"))
    if expires_at <= observed_at:
        raise ValueError("expires_at must follow observed_at")
    schema_observation = receipt["schema_observation"]
    for count_key, values_key in (
        ("tool_count", "tool_names"),
        ("resource_count", "resource_uris"),
        ("resource_template_count", "resource_template_uris"),
    ):
        if schema_observation[count_key] != len(schema_observation[values_key]):
            raise ValueError(f"{count_key} does not match {values_key}")
    registration_subject = {
        "issuer_owner": receipt["issuer_owner"],
        "consumer_id": receipt["consumer_id"],
        "consumer_version": receipt["consumer_version"],
        "observed_at": receipt["observed_at"],
        "registration": receipt["registration"],
        "schema_observation": receipt["schema_observation"],
        "call_observation": receipt["call_observation"],
    }
    expected_subject_digest = canonical_digest(registration_subject).removeprefix("sha256:")
    if not str(receipt["registration_ref"]).endswith("/" + expected_subject_digest):
        raise ValueError("registration_ref does not match canonical registration subject")
    if receipt["call_observation"] is not None and receipt["call_observation"]["is_error"]:
        raise ValueError("a failed direct MCP call cannot issue a usable consumer receipt")


def write_receipt(receipt: Mapping[str, Any], output_dir: Path) -> Path:
    registration_name = receipt["registration"]["registration_name"]
    digest = str(receipt["receipt_digest"]).removeprefix("sha256:")
    destination = output_dir.expanduser().resolve() / registration_name / f"{digest}.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(receipt, ensure_ascii=False, indent=2) + "\n"
    if destination.exists() and destination.read_text(encoding="utf-8") != text:
        raise ValueError(f"content-addressed receipt collision at {destination}")
    destination.write_text(text, encoding="utf-8")
    destination.chmod(0o600)
    return destination


def build_stack_overlay(receipt: Mapping[str, Any], organ_id: str) -> dict[str, Any]:
    """Transport the consumer-issued claim into the stack overlay contract."""

    registration_ref = receipt["registration_ref"]
    evidence = {
        "state": "exact",
        "observed_at": receipt["observed_at"],
        "expires_at": receipt["expires_at"],
        "evidence_refs": [
            {
                "owner": receipt["issuer_owner"],
                "evidence_ref": registration_ref,
                "revision": receipt["receipt_digest"],
                "observed_at": receipt["observed_at"],
                "expires_at": receipt["expires_at"],
            }
        ],
        "reason_codes": [],
    }
    return {
        "schema_version": "abyss_stack_runtime_evidence_overlay_v1",
        "generated_at": receipt["observed_at"],
        "expires_at": receipt["expires_at"],
        "contains_secrets": False,
        "subjects": [
            {
                "organ_id": organ_id,
                "policy_family": "read",
                "consumers": [
                    {
                        "consumer_id": receipt["consumer_id"],
                        "registration_ref": registration_ref,
                        "registered": True,
                        "observed_schema_digest": receipt["schema_observation"][
                            "schema_digest"
                        ],
                        "observed_protocol_versions": receipt["schema_observation"][
                            "protocol_versions"
                        ],
                        "evidence": evidence,
                    }
                ],
            }
        ],
    }


def write_private_json(payload: Mapping[str, Any], destination: Path) -> Path:
    path = destination.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    path.chmod(0o600)
    return path


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registration", required=True)
    parser.add_argument("--protocol-version", default=DEFAULT_PROTOCOL_VERSION)
    parser.add_argument("--codex-binary", default="codex")
    parser.add_argument("--timeout-sec", type=float, default=90.0)
    parser.add_argument("--ttl-hours", type=int, default=24)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--organ-id")
    parser.add_argument("--overlay-output", type=Path)
    parser.add_argument("--call-tool")
    parser.add_argument("--call-arguments", default="{}")
    parser.add_argument("--call-cwd", type=Path, default=Path.cwd())
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.timeout_sec <= 0:
        raise ValueError("timeout must be positive")
    if not 1 <= args.ttl_hours <= 168:
        raise ValueError("ttl-hours must be between 1 and 168")
    call_arguments = _json_object(args.call_arguments, "--call-arguments")
    if args.call_tool is None and call_arguments:
        raise ValueError("non-empty --call-arguments requires --call-tool")
    if (args.organ_id is None) != (args.overlay_output is None):
        raise ValueError("--organ-id and --overlay-output must be supplied together")

    registration = read_registration(args.codex_binary, args.registration, args.timeout_sec)
    consumer_version = read_consumer_version(args.codex_binary, args.timeout_sec)
    observed_at = datetime.now(timezone.utc).replace(microsecond=0)
    with AppServerClient(args.codex_binary, args.timeout_sec) as client:
        initialize_app_server(client)
        status = list_server_status(client, args.registration)
        call_observation = None
        if args.call_tool is not None:
            call_observation = run_tool_call(
                client,
                args.registration,
                args.call_tool,
                call_arguments,
                args.call_cwd,
            )
    expires_at = observed_at + timedelta(hours=args.ttl_hours)
    receipt = build_receipt(
        registration,
        status,
        consumer_version,
        args.protocol_version,
        observed_at,
        expires_at,
        call_observation,
    )
    destination = write_receipt(receipt, args.output_dir)
    overlay_destination = None
    if args.overlay_output is not None:
        overlay_destination = write_private_json(
            build_stack_overlay(receipt, args.organ_id),
            args.overlay_output,
        )
    print(f"receipt_path={destination}")
    print(f"receipt_digest={receipt['receipt_digest']}")
    print(f"registration_ref={receipt['registration_ref']}")
    print(f"schema_digest={receipt['schema_observation']['schema_digest']}")
    print(f"direct_call_observed={str(call_observation is not None).lower()}")
    if overlay_destination is not None:
        print(f"overlay_path={overlay_destination}")
    print("secrets_included=false")
    print("live_config_mutated=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
