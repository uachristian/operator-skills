---
name: dependency-security-release-review
description: "Use when reviewing a dependency or lockfile security remediation (npm, Python) for real fixes, overrides, and runtime compatibility."
version: 1.0.5
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [dependencies, security, lockfiles, release-review, npm, uv]
    related_skills: [development-quality-loop]
---

# Dependency Security Release Review

## Purpose

Review a frozen dependency/security remediation as an immutable release candidate, not as a request to repair it. Distinguish version correctness, artifact identity, compatibility, and test adequacy. Return an explicit `APPROVE` or `HOLD` verdict grounded in exact commit evidence.

See `references/npm-lock-integrity-and-compat-patch-boundaries.md` for structural probes and the multi-root compatibility-patch failure pattern.

See `references/version-metadata-advisory-reconciliation.md` when a scanner flags a release version but the deployed source may already carry the referenced fix; require exact ancestor or stable patch-ID evidence plus deployment parity and focused behavior checks before calling it a metadata false positive.

## Trigger Conditions

Use this skill when a candidate changes any combination of:

- package manifests or lockfiles,
- dependency security floors or overrides,
- npm lifecycle compatibility patches,
- Python `requires-python`, constraints, overrides, or `uv.lock`,
- React/TypeScript/router/bundler versions,
- release tests that assert dependency health.

## Rules

- Stay strictly read-only unless remediation is separately authorized. Enforce that structurally: review an immutable archive for content-only work or a disposable detached worktree for Git-dependent checks; do not give a reviewer the mutable release-candidate worktree as its scratch checkout. A read-only prompt alone is not an isolation boundary.
- Freeze target commit, parent, tree, status, and expected tracked test paths before analysis. After any delegated review, verify the real candidate's HEAD/tree/status and tracked-file presence; restore unexpected drift only from the verified commit and invalidate any evidence collected after the drift began.
- Attribute runnable evidence only to the immutable target; recheck `HEAD` and critical blob IDs afterward.
- Parse manifests and locks structurally. Do not trust textual version mentions alone.
- Report reproduced critical/high release blockers first, then medium/low observations.
- Do not turn local interpreter/package absence into a product defect; use available read-only structural gates and disclose the evidence boundary.

## Review Workflow

### 1. Freeze scope

Record:

1. target SHA and tree,
2. exact parent/baseline SHA and tree,
3. parent-to-target changed-file set,
4. clean/dirty status,
5. critical file object IDs.

Run `git diff --check <parent> <target>`. Reject tests from a moving checkout unless source/test blobs are proven identical.

### 2. Map package roots

Enumerate every independent package root and lockfile, including workspaces, documentation sites, sidecars, examples, and nested applications. For each root, identify:

- supported install command,
- lifecycle scripts,
- manifest/lock root metadata,
- engine constraints,
- build/typecheck/audit commands,
- whether it is installed independently or through the root workspace.

Never assume a root `postinstall` protects a separately installed subproject.

### 3. Verify manifest/lock consistency

For npm roots, compare `dependencies`, `devDependencies`, `optionalDependencies`, and `engines` between each `package.json` and its corresponding lock root/workspace entry.

For each changed package:

- verify exact resolved version,
- verify every consumer range/override,
- distinguish direct, dev, optional, peer, transitive, workspace-link, and bundled use,
- require every non-link, non-`inBundle` registry artifact to retain HTTPS `resolved` and `integrity`,
- treat `inBundle` bytes as covered by the parent tarball identity rather than an independently hashed registry fetch,
- compare whole-lock integrity coverage against the parent.

A green version-floor test is insufficient if lock hashes disappeared. A raw count that includes `inBundle` entries is also insufficient because it can manufacture false blockers.

### 4. Verify Python constraints and lock identity

Parse `pyproject.toml` and `uv.lock`; verify:

- `requires-python` agreement,
- direct/extra pin agreement,
- every constraint/override appears in lock manifest metadata,
- locked versions meet floors,
- sdist/wheel hashes remain present,
- `uv lock --check --offline` passes when available.

Inspect reverse consumers of forced overrides. An override can resolve an advisory while violating an upstream compatibility cap.

### 5. Review compatibility patches adversarially

For any patched dependency export/API:

1. freeze expected package version and source shape,
2. require fail-closed source anchors,
3. ensure atomic/idempotent patching,
4. map patch execution to every install root,
5. exercise the exact risky branch through a legacy consumer,
6. pair rejection/fail-closed cases with healthy controls.

Syntax checks and source-token tests do not prove the patched runtime contract.

### 6. Review framework/toolchain migrations

For React/router/TypeScript/Vite/Rolldown changes:

- enumerate all old and new imports,
- prove no legacy package references remain in bounded source,
- verify peer/engine floors against exact pins,
- inspect bundler config and chunk regexes for stale names,
- distinguish static client use from server-component exposure,
- do not infer exploitability from a package version without the vulnerable runtime package/path.

### 7. Run bounded read-only gates

Prefer tests that do not install, generate, clean, or rewrite artifacts:

- focused dependency-floor tests with cache/bytecode disabled,
- strict JSON/TOML parsing,
- lock checks,
- script syntax checks,
- exact static import scans,
- structural adversarial probes.

Do not run package installers or builds that mutate the frozen checkout unless the review contract explicitly permits a disposable exact worktree.

### 8. Re-freeze and report

Before verdict:

- recheck `HEAD`, status, and critical blob IDs,
- rerun `git diff --check`,
- state repository files created/modified (`None` for a clean read-only review),
- separate product findings from unavailable environment-dependent evidence.

## Severity Guidance

- **Critical:** directly exploitable release path with catastrophic impact.
- **High / HOLD:** widespread loss of lock artifact integrity; unresolved known high advisory on a shipped path; canonical install/build/start command broken; compatibility patch absent from a required install root.
- **Medium:** reachable but non-default compatibility failure; incomplete regression gate likely to permit recurrence.
- **Low:** stale claims, duplicate config tokens, or inconsistent pins without a demonstrated vulnerable/release path.

## Common Pitfalls

- Checking versions but not `integrity` fields.
- Sampling a few newly hashed entries instead of measuring the whole lock.
- Treating separate lockfiles as one security boundary.
- Assuming `npm ci` restores reviewed-byte identity when the lock omits hashes.
- Treating successful `npm ci --ignore-scripts` plus a zero audit as installed-graph consistency. Run `npm ls --all --json` too, including dependencies of installed optional parents. A nested Lightning CSS version can lack matching platform bindings and resolve a wrong hoisted native version; a WASM binding can exist while its required runtime subtree is absent. Preserve existing lock entries, resolve missing subtrees through npm, verify every supported native binding against its parent's exact optionalDependency version, and pair structural rejection tests with actual native transformation/WASM loading in an isolated environment. Lock-only refresh may leave these holes intact. Do not patch binary filenames or suppress npm-ls errors to declare readiness.
- Trusting manifest overrides without verifying actual locked paths. npm can leave stale transitive lock entries after `npm install --package-lock-only`, even when new overrides are present; explicitly update only the affected names with `npm update <names> --package-lock-only --ignore-scripts --include=dev`, then inspect every nested resolution and rerun the audit. Preserve package-age protection: prefer the earliest compatible patched release, and use narrowly documented exceptions for exact security pins rather than globally disabling the age rule. A newer patch can pull additional fresh data/tooling packages and unnecessarily expand the exception set.
- Treating a postinstall patch as repository-global.
- Calling an RSC advisory reachable in a static site without finding an RSC package/path.
- Treating a version-range scanner hit as a proven vulnerable runtime path when the deployed source may carry later fixes—or dismissing it from a commit message alone. Reconcile the advisory's named path and referenced fix through ancestry or stable patch-ID equivalence, then prove installed-source parity and focused behavior.
- Treating a metadata-free archive as sufficient for Git-dependent source/release invariants. First prove archive bytes and executable modes match the exact commit, then run history-aware gates in a disposable detached worktree at that commit. Do not initialize a synthetic one-commit repository around the archive when validators may require parent objects, tracked-file history, or exact commit identity.
- Comparing `git ls-tree` and extracted-file manifests after applying a plain whole-line sort. `git ls-tree` lines begin with mode/type/blob, so whole-line sorting does not align entries by path and creates a false mismatch. Prefer extracting `git archive <tip>` and using recursive byte comparison plus a separate executable-path/mode comparison, or sort both manifests explicitly by the tab-delimited path field.
- Hiding an unavailable test behind a generic “verification passed” claim.
- Treating hashes over caller-supplied SBOM/SARIF files as scanner provenance. A public writer/verifier can still bless synthetic zero-finding reports even when schemas and hashes are strict. For a release-authorizing local image gate, accept no pre-existing reports: require a clean exact source, fixed signed scanner executables, one inspected immutable image ID, fresh owner-private outputs created by that process, explicit SBOM root digest binding, scanner-derived severity counts, and atomic publication. Keep later artifact revalidation structurally unable to elevate HOLD to PASS. Verifying a signed Docker CLI plugin is not sufficient if the gate later invokes it through `docker <plugin>`: `DOCKER_CONFIG` and CLI-plugin search precedence can substitute an unsigned executable while the receipt attests the verified one. Invoke the verified plugin binary directly by absolute path, sanitize caller-supplied Docker routing/plugin environment, and regression-test with an adversarial fake plugin. Removing `DOCKER_*` variables is still insufficient when caller-controlled `HOME` selects `$HOME/.docker/config.json` and `currentContext`; bind Docker and the scanner to a canonical, owner-owned Unix socket, validate/record the expected local daemon identity and socket inode before and after scanning, and prove hostile `HOME` cannot redirect either operation.
- Treating an import probe as proof of the disposable Python lock install while it inherits caller `PYTHONPATH` or user-site packages. The installer can correctly place the locked wheel while `python -c 'import package'` loads a different ambient version. For exact import evidence, remove `PYTHONPATH`, set `PYTHONNOUSERSITE=1`, invoke the disposable venv interpreter with `-I`, print each package version and `__file__`, require every path to sit under that venv, and run `uv pip check --python <venv>/bin/python`. Classify the contaminated first probe as harness evidence, not a product defect.

## Acceptance Checklist

- [ ] Exact target/parent/tree/status and expected tracked test paths frozen.
- [ ] Reviewer ran from an immutable archive or disposable detached worktree rather than the mutable release candidate; candidate HEAD/tree/status/test-path presence were rechecked afterward.
- [ ] Changed package roots and lockfiles enumerated.
- [ ] Manifest/lock metadata agrees structurally.
- [ ] Every non-link, non-`inBundle` registry artifact retains version, HTTPS resolved URL, and integrity; bundled entries are covered by a byte-bound parent tarball.
- [ ] Whole-lock integrity coverage did not regress from parent.
- [ ] Python constraints, overrides, versions, and hashes agree.
- [ ] Compatibility patches cover every supported install root and risky branch.
- [ ] Framework/toolchain peer and engine floors are coherent.
- [ ] Version-based advisory findings were reconciled to the named vulnerable path and exact fix; any local cherry-pick claim has ancestor or stable patch-ID evidence plus installed-source parity and focused behavior proof.
- [ ] Any release-authorizing SBOM/SARIF verdict is bound to a fresh trusted scanner execution and immutable image identity; caller-supplied report hashing alone cannot grant PASS.
- [ ] Focused tests and static probes ran from exact source.
- [ ] Final blob/status recheck passed.
- [ ] Verdict and residual evidence boundaries are explicit.
