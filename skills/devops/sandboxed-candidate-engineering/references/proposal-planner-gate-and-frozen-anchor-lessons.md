# Proposal-planner gate and frozen-anchor lessons

Use this reference when a proposal-only lab is being extended toward a future execution handoff but the current task is plan-only, the old planner has a frozen source trust anchor, or exact-tip verification runs from a worktree without ignored local evidence.

## Separate the plan release from implementation

A user approval to prepare/review a gate plan is not approval to implement that gate. The durable plan should state:

- exact source identities used for planning;
- goal, non-goals, trust boundaries, accepted file set, tests, risks, rollback, and completion budget;
- which later gates remain separately owner-approved;
- that no real eligible plan, signature, install, enablement, approval, or execution occurs in the planning release.

Release the plan as documentation-only, independently review the exact tip, and stop for a new implementation decision.

## Supersede synthetic contracts deliberately

If an earlier source-only controller contains a narrow synthetic fixture with the same nominal schema version, do not silently make a new installation-grade producer compatible. Freeze a distinct exact contract and action identity, require the current validator to reject it, and defer the cross-repository acceptance test to the separately approved controller-integration gate. This prevents a parser fixture from becoming accidental production authority.

## Avoid self-referential Git manifests

A file committed inside a Git tree cannot contain the final commit/tree identity that depends on those same bytes. Bind commit and tree outside the self-referential object and keep that binding non-authorizing until a later signed gate.

Two valid patterns serve different release shapes:

1. **External evidence envelope:** commit the source normally, then emit content-addressed post-commit evidence binding its commit/tree and manifest hash. Treat the envelope as untrusted evidence, not a signature or authorization.
2. **Two-commit source wrapper:** freeze source commit **A** with all code/tests/policy but no release manifest; make wrapper commit **B** add only a canonical unsigned release manifest that binds A's commit/tree and every reviewed inventory hash. The manifest must not claim B's identity. A later owner-signed installation envelope binds exact B commit/tree plus the manifest hash. Any remediation to source A invalidates and regenerates B.

For the two-commit pattern, verify mechanically that B changes exactly one manifest path, A is a local ancestor, every bound inventory path at B is byte-identical to A, the manifest is canonical, and the installation/runtime verifier distinguishes `install: true` runtime files from bound-but-not-installed tests/docs/review evidence.

## Cross-repository producer/consumer contracts

Do not approve compatibility using a hand-built JSON object that merely resembles the producer. Add one required disposable integration gate that runs the **actual producer** against synthetic inputs and feeds its canonical bytes to the **actual consumer** at both frozen tips. Require the positive path plus one-field-at-a-time mutations for schemas, action/trust identities, inventory, deadlines, and authorization booleans. The gate must retain no real plan/evidence artifact and must fail release if skipped because the peer checkout is absent.

When a legacy producer and consumer intentionally reject one another, keep that RED test until the separately approved integration gate. Replace it with the real positive integration only when both exact contracts exist.

## Preserve frozen runtime trust anchors

When an external authoritative repository advances beyond a planner's reviewed pinned commit, the old planner should fail closed. Do not advance the runtime anchor merely to turn tests green.

Instead:

1. Prove the candidate change did not modify runtime/test/config blobs when the current release is documentation-only.
2. Record the exact fail-closed reason and affected test count.
3. For future implementation, stabilize historical tests with a disposable local checkout at the already-reviewed commit.
4. Assert the runtime constant, historical output bytes, and rejection behavior remain unchanged.
5. Let the new planner consume its own strict post-commit evidence contract rather than inheriting the historical constant.

## Detached-worktree fixture pitfall

Git worktrees do not contain ignored local `state/` evidence. A suite that fails with missing ignored fixtures has not yet tested product behavior.

- First classify missing-fixture setup errors separately from assertion failures.
- Derive the **minimal transitive fixture closure** instead of copying the whole ignored state tree: start from the test's named proposal/receipt, follow only its bound Markdown, verification manifest, patch/source artifacts, and exact historical baseline/candidate files, and stop when the unchanged baseline passes.
- Copy each resolved regular file into the disposable worktree with its relative path, confirm every copied path is ignored, and assert prohibited output roots (for example prospective plans or source-candidate evidence) remain absent.
- Verify fixture hashes/identities when the contract provides them; never bulk-copy logs, credentials, keys, runtime state, or unrestricted profile directories merely because the worktree is missing data.
- Prefer a disposable, sanitized fixture copied or reconstructed under a temporary root.
- If a docs-only release changes no executable/test blobs, prove blob identity and run the unchanged suite from the canonical fixture-bearing checkout, while clearly attributing any pre-existing failures.
- Run reviewer/test commands with bytecode disabled and cache-free tooling when possible. Read-only analysis can otherwise leave ignored `__pycache__` or `.ruff_cache` files that later strict repository verifiers correctly reject; remove only the known generated caches and recheck tracked status before release.
- Never copy credentials, private keys, production state, or unrestricted profile data into the review worktree.

## One-shot independent reviewer invocation

Do not freeze one Hermes one-shot flag shape into the workflow. Before an exact-tip review, inspect the installed CLI's current `hermes --help` and, when applicable, `hermes chat --help`; releases may expose top-level `-z PROMPT`, while other versions expose `hermes chat -q PROMPT`.

A safe current shape when top-level help advertises `-z` is:

```bash
hermes --safe-mode --provider <provider> -m <model> -z "$prompt"
```

Rules:

- Use safe mode and a compact packet naming one immutable commit/tree, one subsystem, one question, and bounded read-only commands.
- Capture stdout and stderr separately plus exit code and byte counts.
- If argparse exits `2` and reports the whole prompt as an invalid command, no reviewer ran; correct the invocation from current help once rather than treating it as a review failure or rerunning unchanged.
- Do not pipe a multiline prompt into top-level interactive Hermes. Terminal UI output, timeout noise, or zero review stdout is no verdict.
- A verdict applies only to the exact bytes reviewed. Any remediation requires deterministic gates and a fresh exact-tip verdict when the frozen release contract requires independent approval.

## Strict ancestor guards and macOS temporary roots

A strict non-symlink-ancestor validator can correctly reject lexical `/tmp` or `/var` on macOS because those paths may traverse symlinks to `/private/tmp` or `/private/var`. This can make an otherwise hermetic test suite pass only when the orchestrator exports a special `TMPDIR`, while the plain documented test command fails.

Make tests self-contained instead of depending on the caller's environment:

```python
from pathlib import Path
import tempfile


def temporary_directory():
    return tempfile.TemporaryDirectory(
        dir=Path(tempfile.gettempdir()).resolve()
    )
```

Use that helper for every synthetic source/evidence/output root subject to ancestor checks. Verify both the focused suite and the plain documented full-suite command without a special `TMPDIR`. Do not weaken the runtime symlink guard merely to accommodate test defaults.

## Output failure semantics include directory creation

“Failure writes nothing” is stronger than “failure writes no plan file.” If the producer creates the fixed output directory before an atomic link/write, an injected link or filesystem failure may leave an empty directory behind.

Choose and test one truthful contract:

1. Track whether the output root was created during this invocation; on failure, remove any link/file created by this invocation and then remove the newly created empty root when the filesystem permits it; or
2. Document that failures write no plan bytes but may leave the fixed empty output directory.

Add failure-injection regressions at both allocation and publication boundaries:

- Inject `tempfile.mkstemp` failure after root creation. If the contract promises no directory remnant, the allocation call must sit inside an outer cleanup boundary that knows whether this invocation created the root.
- Inject `os.link`/rename failure after temporary-file creation. Cleanup order matters: unlink the temporary file first, unlink any final link created by this invocation, then remove the newly created empty root. Calling `rmdir()` while the temporary file still exists silently defeats cleanup.
- Assert both absence of content-addressed plan bytes and the chosen directory-state behavior.
- If the implementation deliberately accepts an empty owner-only root after allocation failure, record it as a residual boundary rather than claiming universal cleanup.

Qualify cleanup claims for host-filesystem errors rather than promising impossible atomic rollback across every filesystem failure.

## Interrupted remediation is not a release

An independent APPROVE on commit A remains useful finding evidence, but it is not an exact-tip verdict for remediated commit B. If work stops after findings are patched but before deterministic verification, commit, fresh review, integration, and cleanup, report the state precisely as **implemented candidate, unreleased**. Do not fast-forward the canonical lab, update the release closeout, or imply Gate completion from the pre-remediation verdict.

## Release evidence shape

For a reviewed planning-only release, retain:

- exact local commit/tree;
- documentation-only changed-file proof;
- live/source/key-boundary readbacks;
- disclosed known-red baseline with root cause;
- different-family exact-tip verdict;
- rollback bundle identity;
- explicit no-implementation/no-state-artifact proof;
- remote/CI truth (for example, remote-free local source means CI is not applicable, not "pending").
