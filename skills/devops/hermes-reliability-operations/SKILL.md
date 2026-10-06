---
name: hermes-reliability-operations
description: "Use when building an SRE/reliability lane for an agent fleet: deterministic health checks, watchdogs, script-only alerts, inventory drift detection."
version: 1.0.4
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, reliability, sre, ops, watchdogs, cron, launchd, profiles, fleet]
    related_skills: [operational-change-control]
---

# Hermes Reliability Operations

Use this skill when the owner asks to bulletproof Hermes, create or operate an IT/SRE profile, move infrastructure/security crons into a reliability lane, add watchdogs, or ensure new profiles/services/processes are automatically considered for monitoring.

## Core principle

The ops/IT profile is a reliability operator, not an unrestricted admin.

It should:

- discover fleet state automatically
- detect drift and failure quickly
- keep deterministic reports and local state
- self-heal only narrowly approved low-risk cases
- escalate risky changes to the orchestrator/owner with evidence

It should not silently become the owner of business workflows, customer communications, credentials, provider settings, gateway allowlists, or cross-profile governance authority.

## Recommended architecture

1. **Dedicated `ops` profile**
   - Minimal isolated config.
   - No copied business/API secrets by default.
   - Gateway stopped unless there is a deliberate need.
   - SOUL.md states strict read-only/default-safe boundaries.

2. **Deterministic fleet health script**
   - Lives under `<ops-profile-home>/scripts/`.
   - Uses pinned real fleet root when auditing all profiles, not profile-scoped `Path.home()`.
   - Writes JSON/Markdown reports under `<ops-profile-home>/reports/`.

3. **Independent launchd watchdog**
   - Runs outside Hermes cron so it can detect Hermes cron failures.
   - Healthy run prints nothing or writes only local logs.
   - Critical/new-inventory output is concise and actionable.

4. **Script-only Hermes crons**
   - Daily full report: no-agent, delivered to origin.
   - Critical watchdog: no-agent, frequent, silent on empty stdout.

5. **Monitor manifests**
   - Put explicit endpoint checks in `<ops-profile-home>/monitors.d/*.json`.
   - Add monitors for dashboards, webhook receivers, tunnels, service ports, or integration health endpoints.

## Auto-discovery requirement

Do not rely only on a hand-maintained watch list. Each health run should discover:

- root `~/.hermes` and every profile home
- loaded Hermes-related launchd labels
- Hermes-related launchd plist files
- profile cron stores and job names
- profile scripts for syntax checks
- declared monitors in `monitors.d/*.json`

Keep a baseline inventory in ops state, for example:

```text
<ops-profile-home>/state/known_inventory.json
```

Compare current inventory against the baseline. Emit `NEW_INVENTORY` for new profiles, cron jobs, launchd jobs/plists, or monitors until classified. This prevents the owner from having to remember to say “make sure IT watches this too.”

## Repairing profile-relative cron script findings

When cron preflight reports `missing_resolved_script` for a specialist-profile job but an alternate root script exists, treat it as an ownership-resolution defect—not a reason to move the job or weaken preflight.

Safe default:

1. Verify the exact live job is unique and preserve its profile, schedule, enabled/paused state, delivery, and workflow gates.
2. Prove the root implementation exists, compiles, and is safe to delegate to.
3. Back up the cron store, root script, and latest Ops report.
4. Add a minimal executable profile-local wrapper that fails closed if the root target is missing and delegates with `runpy.run_path(..., run_name="__main__")`.
5. For read-only collectors, smoke the wrapper with output captured and shape/size checked; never dump observer packets into chat. Do not run public-action workers merely to verify path resolution.
6. Require cron preflight 0 critical/0 warnings, fleet critical-only output of zero bytes, watchdog output of zero bytes, `latest.json` green with empty new inventory, and a semantic readback proving the original cron settings did not change.
7. Distinguish intentional future `first_run_pending` jobs from actual script-resolution failures.


## Unattended overnight repairs

When the owner wants maintenance that acts overnight without an approval tap, extend a narrow, allowlisted overnight repair runner; do NOT set `approvals.cron_mode` to approve. The plan is advisory input, never authority. New menu types need the owner's approval, a self-test case (reject + healthy control), a source update in the repair runner's own repo (manifest + CI), and reinstall with `cmp` readback. Running a live smoke of `apply` is safe only after the runner's dry-run mode shows the queue. A discovered `npm_ci` action that skips with "npm ls clean" means the cron error is stale (deps already restored) — the job clears on its next scheduled run.

## Proposal-only overnight jobs (stale facts, disk space)

- an owner approval naming specific numbered items: read the latest stale-facts proposal file, apply only those numbered edits (memory via the memory tool, skills via skill_manage, vault via the notes tool with backup), then reply with what changed.
- Disk-usage scan age rules: download caches (uv/npm/Homebrew) are touched constantly, so judge them by size, not mtime; an age threshold makes the scan find nothing.
- Archive verification uses per-file sha256 (`tree_hashes`); `rsync -an --checksum --itemize-changes` reports a spurious diff for single files and must not be the gate.

## Moving existing IT crons into ops

Good candidates:

- security audits
- shared-file/edit audits
- supply-chain scans
- fleet health reports
- cron/gateway/launchd watchdogs
- backup/restore verification jobs

Leave in default/specialist profile unless explicitly approved:

- cross-profile improvement orchestrators and governance summaries
- memory/vault governance jobs
- business-domain and personal-domain observers
- customer-facing workflows
- credential/provider/allowlist changes

## Safe migration checklist

1. Back up `~/.hermes/cron/jobs.json`.
2. Inspect candidate scripts for `$HOME/.hermes`, `Path.home()`, relative paths, env assumptions, and credentials.
3. Patch wrappers that must audit the whole real fleet to pin the root explicitly, e.g.:

```bash
export HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
```

or in Python:

```python
ROOT = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
```

4. Run syntax checks (`bash -n`, Python parse/compile as appropriate).
5. Move the cron profile using the cron management tool.
6. Force-run or inspect output.
7. Verify the report still sees the expected whole-fleet counts, not just the ops sandbox.
8. Update the ops inventory baseline only after the new service/job is intentionally classified.

## Pitfalls

- A profile's `cron/` directory is not proof that it has configured jobs. Hermes `load_jobs()` creates ticker/output/lock/execution metadata and returns an empty list when `jobs.json` is absent. Accept genuinely cronless profiles; fail closed when the root or a profile with inventory-declared jobs loses its store. Validate bounded JSON once and pass the same snapshot to reporting consumers—never fall back to an unbounded re-read after rejecting a symlink, malformed, or oversized file.

- Profile-scoped crons may run with `HOME` pointing at the profile sandbox. A script can falsely report green because it scanned only `profiles/ops/home/.hermes` or a reduced profile view.
- Do not let watchdogs spam routine warnings every 15 minutes. Alert fatigue is a reliability failure.
- For async SDKs that self-reconnect, cancelling only task attributes exposed by the SDK is not a sufficient teardown contract: reconnect code may overwrite those attributes while an older task remains alive. Install ownership/tracking before any SDK work starts, independently track wrapper and underlying operation tasks, signal shutdown, cancel and await all tracked work in bounded rounds, and only then close the shared HTTP session. Reproduce the overwritten-reference race in a regression test and verify the real installed SDK path. During live restart verification, separate final stderr emitted by the old draining process from the new-process boundary; require zero recurrence after that boundary across multiple watchdog cycles.
- For URL monitors that target launchd-supervised services with short restart/build windows, add manifest-level retry grace (`attempts` + `retry_delay`) instead of weakening the monitor or marking it non-critical. Verify critical-only watchdog output stays empty after the patch. If an alert has already exhausted all retries, first prove supervisor PID/exit state, expected listener, and several direct endpoint probes. When the same long-running process is healthy again, rerun fleet health and the watchdog to clear transient state; do not restart a healthy active service merely to clear the alert.
- For liveness/status endpoints, `asyncio.wait_for(loop.run_in_executor(...))` times out only the awaiter; it does not stop the blocking worker. Repeated health probes can therefore fill the shared executor and make every later probe hang. Keep the request path independent of the executor: serve validated profile-scoped stale snapshots, allow at most one daemon refresh per field/profile, propagate `contextvars` into refresh threads, and run startup warming in a daemon thread so locked state does not delay shutdown. Context propagation alone does not repair dependencies whose defaults were bound at import time; pass the active profile's database/config path explicitly and test the real collector under a named profile. Never publish a generic cold fallback for a field that sizes a shutdown/drain deadline—resolve it first through a lightweight environment/profile-config parser that avoids heavyweight imports. Regression tests must block collectors longer than the monitor deadline, saturate the default executor, exercise remote-health and topology branches, prove a timely fallback response, and verify single-flight plus profile isolation.
- For `Too many open files` in a long-lived Python dashboard, identify the descriptor owner rather than patching the first endpoint that failed. A shared SQLite object that caches one `threading.local()` WAL reader per thread becomes unbounded when each turn uses a fresh short-lived thread. Prove it with a temporary database and descriptor aggregation, fix reader lifetime at thread teardown while preserving same-thread reuse, race-test owner shutdown and tracked-connection drainage, and restart only the affected supervised service after frozen-candidate review. Raising `maxfiles` or restarting alone is containment, not remediation. See `references/thread-local-sqlite-descriptor-exhaustion.md`.
- Treat macOS File Provider/iCloud traversal and note reads as the same class of blocking dependency. Search must serve a last-good read-only index; refresh and direct reads need hard subprocess bounds, atomic validated candidates, incremental fingerprints, cross-process serialization, and dirty-generation protection. Use Python `fcntl.flock()` for plugin processes even though macOS lacks a standard command-line `flock` binary.
- Do not move default-governance jobs into ops just because they mention audits or profiles. Ops detects; default governs.
- For no-agent crons, empty stdout means silent delivery. Design critical watchdogs around that behavior.
- Byte/hash parity does not bind executable intent. For source-controlled shell cron runners, require Git/archive executable mode, an exact boolean executable field in source-authority manifests, source and live executable checks, and a regression that rejects non-boolean truthy values plus source/live mode loss. A content-only installer that preserves an existing `0600` destination can leave an intended runner non-executable; repair live owner-only mode (normally `0700`) only after byte equality and backup proof, then rerun cron preflight and the silent watchdog.
- Never copy raw matching log lines into reports or alert output. Emit structured signal/exception/HTTP fields plus a stable truncated hash; arbitrary log text can contain tokens, signed URLs, customer data, or request bodies that pattern redaction misses.
- Generic log keyword scans must preserve event semantics: parse valid JSON reports by explicit success/failure fields instead of matching `"error": null`; do not let timestamp-free traceback/stderr history inherit a file's current mtime; deduplicate identical fingerprints across `agent.log`, `errors.log`, and `gateway.log`; and correlate a transient failure with a later recovery across mirrored streams. Add regression tests proving recovered events clear while the same unresolved event still warns. Long-lived timestamp-free aggregate stderr files should be excluded only when a current structured log or live service probe covers the same failure mode.
- Use the same `is_critical_label()` predicate when collecting launchd inventory and when evaluating it. Filtering collection to labels containing `hermes` drops critical jobs with other naming families before they can be classified.
- On hosts with mesh-VPN SSH enabled, do not assume a port-22 connection traverses OpenSSH or inherits `Match User`/chroot/forced-command policy. For restricted SFTP/restic targets, preserve mesh-VPN SSH for administration and use a separately validated OpenSSH listener on a VPN-only port. Prove the real SFTP working directory and write boundary; an SSH command's exit status alone is not a reliable shell-denial test. With restic 0.19.x, use `sftp.args` for identity/port flags rather than a partial `sftp.command`.


## Reviewing summary-cron recommendations

When the owner asks whether recent ops/owner summary crons recommended anything worth changing:

1. Compare the latest 3–5 summary outputs with the current live fleet-health and cron-preflight artifacts.
2. Follow embedded observer/weekly-review references to the source evidence instead of treating an aggregate YELLOW count as the diagnosis.
3. Reproduce verification defects directly and distinguish source compile failures from missing tests, missing runners, or zero collection.
4. Inspect structured warning examples; pattern counts can contain expected/transient events and literal `"error": null` fields.
5. Classify findings as urgent repair, low-risk maintenance, workflow/owner decision, or already-resolved/stale wording.
6. Do not change production crons or specialist-profile behavior from a read-only review without the owner's approval.

A YELLOW summary with zero criticals and a GREEN cron preflight is normally maintenance/reporting debt, not an outage. Prefer fixing signal quality, stale recommendations, broken verification harnesses, and closure metrics before adding more alerts or cards.

## Independent public-site monitoring

When the owner asks for credential-free monitoring of public sites from an independent host:

1. Ground the endpoint list in live public sources (`robots.txt`, canonical sitemaps, page titles/markers, DNS, and TLS). Never guess routes or preserve a stale documented claim when the live public state now differs.
2. Use GET-based status/latency/content checks, plus DNS and TLS expiry. Pair wrapper pages with the embedded third-party origins they depend on.
3. Treat expected `401`/`403`/`405` responses as valid route-contract checks where appropriate, but state that they do not prove authenticated backends. Never synthetic-POST to lead, chat, booking, payment, or customer-write endpoints during routine uptime checks.
4. Keep the runtime independent of the agent: deterministic script, local state/deduplication, a system timer, redacted alerts, and no copied profile tokens.
5. For private chat delivery, prefer an owner-created dedicated bot/app with only a send-message scope, delivering to the owner's known user ID; store its token only on the monitoring host.
6. For read-only design requests, clearly separate what can be built credential-free from the unavoidable owner-created transport credential, and make no changes.

See `references/credential-free-public-site-monitoring.md` for endpoint classes, safe probe contracts, DNS/TLS thresholds, noise controls, and the reporting checklist.

## Scheduled notification and review evidence

Keep collector and delivery state separate when two schedulers share a watchdog: logfile-only collection must never reserve a delivered-alert fingerprint. An attempt-only ledger with retries for unchanged alerts is not confirmed delivery or an exactly-once outbox. Do not infer acknowledgment from a saved artifact or last_status, because artifact saving precedes transport. Preserve explicit retry semantics when modifying either wrapper.

For completion-receipt checks, match scheduler save/completion timing explicitly: timestamps may differ due to delivery latency. Use bounded candidate filenames, exact job/header/dispatch binding, ambiguity rejection and metadata recheck—not arbitrary latest-file fallback or exact completion-second equality. Legacy missing receipts remain UNKNOWN; producer attestations validate coverage structure, not independent semantic truth. Keep one source of truth per runtime helper and never overwrite it with a similarly named copy from another tool.

## Verification

After setup or migration, verify:

```text
profile=ops on intended IT crons
last_status=ok after a forced or scheduled run
fleet health sees expected profile count
launchd watchdog loaded with last exit 0
critical watchdog dry-run prints 0 bytes when healthy
latest report exists under profiles/ops/reports/
```

## Classifying `NEW_INVENTORY` safely

The fleet watchdog intentionally reports new cron jobs, launchd labels/plists, profiles, and monitors until they are classified in:

```text
<ops-profile-home>/state/known_inventory.json
```

Do not treat the signal as noise or blindly silence it. Classification means “this object is intentional and owned,” not “activate or trust its runtime behavior.”

1. Validate the live object, ownership docs, health, uniqueness, and safety boundary before editing inventory.
2. For cron jobs, read the exact canonical job record; a one-line CLI grep can omit multi-line `enabled`/`paused` state.
3. For paused or public-action-capable jobs, preserve the pre-change state and do not execute or resume the job merely to classify it.
4. Treat an intentional future `first_run_pending` job as unproven-but-not-failed: preserve `last_run_at=null` / `last_status=null`, compile and inspect the complete delegated script chain, confirm ownership documentation and fail-closed boundaries, and do not force-run it solely to satisfy inventory classification.
5. Distinguish public/customer actions from approved internal state refreshes. A job may remain operationally read-only while writing bounded local artifacts or sanitized internal analytics snapshots; inspect the exact method/endpoint, ensure source systems cannot be mutated, and verify there are no post/comment/message/upload/delete primitives before classifying it.
6. Back up `known_inventory.json` with a timestamped copy and checksum manifest.
7. Add only the exact missing inventory key. For a launchd guard, classify both label and plist when both inventory classes exist.
8. Validate JSON and syntax-check referenced scripts.
9. Run both the critical fleet scan and the watchdog script (a reference implementation, `ops-monitoring/ops-fleet-watchdog.sh`, ships in the sibling public repo [operator-safety-kit](https://github.com/uachristian/operator-safety-kit)); require exit 0 and empty stdout when healthy.
10. Confirm `latest.json` has `new_inventory: {}`, no critical issues were introduced, and the source object's runtime state is unchanged. Prefer a fully GREEN report, but if `latest.md` remains YELLOW solely for independently reproduced unrelated warnings, report those separately; do not suppress them or broaden the classification task merely to manufacture GREEN.
11. Capture the classification in the existing canonical notes page and log meaningful README wiring; avoid creating a narrow one-session concept note when a class-level page already exists.


## References

- `references/credential-free-public-site-monitoring.md` — credential-free external uptime monitoring: endpoint classes, safe probes, DNS/TLS thresholds, noise controls.
- `references/fleet-change-guard.md` — independent restart-loop/change guard: launchd install, safety contract, verification, and rollback.
- `references/fleet-log-signal-classification.md` — state-aware procedure for resolving false-positive fleet log warnings without hiding unresolved failures; includes JSON semantics, timestamp rules, cross-stream recovery correlation, regression matrix, and verification contract.
- `references/thread-local-sqlite-descriptor-exhaustion.md` — diagnose SQLite/WAL descriptor ownership, reproduce per-thread reader retention, implement thread-teardown cleanup, triage baseline test contamination, and release only the affected supervised service.
