# Contained automation qualification

Use for synthetic parser-to-wrapper tests whose fixture already applies an OS sandbox.

## Procedure

1. Inspect both the suite launcher and the fixture subprocess method. Record required executable/runtime paths, readable roots, synthetic cwd/HOME/TMPDIR, write roots, and network/Apple Events restrictions. A nested sandbox startup error is not an application regression.
2. If nesting prevents execution, compose a single test-only boundary satisfying both policies. Keep real-home data and network denied; permit writes only in synthetic scratch and explicitly required device sinks. Use the discovered executable allowlist and exact runtime paths, not broad home access. Bind shell fixtures to writable synthetic cwd as well as HOME/TMPDIR.
3. Before importing pytest or fixtures, verify actual denied operations inside that boundary:
   - Check protected paths with metadata-only stat; require permission denial without opening private content.
   - Open a known test source with `os.O_WRONLY`, without truncation or creation flags. Require denial; close immediately and fail if unexpectedly permitted.
   - Attempt creation only at an owned disposable probe outside the allowed write root; unexpected creation fails qualification.
   - Attempt a local ephemeral socket bind rather than an outbound connection; require denial.
   - Invoke forbidden executables with harmless help/version arguments and a short timeout. Require execution denial, not merely a nonzero program exit. Never use provider calls, credential-bearing arguments or Apple Events as probes.
4. Only after probes pass, inject the test fixture command method to execute under the existing outer boundary instead of starting another sandbox. Assert its synthetic home is beneath the authorized scratch root. An environment flag alone must never authorize skipping a boundary. Production dispatch remains unchanged.
5. Pass absolute test paths when the launcher changes cwd. Inspect whether positional paths replace or append defaults; explicitly enumerate the complete parser, preservation and installed-style flow suites so a green subset is not reported as the full gate.
6. Keep each failed run's log, execute the combined gate after correction, and bind results to source and adapter hashes. Report executed assertions separately from setup failures, missing dependencies and untested production behavior.

## Probe interpretation

Do not treat `sandbox_check` returning −1 as a permission verdict: path resolution can fail before evaluation. ENOENT proves absence, not isolation. Prefer known existing test targets or actual harmless probes. A protected-path EPERM supports only the denied operation actually observed; do not generalize it into proof of unrelated command or write restrictions.

## Real dependency qualification without live imports

1. When a fixture assumes a sibling core checkout, locate the actual required symbol in current source before treating the test as unavailable. Inspect the minimal import closure; do not import the live plugin or copy its credential/state tree just to satisfy one code dependency.
2. Stage explicit regular code files into a separate fixture root, record source identities and byte hashes, and inject that root through the existing contained test adapter. Exercise the real registry/helper rather than replacing the behavior with a stub.
3. If package initialization pulls unrelated runtime hooks, use a documented namespace-only fixture package only when the exercised module does not depend on those initialization effects. Label the proof as the selected module/entrypoint path, not full plugin initialization.
4. Rerun the entire previously blocked test file plus the feature integration suite. Keep frozen candidate bytes unchanged; if implementation advances concurrently, bind this result to the old tip and rerun affected gates on the successor.
5. Compare required installed code dependencies separately from the intended changed destinations. Preserve unrelated drift; successful fixture imports do not establish installed dependency parity or loaded gateway compatibility.

## Efficient recovery

After repeated workers hit the same setup failure, inspect the precise launcher/fixture call chain in the parent and verify the smallest correction before redispatching. Give the next worker the working command, interpreter, absolute test inventory and actual result—not another open-ended request to troubleshoot the environment. Do not broaden production scope or weaken containment to finish faster.
