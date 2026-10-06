---
name: contained-synthetic-demo-releases
description: "Use when building and releasing an isolated local demo UI on synthetic data without expanding backend authority or touching real data."
version: 1.4.1
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [demo, browser-uat, synthetic-data, postgresql, docker, release, security]
    related_skills: [development-quality-loop, operational-change-control]
---

# Contained Synthetic Demo Releases

## Use this skill when

- Converting an engineering/internal UI into a polished local stakeholder demonstration.
- The demo must use synthetic data, remain loopback-only, and preserve an accepted database/runtime.
- Verification spans browser role simulation, Docker hardening, PostgreSQL isolation, reset determinism, restore proof, security scans, and exact-tip review.
- An Apple-platform prototype needs a Dockerized synthetic/demo lane while Xcode, SDK linking, signing, Simulator, and device evidence remain on macOS.
- An exact unsigned Apple release must be handed to an independent/offsite Mac without copying Hermes runtime state, credentials, signing material, captured content, or customer data.

Do not use this as permission to add real data, remote exposure, production authentication, external integrations, migrations, or new backend business authority.

## Core contract

Freeze before editing:

- accepted backend/source tip and database baseline,
- goal and explicit non-goals,
- trust boundaries and fixed demo database/container names,
- browser journeys and role/tenant matrix,
- exact verification commands,
- rollback artifacts,
- one implementation, one adversarial review, one remediation, and one exact-tip release cycle.

## Release workflow

1. **Isolate** — use a fixed allowlisted demo database and loopback runtime; never reset the accepted database.
2. **Bind** — verify current source hash, image payload/hash, immutable image ID, runtime state, database name, and application role separately.
3. **Reset** — operator-only reset; no browser reset endpoint. Fingerprint accepted state before/after and compare two normalized reset outputs after real demo mutations.
4. **Exercise** — run the complete browser journey through visible controls and role simulation, including authorization invalidation, checklist authority, fulfillment authority, read-only denial, and tenant isolation.
5. **Measure responsive behavior** — combine screenshots with exact document/component overflow metrics at desktop and tablet widths.
6. **Verify serially** — static and unit tests, live database contract, accepted runtime, disposable-clone UAT, demo verifier, scans, backup/restore, and global cleanup census.
7. **Review exact tip** — freeze a commit, dispatch one bounded independent review, remediate reproduced findings, and supersede any pre-edit verdict.
8. **Release and read back** — merge only the intended private repository, verify remote SHA/runtime identity, reset the demo to baseline, and publish rollback evidence.

## Autonomous preflight without stakeholder overclaim

When human role sessions are unavailable, continue with useful machine evidence but preserve the human gate:

- Label the run `AGENT-PREFLIGHT`, record zero human sessions, and keep stakeholder feedback `not-collected`.
- Map every stakeholder task to browser evidence, disposable-clone UAT, both, or an explicit human-only judgment boundary.
- Keep priority ranking, terminology/role fit, and roadmap value human-only; automation does not prove operational fit.
- Prefer a bounded, dependency-free Chrome/CDP runner when approved Node and Chrome already provide `fetch` and `WebSocket`.
- Probe every fixed role/tenant at desktop and tablet widths; fail on console/network errors, unnamed AX controls, duplicate IDs, document overflow, tenant leakage, role-surface drift, or broken navigation/tabs/filters.
- Compose reset, demo verification, disposable UAT, browser probes, and accepted-data fingerprint comparison into one host-only machine-readable gate.
- Do not persist raw traces, recordings, or participant-like artifacts unless the frozen contract requires them.

## Human stakeholder session readiness

When moving from agent preflight to real role sessions:

- Correct the evaluated source pin before generating packets; the evaluated application tip may differ from a later docs/helper-only readiness commit.
- Generate blank packets only in an owner-private directory outside Git with `0700` directories and `0600` files.
- Accept exactly one fixed role argument; reject unknown roles and extra identity-like arguments. For the outside-Git boundary, compare filesystem identity across existing ancestors (`-ef` / `samefile`), not just canonical-path text: case-insensitive APFS aliases can bypass string-prefix guards. Reject before creating any directory.
- Initialize packets as `not-started`, evidence `not-assigned`, feedback `not-collected`, and human sessions `false`. Packet generation and an open browser prove readiness, not participation. Before the real participant begins, automation may prefill only directly verified setup facts; do not change evidence/session state until explicit start.
- Do not capture participant names in Git, logs, manifests, the vault, or generated status. Do not send invitations or team messages unless separately authorized.
- Preserve the explicit next-phase gate until the required real sessions and aggregate human decision record exist.

## Path-stable source/image contracts

Source-bound images must hash content and repository-relative identities, not absolute worktree filenames:

- Centralize each image family's contract in one helper and make build, startup, UAT, and verification consumers call it.
- Hash a deterministic ordered set after changing to the repository root; include Docker/compose inputs, policy files, pinned literals, and the helper itself.
- Regression-test the same input set in two filesystem roots for equal hashes, then mutate one byte and require inequality.
- When normalizing an existing contract, tag current images for rollback, fingerprint accepted data, rebuild once through canonical lifecycle targets, verify every dependent runtime, and compare the fingerprint afterward.
- Never weaken source binding merely because a new worktree reports mismatch; first distinguish byte drift, stale runtime identity, and path-sensitive hashing.

## Dockerized worktree execution planes

Treat Git metadata authority and Docker lifecycle authority as separate prerequisites:

- If a worktree's `.git` pointer names a container-only mount path, run Git, archive, diff, and Git-enumerated documentation checks inside that container. Do not "repair" the worktree by rewriting its metadata for the host.
- If one frozen candidate must be verified from both macOS and a bind-mounted container, prefer an independent clone under the mounted profile root: remove its temporary remote, assert exact HEAD, run both execution planes, then delete the clone. A normal worktree may contain a host-only absolute `.git` pointer that the container cannot resolve.
- If the build container intentionally has no Docker socket, run reset/up/down/verify lifecycle targets on the host with both the expected profile root and the exact allowlisted worktree root. Never mount the Docker socket merely to make a nested lifecycle command work.
- A fresh worktree does not inherit ignored dependencies. Hydrate exactly the lockfile before canonical verification (`npm ci --ignore-scripts --offline` when the approved cache is complete; otherwise use the project's approved network path). Do not alter the lockfile to cure worktree-local setup state.
- Stage intended new documentation before a `git ls-files`-based link checker so untracked files are not silently omitted; then remove every temporary checker and require a clean tree.

## Required evidence

- Full maintained Python/Node/static gates and collection counts.
- RLS/ACL/role/version/idempotency/audit/outbox/reconciliation checks.
- Accepted-database fingerprint preservation during reset, browser UAT, and demo verification.
- Non-root/read-only/capability-dropped/no-new-privileges runtime with loopback-only binding.
- Zero known application, toolchain, and shipped-image vulnerabilities at the project’s required threshold.
- Fresh backup plus mutation-sensitive restore verification.
- Family-wide absence of disposable UAT/restore/upgrade/debug databases and containers.
- When visual release evidence is required, capture desktop/tablet views plus DOM overflow metrics; an autonomous preflight may remain capture-free when its frozen artifact contract forbids persistent visual evidence.
- Completed exact-tip independent review with no unresolved release blocker.

## Browser authority sequence

A common safe sequence for a generic service-order workflow is:

1. A coordinator role creates the service order, assignment, line items, plan, quote, and customer decision.
2. The coordinator creates any structured checklist run the order requires.
3. The assigned worker records checklist evidence and completes the checklist.
4. A scope change invalidates the prior approval; the coordinator records a change and a fresh decision.
5. A fulfillment role allocates/releases materials; the assigned worker consumes them.
6. The worker completes the work items; a manager advances the order through review to Ready.
7. A read-only role has no mutation controls; an alternate tenant sees only its own queue.

Create checklist runs before work completion. An absent create action in a terminal state may be correct enforcement rather than a UI defect.

## Pitfalls

- Node's `os.tmpdir()` trusts inherited `TMPDIR`; a prior isolated reviewer may leave it pointing at a directory that has already been deleted. For deterministic Chrome/CDP harnesses, create disposable browser profiles under an ignored, explicitly created artifact-temp root owned by the current run, then remove that root in `finally`.
- Health `200` does not prove source/image/runtime identity.
- Rebuilding a shared image tag can leave another runtime-state file bound to the prior image. Diagnose the exact contract assertion and rebuild through the canonical `up` target; never weaken source binding.
- Aggregating `shasum` output over absolute filenames makes identical source hash differently in each worktree because filenames are part of the aggregate. Use one repository-relative helper per image family, include the helper itself, and prove cross-root equality plus content sensitivity.
- Do not defer phase/stage/manifest/validator alignment until after the final full suite. Late metadata edits supersede earlier green evidence; rerun affected gates and preserve enough completion budget for commit, exact-tip review, release, readback, vault handoff, and cleanup.
- Hardcoded fingerprint table lists go stale. Enumerate the complete application schema dynamically.
- A screenshot alone does not prove responsive safety. Verify document scroll width and identify intentional component-level scrolling separately.
- Accessibility-tree roles do not always match HTML input vocabulary: Chrome reports `type="search"` as `searchbox`, and ARIA list rows may be `option`. Centralize the complete interactive AX-role set in tested shared code, cover every role emitted by the current surface, and fail on every unignored unnamed control.
- Fresh scanner intelligence can invalidate a previously green unchanged toolchain. Hold release, reproduce the exact package paths, and rescan every lane; never preserve the old verdict with an exclusion.
- If the latest upstream CLI still bundles a vulnerable dependency but an official fixed package exists, checksum-pin and verify the fixed archive before replacing only that proven bundle directory. Assert installed versions, patch every duplicated Dockerfile, add a regression invariant, and rescan toolchain plus shipped runtime images.
- When a strict repository validator scans ignored local files, run locked dependency tests/audit first, remove only the disposable dependency cache, then run the validator. Do not weaken ignored-path coverage.
- A reset is not proven deterministic until the demo was mutated and two normalized reset outputs match.
- Per-run teardown is not global hygiene; enumerate disposable resource families afterward.
- For exact-tip review, create a fresh unique immutable archive directory and generate the archive/diff in the environment where Git metadata is valid. Never pre-delete or reuse a fixed reviewer path; an approval timeout is no action and keeps release on HOLD.
- One-shot reviewers may restore their configured project directory instead of honoring the launcher working directory. Put the exact immutable archive and diff at host-readable paths and include those absolute paths in the review prompt; a reviewer that cannot locate the named commit must issue no verdict.
- Current Hermes one-shot review syntax is `hermes chat --provider <provider> -m <model> -Q -q "$prompt"`. The `-q` query flag belongs to the `chat` subcommand; the older `hermes --provider ... --model ... -q` form fails argument parsing before any model executes and produces no review evidence.
- Run multi-step rollback creation and verification under fail-fast shell semantics. `git bundle verify` requires a repository working directory; a later successful checksum must never mask a failed bundle-verification step.
- If an independent exact-tip reviewer returns `APPROVE` with no Critical/High/Medium findings, do not invalidate the reviewed tip for optional cosmetic Low findings. Remediate only when a Low finding reproduces a required-gate failure or materially weakens the frozen contract.
- Do not announce release while browser readback, final reset, exact-tip review, merge, or runtime/remote readback remains pending.

## Detailed reference

See `references/contained-synthetic-demo-ui-release.md` for the full implementation and verification playbook, including source/image drift diagnosis, Chrome DevTools overflow probes, and cleanup gates.


See `references/automated-preflight-and-toolchain-cve-remediation.md` for the truthful `AGENT-PREFLIGHT` evidence model, dependency-free Chrome/CDP probe design, accessibility/network checks, strict-validator cleanup ordering, and checksum-pinned remediation of vulnerable packages bundled by an otherwise current toolchain.


