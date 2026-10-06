# Immutable start snapshots for moving non-Git candidates

Use this reference when reviewing a frozen manifest or bundle whose bound artifacts live at mutable absolute paths and another process may publish a successor during the review.

## Core risk

A review can correctly freeze the manifest at start, then accidentally execute successor bytes because a later disposable harness reopens the implementation pathname. Re-hashing at closeout detects the drift, but it does not make the intervening behavioral result exact-candidate evidence.

The same problem applies to shipped tests: a manifest-bound test file may still import the implementation from its live pathname. Hashing the test itself does not bind the bytes it later imports.

## Required start snapshot

Immediately after the starting manifest and every bound size/hash/type check pass:

1. Descriptor-read every behaviorally relevant bound artifact once.
2. Verify the captured bytes against the manifest's expected size and digest.
3. Keep those bytes in memory, or write them to a private disposable snapshot whose own manifest records role, original path, size, and SHA-256.
4. Execute source from the captured byte buffer with `compile(...); exec(...)`, or from the verified disposable snapshot. Never have the probe reopen the mutable candidate pathname.
5. Inspect test/import roots. Rebind a pathname-importing test only inside the disposable harness so it consumes the captured implementation bytes.
6. Keep credentials, network, provider UI, and production state unavailable.

Treat this as one indivisible freeze phase, not as a hash call followed later by tests against the original absolute paths. A publisher can replace the implementation between tool calls while the hash output still looks correct, and a maintained test can remain byte-identical while silently importing the successor. Before the first runnable gate, assert that every implementation, test, and fixture path resolved by the harness is snapshot-local. A `read_file` transcript or screenshot of source is review evidence, but it is not an executable snapshot.

Run independent required gates so one failure does not suppress unrelated evidence. In particular, do not place compile after the test suite behind `set -e` when the review contract requires both results; run compile separately or capture and report each status explicitly. A missing compile result is an evidence gap, not proof that compilation failed.

A useful probe record is:

```json
{
  "reviewedBundleSha256": "...",
  "captured": {
    "implementation": {"size": 0, "sha256": "..."},
    "offlineProbes": {"size": 0, "sha256": "..."}
  },
  "executionSource": "captured-bytes"
}
```

Do not copy unverified pathname contents and call that an ancestor reconstruction. The capture must have occurred while the requested bundle still bound those exact bytes.

## Phase-bound evidence

Label each result with the bundle digest and capture generation it actually consumed.

- A probe that compiled the start-captured bytes remains evidence for that starting digest even if the live pathname later changes.
- A probe that reopened a mutable pathname after drift is evidence for neither the requested predecessor nor the successor unless separately frozen and reviewed.
- Static observations recorded from verified start bytes remain valid findings against the predecessor, but do not approve or reject the successor automatically.
- If the starting bytes were not captured and disappear, stop behavioral review. Use `hash-verified-in-memory-ancestor-reconstruction` only when every reconstructed byte can independently reproduce the advertised digest.

## Drift closeout

At the first unexpected exception suggesting schema/source drift, re-hash the bundle and every bound file before debugging the probe. If identity changed:

1. Return `HOLD` for the requested digest.
2. Do not repair the harness against or continue reviewing the successor in the same review.
3. Preserve only results demonstrably bound to the start snapshot.
4. Report which bound roles changed and which trust anchors remained exact.
5. Remove disposable snapshot/harness files and state explicitly that the review made no candidate writes.

## Pitfalls

- A temporary harness containing `Path(LIVE_IMPL).read_bytes()` is still pathname-coupled.
- Passing a shipped suite before drift does not validate later custom probes that reopened live paths.
- A self-consistent successor manifest at end cannot close the predecessor's exact-candidate review.
- Do not report a probe setup failure caused by successor bytes as a predecessor product defect; classify it as invalidated evidence and rely on independently bound static findings only.
