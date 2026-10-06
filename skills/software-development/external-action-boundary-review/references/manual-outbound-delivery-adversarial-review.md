# Manual Outbound Delivery Adversarial Review

Use this pattern when reviewing a manual, owner-gated notification or proposal sender that wraps an existing messaging CLI/API.

## Review sequence

1. **Freeze and re-freeze.** Capture `HEAD`, status, scoped hashes, and expected test paths before reading. Recheck after tests and before the verdict. If a dirty worktree becomes committed or moves during review, reread final files and rerun focused tests at the new exact tip; stale line numbers and already-remediated findings are invalid.
2. **Trace the real transport.** Inspect the exact installed sender reached by production argv. Determine whether it retries transient errors, performs formatting fallbacks, chunks messages, extracts media/button directives, or resolves targets/profile state.
3. **Separate invocation dedupe from transport idempotency.** A durable attempt journal plus one subprocess call does not prove one provider mutation. Inject a fake transient failure into the real retry helper and count lowest-level calls. Treat commit-then-error as ambiguous and non-retryable absent a provider idempotency key.
4. **Bound post-format transport units.** Feed validator-accepted worst-case content through the real formatter and platform byte/UTF-16 length function. Assert one chunk when the contract promises one message. For intentional multipart delivery, journal every part, receipt every server message ID, and test failure after each part.
5. **Verify destination evidence provenance.** A returned destination copied from the request is intent, not server attestation. Prefer the platform response's actual chat/channel identity and test the real result-normalization path.
6. **Audit receipts.** Require strict key equality, schema version, proposal/content hashes, fixed target/label, platform, actual chat ID, validated message ID, timestamp, regular-file/non-symlink checks, and atomic readback. Document whether the delivery-state directory is trusted; any writer to an unsigned receipt directory can fabricate a perfectly matching receipt.
7. **Prove dry-run isolation twice.** At the API boundary, return before lock/journal/credential/executable/transport. At the CLI boundary, test no flags, confirmation only, send only, both exact flags, and abbreviated prefixes. Python `argparse` enables long-option abbreviation unless `allow_abbrev=False`.
8. **Validate every claimed artifact surface.** If JSON and Markdown/HTML sidecars are declared untrusted, check each against the documented link, markup, secret, and transport-directive policy. If a sidecar is never sent, classify acceptance-policy mismatch separately from transport injection.
9. **Bind provenance fields.** A hash that is only shape-checked can carry false provenance and churn artifact identity. Compare it with a trusted current source or remove the claim.

## Safe no-network probes

- Fake transport: first call raises a retryable `502`/`429`, second succeeds; assert total transport calls.
- Formatting: punctuation-heavy accepted fields pass through the real renderer/formatter; count chunks with the real platform length rule.
- CLI parser: parse shortened flags such as `--s --c` and inspect booleans without calling the command.
- Receipts: test symlink, missing/extra keys, wrong hashes/target/platform/chat/message ID, unreadable JSON, and an exact forged receipt to expose the local-state trust assumption.
- Crash matrix: inject failure before journal, after journal/before call, commit-then-timeout, after success/before receipt, after receipt/before attempt cleanup, and on receipt readback.

Never invoke live delivery during review unless explicitly authorized. Help output, source inspection, parser-only probes, formatter execution, and fake transports provide strong evidence without network access.

## Severity guidance

- **High:** hidden retries can duplicate external actions; dry run reaches transport; artifact controls destination/media/promotion; evidence validation is bypassable.
- **Medium:** one logical action becomes unjournaled multipart delivery; partial success cannot be reconciled; destination confirmation is request echo; receipt integrity materially underperforms claims.
- **Low:** unused sidecar policy mismatch, unbound non-authoritative provenance, CLI abbreviation, or missing tests without demonstrated external effect.

A green suite that mocks the runner proves wrapper behavior only. Report separately what is known about the real downstream transport.