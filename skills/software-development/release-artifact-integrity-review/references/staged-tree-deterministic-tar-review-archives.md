# Staged-tree deterministic tar review archives

Use this when creating or reviewing an immutable source archive that must be approved by exact-byte reviewers after remediation.

## Lessons

1. **Freeze the staged tree, not the mutable checkout.** Run staged whitespace/source-authority/test gates first, then record `git write-tree`. Create the archive from Git object bytes for that staged tree so untracked/unstaged drift cannot enter the review candidate.
2. **A HOLD always supersedes the archive.** If any required reviewer reports a Critical/High finding, preserve the report as input, patch the moving worktree, rerun gates, create a new archive/digest, and dispatch fresh reviewers. Never transfer an `APPROVE` or `HOLD` verdict across digest changes.
3. **Read complete reviewer outputs.** A delegation batch-complete event or truncated summary is not release evidence. Recover full summaries/transcripts, check the exact archive path, full SHA-256, tree, and explicit verdict before using the result.
4. **Compare tar permission modes to permission bits only.** Git tree modes include file-type bits (`100644`, `100755`); tar `mode` should normally be `0644` or `0755`. If the manifest records both, name them `git_mode` and `mode` and compare each to the correct source.
5. **Do not require an in-archive manifest to contain the archive's final digest.** Adding the digest inside the archive changes the digest. Put final `archive_sha256` in an external owner-only manifest; the in-archive manifest should bind file paths, sizes, hashes, modes, blob IDs, and staged tree.
6. **Avoid tool-output byte transport.** For hundreds of files, do not reconstruct archive bytes from line-oriented tool output or per-file tool calls. Use local filesystem/Git subprocess byte reads inside a single script, then independently verify the result.
7. **Verify before dispatch.** Check owner-only archive mode, digest, unique/normalized-safe members, no traversal/links/unsupported types, file count, every file SHA-256/size/mode/blob ID, in-archive manifest parity, and external manifest parity.
8. **Report deployment held while review is pending.** Tests, scans, and archive verification are prerequisites, not approval. Require all configured independent reviewers to return explicit `APPROVE` for the same full digest with no Critical/High findings.

## Compact verification shape

- `git diff --cached --check`
- `git write-tree`
- source-authority / manifest verifier
- focused tests + full suite + syntax/lint/security gates appropriate to the project
- deterministic archive generation from `git ls-tree` + `git cat-file blob`
- archive verifier: digest, mode, member safety, path set, byte hashes, sizes, tar permission modes, Git blob IDs, manifest parity
