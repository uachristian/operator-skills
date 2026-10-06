# Full-suite failure triage pattern

Use this when a broad/full test suite fails after an update, dependency refresh, or large rebase.

## Pattern

1. Preserve the canonical full-suite log path before making fixes.
2. Build a targeted rerun from the failing node ids, but keep it representative enough to catch shared-fixture fallout.
3. Separate failures into three buckets before editing:
   - product behavior regressions,
   - test assumptions that are stale because product behavior intentionally changed,
   - host/environment assumptions in tests (for example macOS vs Linux permissions or missing platform service binaries).
4. Fix product code first. Patch tests only when the assertion is demonstrably stale or over-specific.
5. After each fix batch, rerun the targeted subset and read the new failure list; do not keep piling edits on top of an unknown state.
6. Before final handoff, rerun the full suite and then run post-suite health/security checks.

## Pitfalls from the Hermes full-suite update session

- If a test runner can see both `.venv` and `venv`, verify which interpreter it selected before trusting failures. A stale alternate virtualenv can create false dependency/test results.
- When changing generated shell snippets, update string-inspection tests to assert the durable invariant, not a single literal token. Example: a safer temp filename may use `${BASHPID:-$$}.$RANDOM`; tests should assert per-writer uniqueness and no bare `.tmp.$$`, not only literal `$BASHPID`.
- Platform-specific permissions may differ (APFS/macOS can clear setgid bits on temp dirs). Keep product/runtime checks strict where they matter, but make unit tests express the portable invariant when they run on multiple OSes.
- Avoid editing many tests to fit the local machine before confirming whether the underlying code or the test harness is at fault. Targeted reruns are for feedback, not final verification.
