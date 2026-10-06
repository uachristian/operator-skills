---
name: build-execution-standard
description: "Use when building, fixing, or reviewing software of any size. Contract first, verify with real execution, close out honestly."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [build, verification, delegation, safety]
    related_skills: [development-quality-loop]
---

# Build Execution Standard

## When to Use

Orchestrator and builder profiles load this for authorized substantial software builds, fixes, and release reviews, across projects. For tiny reversible edits, apply its safety/verification principles proportionately without creating unnecessary process artifacts.

## Scope and priority

Standing build process for **the orchestrator and authorized builder profiles**, across their authorized projects. Safety, accuracy, and verified execution come first; optimize elapsed time through early proof and useful parallel work. No authority expansion: profile privacy, tool limits, project instructions and exact owner approvals remain binding. Do not install this in other specialists or turn ordinary triage/cron work into a software build.

Use this proactively without the owner reminding you. Keep shared guidance/templates here; discover project-specific commands in the actual repo. Do not create a repo-specific pilot to implement a system-wide process improvement. No new orchestration service, cron, provider, permission, or restart is implied.

## 1. Freeze outcome and adapter

For substantial work, use `templates/build-contract.md` in an authorized repo/task location. Record outcome, smallest solution, non-goals, risk/trust/data boundaries, exact allowed paths/actions, interface version, acceptance IDs/commands, rollback, ownership, and completion budget. Reserve integration, review/remediation, full verification, and closeout time. Build approval is not deployment, publication, real-data access, or external-write approval.

Discover commands from actual project instructions, manifests, task runners and CI. Record cwd, executable, inputs, side effects and evidence for preflight, fast checks and full release gates. Never present template placeholders as runnable commands or invent universal build commands. Inspect commands before running; no automatic installs, lifecycle scripts, credential loading or production access.

### System inventory

If your setup keeps a system inventory, check it before planning to avoid duplicate builds; register new systems at closeout.

## 2. Preflight before fan-out

Verify workspace/commit and dirty/untracked ownership, runtime versions, dependencies/locks, declared test inventory, relevant service availability/resources, and existing failure baseline. Avoid dumping secrets. Preserve unrelated work; never reset it to make tests green. Missing prerequisites mean BLOCKED or an approved alternative, not fabricated PASS. Cheap source/contract prerequisites precede expensive gates; full required proof is never skipped.

For shared interfaces, define versioned synthetic fixtures used by the real producer and consumer: valid, denied/error, omitted/null/empty, and boundary cases. Freeze concrete field types and representations (for example, numeric epoch timestamps versus ISO strings, and status keys versus display labels); independent hand-authored envelopes can otherwise pass while the real healthy path silently falls back. Assign fixture ownership. Do not create diverging mocks that agree only with their own implementation. For scheduled-script integration, also exercise a fresh interpreter from the installed-style working directory without repository PYTHONPATH or preloaded modules; lay out only the synthetic dependencies the deployed entrypoint actually resolves. A test runner's imports can otherwise hide a missing production dependency path. Anonymize reported examples without simplifying their triggering structure: preserve date punctuation, address fields, optional prose and transport wrappers. Recheck the full reported layout before release; a simplified synthetic analogue can pass while the user's actual format still fails.

When a regression uses prior source as an output oracle, make that exact hash-bound snapshot self-contained in test fixtures unless the real CI adapter explicitly fetches the required history. A local `git show <old-commit>` oracle can pass in a full clone but fail in a shallow checkout. Preserve provenance and byte identity when packaging the fixture; rerun affected/full gates and verify that production bytes remain unchanged for a test-only correction.

## 3. Proactive parallel work

Default to useful independent discovery, implementation, test-design, and UX lanes early—not only reviewers at the end. Use 2–5 concurrent workers when ready work and actual profile/tool/resource caps support it; never fabricate delegation or bypass a lower cap. Do not assume an executive profile or an already-running session has the same cap as the orchestrator. Parent actively integrates and verifies while workers run.

Each packet names one bounded outcome/question, frozen base, allowed paths/forbidden actions, shared contract, exact artifact, focused commands and stop budget. Separate writer worktrees: any time two or more writers touch the same repo concurrently, use a parent-created `wt/<task>` branch at a recorded base, outside the checkout, with serial parent integration and owned-only cleanup. One writer per shared file/fixture/lock/output. Worktrees are not a hostile-code sandbox: inspect absolute live paths and preserve privacy. Bound aggregate heavy CPU/RAM/disk/API workloads; serialize shared runtime/browser operations. Advance lightweight independent work during backup/build waits. Backfill slots with ready in-scope work, not busywork.

Children inherit provider/model unless configured otherwise; same-model contexts are not different-family independent evidence. Do not change caps, models, tools or authority as a delegation shortcut. Parent owns long-lived servers; child-returned PIDs are not process ownership transfer.

## 4. Early working slice and fast feedback

Prove one real end-to-end path before broadening implementation. Exercise shared fixtures through actual producer/parser/API/consumer. UI work needs a real representative interaction and visual/product checkpoint; syntax, screenshots of an unrelated shell, or source substring checks do not prove functionality. Label disconnected/simulated boundaries honestly.

Reproduce bugs, test root cause, then implement; claim RED–GREEN only after an observed intended failure. During edits use focused tests/types/lint/contracts with true exit codes and test collection. New guards need both rejection and canonical healthy controls.

Keep test failures from isolation/setup separate from product regressions. Discover checkout-basename and outside-checkout scratch requirements before allocating worker paths. Give shell-wrapper fixtures an explicit writable synthetic cwd as well as HOME/TMPDIR; legacy shells can otherwise fail creating heredoc files despite a temporary HOME. Redirect hard-coded profile-root constants in fixtures even when a synthetic token is already supplied, because loaders may still inspect the real credential path. Preserve network/live-data denial and all assertions; fix fixture placement/injection rather than broadening sandbox access or reporting a blocked branch as tested.

For frozen candidates, put isolation adapters outside the checkout and inject only discovered path constants into actual imported modules. If a self-test exists solely under `__main__`, a narrowly matched child bootstrap may inject those constants at the inspected main-guard boundary while executing the unchanged file and assertions; fail closed if injection does not occur exactly once. Scope generic credential-path denial exceptions to a fresh synthetic fixture subtree, and prove real credential metadata remains denied with stat-only checks, including a fixture symlink to the protected target. Preserve original failed logs, compare tracked-file hashes and commit before/after, and keep an expected install-parity failure nonzero rather than relabeling it PASS.

If discovery invalidates the interface, pause only dependent work. Parent resolves evidence, revises contract/tests and explicitly reissues affected assignments; unaffected lanes continue. Scope/authority expansion requires owner approval. Separate unrelated infrastructure repair and optional polish from the requested outcome.

## 5. Full verification and bounded review

Freeze integrated source, dependency/environment and artifact identities. Run all applicable required suites, builds, contract/integration/UI checks, security scans and risk-required authority/migration/restore probes. Parent inspects child artifacts as untrusted claims and verifies independently. Test collection loss or moving checkout drift invalidates evidence. Rerun affected required gates after relevant changes; dependency repair after a suite requires the full suite again.

Production-facing dependency/security checks retain zero known vulnerabilities, including dev/build tooling and shipped images where applicable. Record coverage and freshness; missing scans or exclusions are not clean proof. Never weaken security, recovery or acceptance to fit budget.

Routine reversible fixes need focused spec/diff/tests and verification, not a reviewer swarm. Major/high-risk default: implementation → frozen adversarial review → one coherent remediation → final exact-tip delta/affected-boundary review. Prefer different-family review for high risk when available. Required pending/timed-out reviews leave HOLD. Extra cycles need reproduced critical/high findings, failing required gates, missing mandatory integration evidence, or owner-approved scope. RC3 or roughly twice the scoped effort triggers owner scope review. Optional cleanup goes to backlog.

## 6. Handoff and closeout

Use `templates/build-closeout.md` and maintain the build contract at milestones. Track phase and blocked time separately, first actual integration proof, handoffs/retries, accepted defects/regressions and owner scope changes. Unknown timings/costs stay unknown. A tiny sample does not establish speedup.

Keep temporary progress in the authorized repo/task handoff, not persistent memory. For delayed or resumed work, use operational-change-control’s mission-handoff template and result-reconciliation reference: match mission, scope, candidate and worker; record incorporation only after parent verification. A stale security finding still requires current reproduction. Preserve exact candidate, dirty ownership, commands/exits, required reviewer status, blockers, rollback and next command before context rollover. Do not re-dispatch unchanged timeouts; preserve partial work and finish the shortest safe path.

Verify all acceptance IDs, source/artifact identity, reviews, rollback readiness and only-owned temporary cleanup before DONE. Distinguish built, tested, reviewed, deployed and live-verified. External writes need exact readback; plans, stubs, green subsets and child summaries are not completion. Stop once approved gates pass.

## Supporting material

- `templates/build-contract.md` — build contract, discovered adapter, shared fixture matrix and milestone handoff.
- `templates/build-closeout.md` — evidence-backed verdict and lightweight timing/rework receipt.
- `development-quality-loop` — implementation/debugging and selectively loaded domain gates.
- `subagent-driven-development` (optional, upstream Hermes skill if installed) — isolated packets, async workers, integration and review mechanics.
