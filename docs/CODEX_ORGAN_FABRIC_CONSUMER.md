# Codex Consumer for the OS Abyss Organ Fabric

This note defines the source-owned Codex consumer projection for OS Abyss
organs reached through MCP. It complements the portable Codex-plane render; it
does not replace the live deployment or make `8Dionysus` the owner of organ
runtime, admission, credentials, or domain meaning.

## Why a separate consumer projection exists

The legacy Codex configuration accumulated individual MCP registrations. A
2026-07-25 baseline observed ten active servers, 118 active tools, and 74,098
bytes of active tool catalog. Nine effective loopback registrations used one
shared bearer-token environment name and had no explicit allowlists or
timeouts.

That baseline is useful compatibility evidence, but it is not the intended
organ fabric:

- registration is not admission;
- one shared credential does not express owner or effect boundaries;
- a full always-loaded catalog spends context before an agent selects a route;
- a URL or green initialize result does not prove current schemas, grounded
  calls, owner acceptance, or rollback;
- removing a legacy registration before consumer-zero proof can break active
  clients.

The new projection is therefore profile-scoped, owner-separated, receipt-gated,
and deny-by-default.

## Authority map

| Surface | Owner | What it proves |
| --- | --- | --- |
| Codex consumer manifest, renderer, source fragment | `8Dionysus` | intended consumer shape and deterministic derivation |
| organ registry and admission state | `aoa-sdk` | typed registration state and admission evidence |
| MCP packages, loopback services, canaries | `abyss-stack` | runtime implementation and runtime receipts |
| domain meaning and acceptance | organ repository | semantic contract and owner review |
| credential issuance and live config apply | operator | deploy-local authority |

MCP is the access plane across these owners. It is not a replacement owner.

## Source surfaces

- `config/codex_plane/organ_fabric/codex_consumer_manifest.v1.json`
- `config/codex_plane/organ_fabric/current_consumer_observation.public.json`
- `scripts/render_codex_organ_fabric.py`
- `scripts/validate_codex_organ_fabric.py`
- `scripts/observe_codex_organ_fabric.py`
- `schemas/codex_organ_fabric_*_v1.json`
- `schemas/codex_consumer_registration_receipt_v1.json`
- `config/codex_plane/organ_fabric/generated/core-read.target.toml`
- `config/codex_plane/organ_fabric/generated/core-read.plan.json`

The observation is public-safe. It records configuration shape, never bearer
values. Each exact consumer receipt also records canonical observed inventory,
tool-schema, resource-catalog, and resource-template byte counts. Those are
context-economy measurements for the observed client surface, not proof that
every byte was inserted into one model prompt.

For one exact live registration, `observe_codex_organ_fabric.py` starts a fresh
Codex app-server client, reads the full MCP inventory that client initialized,
and emits a content-addressed consumer receipt to an operator-selected output
directory. It reads the public registration shape through `codex mcp get`; it
does not read bearer values or edit configuration. An optional direct tool call
uses an ephemeral Codex thread and records only argument and result digests.

```bash
python scripts/observe_codex_organ_fabric.py \
  --registration aoa_kag \
  --protocol-version 2025-11-25 \
  --call-tool kag_discover \
  --call-arguments '{"detail":"compact","owner":"aoa-kag"}' \
  --output-dir <private-receipt-root> \
  --organ-id aoa-kag \
  --overlay-output <private-overlay-fragment>
```

The protocol version is an explicit runtime binding because Codex app-server
currently exposes the initialized tools, resources, templates, server info,
and auth class but not the negotiated MCP protocol field. Central proof must
therefore cross-check the receipt's canonical schema digest against runtime
canary evidence for that exact protocol. The receipt alone is neither central
proof nor owner acceptance.

When both overlay flags are present, the issuer also writes a mode-`0600`
`abyss_stack_runtime_evidence_overlay_v1` fragment containing only the exact
consumer observation. `abyss-stack` may compose and carry that fragment, but
does not become its issuer.

## Profiles instead of one catalog

The manifest currently defines these mutually intentional routes:

| Profile | Purpose |
| --- | --- |
| `core-read` | KAG, stats, and decision navigation |
| `runtime-read` | `abyss-stack` and machine diagnostics |
| `memory-read` | durable memory and session evidence |
| `proof-read` | eval discovery and candidate shaping |
| `corpus-read` | authored Tree of Sophia corpus |
| `connectors-read` | bounded local connector evidence |
| `candidate` | explicitly prompted candidate-producing tools |

Every profile is capped at six registrations and 64 enabled tools. The full
catalog is forbidden as an always-loaded profile. Read and candidate contours
use different registration names, URLs, credential classes, environment
variables, and approval policy.

For `aoa-session-memory`, the admitted consumer shape enables only six
argument-bearing query, retrieval, and freshness tools. Exact known-session
briefs, manifests, indexes, and rehydration packets remain MCP resource
templates, so the consumer opens them on demand instead of loading broad tool
schemas or whole indexes into every task context. Its durable credential class
is `session-memory-read`; the longer bearer environment variable and systemd
credential names are delivery bindings, not policy identities.

## Admission gate

A selected registration renders only when all of these are present:

1. registry state `admitted`;
2. expected consumer schema digest;
3. registry admission receipt;
4. fresh consumer-schema observation receipt;
5. central proof receipt bound to the exact source, deploy, process, schema,
   consumer registration, and canary;
6. runtime canary receipt;
7. organ-owner acceptance receipt;
8. rollback receipt.

The whole selected profile must pass. A partially admitted profile renders
zero registrations, preventing a plausible-looking partial config from
becoming the accidental rollout unit.

`shadow`, `suspended`, `deprecated`, and `retired` records do not render.
Suspended legacy registrations are removed only after a distinct removal
receipt. Without it, the plan keeps the legacy route visible as a blocker.

## Derived plan actions

The deterministic plan uses these actions:

- `withhold`: source target is not eligible and no live removal is implied;
- `add`: admitted selected target is absent;
- `replace`: admitted selected target differs from the observation;
- `retain_exact`: the admitted target is already observed exactly;
- `retain_legacy_until_replacement_gates`: the existing route remains until
  replacement or consumer-zero gates close;
- `remove_after_receipt`: a suspended or retired route has explicit removal
  evidence;
- `investigate_unmanaged`: an observed registration has no source manifest
  record.

The renderer has no apply mode. `mutation_allowed=true` is plan evidence, not
permission to edit user-global or project Codex configuration.

## Current source posture

The current checked-in candidate is intentionally pre-admission. The original
shared-bearer baseline remains in catalog policy as historical comparison, but
the manifest and public observation now record the owner-scoped Codex 0.146.0
contour. The runtime-read profile includes the bounded
`stack_orchestration_inspect` read surface, but its live audit defect and source
fix remain rollout evidence rather than admission:

- 18 source registrations;
- ten observed owner-scoped registrations retained pending admission;
- eight absent targets withheld;
- zero rendered registrations;
- zero admitted schema digests or receipts;
- no authorized mutation;
- `tos_corpus` suspended.

The `aoa_kag` observation includes the full consumer schema digest and links to
a separate content-addressed live receipt outside source control. That receipt
does not by itself change the source manifest's shadow state.

The stack read and candidate registrations bind the runtime-owned credential
classes `abyss-stack-read` and `abyss-stack-candidate`. Their environment
variable names remain consumer wiring only; adding `-mcp-` to the credential
class would create identity drift from the stack runtime catalog and private
registry rather than a stronger isolation boundary.

This is a complete source contract and an incomplete rollout. It must not be
reported as live migration.

## Rendering and validation

```bash
python scripts/render_codex_organ_fabric.py
python scripts/render_codex_organ_fabric.py --check
python scripts/validate_codex_organ_fabric.py
python -m unittest tests.test_codex_organ_fabric
python -m unittest tests.test_observe_codex_organ_fabric
```

The output is a TOML fragment for review. It is not a replacement for
`~/.codex/config.toml` or `<workspace-root>/.codex/config.toml`.

## Future live rollout

After registry and runtime receipts exist, the operator-controlled rollout
must:

1. capture a fresh sanitized pre-change observation;
2. render one bounded profile and review its plan;
3. issue owner- and contour-specific credentials outside source control;
4. compose the fragment into the intended global or trusted-project layer;
5. start a fresh Codex process;
6. re-observe the effective registrations and exact tool schemas;
7. execute authorized, grounded canaries;
8. record owner acceptance or roll back;
9. prove consumer-zero before removing superseded legacy routes.

Codex MCP configuration fields in this source were exercised with Codex CLI
0.146.0 on 2026-08-01; the previous official-reference pass was for 0.145.0 on
2026-07-26.
Because Codex and MCP evolve quickly, the consumer fields and fresh-process
posture must be reverified immediately before live rollout.

## Claim boundary

A source manifest does not prove registry admission. A rendered TOML fragment
does not change a live config. A config entry does not prove process,
authentication, schema, call, freshness, acceptance, or rollback. A running
client does not prove that it hot-adopted a changed catalog.
