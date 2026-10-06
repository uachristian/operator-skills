# Build contract and milestone handoff

Fill before implementation. Placeholders are not commands. Keep the filled copy with the task, not in long-term memory. No secrets or real customer data.

## Outcome and authority
- User-visible outcome / smallest viable solution:
- Non-goals:
- Approval reference and exact authorized actions:
- Prohibited actions, data, credentials, production surfaces:
- Risk tier (routine / elevated / high) and extra gates:
- Repo root, base commit, existing dirty/untracked files and their owners:
- Rollback artifact and exact recovery steps:
- Completion budget; time reserved for integration, review, release:

## Discovered project commands
Copy from project docs, manifests, task runners, CI. Read side effects before running.

| Gate | Purpose | Source of command | Exact command + cwd + env | Side effects | Required evidence |
|---|---|---|---|---|---|
| P1 | Read-only preflight | TO DISCOVER | NOT RUNNABLE | none | runtime, deps, status, baseline failures |
| F1 | Fast affected checks | TO DISCOVER | NOT RUNNABLE | local only | exit code, log, test count |
| R1 | Full release checks | TO DISCOVER | NOT RUNNABLE | per risk | full suite, integration, security scan |

- Baseline failures that existed before this work:
- Missing prerequisites and approved resolution:
- Security scan surfaces; known vulnerabilities (target: zero):

## Acceptance
| ID | Observable result | Test or probe | Evidence + exit | Status |
|---|---|---|---|---|
| A1 | TO DEFINE | NOT RUNNABLE | none | NOT VERIFIED |

## Shared interfaces
- Interface version and fixture owner:
- Synthetic fixture paths:
- Cases covered: healthy, rejected/denied, missing, null/empty, boundary, stale:
- Exact field types and representations (e.g. epoch number vs ISO string):
- First real end-to-end slice and expected result:
- UI checkpoint, if any; simulated boundaries labeled as simulated:

## Parallel lanes
| Lane | Depends on | Worktree / branch / base | Write paths | Deliverable + check | Status |
|---|---|---|---|---|---|

- Worker cap actually available:
- Parent-owned shared files and long-running processes:
- Contract change protocol: pause dependent lanes, revise contract and tests, reissue; independent lanes continue.

## Milestone handoff (update when state changes)
- Current commit / artifact identity:
- Dirty paths and owners:
- Acceptance IDs passed, with evidence:
- Open failures and accepted review findings:
- Required reviews pending:
- Remaining approvals, rollback, next exact command:
- Time used / blocked / remaining:
