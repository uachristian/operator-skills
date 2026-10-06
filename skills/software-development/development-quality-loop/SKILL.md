---
name: development-quality-loop
description: "Use when planning, implementing, debugging, or reviewing software. Plan, TDD, systematic debugging, adversarial review, verification."
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [planning, debugging, testing, code-review, quality]
    related_skills: [build-execution-standard]
---

# Development Quality Loop

## Governing process

Load **build-execution-standard** for any substantial software build, repair, or release review. Safety, accuracy, and verified execution come first; reduce elapsed time through early proof, proactive parallel work, and bounded convergence—not weaker gates. This skill supplies implementation/debugging technique and routes to preserved specialist evidence. Existing profile authority, owner approvals, project rules, and applicable domain security requirements remain binding.

Do not start a repo-specific project merely to improve the system-wide build process. Shared guidance/templates belong at the Hermes layer; project adapters discover actual commands without imposing one toolchain on every repo.

## Before code changes

Explain the immediate user problem, smallest viable solution, non-goals, expected scope/budget, and remaining boundaries. Freeze acceptance commands, interfaces/representative payloads, path ownership, risk, rollback, and release owner. Read actual schemas, validators, runtime/toolchain and project scripts before designing from conversational guesses.

Use a read-only preflight: current repo state, declared runtimes/dependencies, test discovery, necessary local services/resources, and existing failing baseline. Never auto-install, repair, run lifecycle scripts, or activate production as an implicit preflight step. A missing prerequisite is BLOCKED, not PASS.

## Implement and diagnose

1. **Reproduce or define behavior.** Establish a real failure or an executable acceptance witness; inspect logs/source before modifying code.
2. **Spike uncertainty.** Test one API/runtime/migration assumption in an isolated disposable environment; define VALIDATED / PARTIAL / INVALIDATED criteria first. Do not promote throwaway scaffolding accidentally.
3. **RED–GREEN.** Add the failing regression or contract check, run it to prove the intended failure, make the smallest coherent implementation, rerun. Do not claim TDD without an observed RED.
4. **Integrate early.** Exercise actual producer → parser/API → consumer with shared synthetic fixtures, including missing/null/invalid/healthy inputs. UI work needs a real representative interaction/visual checkpoint, not merely source-substring or syntax checks.
5. **Fast feedback.** Run focused affected tests, types/lint/contracts during iteration. Inventory test files so a green command cannot hide omitted suites. Use debugger/inspector when more efficient than repeated guess patches.
6. **Full evidence.** Run all applicable required integrated tests, security/dependency scans and recovery/runtime checks at the release boundary. Repeat evidence invalidated by source/dependency/environment changes; never reuse stale candidate claims.

A new guard requires both an adversarial rejection witness and a canonical healthy-producer control. Turn accepted findings into maintained regression tests or executable invariants. Parse JSON/YAML/OpenAPI contracts structurally rather than searching source strings. A mocked suite cannot prove a real external integration or deployed runtime.

## Risk-proportionate review

Small reversible repairs: focused tests, spec/outcome and diff review, backup/readback where applicable; no mandatory reviewer swarm. Major/high-risk builds: one implementation pass, frozen adversarial review, one coherent remediation batch, final exact-tip delta/affected-boundary review. Spec and quality are review dimensions, not two compulsory child sessions per tiny edit. Path-based escalation: any change touching auth/permissions, secrets, schema/migrations, payments/pricing, or that removes/weakens a validation or allowlist guard (or its negative test) gets the thorough lane regardless of diff size; a removed guard needs a named regression case proving the boundary still refuses bad input.

Continue only for a reproduced critical/high finding, failing required gate, missing mandatory integration evidence, or newly approved scope. RC3 requires owner scope review. Never waive a lower-severity issue if it fails an already-required security or acceptance gate. Production-facing dependencies and dev tooling retain the zero-known-vulnerability requirement.

Required reviewers must complete before release. Same-model fresh context is useful but not different-family independence. If a required late HOLD arrives, reopen/contain the release; do not ignore it because another check passed. Stop on verified approved outcomes, not imagined polish. Scope growth, roughly twice the stated estimate, or a new service/database/protocol requires an owner decision rather than silent expansion.

## Evidence hygiene

- Parent verifies child artifacts, semantics, exact commits, tests and external readback; summaries alone are not proof.
- Isolate concurrent writers/review execution; check candidate identity and test collection before/after gates. Never test a moving shared checkout as if immutable.
- Preserve true exit codes; no failure-masking pipes or succeeding cleanup commands. Scope HOME/HERMES_HOME/TMPDIR/env overrides to one process; no credentials in evidence.
- Separate source, installed artifact, runtime behavior, and deployment authority. A successful read/delete call is not verified state or absence.
- Keep temporary progress in the repo handoff; durable facts in the vault, reusable technique in skills. Close with actual acceptance evidence and explicit unverified boundaries.

## Specialized guidance — selective loading

All pre-consolidation specialist references remain in this skill; they were not removed or weakened. Load the matching reference before work on that subsystem:

- `references/advanced-quality-pitfalls.md` — preserved concrete failure modes; load for the affected domain, not automatically in every routine task.
- `references/advanced-verification-checklist.md` — select applicable specialized gates before editing; required applicable gates remain mandatory.

Do not reload the whole historical catalog just to perform a routine edit. Do not interpret selective loading as permission to omit required risk-specific verification.
