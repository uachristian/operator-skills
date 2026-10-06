# Git archive to exact checkout reconstruction

Use this when an immutable `git archive` is the review input but mandatory tests require checkout semantics: `.git` metadata, `git check-ignore`, or non-group-writable source modes.

## Why direct extraction can give false failures

A normal Git TAR archive may encode regular files as `0664` and executables as `0775` because archive creation applies a permissive archive umask. Git trees record only file type plus executable intent (`100644`, `100755`, `120000`), not every POSIX permission bit. Directly extracted group-writable files can therefore fail security/parity checks that pass in a normal checkout. A metadata-free archive also makes Git-dependent tests fail with `not a git repository`.

Do not classify either condition as candidate behavior until the archive has first been proven safe and exact, then reconstructed with checkout semantics.

## Read-only reconstruction procedure

1. Verify the archive digest before any extraction.
2. Inspect all members before extraction; reject duplicate and normalized-duplicate names, traversal, escaping links, and unsupported member types.
3. Compare every non-directory member with the immutable commit:
   - path set,
   - blob bytes or symlink target,
   - Git executable intent.
4. Extract only to a disposable root.
5. Normalize each extracted tracked path from `git ls-tree -r -z <commit>`:
   - `100644` to `0644`,
   - `100755` to `0755`,
   - preserve symlink semantics for `120000`.
6. Initialize Git only inside the disposable root, force-stage the complete tracked file set, and run `git write-tree`.
7. Require the reconstructed tree ID to equal `<commit>^{tree}` before using any test result.
8. Run tests from that disposable root with the declared interpreter/tool versions. Git-dependent tests may now use `git check-ignore`, path inventories, and related checkout contracts without reading the mutable source checkout.
9. Re-hash the original archive, verify the source repository stayed clean and at the same target commit, and delete the disposable root.

## Interpretation

- A direct-extraction failure that disappears only after exact-tree reconstruction is a harness/checkout-semantics issue, not a product defect.
- A failure that remains after `git write-tree` equals the target tree is candidate evidence.
- Archive permission metadata is still release-relevant when the TAR itself is the deployment transport or a consumer promises to preserve every POSIX bit. Do not normalize away an explicit mode-bound release contract.
- Never claim exact-candidate tests from a reconstructed root unless the path/blob/symlink/executable comparison and exact tree-ID assertion both passed.

## Common command pattern

```bash
# In the disposable extracted root only:
git init -q
git add -f .
test "$(git write-tree)" = "$(git -C "$SOURCE_REPO" rev-parse "$TARGET_COMMIT^{tree}")"
```

Perform permission normalization from a NUL-delimited `git ls-tree` parser rather than from filename-splitting shell loops, so spaces and unusual tracked names remain safe.