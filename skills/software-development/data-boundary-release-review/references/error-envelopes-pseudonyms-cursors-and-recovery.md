# Error envelopes, pseudonyms, cursors, and recovery registration

Use this reference when an exact-commit dashboard remediation appears to have fixed count checks, viewer ACLs, and semantic database receipts but may still falsely label partial or privacy-bearing data trustworthy.

## 1. Probe complete paths, not parser rejection alone

A wrapper can require `success: true` yet still accept `{ success: true, data: [...], errors: [...] }`. Another provider parser can accept `{ success: false, error: "partial", rows: [...], total: N }` if it only checks row and count shapes.

Build one healthy-looking fake response per configured scope/lane with a non-empty `error` or `errors` field. Pass it through:

1. envelope parsing;
2. pagination/window collection;
3. row sanitization;
4. projection completion;
5. persistence receipt comparison.

The decisive assertion is that the final projection cannot be `complete` or `decision_usable`, not merely that one parser throws for a missing field. Require an explicit clean-success vocabulary and reject contradictory success/error combinations before consuming rows.

A short-page sentinel is not source completeness when the response also carries an error or when no provider total/terminal marker exists. Counts derived from the same received rows are self-consistency, not source completeness.

## 2. Pseudonyms must not be raw-identifier substrings

Deriving `Lead <last-six-alphanumerics>` from a provider ID leaks contact data when a malformed ID is phone-, email-, VIN-, or account-shaped. It also creates avoidable collisions.

For untrusted provider identities:

- enforce an opaque provider-ID grammar and length bound;
- reject contact-shaped or otherwise privacy-bearing IDs before persistence;
- derive display labels from a domain-separated cryptographic digest or server-held mapping, never a prefix/suffix of the raw ID;
- revalidate the pseudonym/ID relationship at the SQL boundary where practical;
- probe producer → SQL → RPC → browser with phone/email/VIN-shaped IDs.

Do not waive semantic privacy merely because immutable IDs are normally allowed fields.

## 3. Capped feeds need delivered-boundary cursors

For each scope, pair the returned page with:

- `has_more`;
- the highest matching ID actually delivered;
- an exact scope-specific latest ID if exposed separately.

Never attach a global `max(id)` to a scope-limited `LIMIT N` page and let the browser acknowledge that global value. With `N+1` matching changes, the unseen final row is skipped forever.

The regression must insert or model `LIMIT + 1` matching changes for every scope and prove the cursor cannot advance beyond the highest row in the response.

## 4. Recovery gates must include the candidate objects

A recovery job can be green while restoring a committed baseline whose manifest predates the candidate migration. Check all of these independently:

- baseline/manifest migration cutoff includes the candidate;
- candidate tables, functions, policies, RLS/FORCE state, owners, ACLs, and critical function bodies appear in canonical fingerprints;
- CI invokes the candidate-specific migration verifier;
- fresh target baseline equals parent baseline plus ordered candidate migrations;
- rollback and reapply preserve ledger and normalized target parity.

A maintained verifier that exists in the repository but is absent from CI/recovery registration is not release evidence.

## Compact reporting pattern

For every reproduced HIGH, include exact lines, the accepting sequence, final observed result, the narrow fix, and the required regression. State explicitly when maintained tests or source gates pass despite the exploit.