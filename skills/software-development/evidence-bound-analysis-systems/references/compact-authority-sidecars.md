# Compact Authority Sidecars for Large Deterministic Evidence

Use this pattern when a deterministic upstream analyzer emits a very large inventory, while a downstream evidence system deliberately enforces a small bounded-input limit.

## Do not weaken the downstream size bound

Do not raise the consumer's maximum input size merely to parse a 100+ MB inventory. Large derived records increase memory, parsing, denial-of-service, and accidental-value-promotion risk. Preserve the bound and make the producer emit a compact authority projection.

## Authority sidecar contract

The upstream producer should deterministically emit a manifest-bound `authority.json` (or equivalent) containing only:

- authority format/version;
- inventory format and inventory SHA-256;
- read-only mode and an empty write-capability list;
- platform/build identity;
- exact source hashes, including the original source container;
- definition/provenance verification results;
- the explicitly matched authority revision;
- input-integrity hashes.

Exclude:

- configuration/settings values;
- table values;
- secrets/credentials;
- local filesystem source paths;
- free-form recommendations.

Add the sidecar to the same output hash manifest as the full inventory. The consumer must verify the sidecar's manifest row, but that check alone is only self-consistency.

## Reject sidecar-plus-manifest self-attestation

A mutable `authority.json` next to a mutable manifest can be forged as a self-consistent pair. The downstream consumer needs an independent reviewed trust root, such as pinned exact digests or a verified signature, for:

- the authority sidecar itself;
- the complete producer manifest;
- the manifest's full-inventory row;
- the provenance and source-artifact pair matched by the producer;
- the source container and synchronized evidence/log identities.

Require the sidecar's `inventory_sha256` to equal both the reviewed inventory digest and the manifest row. Require its source hashes and input-integrity hashes to equal the independently anchored provenance/source-artifact/container identities. A label such as `status: verified`, an authority-revision name, or a matching adjacent manifest is not authority.

Replay two public-boundary attacks before release: (1) a structurally valid forged sidecar plus rewritten adjacent manifest, and (2) a genuine sidecar rebound under a different sidecar or manifest digest. Both must yield a controlled `Not proven`/validation rejection, while the canonical producer-built sidecar succeeds. Malformed records must fail closed without crashing the consumer into an ambiguous partial state.

## Immutable-plus-additive authority pairs

When approving a new build/definition chain:

1. Keep the original approved provenance constants byte-for-byte.
2. Add a second exact provenance/source-artifact pair.
3. Return the matched authority revision explicitly.
4. Reject mixed old/new pairs and every unknown pair.
5. Keep the historical integration fixture and prove it remains green.

A released decoder does not automatically authorize a new build chain. A verified new chain does not prove what is currently deployed and does not grant deploy/write authority.

## Consumer linkage gate

The downstream system should accept current-artifact linkage only when all required identities agree:

- exact independently anchored sidecar hash;
- exact independently anchored complete producer-manifest hash;
- sidecar `inventory_sha256`, reviewed inventory digest, and manifest inventory row;
- exact pinned provenance/source-artifact pair and matching input-integrity hashes;
- exact manifest-bound source artifact and synchronized log/evidence hashes;
- sidecar source-container hash equals the source artifact hash;
- expected build and authority revision;
- `mode = read-only`, no write capabilities, and verified definition status/evidence.

Any missing, duplicated, mixed, self-attested, or mismatched field leaves the linkage `Not proven`. Informational status output must derive from this validated linkage, identify historical and current imports separately, and keep deploy/write authority explicitly false.

## Verification sequence

1. Add RED/GREEN unit tests for old pair, new pair, mixed-pair rejection, unknown-pair rejection, forged sidecar+manifest rejection, and sidecar/manifest rebound rejection.
2. Add a sidecar test proving no settings/tables/domains/paths appear and serialized size remains bounded.
3. Generate the real candidate into two temporary directories and require byte-identical outputs.
4. Verify the complete output manifest and independently anchor the reviewed sidecar, manifest, inventory row, provenance pair, source container, and synchronized evidence.
5. Promote deterministic outputs with hash readback and re-run the same attack probes against the public consumer boundary.
6. Regenerate revision diffs from the promoted inventories.
7. Exercise the real public ingest → analysis → handoff → status path.
8. Inspect machine-readable blockers and prohibited actions, not just prose.
9. Mark prior closeouts as historical/superseded rather than leaving stale HOLD/current-map-missing claims as active operational truth.

Real-flow execution is required: unit tests can miss record-shape assumptions such as a renderer requiring fields that only linked revisions introduce.

## Concurrent specialist-profile handling

When the producer is a live specialist profile, a foreground answer can finish while delegation completions or automatic curators are still modifying skills/reports. Before backup, candidate hashing, or edits:

- wait for the foreground turn and every related background finalizer to end;
- bound or suspend automatic curation during a long release-critical foreground pass, then verify the runtime setting rather than assuming a config key exists;
- list files modified during the audit window;
- re-read concurrently touched files before patching;
- resolve paths from the actual profile root (or use verified absolute paths); never embed another profile's absolute home path inside an isolated profile whose `HOME` may already be remapped;
- do not use a naive whole-tree hash across the live profile.

Freeze a manifest-owned rollback pack containing every planned edit and generated output. Record source evidence separately as protected, unmodified hashes.

## Release boundary

Reserve budget for full suites, deterministic regeneration, source-integrity checks, baseline update, independent exact-tip review, and runtime readback. If the execution/tool ceiling arrives first, report **candidate implemented; release unresolved**. Never promote partial verification to APPROVE.
