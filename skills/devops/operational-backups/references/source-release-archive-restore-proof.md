# Source release archive restore proof

Use this when producing a source-only release or rollback bundle from an exact Git commit.

## Why this gate matters

Archive integrity and checksums prove transport integrity, not recoverability. A disposable restore can expose verifier assumptions that are invisible in the live checkout—for example, inferring a profile root from a fixed parent depth or requiring `.git` metadata that `git archive` intentionally excludes.

## Procedure

1. Prove absolute roots: repository, real profile root, destination, `HOME`, `HERMES_HOME`, and language-path overrides.
2. Freeze the exact commit and tree; require a clean worktree and record whether remotes exist.
3. Generate the archive from the exact commit with `git archive`, not from mutable working-tree files.
4. Test compression integrity and compare archived regular-file count with the exact commit's tracked-file count.
5. Extract into a fresh disposable directory outside both the checkout and profile.
6. Run the shipped verifier from the extracted tree. The verifier must support two explicit modes:
   - **Live profile:** identify the profile only through strong sentinels (for example both `SOUL.md` and `vault/AGENTS.md`) and scan the complete profile boundary.
   - **Standalone source:** when those sentinels are absent, confine scans to the restored repository root.
7. Handle Git metadata deliberately and repository-locally:
   - Detect lexical presence with `os.path.lexists(repo / ".git")`; `Path.exists()` follows symlinks and falsely treats a dangling `.git` symlink as absent.
   - Reject symlinked `.git` paths, including dangling symlinks.
   - If `.git` is absent, do not invoke ancestor-searching Git discovery. Treat the tree as a source snapshot and mark live-Git assertions unavailable rather than failed.
   - If local metadata is present, strip every inherited `GIT_*` key before both identity and remote subprocesses. Otherwise ambient `GIT_DIR`, `GIT_WORK_TREE`, config, object, index, or discovery overrides can redirect validation to unrelated metadata.
   - Run `git rev-parse --show-toplevel` under that sanitized environment and require the resolved top level to equal the intended source root exactly.
   - Reject malformed local metadata and enforce remote policy using the same sanitized environment.
8. Add a nonrecursive portability smoke that copies the source without `.git` or build caches and invokes only the low-level validator. Do not call the master verifier from that smoke or it can recurse. Its deterministic layouts should cover: metadata-free standalone; metadata-free restore under an unrelated Git ancestor with a remote; dangling and valid-target `.git` symlinks; malformed `.git` file/directory; valid local zero-remote and forbidden-remote metadata; and malformed/forbidden local metadata while ambient `GIT_DIR`/`GIT_WORK_TREE` point to an unrelated clean repository.
9. After the restored verifier passes, build the final evidence bundle, write its manifest/exclusions/rollback outline, generate checksums last, and verify them.
10. If any multi-step attempt fails after writing files, inventory partial artifacts, sizes, modes, and hashes before retrying or deleting. Build the corrected bundle at a new path; delete the failed partial only after the replacement is verified.

## Release-discipline consequence

A verifier fix changes the exact release tip even when product blobs are unchanged. Freeze the new tip, prove product-blob parity with the previously approved parent, and run a narrow exact-tip review of the verifier-only delta before issuing the bundle.

## Common pitfalls

- Blindly setting a scan root with `repo.parents[N]`; an extracted archive under `/tmp` can accidentally scan unrelated temporary files, secrets, and media.
- Calling a source archive unrecoverable merely because `.git` is absent.
- Weakening live-checkout remote checks to make archive mode pass.
- Generating checksums before verdict/manifests are final, causing silent evidence drift.
- Treating `gzip -t` or checksum success as a restore proof.
