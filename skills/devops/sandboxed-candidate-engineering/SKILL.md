---
name: sandboxed-candidate-engineering
description: "Use when building proposal-only labs that find bounded improvements, build candidates in isolation, and hand humans a reviewable packet."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [sandbox, candidate, verification, proposals, change-control, docker, security]
---

# Sandboxed Candidate Engineering

Use when building a bounty-style improvement lab, autonomous patch scout, disposable candidate builder, untrusted update verifier, or any workflow that should produce tested change proposals without modifying production.

This skill governs the full class-level pipeline:

```text
approved sanitized inputs
  → one bounded problem
  → isolated baseline and candidate
  → protected proof contract
  → hardened execution
  → independent review
  → untrusted local proposal
  → separate owner-approved promotion
```

For production promotion, load `operational-change-control`.



## Default operating contract

Freeze these before implementation:

- Goal and non-goals.
- Approved source lanes and explicit exclusions.
- Trust boundaries and credential policy.
- One-candidate run budget.
- Acceptance criteria and exact verification commands.
- Proposal schema and human approval boundary.
- Rollback and artifact-retention policy.

Safe default: on-demand pilot, local proposals only, no cron, no messaging token, no production credentials, no external writes, and no automatic promotion. Prove two or three representative candidates before proposing scheduling.

## Trust model

Treat all of the following as untrusted:

- Candidate source and configuration.
- Candidate-authored tests.
- Command specifications.
- Test stdout/stderr.
- Finding, risk, rollback, and proposal text.
- Third-party pages or issue descriptions used as evidence.

The trusted computing base should be deliberately small: reviewed controller, pinned verifier runner, immutable verifier image, policy, container runtime, and owner-approved input catalog.

## Sanitized input catalog

1. Put approved source roots in trusted policy, never in caller-controlled catalogs. Reject catalogs that try to self-authorize roots.
2. Use exact allowlisted files or immutable source revisions; never broadly mount a home directory, profile root, vault, or production repository.
3. Reject symlinks, special files, unsupported/binary files, oversized files, path traversal, sensitive path components, and secret-like text or common JSON secret shapes.
4. Apply the same checks to destination paths and descriptive labels, not just source filenames.
5. Read once, enforce the byte limit again after reading, scan those exact bytes, and hash the staged bytes—not a second read of a moving source path.
6. Emit a deterministic manifest with per-file hashes and a content-addressed snapshot ID.
7. On cache reuse, revalidate the exact manifest, the complete snapshot-root inventory (not only the expected payload subtree), staged file set, regular-file/symlink status, size, SHA-256, UTF-8, and secret scan. Reject every unexpected root-level file; a matching directory name or snapshot ID alone is not evidence.
8. For structured formats such as JSON, scan both the exact raw bytes and a parsed/canonical semantic representation. Unicode-escaped or otherwise encoded key names must not turn into secret-like keys only after downstream decoding.
9. Never copy `.env`, auth stores, sessions, customer transcripts, raw messages, personal-only material, or live service state.
10. Re-run source and trusted-policy hashes after verification so mutation cannot be hidden.

## Proof contract

A passing test is not enough. The verifier must establish that the candidate fixed the reproduced problem under the same contract:

1. Require at least one baseline command to reproduce a real nonzero failure.
2. Require every candidate command to exit successfully.
3. Require baseline and candidate to run byte-identical command vectors and timeouts.
   - Resolve the trusted test runner before candidate-controlled paths enter module search. For Python unittest, use isolated startup such as `python3 -I -m unittest ...` with an explicit reviewed top-level, or execute a trusted absolute harness entrypoint. Add a regression where candidate root `unittest.py` exits zero and require the verifier to reject it.
4. Keep the protected `tests/` tree byte-identical between baseline and candidate, or mount one separately reviewed test tree into both phases.
5. Reject “command not found,” timeout, containment failure, or runner error as a valid baseline reproduction even if it is nonzero.
6. Run baseline and candidate in separate disposable containers. Each phase sees only its own read-only source tree and the read-only spec; never expose both writable copies in one workspace.
7. Validate the returned evidence envelope on the host: exact result-envelope key set, phase, containment key set/booleans, command count/order, exact argv, expected exit, actual exit, timeout state, harness-error absence, output size/digest format, and every `passed` field.
8. Hash the spec, trusted policy, host verifier/controller modules, baseline tree, candidate tree, protected tests, verifier runner, Dockerfile, immutable image ID, and patch into the candidate identity.
9. Keep a trusted image-build record binding the immutable image ID to the current runner and Dockerfile. Refuse verification when host source changed after the image was built; otherwise a manifest can claim current runner bytes while executing an older baked runner.
10. Recheck spec, policy, controller, and source hashes after execution, and require proposal generation to compare them with the successful manifest.

## Hardened candidate execution

Use all applicable controls:

- `--network none` and verify there are no non-loopback routes.
- `--read-only` root filesystem.
- `--cap-drop ALL`.
- `--security-opt no-new-privileges:true`.
- Non-root UID/GID.
- CPU, memory, PID, file-size, file-descriptor, and wall-clock limits.
- No Docker socket.
- No host home, production source, profile, credential, vault, cloud, SSH, or live-state mounts.
- Read-only source and specification mounts.
- Writable `tmpfs` only for disposable workspace and temporary files.
- Explicit minimal child-process environment; never inherit the orchestration shell.
- Named containers plus `--rm` and forced cleanup on timeout.

Resolve a tag to an immutable image ID and run the ID itself. Inspecting an ID but executing the mutable tag leaves a time-of-check/time-of-use gap.

## Dependency and image gate

- Pin the base image by digest.
- Keep the image minimal and remove package managers/tools the verifier does not use.
- Scan the final image, not merely the base image.
- A good production-facing default is zero known vulnerabilities, including low-risk tooling findings. Replace the base or remove unused vulnerable packages rather than normalizing exceptions.
- Record the immutable final image ID and scanner result in evidence.
- Do not silently introduce an unfamiliar third-party runtime image merely to improve a scan; prefer a hardened official base or obtain explicit approval.

## Proposal integrity

Proposal generation is a separate trust boundary:

1. Refuse failed, malformed, or incomplete verification manifests.
2. Compare current spec, trusted-policy, host-controller, baseline, candidate, and patch identities with the successful manifest before rendering.
3. Record the proposal-generator hash in the proposal artifact and carry an explicit machine-readable trust label in JSON as well as the human-facing banner.
4. Show complete command vectors, exits, exact image ID, policy/controller/runner identities, patch hash, manifest hash, risk, rollback, and limitations.
5. Label candidate prose as untrusted and review-only. Escape or reject raw HTML, tracking pixels, clickable links, control characters, unsafe Markdown, and candidate language that falsely asserts production approval.
6. Never let candidate text assert approval or change the promotion boundary.
7. Local outbox creation is not delivery; delivery is not promotion; promotion is a separate owner-approved workflow with fresh verification.

## Review sequence

Default substantial-build budget:

1. One implementation pass.
2. One parent adversarial pass.
3. One focused independent review of an immutable archive or exact commit.
4. One remediation pass for reproduced material findings.
5. One exact-tip rerun of every required deterministic gate.
6. One bounded exact-tip release review when the frozen acceptance contract requires independent approval.

Give reviewers one frozen artifact, one subsystem, one question, and bounded reproduction commands. Preserve review findings as regression tests. A review of the pre-remediation commit remains a finding source, not an exact-tip verdict. Reserve tool/call budget for the final review; if it cannot execute, return **HOLD** rather than extrapolating from earlier evidence.

## Pilot design

Use representative but clearly labeled fixtures:

- Deterministic output compaction or parser correction.
- Stale-reference or schema drift detection.
- Fail-closed snapshot/secret boundary.
- Containment probe proving candidate cannot see or mutate the other phase.

Synthetic pilots validate the machinery; they do not establish real-world value. Continue toward scheduling only after at least one real sanitized estate candidate is valuable enough to consider promoting.

## Pilot pattern

After the synthetic pilots pass, run two or three on-demand real bounties before adding delivery or scheduling:

1. Stay inside the already-reviewed trusted-policy allowlist. If a tempting lane such as a live cron store is not allowlisted yet, it may supply read-only discovery evidence but must not become candidate snapshot source without separate policy review.
2. Choose a deterministic, behavior-level, low-risk defect that can be reproduced with synthetic local fixtures and no credentials. Reject lint-only cleanup, stale-looking paths that resolve after an intentional `cd`, and historical nonzero exits that encode expected health semantics.
3. Reproduce the defect against the live source read-only, then snapshot that exact file through the lab catalog and build baseline/candidate only from the sanitized snapshot.
4. Keep the protected tests byte-identical and prove host controls first: baseline fails for the intended behavior and candidate passes under the same isolated command.
5. Protected tests must exercise an interface that exists in both baseline and candidate. Do not make the baseline fail merely by calling a helper signature introduced only by the candidate; prove the original behavior through the shared public surface.
6. Keep specs inside trusted enums and schemas, including allowlisted classification labels. A rejected spec is not verifier evidence even if host tests pass.
7. Run the hardened verifier, fixture secret scan, and public proposal path. Treat `propose` as the final evidence gate because it should rerun verification and strictly revalidate the manifest before rendering.
8. End with local outbox artifact paths and hashes, no remaining containers, no tracked source changes, and an explicit statement that production promotion remains separate owner-approved change control.
9. Count a run as useful only when the proposal addresses a reproducible operational, security, or reliability behavior—not because the harness turned green.

## Graduation to external delivery

After two or three useful real proposals, stop the pilot and make a release decision before wiring messaging:

1. Summarize proposal usefulness, false leads rejected, verification results, and operational diversity. Do not graduate solely on pass count.
2. Treat any Telegram/Slack/email sender as a new external-delivery boundary requiring an exact plan, risks, rollback, route review, and owner approval.
3. Safe first delivery stage is manual-only and owner-private: validate the proposal JSON/schema and recorded hashes, escape untrusted text, allowlist the destination, dedupe by proposal ID, record a delivery receipt, and send exactly one packet.
4. Delivery must never be interpreted as approval. Preserve explicit `review-only`, `untrusted candidate`, and `separate promotion required` fields in machine and human output.
5. Keep cron, automatic retries that can duplicate messages, production writes, and automatic promotion disabled until delivery itself has been tested and separately graduated.
6. Rollback should disable/remove only the sender and its local receipt state; the lab, verified proposal, and production systems should remain untouched.

## Common failure modes

- **Shared writable baseline/candidate workspace:** one phase can forge the other. Use separate containers and source mounts.
- **Candidate edits its own tests:** enforce a protected identical test tree.
- **Candidate root module shadows the test runner:** `python -m unittest` from the candidate root can import candidate `unittest.py` and exit before tests run. For Python unittest suites, use isolated startup (`python3 -I -m unittest discover -s tests -t . -v`), make `tests/` importable when needed, and keep a regression proving root-level shadow modules cannot false-pass.
- **Different commands per phase:** a trivial candidate command can fake success. Require identical vectors/timeouts.
- **Any nonzero counts as reproduction:** runner errors can masquerade as baseline failures. Validate the complete result envelope.
- **Mutable image tag after inspection:** execute the inspected immutable image ID.
- **Stale spec/policy/controller with fresh-looking proposal:** compare every current trust-base identity before rendering. Public proposal commands should run fresh verification first, then strictly revalidate the manifest envelope, patch bytes, source identities, containment, and command evidence before writing outbox artifacts.
- **Catalog self-authorizes source roots:** source authority belongs in trusted policy, not caller input.
- **Snapshot cache trusts its name/ID:** revalidate manifest, file set, bytes, and scans on every cache hit.
- **Source is read twice:** a concurrent change can make the manifest hash bytes that were not staged; hash the already-read staged bytes.
- **Current runner hash with an older baked runner:** bind image ID to runner/Dockerfile in a trusted build record and require a rebuild on mismatch.
- **Raw candidate Markdown:** can add links, HTML, tracking pixels, or approval-looking text. Treat all proposal fields as untrusted.
- **Scanner regression fixture triggers the repository's own tracked-file scan:** construct synthetic key/value strings at runtime while still emitting the exact secret-shaped fixture under test.
- **Compile/test artifacts pollute candidate trees:** direct Python bytecode/cache output to disposable paths and reject generated binaries before verification.
- **Scanner only checks the base:** scan the final image after local changes.
- **Design pilot quietly becomes production automation:** no cron, delivery, or promotion until separately approved.
- **Frozen source anchor is advanced just to recover green tests:** an external authority moving past a reviewed planner commit should make the historical planner fail closed. Preserve the runtime anchor and historical bytes; stabilize tests with a disposable checkout at the frozen commit. Also remember that detached Git worktrees omit ignored local `state/` fixtures—classify missing-fixture setup errors separately, materialize only the minimal transitive sanitized fixture closure, prove every copied path stays ignored, and never weaken trust or bulk-copy credential-bearing state merely to make the suite green. See `references/proposal-planner-gate-and-frozen-anchor-lessons.md`.
- **Producer/consumer compatibility is proved with hand-built JSON:** schema lookalikes miss canonicalization, defaulting, and field-coupling defects. At the integration gate, run the actual producer on disposable synthetic inputs and feed its exact canonical bytes to the actual consumer; require the gate to run without skip and retain no real artifact.
- **A tracked release manifest tries to bind its own commit/tree:** use either post-commit evidence or source commit A plus a manifest-only wrapper B. Bind B itself only in a later signed envelope, and regenerate B after every source remediation. See `references/proposal-planner-gate-and-frozen-anchor-lessons.md`.
- **Producer and consumer silently choose different wire details:** freeze nested key names, Git-versus-POSIX source modes, exact integration environment names, confirmation flags, allowed file additions, verifier ownership, and exact installable/review-only inventory membership before parallel implementation. Require actual producer → actual consumer with zero skips. See `references/bounded-source-only-security-controller-builds.md`.
- **Release validation accepts a mandatory subset:** subset checks allow omitted runtime modules or arbitrary review rows. Require exact inventory membership, exact install flags/modes, and one-read canonical byte validation; wrapper B inventory bytes must equal source A. See `references/bounded-source-only-security-controller-builds.md`.
- **Parent and worker edit one worktree concurrently:** a worker's internal “done” checklist is not formal delegation completion. Wait for the final result, then re-read changed bytes; use a separate snapshot/worktree for concurrent review. See `references/bounded-source-only-security-controller-builds.md`.
- **Strict ancestor-symlink guard breaks only the test harness:** macOS temp paths may lexically traverse `/tmp` or `/var` symlinks. Resolve the temp parent inside the test helper and prove the plain documented test command; do not weaken the runtime guard or rely only on an orchestrator-set `TMPDIR`.
- **“Failure writes nothing” ignores output-root creation and allocation order:** inject failures at both temporary allocation (`mkstemp`) and atomic publication (`link`/rename). Track whether this invocation created the root; cleanup in dependency order—temporary file, final link created by this invocation, then empty root. If allocation remains outside the cleanup boundary, document the possible owner-only empty-root remnant instead of claiming universal rollback. See `references/proposal-planner-gate-and-frozen-anchor-lessons.md`.
- **Pre-remediation review is reported as the release verdict:** any changed bytes supersede the earlier exact-tip verdict. Rerun deterministic gates and the required independent review; if interrupted first, report **candidate implemented, unreleased**.
- **Interrupted-cycle recovery is counted as completed analysis:** a fail-closed infrastructure/error terminal record must not advance unchanged-source cooldown, `last_completed_at`, or last analyzed source identity. Preserve prior successful coverage, but keep the interrupted same-source target immediately eligible for retry.
- **Abandoned disposable roots retain copied broker credentials:** startup recovery must remove or quarantine strictly scoped stale `RUN_ROOT/<cycle_id>` directories after stale containers are gone and before new work begins. Reject symlinks, non-directories, and unknown residue rather than deleting broad paths or continuing with credential copies on disk.
- **Source-only controller breadth outruns verification:** adding every planned module before updating the exact-file repository verifier, replacing stale tests, and completing one real role path can exhaust the execution budget with a large unverified diff. Freeze the latest exact vocabulary first, implement complete vertical slices, rerun the original RED batch after each slice, and reserve budget for verifier/full-suite/lint/compile/diff gates. Source-only containment scaffolds that always reject are not installation-grade role implementations. See `references/bounded-source-only-security-controller-builds.md`.
- **Static wrapper text is mistaken for parser proof:** a shared parser factory may correctly disable abbreviation even when the literal does not appear in each script. Exercise the real parsers with accepted and forbidden argv, then use AST/call-order tests for role isolation and installed-gate precedence.

## Release checklist

- [ ] Goal, non-goals, trust boundaries, acceptance criteria, rollback frozen.
- [ ] Source roots and command suites come from trusted policy, not caller catalogs/specs.
- [ ] Source catalog exact and secret/path/symlink gated; staged bytes—not a second source read—are hashed.
- [ ] Cached snapshots are fully revalidated before reuse.
- [ ] Baseline failure reproduced under protected tests.
- [ ] Candidate passes the same commands/tests.
- [ ] Baseline and candidate run in separate containers.
- [ ] Immutable image ID executed and recorded; trusted image-build record matches current runner/Dockerfile.
- [ ] Policy, host controller, spec, source trees, tests, runner, Dockerfile, image, and patch identities are bound and rechecked.
- [ ] Every containment and result-envelope field host-validated.
- [ ] Source/spec/patch hashes unchanged after execution.
- [ ] Final image vulnerability scan passes policy.
- [ ] Independent review findings converted to regression tests.
- [ ] Exact final tip reran all deterministic gates.
- [ ] Required exact-tip release review completed; otherwise verdict remains HOLD and earlier reviews are marked superseded.
- [ ] Any cross-repository schema handoff is exercised actual-producer → actual-consumer on disposable synthetic inputs with no skip or retained artifact.
- [ ] Any tracked source-release manifest avoids Git self-reference (external evidence or source A / manifest-only wrapper B) and later signed authority binds the wrapper identity.
- [ ] Proposal remains local/untrusted and promotion remains separately gated.
- [ ] No containers remain and rollback is documented.

## References

- `references/proposal-planner-gate-and-frozen-anchor-lessons.md` — planning-only gate separation, deliberate schema incompatibility, post-commit evidence without Git self-reference, frozen-anchor test stabilization, ignored-state worktree handling, and correct one-shot review invocation.
- `references/bounded-source-only-security-controller-builds.md` — exact-contract reconciliation, complete vertical-slice budgeting, RED/stale-suite discipline, installed-versus-disposable capabilities, real role wiring, source-A/wrapper-B release construction, and interruption reporting for privileged source-only controller builds.
