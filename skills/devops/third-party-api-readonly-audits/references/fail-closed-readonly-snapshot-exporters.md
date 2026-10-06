# Fail-closed read-only snapshot exporters

Use this pattern when a local job reads a public or OAuth-protected third-party source and commits a sanitized static JSON snapshot for a website, report, or downstream consumer.

## Transport boundary

- Allowlist exact HTTPS origins, default ports, and path classes. Reject userinfo, fragments, credentials in URLs, lookalike hosts, and unexpected query parameters before transport.
- Disable implicit redirects. Parse each `Location` relative to the current approved URL, validate it, enforce a small hop limit, and only then send the next request.
- For OAuth 1 or other request-bound signatures, create a fresh authorization header only after the next URL is approved. Never attach credentials and then call a client that follows redirects automatically.
- Keep a final `response.url` validation as defense in depth, but do not confuse it with pre-request redirect protection.
- Regression-test approved→unapproved and approved→unapproved→approved chains. Assert that the unapproved transport receives zero requests and zero authorization material.

## Bind returned identity to requested identity

Exact-host validation does not prove the response belongs to the requested resource. Require stable response identifiers and canonical paths to match the requested listing, album, image, tenant, or account.

- Inventory/detail exporters should compare the normalized returned public path/ID with the exact detail URL fetched.
- Album/media exporters should require the returned album key on album and image records, then bind secondary media endpoints to the selected image key plus any provider serial/version component.
- Add identity-swap fixtures where a valid approved endpoint returns another valid resource. The exporter must HOLD rather than silently relabel it.

## Resource and privacy bounds

- Enforce both declared `Content-Length` and streaming byte limits; checking size only after `read()`/`arrayBuffer()` still permits memory exhaustion.
- Bound retries, per-request timeouts, redirect hops, item counts, field lengths, and final serialized snapshot bytes.
- Treat free-form names/descriptions as untrusted. Reject control characters and privacy-sensitive patterns (VINs, emails, phone numbers, customer-ownership wording) unless the product contract explicitly requires and safely handles them.
- Log fixed-shape status/count/delta/error codes only. Never log raw bodies, signed URLs, authorization headers, or credential-file contents.
- Pair hostile fixtures with a current sanitized live read/check so a fail-closed validator is also proven to accept the healthy source.

## Credential-file contract

For a dedicated exporter credential file:

- require a regular non-symlink file;
- require ownership by the runtime user and exact mode `0600`;
- read only the named variables required by that exporter;
- ignore ambient credential variables when the dedicated-file design is meant to be exclusive;
- keep credentials local when the output can be committed as public sanitized data.

## Lock and atomic-write contract

A naïve `open(..., exclusive)` followed by a lease write has a race: another process can observe the newly created empty file and reclaim it as malformed.

Use a lease containing PID, creation time, and random owner token:

1. create exclusively;
2. write and flush the lease;
3. if another process sees malformed content, treat a recently modified file as active for a short creation-race grace period;
4. never reclaim a lease whose PID is still alive; reclaim dead-owner leases and old malformed leases;
5. before cleanup, reread the lease and delete only when the owner token still matches.

Where practical, bind PID to process start time to reduce PID-reuse ambiguity. Write candidates in the destination directory, flush, validate completely, compare semantically, and atomically replace only after all HOLD policies pass. Preserve the last known-good bytes and timestamp on no-change or failure.

## Candidate policy and tests

- Default HOLD on removals, suspicious count deltas, identity changes, privacy violations, and malformed/incomplete sources.
- Keep report-only/check mode incapable of replacement.
- Test hostile redirects, identity swaps, declared and streamed oversize bodies, privacy/control text, bounded retry exhaustion, atomic interruption, semantic no-change, live lock contention, dead-owner recovery, recent malformed-lease protection, and stale malformed-lease recovery.
- Verify exact CLI/package scripts include every maintained suite; a green umbrella command is not evidence when a security suite is omitted.
