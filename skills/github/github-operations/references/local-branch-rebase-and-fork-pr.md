# Local branch rebase + fork PR cleanup pattern

Use when a production checkout has pre-existing local commits or dirty changes and the owner says to finish/clean it up without micromanaging.

## Pattern

1. Discover first:
   - `git status --short --branch`
   - `git remote -v`
   - `gh auth status || true`
   - `gh repo view --json nameWithOwner,defaultBranchRef,visibility || true`
2. If the working tree is dirty, commit coherent groups on a local branch before any rebase/pull.
3. Before rebasing a local branch that contains valuable work, create a backup branch:
   - `git branch backup/<branch>-pre-rebase-YYYYMMDD`
4. Rebase onto the upstream default branch only after the backup exists.
5. During conflicts, preserve both valid behaviors when possible. In a command-priority conflict, merge the priority lists rather than picking one side blindly.
6. If a lockfile conflicts, prefer a valid generated lockfile over hand-editing large conflict regions:
   - resolve the package manifests intentionally
   - regenerate with the package manager using lockfile-only mode when available
   - validate the resulting JSON
7. Continue the rebase with `GIT_EDITOR=:` in non-interactive shells if Git prompts for a commit message.
8. Run targeted tests and `git diff --check` after the rebase.
9. Before any push to a fork or PR to a public upstream, run the public-safety scan (operator-safety-kit `tools/privacy_gate.py`) and get the owner's explicit approval for that exact push; a public push cannot be undone. If direct upstream push is denied, create/use the authenticated user's fork, push the branch there, and open a draft PR against upstream:
   - `gh repo fork --clone=false --remote=true`
   - push to the fork remote
   - `gh pr create --repo OWNER/REPO --head USER:branch --base main --draft ...`
10. If `gh repo fork` rewrites `origin` to the fork, restore the canonical remote layout afterward:
   - `origin` = upstream canonical repo
   - `fork` = user's fork

## Verification contract

- working tree clean
- branch rebased on current upstream default branch
- backup branch exists
- branch pushed to fork or upstream
- PR URL captured
- relevant tests passed with real output
- `git diff --check` clean

## Pitfalls

- Do not `git pull` a divergent main with dirty files; preserve work first.
- Do not force-push or push to upstream when permission/policy is unclear.
- Do not leave remotes swapped after `gh repo fork`; future update workflows may assume `origin` is upstream.
- Do not treat pre-existing pytest warnings as blockers, but report them explicitly if tests pass.
