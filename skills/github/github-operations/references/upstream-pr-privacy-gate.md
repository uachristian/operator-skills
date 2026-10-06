# Upstream PR privacy gate (Hermes / any public repo)

Treat every public push as irreversible: the upstream `refs/pull/N/head` can't be deleted by the contributor once a PR is opened.

Rules:
- Before ANY push to a public remote or PR creation, run a privacy gate such as `tools/privacy_gate.py` from the sibling public repo [operator-safety-kit](https://github.com/uachristian/operator-safety-kit) (`python3 privacy_gate.py --denylist <private-denylist> <commits or A..B>`) and require exit 0. It scans commit messages, author/committer identity (must be a noreply address) and ADDED diff lines for home paths, owner/business names from a private denylist kept outside the repo, emails, private IPs, chat/user IDs, phone numbers, token shapes, host aliases, and exact local .env secret values. Reports categories + file:line only, never values.
- An empty scan must fail (the gate exits 2); a range that resolves to zero commits must never count as a pass.
- Self-test the gate against planted fixtures before trusting it after edits.
- Plain lowercase identifiers from non-secret env keys (model/provider names) are excluded to avoid false positives; values under KEY/TOKEN/SECRET/PASS/AUTH/etc. keys are always checked.
- Local carry notes (CARRY_*.md) are private and never go upstream; rebuild PR branches from origin/main with only the code/test hunks.
- Follow CONTRIBUTING.md: Conventional Commits, fix/<desc> branches, one logical change per PR, tests for bug fixes, duplicate search first, PR template filled.
- Show the owner the exact diff + gate output per PR; push/submit only on their explicit go for that PR.
