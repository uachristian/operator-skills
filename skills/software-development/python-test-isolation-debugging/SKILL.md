---
name: python-test-isolation-debugging
description: "Use when a pytest test passes alone but fails in the full suite. Find the leak (sys.modules, env, globals) and fix the cause."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [pytest, test-isolation, flaky-tests, sys.modules, conftest]
    related_skills: [build-execution-standard, development-quality-loop]
---

# Python test-isolation debugging (pass alone, fail together)

## When to Use

A test passes alone but fails in a full or combined run. Covers order-dependent pytest failures: module, global, env, or sys.modules state left behind by another file or a conftest. The goal: find the polluting file, fix isolation, and prove the whole set passes together. Follow build-execution-standard for the surrounding build gates.

## Procedure

1. **Isolated workspace and env, outside the Hermes home.** Create the worktree and test interpreter under `~/.cache/...` (e.g. `~/.cache/hermes-test-wt/<task>`, `~/.cache/hermes-test-envs/<task>`). Do this *before* building, and never move the worktree afterwards. Why: Hermes' home-I/O test guard fails any I/O under `~/.hermes`, and PM probes `<checkout parent>/manifest.json`, so every test fails falsely there. A moved worktree also keeps stale editable-install paths and pytest assertion-rewrite caches. Build the env with the repo's documented command (Hermes: `python -m pm.build_env --source . --out <abs path> --group dev --group test --extra <feature>`) and include the optional extra the tests import (`--extra telegram`), or those tests skip or fail to collect.
3. **Reproduce in ONE shared process.** Write a wrapper script with the same hermetic env as the runner: `env -i PATH HOME TZ=UTC LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONHASHSEED=0 PYTHONUTF8=1 <env>/bin/python -m pytest -p no:randomly -p no:cacheprovider "$@"`. Run it over the whole related file set and save the log. Group failures by file and by `E ` line.
4. **Bisect by pairs:** `for f in candidates; do pytest -q -x $f <victim>; done`, then record the failing pairs. If nearly every file in one directory breaks the victim, the polluter is that directory's `conftest.py` or a shared helper, not a single test.
5. **Fix the polluter, not the victim.** See `references/sys-modules-mock-leaks.md` for the common mock-install pattern and its fix. Prefer "don't install the global stub when the real thing is available", or scope it with `monkeypatch.setitem(sys.modules, ...)`. Don't add re-import hacks to victim files.
6. **Handle the fallout.** Tests that only passed because of the stub now see real library behavior. Fix their inputs to match real semantics; don't re-mock.
7. **Separate residual failures.** Rerun any remaining failure alone, 3 times. If it also fails alone, it is not the leak. Trace it with temporary prints, restoring the files from a backup copy afterwards. Don't label it a product bug before tracing.
8. **Prove it, with three pieces of evidence:**
   - (a) The shared-process run over the full related set is green.
   - (b) The canonical per-file runner on the same set is green.
   - (c) A wider directory per-file run has the identical failing-file set before and after the change. Compare with `grep '^  tests/' log | sed 's/  (.*//' | sort -u` and `comm`.

   Report pre-existing unrelated failures as unverified, not as fixed.
9. **Commit test-only changes** on a local branch. Before merging or pushing, ask whether the user wants a merge or a PR.

## Pitfalls

- Run long suites (full directories take about 9 minutes) as background processes and poll them. Keep foreground calls short. Avoid `git log -L` or broad history queries in the foreground, because they can exceed the tool timeout and orphan the turn.
- The agent safety rail may block bulk `find ... -delete` of `__pycache__`. To invalidate stale rewrite caches, `touch` tracked `.py` files or set a fresh `PYTHONPYCACHEPREFIX` instead.
- Read a pipe's real exit code. `cmd | tail` reports tail's status, so redirect to a log file and `echo exit=$?`.

## Communication

While the long environment setup or suite runs, send the user short status updates. Explaining a delay after the fact ("why'd you get stuck?") means the updates came too late. When the user asks what the bug was, explain the mechanism in plain words first (what state leaked, why it shows only in shared runs), then the fix.

## References

- `references/sys-modules-mock-leaks.md`: conftest stub leaks, the `__file__` guard bug, the PathFinder fix, real-library semantic fallout, and asyncio done-callback timing.
