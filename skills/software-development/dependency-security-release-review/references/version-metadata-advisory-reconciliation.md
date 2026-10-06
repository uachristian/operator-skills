# Reconciling version-based advisories with patched source

Use this when a package scanner flags the installed version even though the deployment carries security commits beyond that release tag.

## Principle

A scanner finding is not automatically a live vulnerable path, but a local commit message is not proof either. Reconcile the advisory to exact source evidence before classifying it as a version-metadata false positive.

## Evidence sequence

1. Capture the advisory ID, affected range, vulnerable file/function/path, referenced fix PR/commit, and whether the advisory declares a patched package version.
2. Freeze the installed source commit/tree and prove that the running environment imports that tree rather than a different wheel/site-packages copy.
3. If the advisory references an exact fix commit, require one of:
   - `git merge-base --is-ancestor <fix> <installed-tip>` succeeds; or
   - a local cherry-pick/remediation has the same stable patch ID as the upstream fix.
4. For patch-ID equivalence, calculate both with `git show <commit> --pretty=format: | git patch-id --stable`; equality proves the same textual patch even when commit ancestry differs.
5. Verify the relevant installed file/blob matches the frozen source and run focused regression tests for the vulnerable path. An ancestor or patch-ID match alone does not prove deployment parity.
6. Keep the scanner finding visible in the report. Classify it as **patched code / stale version metadata** only when source, deployment, and focused behavior evidence agree.
7. If no patched package version exists, record that the scanner will continue flagging the release version until upstream metadata/versioning changes. Do not suppress the scanner globally.

## Failure modes

- Same commit message but different patch.
- Fix exists in another branch but is not an ancestor of the deployed tip.
- Source checkout is fixed while the venv imports an older installed wheel.
- Cherry-pick changed tests/docs but omitted the vulnerable runtime hunk.
- Scanner finding is dismissed because exploitability appears unlikely without verifying the named function/path.

## Worked pattern

A pinned package is flagged for advisories whose database metadata covers `<=<installed-version>` and names no patched version. Check each referenced remediation commit: if it is an ancestor of the installed stack, or a local cherry-pick whose stable patch ID (`git patch-id --stable`) matches the upstream fix, the runtime path is patched. Keep the scanner findings visible in the report, but classify them as patched-code/version-metadata findings rather than unremediated runtime paths, and confirm the running source is the frozen tree you inspected.
