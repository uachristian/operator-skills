# Hermes local commit → public/private push gate

Use this when a Hermes/operator repo has local repair commits and the user says to do repo housekeeping, push, or asks whether a private push is correct.

## Core lesson

Do not infer privacy from remote names like `fork`, from the owner's GitHub username, or from the fact that work is operator/internal. Verify the exact target repository visibility before any push.

For `~/.hermes/hermes-agent`, both common remotes may be public:

```bash
git remote -v
gh repo view --json nameWithOwner,visibility,defaultBranchRef,url
# For non-origin remotes, inspect the exact owner/repo from `git remote -v`:
gh repo view OWNER/REPO --json nameWithOwner,visibility,defaultBranchRef,url
```

If visibility is `PUBLIC`, treat every push/PR as public exposure.

## Safe closeout sequence

1. Inspect remotes and visibility before pushing.
2. If the repo is public:
   - local commit is okay when the user has asked for repo housekeeping;
   - do not push or open a PR yet;
   - run a public-safety scan on the diff/commits for secrets, raw IPs/Tailscale `100.x`, customer/business/vendor details, personal names/emails, `.env`/auth/session/log/state paths, and operator-specific constants;
   - get explicit user approval for the first public push/PR after showing the target remote and scan result.
3. If the user wants private pushes, create or select a separate private mirror and verify `visibility: PRIVATE` with `gh repo view` before pushing.
4. Preserve a pre-commit backup for live Hermes repair work:

```bash
mkdir -p "$HOME/.hermes/backups/repo-housekeeping-$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR=$(ls -td "$HOME/.hermes/backups"/repo-housekeeping-* | head -1)
git diff > "$BACKUP_DIR/working-tree.diff"
git status --short --branch > "$BACKUP_DIR/git-status.txt"
```

## Good final wording

- "Committed locally; repo is now ahead of origin. I did not push because the verified remote is public."
- "Private push is only correct after verifying the target repo itself is private, not just because it is a fork or a user-owned remote."
