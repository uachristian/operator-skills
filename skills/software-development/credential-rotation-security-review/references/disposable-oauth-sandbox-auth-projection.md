# Refresh-safe OAuth projection into disposable sandboxes

Use this pattern when a bounded child process needs model/API authentication but must not inherit the parent profile's full credential authority.

## Failure mode

Copying a provider's complete OAuth state into a throwaway `HOME` or `HERMES_HOME` can be unsafe even when the directory is private and deleted afterward. If the provider uses rotating or single-use refresh tokens, the child may:

1. refresh the access token inside the disposable home;
2. invalidate the refresh token held by the canonical profile;
3. receive a replacement refresh token;
4. lose that replacement when teardown deletes the sandbox.

The wrapper can then report a successful child call while silently breaking the durable profile credential. File mode, directory containment, and cleanup do not solve this authority-lifecycle bug.

## Preferred authority order

1. Prefer a distinct provider credential or distinct OAuth login for the isolated worker when the provider supports it.
2. Otherwise, if the owner has explicitly approved a profile-local provider credential and the child can tolerate fail-closed expiry, project only the current access token into the disposable child.
3. Never copy a refresh token into a home whose auth-state updates will be discarded.
4. Do not silently fall back to a default/global profile, ambient SDK home, provider environment variable, or unrelated credential pool.

A copied profile-level OAuth block may still duplicate one refresh lineage across profiles. Treat that as an explicit residual risk; separate logins are safer when both profiles can refresh concurrently.

## Access-token-only projection contract

The trusted parent should:

- read exactly one approved profile-local auth file;
- select one exact provider identity;
- require a nonempty string access token from the canonical provider state;
- create an auth document whose provider set is exactly that provider;
- force the child credential-pool entry for that provider to an empty list;
- include only allowlisted nonsecret metadata plus `tokens.access_token`;
- exclude `refresh_token`, pool rows, unrelated providers, `.env`, SDK credential homes, and fallback-provider configuration;
- set isolated `HOME`, `HERMES_HOME`, `TMPDIR`, and workspace paths;
- pass an allowlisted environment rather than inheriting ambient credential variables;
- bind the exact provider/model in both configuration and argv;
- fail before child launch when the access token is missing, empty, malformed, expired, or from the wrong provider;
- remove the disposable home only after the child and all descendants are extinct and any watchdog receipt is resolved.

If the access token is a JWT, its expiry claim may be decoded for a bounded preflight without logging or persisting the token. Do not treat JWT shape alone as signature or authorization proof.

## Operational profile-auth copy

When the owner explicitly authorizes copying one provider from a source profile to a target profile:

1. back up the target auth file and checksum the backup;
2. construct the target document from the target's current JSON, not by copying the source file wholesale;
3. replace only the approved paths, typically `providers.<provider>` and `credential_pool.<provider>`;
4. prove all other top-level/provider/pool semantics are unchanged;
5. write atomically under the target owner with mode `0600` (or the platform's equivalent restrictive ACL);
6. read back and verify exact-path scope, ownership, mode, valid JSON, and provider usability without printing credential values;
7. preserve executable rollback until the target credential and consuming workflow pass their smoke tests.

Approval to copy one provider is not approval to copy unrelated credentials, `.env`, behavioral configuration, gateway tokens, or external-action authority.

## Adversarial test matrix

Pair every rejection with a healthy positive control.

- Full source provider contains access + refresh tokens, pool rows, and unrelated providers: child output contains only the exact provider access token and an empty pool.
- Refresh-token-only source: reject before child launch.
- Pool-only access token: reject unless pool selection is an explicit reviewed contract; do not accidentally restore refresh authority through a pool fallback.
- Missing, empty, non-string, malformed, expired, or wrong-provider access token: reject before launch.
- Ambient provider environment variables and host SDK homes: prove they are absent/unreachable from the child.
- Actual runtime tool resolution: verify the child receives only the intended tool surface; argv text such as `--toolsets web` is not sufficient proof.
- Provider/model fallback: remove or invalidate the exact provider and prove there is no fallback call.
- Successful child call: verify no refresh token or unrelated credential appears in the post-call sandbox auth file.
- Teardown: verify no sandbox, child, descendant, secret-bearing log, or unresolved receipt remains.
- Output gate: report only booleans, counts, modes, expiry margin, and hashes; never token bytes or provider responses.

A live provider probe requires explicit owner authority. When authorized, use a disposable profile, a deterministic prompt/response, no external-action tools, bounded timeout, and sanitized output.

## Actual resolver and cache-isolation probe

Treat the initial projected `auth.json` and the post-resolution auth store as separate evidence lanes. A real provider resolver may seed a credential-pool row from singleton state, interpret an empty pool as global-fallback permission, rediscover an SDK home, persist normalized state, or apply weaker expiry checks in a pool fallback.

Run the real installed resolver with synthetic sentinels and blocked network:

1. Put access, refresh, pool, and unrelated-provider sentinels in the synthetic source profile; never read real credentials.
2. Project auth and freeze its exact key set and forbidden-sentinel absence.
3. Start a fresh process with the production child directory layout and exact environment allowlist. Use fresh processes—not repeated cases in one interpreter—for valid, expired, malformed, and fallback cases because Hermes/config/provider/pool modules may memoize home, config, or auth state.
4. Invoke the exact provider/model resolver and record effective provider, credential source, selected synthetic key, fallback chain, refresh-call count, and auth bytes before/after.
5. Resolve actual child tool schemas, not only the requested toolset name, and require terminal, file, memory, mutation, and provider-action tools to be absent.
6. Remove the sandbox and prove any access-only normalization was transient and no refresh authority persisted elsewhere.

Evaluate `HOME` and `HERMES_HOME` together. Default-root and provider-home discovery can depend on their physical relationship. Do not create a symlink or host-home directory in the synthetic child unless production creates the same object: that can manufacture a false global-fallback finding. Put host/default sentinels outside the fresh child home and prove they remain unread.

Severity guidance:

- **HIGH / HOLD:** global/default refresh authority is imported, an unrelated credential is selected, shared OAuth state is rotated, refresh authority persists outside the sandbox, or provider/model fallback occurs.
- **Usually Medium:** whitespace-only access reaches child startup and causes avoidable quarantine; an expired access token can only reach a failing provider request with no refresh/fallback authority; or the resolver transiently self-seeds an access-only row that is deleted with the sandbox.

## Account-bound refresh in shared credential pools

When one provider pool holds multiple OAuth accounts, bind each row to a canonical account identity before permitting refresh or persistence:

1. Derive the expected identity from the row's current token/account claims and reject internally conflicting current claims before any network call.
2. Perform the refresh under the pool's existing single-use-token ownership/lock protocol.
3. Derive the returned identity before mutating memory, singleton auth state, pool JSON, cooldowns, or selection state.
4. If the returned identity is missing or differs from the expected identity, make **zero credential writes** for that result, retain the last known-good row, quarantine only that row for re-authentication, and never clear another row or shared singleton as a side effect.
5. On success, persist token and identity as one atomic row update. Under cross-process races, reload durable state and let demonstrably newer token state win; do not overwrite a newer disk refresh lineage merely because the caller started with stale memory.
6. Keep quota/status observation read-only: look up the intended row directly from a snapshot and probe it without calling selection methods that rotate, consume cooldown state, or persist preference changes.

Do not add a refresh-specific identity-mismatch reason to a generic terminal-error set unless every caller has the same semantics. Manual status marking, provider 401 handling, and refresh-result quarantine can share strings while requiring different state transitions; keep the transition local or add an explicit operation context. Grep the test tree for the helper, reason, and transition symbols before widening shared behavior because hand-written mocks and admin paths often encode the older contract outside the focused refresh tests.

The minimum synthetic matrix is: distinct primary/secondary identities; wrong-account refresh with zero writes; conflicting current claims with zero network calls; transient refresh failure preserving usable state; one-refresh behavior under concurrent workers; stale-memory versus newer-disk merge; manual 401 behavior; and observer probes that leave selection/cooldown bytes unchanged. Use unsigned synthetic claims only for parsing/identity tests, never as authorization evidence.

## Review conclusion

Approve only when the credential authority available to the child is strictly smaller than the durable profile authority, token expiry fails closed, no refresh rotation can be lost at teardown, account identity cannot cross pool rows, observers cannot mutate selection state, and the consuming workflow's external mutation/retry boundaries remain unchanged.
