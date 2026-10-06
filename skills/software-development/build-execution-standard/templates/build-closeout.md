# Build closeout

Fill from real execution. Unknown values stay UNKNOWN. Store with the task.

## Owner decisions (first)
1. Decision needed, recommendation, alternative — or "None".
- Deviations from the contract and why — or "None".

## Verdict
- COMPLETE / HOLD / PARTIAL:
- User-visible result:
- Exact commit and artifact identity:
- Built / tested / reviewed / deployed / live-verified (each separately):
- Acceptance IDs: passed / failed / not exercised (list every ID):
- Unresolved boundaries and next exact action:

## Verification
| Gate | Command + cwd | Candidate | Exit + evidence | Result / coverage |
|---|---|---|---|---|

- Focused and full suites; expected vs collected test count:
- Real end-to-end or UI proof:
- Security and dependency scan results and freshness:
- Reviews: who, target, status, independence limits:
- Findings accepted and regression tests added:
- External readback (if writes were authorized):
- Gates NOT exercised and why (never implied PASS):

## Cleanup receipt
| Temporary path | Owner | REMOVED / RETAINED / BLOCKED | Evidence or reason |
|---|---|---|---|

- If nothing temporary was created, write NONE and why.
- Remove only what this task created. Preserve logs, review verdicts, rollback material.
- Remove git worktrees with `git worktree remove`, not recursive delete.

## Efficiency receipt
- Elapsed per phase; blocked time by cause:
- When the first real end-to-end proof happened:
- Worker lanes, retries, timeouts:
- Review cycles and defects by root cause:
- Owner scope changes vs preventable rework:
- No speedup claims without a baseline.

## Stop or hand off
- COMPLETE: stop. Improvements go to backlog.
- HOLD / PARTIAL: preserved paths, pending gate, next command, rollback.
