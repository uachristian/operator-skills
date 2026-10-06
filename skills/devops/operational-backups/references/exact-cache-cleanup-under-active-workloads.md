# Exact cache cleanup while workloads are active

Use this when disk pressure blocks an update/build but candidate cache directories may be shared by long-running npm, npx, uv, browser, MCP, smart-home, or build processes.

## Approval and identity gates

An approved path list is a maximum deletion scope, not permission to ignore later drift.

For every target, record before approval:

- absolute path and owning root;
- allocated size and projected reclaim;
- file count plus a deterministic metadata-tree hash (`relative path`, mode, size, mtime);
- reason the data is reproducible;
- retained backups/state excluded from cleanup;
- current open-file/process evidence.

Immediately before deletion, rerun the identity hash and open-handle check. If the tree changed, became a symlink, moved outside the approved root, or gained an active handle, skip that target. Do not regenerate its manifest and silently treat the old approval as approval of the new contents.

## Active-process checks

A quiet parent-directory timestamp is not proof that a nested cache is unused. Check both:

- process command lines for npm/npx/uv and related workers;
- open or memory-mapped files whose full path falls under each exact target.

`~/.npm/_npx` deserves special care: long-running services and MCP/browser helpers may execute binaries directly from hashed `_npx/<id>/node_modules/...` trees. Deleting that tree can unlink a running executable and make the next restart fail or force an unplanned network reinstall. Skip it while any mapped executable or process command references it.

`~/.npm/_cacache` may change while npm/npx wrappers are alive even when no file is open at the instant of inspection. A metadata-hash mismatch is the reliable stop signal.

## Safe partial execution

If several exact paths were approved and only a strict subset still passes every gate:

1. Delete only the unchanged, inactive subset.
2. Record every skipped path and the precise failed gate.
3. Do not expand to replacement paths without a new manifest and approval.
4. Verify each deleted path is absent and recreate only an empty required parent directory when the owning tool expects it.

This preserves the approval ceiling while avoiding disruption.

## APFS and build-headroom verification

APFS free space can settle upward or downward after deletion. Capture:

1. immediate `df` evidence;
2. a settled reading after other I/O quiesces;
3. another reading after the candidate dependency/build workload, because reproducible caches may be repopulated.

Treat the requested free-space threshold as a floor, not the build budget. Maintain extra headroom for worktrees, candidate venvs, Node installs, Electron artifacts, and APFS variance. Do not claim durable margin from one immediate post-delete reading.

## Rollback and reporting

Caches normally restore by rerunning the owning package manager; do not represent them as irreplaceable backups. The operational rollback is to stop the update, preserve current source/runtime backups, and allow the owner process to repopulate only the cache it needs. Report deleted and skipped targets separately, including whether a target was skipped for identity drift or an active process.
