# Contained Synthetic Demo UI Release Playbook

This reference captures the reusable details behind a local synthetic service-operations demo release. Adapt names and commands to the repository; preserve the invariants.

## 1. Freeze scope and authority

- Record the accepted source/database baseline and rollback artifact before editing.
- Limit the candidate to UI, demo runtime wiring, reset/seed tooling, tests, and documentation.
- Reject new migrations, business rules, external integrations, real data, remote exposure, and browser-accessible reset endpoints unless separately approved.
- Keep permanent UI boundary copy visible: synthetic data, no authentication, external systems disconnected, loopback only.

## 2. Demo database isolation

Use one fixed allowlisted demo database and, if builds require it, a separately fixed ephemeral build database.

Operator reset order:

1. Stop the demo runtime.
2. Fingerprint the accepted database.
3. Drop/recreate only the fixed demo database.
4. Apply immutable migrations and curated synthetic seeds through the schema owner.
5. Verify migration checksums, normalized cardinalities, reconciliation, and expected fixtures.
6. Recompute the accepted fingerprint and require equality.
7. Start the hardened demo runtime as the least-privileged application role.

Fingerprint the entire application schema dynamically. A manually maintained table list can omit later tables while still reporting preservation.

After real browser mutations, execute reset twice, extract the normalized semantic PASS payload from each run, and require exact equality. Do not compare timestamps, transient container messages, or image-build chatter.

## 3. Source/image/runtime binding

Track separately:

- source/build-contract digest,
- application payload digest,
- immutable image ID,
- runtime-state image ID and contract digest,
- active database and role.

A demo rebuild may retag an image shared with an accepted internal runtime. The internal health endpoint can remain green while its runtime-state file references the previous source/image. Maintained UAT should fail closed at the build-contract assertion.

Debugging sequence:

1. Identify the exact failed assertion rather than interpreting a bare `AssertionError` generically.
2. Compare current build-contract digest with runtime state and image labels.
3. If the new source is intentional, rebuild/restart the accepted loopback runtime through its canonical lifecycle target.
4. Verify runtime identity and database readback.
5. Rerun the maintained disposable-clone UAT.

Never remove the source-binding assertion or substitute an ad hoc untracked image.

## 4. Browser role journey

Exercise one complete aggregate (for example a synthetic service order) wherever practical:

1. A coordinator role creates a synthetic service order and primary assignment.
2. Add work scope and a plan; move to the eligible assessment state.
3. Compose a complete quote and record an exact-bound synthetic decision.
4. The coordinator creates a fixed-template checklist run.
5. The assigned worker records every checklist result. Exercise a caution/fail result that atomically creates its follow-up recommendation when supported, then complete the run.
6. Add a material line after approval and confirm the scope-version change invalidates authorization.
7. Compose the change and record fresh approval.
8. A fulfillment role allocates; optionally release/reallocate; verify order and inventory versions.
9. The assigned worker consumes the material and verifies movement history and conservation.
10. The worker advances work items and the order through legal states.
11. A manager moves the clear order through in-progress/review/ready states.
12. Verify terminal-state copy and absence of false blockers.
13. Verify the read-only persona exposes no enabled mutation controls.
14. Switch to another tenant and assert its queue contains no first-tenant identifiers.

Authority nuance: workers may own checklist evidence but not checklist creation. If checklist creation is absent for a worker, switch to the coordinator and inspect the server action matrix before calling it a defect. Create the run before completing the order.

If browser automation cannot reliably commit a native select, set the visible selector’s value and dispatch its ordinary DOM `change` event. This exercises the UI code path; it must not bypass server authorization or replace UI UAT with direct hidden API calls.

## 5. Desktop and tablet evidence

For each supported viewport:

- capture a real screenshot,
- inspect clipping, overlap, density, tap targets, dead space, and readable hierarchy,
- collect `innerWidth`, document/body client widths, and scroll widths,
- enumerate elements whose `scrollWidth > clientWidth`, including computed `overflow-x`.

Pass criteria:

- no document-level horizontal overflow,
- no clipped critical controls,
- intentional component overflow (for example a tab strip with `overflow-x:auto`) remains reachable and does not widen the document.

Headless Chrome plus DevTools Protocol is useful for exact tablet metrics when the interactive browser cannot resize. Start it with a disposable profile and fixed `--window-size`, query metrics through CDP, then terminate the tracked process and delete only its generated profile/artifacts.

## 6. Gate order

Serialize shared-database gates:

1. Static validator, Python tests, Node tests, diff check.
2. Live database verifier.
3. Accepted internal runtime verifier.
4. Disposable-clone workflow UAT.
5. Demo runtime isolation/hardening verifier.
6. Application audit, toolchain scan, shipped-image scan, and whole-profile secret scan.
7. Rebuild/verify/scan unaffected images whose source contracts include changed shared files.
8. Fresh backup and mutation-sensitive restore drill.
9. Family-wide disposable database/container census.
10. Final demo reset and accepted fingerprint comparison after browser UAT.

The restore drill should verify data and security fingerprints, RLS/ACL/owner/policy/function contracts, append-only behavior, reconciliation, mutation detection/repair, and temporary-resource removal.

## 7. Exact-tip review and release

- Freeze and commit only after implementation gates are green.
- Give an independent reviewer one immutable commit, focused diff, explicit scope/security question, and bounded commands.
- When the worktree's `.git` metadata is only valid inside a container or remote execution environment, generate `git archive <exact-sha>` and the base-to-tip diff inside that environment, then extract them into a host-side reviewer directory. Do not copy the live worktree or ask the reviewer to discover the repository.
- Create a fresh unique reviewer directory (for example with `mktemp -d`) for every verdict. Never pre-delete or reuse a fixed temp path with `rm -rf`/`rmtree`; besides risking the wrong directory, destructive cleanup can introduce an approval stall immediately before a required review. Verify the archive commit identity, file count, and absence of Git metadata before dispatch.
- Probe the chosen different-family reviewer with a minimal no-tool response first. If that lane is not authenticated, do not request or copy credentials; use an already-authenticated provider lane or the frozen-policy fallback.
- Treat a timed-out command approval as no action and no reviewer verdict. Keep release on HOLD and wait for renewed user authorization rather than retrying the same archive operation through alternate syntax.
- Treat any later edit as superseding that verdict.
- Reproduce findings in the controller lane; turn accepted findings into tests/invariants.
- Rerun affected gates and obtain a fresh exact-tip verdict.
- Merge only the explicitly intended private repository.
- Verify local tip = remote tip = reviewed tip; verify runtime/image/database readback.
- Publish release and rollback evidence without overstating production readiness.

## Completion checklist

- [ ] Accepted database unchanged outside separately authorized migrations.
- [ ] Demo reset deterministic after mutation.
- [ ] Full visible browser journey includes checklist and fulfillment authority.
- [ ] Desktop/tablet screenshots and overflow metrics pass.
- [ ] Full maintained tests and runtime/database UAT pass.
- [ ] Zero known vulnerabilities at required threshold.
- [ ] Fresh backup and restore drill pass.
- [ ] Disposable resource census is empty.
- [ ] Final demo reset completed.
- [ ] Exact-tip independent review completed after last edit.
- [ ] Private remote and runtime readback match the reviewed commit.
