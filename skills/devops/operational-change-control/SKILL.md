---
name: operational-change-control
description: "Use when changing production systems, crons, configs, or operational workflows. Plan, risk, rollback, approval, verify, close out."
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [operations, change-control, safety, verification]
    related_skills: [operational-backups, build-execution-standard]
---

# Operational Change Control

## When to Use

For the orchestrator profile handling configuration, runtime, automation, gateway, cron, database, deployment, permissions, or infrastructure changes. Installation of this guidance does not authorize any of those actions. Apply existing profile boundaries and owner approvals; do not distribute or change other specialists without explicit scope.

## Core contract

Safety, accuracy and verified execution first. Audit → exact approval → bounded change → exact readback. Prefer the smallest relevant repair and existing supported tooling. No new architecture, broad cleanup or gate weakening merely to finish faster. The presence of a tool, a successful test, an earlier similar approval, or an advisory helper classification is never mutation authority.

## 1. Audit and choose the correct lane

- **Read-only diagnosis / documentation:** inspect current state, report uncertainty; no live repair, credential loading, broad scans or force-runs by implication.
- **Routine reversible change:** exact touched-file backup, targeted edit, syntax/semantic checks and readback. Do not apply a full release ritual to harmless prose.
- **Update/release/production cutover:** freeze source/installed artifact/runtime identities, all local carries, exact activation/rollback executor, capacity and recovery proof; preserve required security and full integration gates.
- **Recovery/retirement/cleanup:** follow operational-backups plus the domain runbook. Failure does not authorize bypass, destructive retries, deleting original data or replacing verified safety controls.

Before editing, record goal/non-goals, exact affected surfaces and owners, trust/data boundaries, commands and side effects, expected outcome, rollback, verification, and completion budget. Confirm actual HOME/HERMES_HOME/cwd/interpreters and inspect relevant live helper/PID/lock/state before starting. A process absent from Hermes' process list may still run under launchd or another session; never create duplicate backups/migrations/restarts.

## 2. Approval and rollback

Present plan, risks, exact scope and rollback; obtain the owner's go unless the exact action is already green-lit in the current conversation. An explicit denial, expiry or approval timeout is a hard stop: do not rephrase, re-route, detach or switch tools to bypass it. An executive profile's operational authority does not grant default infrastructure or cross-profile mutation authority.

Back up every touched pre-change live/source file before the first edit; include newly added scope before editing it. Keep owner-only rollback evidence outside source trees, exact inventory and hashes, prior mode/ownership and source identity. Avoid secrets in ordinary evidence. Secret-bearing full recovery packs need explicit scope and independent authenticated encryption as required by operational-backups. A Git stash/worktree is not the sole backup.

## 3. Execute narrowly

Use supported CLI/API paths and targeted patches. Pin the approved profile, artifact, target and candidate; revalidate immediately before mutation. Serialize shared-file/runtime writers; do not install from a moving checkout. Capture true exit codes and partial effects. Do not retry an ambiguous external mutation; reconcile exact source/readback and retain UNKNOWN if certainty is unavailable.

No unconditional restart after documentation/config edits. Determine the actual reload boundary first. For approved gateway restarts, use the existing guarded handoff/restart workflow; never evade its process-lineage or restart-budget refusal. Preserve active-session handoff, check helper collisions, canary/stability and final readback. Restart only the approved target; keep default last when a separately approved fleet sequence requires it. No terminal-triggered lock deletion based solely on guessed stale ownership.

For updates, separate routine upstream intake, local carry reconciliation and long-term DR/test-harness repair. Rehearse the exact executor with actual runtime versions/package scripts and required production-size rollback proof before downtime. Do expensive installs/full suites/scans/integrity checks before downtime; do not omit them. A changed approved upstream target is a new release cycle, not a free micro-edit. Extra reviews require actual blockers, not speculative polish.

For multi-profile configuration-schema migrations, generate outputs through the supported migrator on fresh copies of the exact current preimages, bind per-profile pre/post hashes and approved semantic paths, and activate only those exact outputs. If pathname writers are possible, use same-filesystem atomic swaps so the displaced live object is retained in owner-only transaction evidence; succeed only when it equals the bound preimage. Unknown/concurrent bytes must never be deleted or overwritten: fail explicitly, preserve the contested object, exclude only that profile, and roll back every uncontested touched profile. Rollback must also avoid remove-then-install gaps, and crash recovery must reconcile durable journaled pre/post/stage states without claiming impossible arbitrary-writer liveness.

## 4. Verify and report truth

For read-only PostgreSQL diagnostics through a session pooler, establish transaction read-only explicitly (for example psycopg `conn.read_only=True` before the first statement) and assert `SHOW transaction_read_only` is `on` before reading business data. Connection startup options alone may not take effect through the pooler; stop on mismatch rather than proceeding under an assumed read-only contract. Use an already-authorized diagnostic identity; never grant table access merely to make a probe work.

Read back the exact changed system, not only the payload or successful API response. Assert intended differences and protected unchanged surfaces. Distinguish source edited, installed, runtime verified and remote mirrored; none implies another. Use `templates/current-state.md` as a compact authoritative record linked to real evidence. Records and prose are claims, not a replacement for source inspection.

Every current-state claim needs owner, scope, observed time, source and artifact identity, verification coverage, unknowns and supersession. A newer plan does not supersede verified runtime state. Keep old decisions/history explicitly historical; use the permitted vault draft lane for locked published notes. Never write 'executed' before execution. No secrets/config dumps in the vault.

Use `templates/mission-handoff.md` at milestones and `references/result-reconciliation.md` for delayed child results. Required reviewers stay tracked until resolved; an old security finding is a signal to reproduce against current source even if the old verdict is superseded. A late reproducible HOLD reopens a release. Preserve evidence, contain if needed, remediate, and rerun required gates.

Conclude with actual changes, exact tests/readbacks and their limits, remaining owner gates, backup/rollback and source/mirror status. No live mutation in a reporting-only pass. No result or stale metadata is UNKNOWN, not healthy. Close once approved acceptance passes; no recurring audit or service unless separately requested.

## Selective domain guidance

- `operational-backups` — consistent recovery packs, encryption, restore proof, retention and exact deletion gates.
- `build-execution-standard` — risk-proportionate implementation, independent workers and exact-candidate evidence.
- `references/reporting-evidence-hygiene.md` — distinguish incidents, repeated reports, historical errors and actionable next steps without reducing monitoring coverage.

Current scope, current user approval and current safety rules supersede old permission-expanding recipes. If a detailed example conflicts, stop and resolve it rather than treating the old example as authority.
