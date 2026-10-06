---
name: private-mcp-server-builds
description: "Use when building a private MCP server over existing business-system connectors: read-only by default, role-scoped, proposal-only writes."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [mcp, connectors, read-only, roles, proposals]
    related_skills: [build-execution-standard]
---

# Private MCP server builds (over existing connectors)

## When to Use
Designing, building or extending a private MCP server that wraps business systems the agent already reaches (`<shop-system>`, `<CRM>`, local read models, a notes vault).

Goal: one server that speaks the business's language, enforces business rules once in code, and never becomes a new write path or credential store. Load `build-execution-standard` for the build process; this skill covers the server design.

## Procedure
1. **Scope:** read the domain's documented data rules first. Do not duplicate a capability another server owns; compose with it (return a hint with exact arguments for the other server's tool).
2. **Server shape:** stdlib newline-delimited JSON-RPC 2.0 over stdio (`initialize`, `ping`, `tools/list`, `tools/call`, plus `resources/*` and `prompts/*` when useful), dispatch via a dict table, `tools/call` threaded so long calls do not block pings. Do not depend on the MCP SDK server API (it changes between versions); use the SDK *client* only in tests to prove compatibility over real stdio.
3. **Connectors by path, GET-only.** Load the existing connector module with `importlib.util.spec_from_file_location`, unmodified, lazily on first use, and call only its GET helper (with any shared rate-limit/priority budget applied around each call). The server never reads `.env` itself; connectors' own loaders find credentials. Missing lib or credential error -> source status `not_configured`/`error`, never a crash.
4. **Read model first, live fallback.** Use the local read model when fresh and complete; fall back to live reads when stale or when the caller forces `live`. Label `source_used`.
5. **One envelope for every tool:** `ok, tool, role, generated_at, sources[{name,status,age_seconds,complete}], trust (current|partial|withheld), write_performed:false, data|error, next_action`. Totals are `null` + `trust: withheld` + plain reason when a source is stale/incomplete; never show 0 for unknown. Per-source degradation is labelled, not hidden.
6. **Business rules in one module** (`rules.py`), each tested with a healthy control and a rejection case. Typical rules: money as integer cents, archived records excluded, receivables counted only from explicitly open states with a positive balance, a payment signal only from positive paid amounts or non-empty payment records, dedupe by ID, and all date bucketing in one explicit timezone (`<business-timezone>`). Prefer privacy-safe lookups (name, order number, record ID) over phone lookups, and match CRM contacts by exact email then exact full name (more than one match = `ambiguous`, no data).
7. **Roles from server env, never from tool args** (`<PREFIX>_ROLE` at startup). Role registry maps role -> tools; tools outside the role are absent from `tools/list` AND denied on call; a field filter strips money/customer fields for low-trust roles; unknown role fails closed to a health tool only. One server process per role/profile. Non-owner roles get no per-customer money anywhere (drop whole money subtrees, not just named fields), and aggregate views must not pair bucket totals with individual record rows for non-owners, since a one-row bucket reveals that balance.
7a. **Redact by value, not only key.** CRM display names are often a phone or email. Apply a strict label rule (7+ digits, `@`, URL -> "Unnamed contact") to person/contact name fields, plus a final recursive value scan for phone/email-shaped strings. Product or asset labels use only the phone-PATTERN check; a digit-count rule hides legitimate years and model numbers (e.g. "2022 Model 500 Pro").
8. **Writes are proposals.** The server prepares an action payload matching the existing approval executor's schema exactly (mirror its validator; capture live `expected_before`; refuse no-ops, archived, ambiguous or missing targets), returns a human preview + digest + the exact register command, and logs the proposal locally. Execution, approval cards and readback stay in the existing executor. Never run or import the executor from server code.
9. **Audit + private state:** JSONL row per call (tool, role, args HMAC-SHA256 with a random per-install 0600 key, ok, error, elapsed) with no argument values, names, phones or money; a plain sha256 of low-entropy args (order numbers, first names) is reversible by enumeration. Data dir 0700, files 0600.
9a. **Transport robustness:** cap input lines (~1 MB) before parsing and catch every decode error (deep nesting raises `RecursionError`, not `ValueError`), replying -32700 and continuing to serve.
10. **Knowledge/vault access:** explicit allowlist of business lanes; deny personal, raw, drafts, archive and other-business paths; resolve symlinks and reject root escape.
11. **Install is an owner gate.** Ship `docs/INSTALL.md` with the exact `mcp_servers.<name>` block (venv python, `-m <pkg>`, `PYTHONPATH`, role, data dir, timeouts), backup + `/reload-mcp` + read-only smoke checklist + rollback. Do not edit the agent config without the owner's go. On go:
    - Back up the config file (`cp -p <config.yaml> <config.yaml>.bak.<name>-<ts>`), insert the block programmatically and confirm with `yaml.safe_load` that every prior server is still present.
    - MCP stdio children get a filtered env: pass credentials as `${VAR}` interpolation in the block's `env` (e.g. `SERVICE_API_KEY: ${SERVICE_API_KEY}`); never paste values.
    - `hermes mcp test <name>` (or your harness's equivalent) must list every tool; tools appear only in sessions started afterwards.
    - Read-only live smoke through the same launch path: each tool once, assert zero phone/email patterns in the combined output, check audit perms. Report live-verified tools separately from offline-only ones.
12. **Rollout to consumers.**
    - Reports: never replace an existing report directly. Add a no-agent shadow job delivered a few minutes after the current one that calls the server with credentials stripped (local read model only), at most a few lines, non-zero exit on failure, and "can't trust" instead of any number from a withheld source. The owner compares for a few days, then decides the switch.
    - Approval cards: a host script chains the propose tool (live GET) -> executor `register` -> executor `card`, printing an inert review card for the owner. Practice with the connector's dry-run mode first. Use a change the owner actually wants as the first live card.

## Build dispatch (when delegating to builder agents)
- Write shared material once in `COMMON.md` (fixed context, rules, gates, commit, report format) and per-milestone `M<n>.scope.md`; assemble with `{ cat M<n>.scope.md; echo; cat COMMON.md; } > M<n>.md` and keep `M<n>.orig.md`. A COMMON fix then reaches all remaining milestones by re-assembling.
- Point the builder at any sibling template repo with exact file names, marked read-never-edit.
- Run every gate yourself at base before freezing the brief, and put the working runner form in the gate.
- Forbid copying package caches into the repo.
- Verify any behavior a brief says to copy actually exists first; a deliberately disabled feature makes the builder BLOCK.
- When a later rule changes behavior an earlier milestone's tests pin, say exactly which assertions may change and which stay; otherwise the builder correctly BLOCKs on the contradiction.
- After the last milestone: one adversarial review on an exact SHA (pre-create its scratch copy yourself with `git archive <sha> | tar -x -C <dir>`), parent reruns its probes to confirm RED, then one remediation brief that copies the probe file in byte-for-byte unchanged. Then the live smoke, which typically finds over-correction from the privacy fix.
- New local-only repo: `git init -b main`, empty `init` commit as BASE, repo-local user.name/email, brief says no remote/never push. Creating a hosted repo is an owner decision. With no CI, the parent reruns the full gate chain on each milestone commit.

## Testing gates
- Fully offline: fakes/injected readers, synthetic tmp data dirs (build real read-model stores with the real store class when possible), a test that blocks `socket.socket.connect` and still passes.
- Real stdio round-trip with the MCP SDK client (initialize, list, call one tool; resources/prompts if offered).
- Safety scans: no write helpers referenced (POST/PUT/PATCH/DELETE helpers, `request("POST"...)`), reader classes expose no write methods, no-PII scan (synthetic `555-01xx` phones, `@example.com` emails only; print file:line, never the match).
- If the agent's venv lacks pytest, run it ephemerally (e.g. `uv run --no-project --with pytest python -m pytest -q tests`) with TMPDIR in a scratch directory.

## Pitfalls
- Server-side roles scope surface and fields; they are not the agent's write gate. Request context does not cross into the MCP subprocess, so the host-side capability gate stays authoritative.
- Never trust convenience booleans or summary totals (e.g. a `paid` flag) as payment evidence without checking the underlying records; they can be vacuously true or stale.
- Never return CRM message bodies/transcripts; status only (last date, direction, unread).
- Verify that a vendor list endpoint actually honors each filter parameter before relying on it; some silently ignore filters and return everything.
- A list endpoint with no total/hasMore cannot prove completeness, so counts from it stay withheld; fix in the source (or its replacement), not by guessing.
- Treat missing status fields as unknown, not as a specific state; defaulting them inflates counts.
- Do not offer a state transition as a proposal until you know all of its side effects in the source system and the approval path can arm it safely.
