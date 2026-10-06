---
name: test-isolation-debugging
description: "Use when any test passes alone but fails in a full run. Bisect the polluter and fix shared state, not the symptom."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [testing, pytest, isolation, flaky]
    related_skills: [development-quality-loop, build-execution-standard]
---

# Test isolation debugging

## When to Use

A test passes alone but fails in a full or combined run, or the user reports order-dependent test failures caused by leftover module, global or env state.

Goal: find the test file or fixture that leaves module, global or env state behind, fix the leak properly (never by deleting assertions, reordering files or adding retries), and prove the whole related suite passes together.

## Procedure

1. **Isolated workspace.** Create a git worktree on a `local/` branch from the target commit, OUTSIDE `~/.hermes` (e.g. `~/.cache/hermes-test-wt/<task>`). Build the test env outside it too: `python -m pm.build_env --source . --out <abs path> --group dev --group test --extra <feature>`. Add the feature extra (e.g. `telegram`) when suites `importorskip` that library; otherwise half the files silently skip. Export `HERMES_PYTHON=<env>/bin/python`.
3. **Reproduce in one process.** Use a wrapper script with the runner's hermetic env: `env -i PATH HOME TZ=UTC LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONHASHSEED=0 PYTHONUTF8=1 PYTHONPYCACHEPREFIX=<fresh dir> <env>/bin/python -m pytest -p no:randomly -p no:cacheprovider "$@"`. Run every related file together and tally failures per file and per `E` line.
4. **Bisect the leaker.** Loop over the candidates, running `<candidate> <victim> -x -q` together, and list the pairs that fail. If nearly every file in one directory breaks the victim, the leaker is that directory's `conftest.py` (it executes at collection, before any test).
5. **Fix at the source**, then rerun the combined set. Expect a second wave: tests that only passed against the leaked fake. Fix their inputs to match real behavior; don't re-add the fake.
6. **Classify the remaining failures.** Rerun each one alone 3 times. If it fails alone, it is not isolation; read the code path before calling it a product bug (often a timing assertion; see the reference).
7. **Prove it.** The combined single-process run is green, the canonical per-file run on the same files is green, and a broader per-file run has a before/after failure-file set diff (`comm -13 base fix`) showing no new failures. Commit test-only changes with an explanatory message; report branch, commits and anything left unmerged.

## Pitfalls

- Never put the worktree or test env under `~/.hermes`: `tests/home_io_guard.py` refuses all I/O under the real Hermes home and the runtime probes `<parent>/manifest.json`, so every test fails for a false reason.
- Don't move a worktree after building its env or running tests. The editable install and pytest's assertion-rewrite caches keep the old absolute paths. Rebuild the env, use a fresh `PYTHONPYCACHEPREFIX`, and `touch` tracked .py files to invalidate rewrite caches (bulk deleting `__pycache__` may be blocked).
- Run helper scripts from a clean directory: a stray `inspect.py` or similar in a scratch dir shadows the stdlib.
- Avoid slow `git log -S` / `-L` over huge histories in a foreground call; it times out and wedges the session. Use `search_files` / `read_file` on the current tree instead.
- Don't call a failure a product bug until you've read the code path; correct an earlier wrong classification plainly in the final report.

## References

- `references/leak-patterns.md`: common leak shapes (sys.modules mocks, conftest collection-time installs) and fixes, plus async timing false positives.
