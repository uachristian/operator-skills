# Fail-Closed Foundation Verification

Use this reference when creating an isolated specialist profile or product-incubation foundation whose initial promise is stronger than “the files exist”: no real data, no external accounts, no deployment, no credential leakage, and no cross-profile bleed.

## 1. Turn policy into executable invariants

Keep one machine-readable manifest with exact values for every blocked boundary, for example:

- `real_data_allowed: false`
- `product_data_mode: synthetic-only`
- `external_accounts: []`
- `remote_repository: null`
- `deployment: none`
- every named gate equal to its complete blocked baseline

Do not validate only that fields begin with `blocked`; compare the full gate map so omitted or newly added gates fail closed.

Critical governance documents also need semantic checks, not presence-only checks. Validate the exact status marker and a few durable security sentences for partner authorization, tenant-context derivation, row-level security, and separation of Hermes state from product state.

## 2. Prove rejection paths with mutations

A happy-path `make verify` is not enough. Copy the repository to a temporary directory, mutate one invariant, run the real validator, and assert nonzero exit plus the expected diagnostic. Minimum mutations:

- add an external account;
- enable or remove a blocked manifest gate;
- place a secret-shaped value in a TypeScript or extensionless file;
- place the same synthetic token below an ignored/build directory and after a NUL byte;
- add an unclassified fixture;
- put a fixture outside the synthetic namespace;
- add a real-looking record at an alternate repository root and use camelCase identifier aliases;
- add an ignored local export/real-data path or repository-local `.env`;
- add an unapproved discovery record or repository symlink;
- change the authorization document from BLOCKED;
- remove the tenant-boundary sentence;
- preserve all required policy sentences but append contradictory approval or tenant-bypass language.

Construct fake token strings from fragments inside tests so the test source does not trigger its own scanner.

## 3. Scan credentials in two layers

**Repository pattern scan:** with Git metadata, enumerate tracked plus nonignored untracked candidates using `git ls-files --cached --others --exclude-standard -z`; this still includes tracked files below ignored/build directory names. In a metadata-free `git archive`, fall back to every archive file. Inspect candidates regardless of suffix and do not suppress scanning because the content contains NUL or is classified as binary—scan a one-byte-preserving representation or fail closed. Reject oversized files rather than silently skipping them. Cover common provider, GitHub, AWS, Google, Stripe, Slack, Telegram, bearer-token, private-key, and sensitive-assignment forms.

**Ignored local workspace scan:** separately inspect ignored paths that are outside the commit surface but forbidden during the blocked phase. Reject repository-local `.env`, key/certificate/database files, import/export/upload/screenshot roots, and real-data fixtures. Do not treat `.gitignore` as an authorization control. If a dependency/cache tree is excluded from this local scan, tracked files below that name must still be covered by the Git candidate set.

For a deliberately frozen discovery-only repository, use an exact artifact allowlist plus a narrow wildcard for strictly validated synthetic fixtures. Reject unknown paths and symlinks. Broaden the allowlist only in the reviewed change that starts implementation.

**Exact-value containment scan:** load approved credential values without printing them, recursively collect token/secret/password fields, deduplicate values, and search the isolated profile for exact copies. Exclude only the approved credential files and encrypted/controlled backups. This catches leakage into logs, sessions, generated state, source, or vault files that regex patterns may miss.

Never print secret values in evidence; record only counts, scanned-file totals, authorized locations, and leak paths.

## 4. Gate synthetic data structurally

While authorization is blocked:

- allow fixtures only below a synthetic fixture root;
- require JSON object roots with `synthetic: true`, `source: generated`, schema version, and ISO generation date;
- require reserved example domains, visibly fictional names, reserved fictional phone ranges, and a synthetic identifier namespace;
- normalize identifier field names across snake_case, camelCase, separators, and capitalization before applying the namespace rule;
- reject import/export/upload/screenshot/real-data roots, including ignored local copies;
- allowlist discovery templates and reject new discovery records until the authorization gate changes through review;
- combine required policy snippets with reviewed SHA-256 locks so contradictory text cannot be appended while the original sentences remain present.

A self-declared `synthetic: true` flag alone is not evidence that the payload is synthetic.

## 5. Verify the effective container boundary

Use both container metadata and process evidence:

- inspect mounts, network mode, privileged mode, security options, capabilities, Docker-socket exposure, and restart policy;
- inspect the live process tree and identify the UID of the actual agent/gateway workload;
- distinguish a root init/supervisor from the application workload in evidence. Do not claim the entire container is non-root when only the workload is dropped to an unprivileged UID.

Run the same verification inside the container, not only on the host bind mount.

## 6. Exact-tip review and rollback

1. Commit the candidate foundation and verify a clean worktree.
2. Give the reviewer the exact commit, one security question, bounded commands, and read-only/no-network limits.
3. If the reviewer returns HOLD, convert every accepted HIGH finding into a regression test before implementation.
4. Commit one remediation pass and dispatch a fresh exact-tip review; the old approval/HOLD applies only to the old commit.
5. Create a credential-free backup, checksum it, extract it to a temporary directory, run the verifier there, and confirm the restored Git tip.
6. Record known limitations separately from release gates; never convert temporary environment failures into permanent skill claims.

## Capability-smoke safety

A smoke test must exercise the target profile, but the agent must not repair a failed smoke by running ad hoc global installs or package-runner bootstrap commands into persistent state. Installation is a separate reviewed dependency/image change with its own rollback and re-smoke.
