# Exact-candidate rollback references and mid-review live drift

Use this focused probe when a frozen, manifest-backed analysis candidate is reviewed alongside a mutable live profile.

## Rollback-reference closure

1. Enumerate every current operational rollback pointer in README, build contract, closeout JSON/Markdown, change contract, and release manifest.
2. Resolve each pointer and classify it as current remediation backup, historical backup, or prospective/not-yet-created verdict.
3. Require current operational instructions to name one manifest-owned current rollback packet. Historical closeouts may preserve their historical rollback only when explicitly marked historical and not reused by the current README.
4. Inspect the referenced restore manifest's actual targets. A stale pointer is HIGH when following it can restore a wider obsolete tool/runtime/skill set or reintroduce an authority/maturity/safety regression.
5. Check packet closure: if the change contract requires `backup-manifest.json`, `RESTORE.md`, or pre-change copies, verify those exact files are frozen or separately identity-bound. Bind the current manifest digest and entry count from the restore instructions, then recompute both. A live-only unpinned rollback packet is not candidate-bound evidence.
6. Cross-check machine-readable cleanup fields against restore prose. A `new_paths_to_remove_on_rollback` list that names nonexistent/generic release files or contradicts a policy to preserve baselines, rejected candidates, verdicts, and audit records is a release blocker. If audit artifacts must remain historical evidence, the removal list should be empty.
7. A forward authority pointer to a not-yet-created verdict is acceptable only as a tightly bounded release transaction: the exact planned path is fixed in the candidate, the record remains explicitly historical/pending and non-authoritative, release remains HOLD, and the verdict is created only after exact-candidate approval. Generic filenames, stale older-candidate pointers, or claims that the prospective verdict already exists are blockers. If those conditions are not met, leave the historical authority field unchanged or use an explicit pending-candidate pointer.
8. Check both prose and machine-readable status twins (`closeout.md` and `closeout.json`, README/build contract, skill/reference, journal/index). Preserve explicitly historical HOLD values and counts, but synchronize the active-authority pointer and supersession marker.
9. When a touched file was omitted from the original pre-change backup, recover its exact prior bytes only from a verified older backup/frozen candidate, record that provenance, and extend the rollback manifest before release. Never reconstruct unknown old bytes from memory.

## Mid-review drift handling

1. Hash manifest, archive members, and corresponding live files before tests.
2. Repeat after every probe batch and before verdict.
3. If live begins at full parity and later drifts, report both observations; do not overwrite the review history with only the final count.
4. Identify every drifted path and expected/actual hash. Check for a newly created successor archive or manifest.
5. Keep the frozen ancestor verdict separate from the successor. Even a remediation-only successor needs a fresh exact-candidate review.
6. Do not interpret concurrent remediation as permission to switch scope silently. Return HOLD for the supplied ancestor/live-integration pair and name the successor as unreviewed.

## Review and closeout budget

Before dispatching an exact-candidate reviewer, run a cheap local closure scan for status twins, stale verdict/baseline names, rollback cleanup contradictions, manifest digest/count drift, archive traversal/symlinks/write bits, and live/archive parity. This avoids spending independent-review cycles on deterministic bookkeeping defects.

Reserve enough tool/session budget after review for:

1. reproducing the reviewer finding in the parent lane;
2. one bounded remediation and a newly numbered immutable candidate;
3. rerunning exact gates and obtaining the successor verdict;
4. writing and reading back the release verdict;
5. durable vault/project closeout.

If the budget ends while the final reviewer is pending, report the candidate as staged/HOLD even when every parent gate is green. A working live fix is not a formal exact-tip release until the named verdict exists.

## Minimal evidence pattern

- frozen manifest hash and declared row count;
- archive `N/N`, with no extras, omissions, traversal paths, or symlinks;
- initial live `N/N` and final live `M/N` if drift occurs;
- exact drifted paths and expected/actual hashes;
- stale rollback pointer line, contradictory current rollback line, and the obsolete restore target behavior it would reintroduce;
- confirmation that no reviewed source or live file was modified by the reviewer.
