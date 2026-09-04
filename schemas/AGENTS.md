# AGENTS.md

## Guidance for `schemas/`

`schemas/` stores machine-readable contracts for `8Dionysus` audit, route, frontier, and projection surfaces. Schema edits are contract edits.

Keep `$schema`, required fields, enums, and compatibility expectations explicit. When a schema changes, update paired examples, generated outputs, tests, and downstream readers.

Schemas here describe entrypoint-owned surfaces. They do not define sibling repo semantics unless the owner repo explicitly imports that contract.

Run the relevant root routes in `../VALIDATION.md` for map, memory-map, and
repository checks, including `unittest discover`.
