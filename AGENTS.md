Project: WorldCodex Art

This repository is a Python Typer-based CLI tool for generating AI images using structured world data exported from WorldCodex.

Codex acts as an implementation agent. Architectural decisions, CLI design, and world schema are already established.

1. Core Mission

WorldCodex Art:

Loads a structured world_bible.json

Allows users to browse world entities (places, characters, motifs, etc.)

Assembles concise, high-signal image prompts

Sends prompts to a pluggable image provider API

Produces reproducible, testable outputs

The system favors explicit structure over freeform prose.

2. Hard Rules (DO NOT VIOLATE)
2.1 CLI Stability

❌ Do NOT rename existing commands

❌ Do NOT remove existing commands or flags

❌ Do NOT change CLI syntax without explicit instruction

❌ Do NOT invent new commands unless requested

All CLI commands must remain backward-compatible.

2.2 Project Structure (MANDATORY)

You must respect the existing layout:

worldcodex_art/
  cli/          # Typer CLI commands
  core/         # World loading, prompt building, config, models
  providers/    # Image provider implementations
tests/


Rules:

All Typer apps must export a top-level variable named app

CLI modules live in worldcodex_art/cli/

Core logic never lives in CLI files

Providers must not import CLI code

2.3 World Data Authority

world_bible.json is authoritative

world_bible.md is fallback only

Schema version must remain:

worldcodex.world_bible.v1


Do not modify schema without explicit approval

World entities are referenced by stable IDs (snake_case).

3. Prompt Construction Rules
3.1 Do NOT dump raw prose

Never include the entire markdown bible in prompts

Use structured prompt snippets only

3.2 Prompt assembly must:

Include global world identity

Include only selected entities (place, character, motif, etc.)

Merge negative prompts cleanly

De-duplicate negative terms

Keep prompts compact and focused

3.3 Subject placement

The user’s subject text must appear near the end of the prompt.

4. Image Provider Rules

Providers must implement a common interface

Providers are replaceable

OpenAI is only one possible backend

No provider-specific logic in CLI code

Providers must never read config files directly

Mock providers must be used for tests.

5. Testing Requirements (NON-NEGOTIABLE)

Every new feature requires tests.

5.1 Minimum tests per change

At least one unit test

At least one CLI smoke test using Typer.CliRunner

5.2 Tests must verify:

CLI commands are registered

Unknown IDs produce clean errors

Prompt assembly uses structured data

JSON schema validation works

Providers are called with correct arguments

If tests are missing, the task is incomplete.

6. Error Handling Philosophy

Fail fast

Error messages must be:

human readable

explicit about what failed

actionable (tell the user what to do)

Avoid stack traces for user-facing CLI errors.

7. Coding Style Guidelines

Prefer explicit code over clever abstractions

Small functions > large ones

Type hints everywhere practical

No magic globals

No silent fallbacks

Clarity > DRY.

8. Allowed Refactors

Codex MAY:

Extract helpers if duplication becomes obvious

Add indexes or caches for performance

Improve error messages

Add tests for existing code

Codex MAY NOT:

Reorganize folders

Introduce new frameworks

Change config file formats

Replace Typer with another CLI library

9. When Requirements Are Ambiguous

STOP.

Ask for clarification before coding.

Do not guess intent.

10. Preferred Workflow

User describes desired behavior

User (or Codex) writes a short test plan

Codex implements code + tests

Tests must pass

Iterate

11. Current High-Priority Goals

In order:

Solidify JSON-based world browsing (world list, world show)

Harden prompt assembly tests

Add OpenAI image provider

Add gallery / prompt provenance tracking

Add autocomplete / discoverability improvements

12. Definition of “Done”

A task is complete when:

Code is implemented

Tests exist and pass

CLI behavior matches specification

No existing commands are broken

Codex is a tool, not an author.
Follow the structure. Respect the world.
Ask when unsure.