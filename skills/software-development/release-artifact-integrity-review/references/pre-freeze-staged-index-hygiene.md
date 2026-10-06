# Pre-freeze staged-index hygiene

Use this before creating or reviewing any immutable source/archive candidate that will later be committed.

## Why

An archive can be behaviorally approved yet still fail the repository's staged hygiene gate. Even removing a trailing blank line changes the payload digest, making the prior exact-byte review stale. Running index checks only after review creates avoidable archive/review churn and tempts unsafe approval transfer.

## Sequence

1. Stage only the exact allowlisted paths; do not use a broad `git add .` in a dirty or production-adjacent repository.
2. Prove the staged path set exactly equals the approved scope with `git diff --cached --name-only`.
3. Inspect `git diff --cached --stat` and the actual staged diff.
4. Run `git diff --cached --check` before hashing, archiving, or dispatching reviewers.
5. Run any deterministic formatter or source gate that may change bytes, then restage and repeat steps 2–4.
6. Run behavioral, compile, secret, parity, and exposure gates against the same staged/worktree bytes.
7. Freeze the immutable candidate and record its digest only after every byte-changing gate is complete.
8. Before commit, prove the staged files still match the approved archive member hashes.

## If hygiene changes bytes after approval

- Do not bypass the gate.
- Do not silently overwrite the immutable archive.
- Mark the prior archive superseded.
- Re-freeze the corrected exact tip under a new path and digest.
- For a demonstrably non-semantic cleanup, request a bounded delta review that verifies: both archive identities, strict member hashes, the complete byte delta, AST/compiled semantic equality where applicable, and no other changed member.
- Commit only after that exact corrected candidate is approved.

This pattern complements stale-async-review handling: old verdicts remain evidence about old bytes, never approval for the successor.