# Bounded Source-Only Security Controller Builds

Use this follow-through after a proposal-only planner graduates to a separately authorized, source-only controller implementation with strict roles, fixed roots, signed artifacts, and no live/key operations during development.

## Freeze the executable contract first

Before writing tests, convert the latest owner instruction into one matrix covering:

- exact base/worktree identity;
- files added, changed, removed, and explicitly deferred;
- role/entrypoint count and exact argument surfaces;
- schema keys, trust identities, fixed roots, action IDs, and content-addressed IDs;
- exact state/event vocabulary and legal transitions;
- final gates and forbidden operations.

The latest explicit owner contract overrides older planning prose where they conflict. Reconcile terminal names, event order, and release construction before creating tests; do not let different modules implement different generations of the design.

Freeze implementation-level choices even when the reviewed plan describes only semantics. A producer and consumer can both look reasonable while disagreeing on details such as:

- whether `source_mode` is a Git index mode (`100644`/`100755`) or a POSIX mode;
- nested policy key names;
- exact cross-repository environment variables;
- confirmation flag names;
- whether a named integration test is an allowed addition;
- whether a repository-local verifier or a parent-owned deterministic command is authoritative;
- the exact installable and review-only release-inventory sets.

Record these choices in one compatibility matrix before parallel implementation. Run the actual producer against the actual consumer with both exact roots set and zero skips. Hand-built lookalike JSON is not compatibility evidence.

## Exact release inventory and byte identity

A required subset is not a release contract. Define three exact sets:

1. installable source paths, each with the one allowed installed mode;
2. review-only paths, each with `install: false` and `installed_mode: null`;
3. prohibited paths, including the wrapper itself, live artifacts, production manifests, private keys, mutable state, and removed modules.

Require inventory membership to equal the first two sets exactly, not merely contain mandatory rows. Bind each row to the source commit's Git mode and content hash, require exact entrypoint path/hash/mode mappings, and reject install-selection drift. In an A/B construction, every inventory path at wrapper B must remain byte-identical to source A.

Read canonical manifests and signed artifacts once through the hardened no-follow reader, then parse and hash those exact bytes. Reopening the same path for validation introduces a TOCTOU gap and can make the capability bind bytes different from those originally inspected.

For local Git observation, use one adapter with an absolute executable, exact read-only argv shapes, replacement environment, fixed CWD, bounded output/time, closed descriptors, and poisoned-`PATH`/`HOME`/`GIT_*` regression tests. Do not reuse a historical helper that invokes `git` through inherited `PATH` merely because its commands are read-only.

## Single-writer worktree discipline

Give each implementation worker its own isolated worktree. The parent must not edit that worktree until the delegation has formally emitted its final result; a worker's internal todo list saying “complete” is not a completion signal. If a patch reports that the file changed since the last read, reject the stale patch, wait for formal completion, and re-read the exact bytes before editing. For concurrent review, snapshot the candidate or use a separate read-only worktree rather than letting reviewer and implementer race on one tree.

## Budget for complete vertical slices

A source-only release is not permission to leave unconditional-rejection placeholders behind. Prefer one complete and verified role path over many half-wired modules.

Recommended order:

1. strict planner/policy validator and checkout-vs-installed capability gate;
2. one actual-producer → actual-consumer RED/GREEN test;
3. one complete disposable signed-artifact/preflight path;
4. transaction journal, consumption, write/readback, runtime proof, and rollback in a disposable root;
5. all role entrypoints and isolation tests;
6. repository verifier/allowlist, docs, and CI;
7. focused tests, full suite, lint, compile, diff, protected-object checks;
8. remediation reserve.

Run the focused test for each slice before expanding scope. Update an exact-file repository verifier as soon as new paths are added rather than postponing a known structural failure until the end.

## RED-first without stale-suite debt

Write the first RED batch against the frozen public contract, then capture the failure once and drive that same batch green.

High-value first RED cases:

- exact canonical bytes emitted by the real proposal producer are accepted by the real consumer;
- all authority Booleans remain literal `false`;
- schema, trust, policy, action, ID, and no-op mutations reject;
- a source checkout, copied tree, altered module path, or monkeypatched constant cannot establish installed authority;
- the installed gate runs before any key, Git/OpenSSL/sandbox subprocess, state, or live open;
- exact role count, strict parsers, freshness algebra, and state-machine prefixes.

When replacing an older architecture, update or replace its maintained tests immediately after the new contract turns green. Do not accumulate old API tests and defer all compatibility cleanup to the final full-suite run.

Avoid text-only assertions such as requiring `allow_abbrev=False` to appear in every wrapper when parser factories live elsewhere. Prefer parsing allowed and forbidden argv through the real parser, AST import checks, and mocked call-order assertions.

## Separate operational and disposable capabilities

Use two distinct authority types:

- **Installed operational capability:** obtainable only after literal fixed-path validation, ordinary non-symlink ancestors, exact owner/modes, complete installed inventory, and signed installed-release verification. Environment changes and monkeypatching must not mint it.
- **Disposable test capability:** limited to one owner-only directory beneath the physically resolved system temporary root. Every fixture key, state directory, candidate, target, backup, journal, and receipt must remain beneath that root.

Operational roles establish installed capability before opening retained keys, subprocesses, state, or live targets. The installer is a separately specified bootstrap exception and must verify exact clean source/wrapper identities before bootstrap artifacts or keys.

Do not expose a generic capability constructor or accept arbitrary production-like roots. A test capability can exercise real write/fsync/rename/rollback mechanics only inside its disposable root.

## Entry scripts must route to real behavior

Thin wrappers are good; stubs are not. A script that parses arguments, verifies installation, and then always rejects proves checkout containment but does not satisfy an installation-grade role contract.

For each role, verify:

- exact non-abbreviable arguments;
- installed/bootstrap gate order;
- only that role’s key, subprocess, read, or write capabilities are reachable;
- signed artifacts bind the full plan/source/preflight/release/policy/action/freshness tuple;
- outputs are content-addressed fixed children;
- wrong-role keys, signatures, artifacts, and capabilities reject.

## Source commit A and wrapper B

When the release manifest binds source commit/tree A, keep it out of A. Commit A contains all source, tests, policy, trust anchors, verifier, docs, and CI changes. Wrapper B adds only the canonical release manifest that binds A.

Any change to an inventory file after A is frozen invalidates both A and B. Regenerate both identities and rerun exact-tip gates/review. Do not create the wrapper manifest while implementing A.

## Verification cadence and interruption reporting

After each file/module batch:

1. rerun the original RED batch;
2. run adjacent role-boundary tests;
3. run the repository verifier when file inventory changed;
4. inspect status/diff for generated, protected, or deferred artifacts.

Before release handoff, require focused tests, the complete maintained suite with expected collection count, repository verifier, no-cache lint, in-memory compile when caches are forbidden, `git diff --check`, full diff review, and Git-object checks for protected source/config blobs when live reads are forbidden.

If the session is interrupted before these gates, report **implemented but unverified/incomplete**, list the exact missing gates, and do not describe the candidate as nearly released. A prior focused pass does not remain final evidence after later edits.