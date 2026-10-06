# Semantic alert dedupe for webhook notifications

Transport-level webhook idempotency is not enough when an upstream service sends several distinct webhook deliveries for the same business event. Use this pattern for payment, invoice, status, shipment, or approval notifications that must not repeat in chat.

## When to use

Use this when duplicate notifications have:

- different webhook delivery IDs or timestamps, but
- the same real-world event: same payment, receipt, invoice, PO, tracking number, approval, etc.

Do **not** replace transport-level dedupe; layer semantic dedupe on top of it.

## Implementation pattern

1. Keep the standard delivery-id ledger for exact retries.
2. Define a semantic key for the alert class:
   - payment: `payment_id`, fallback `receipt:order:amount:fee`
   - invoice: `invoice_id`, fallback `invoice_number:customer:amount`
   - shipment: `tracking_number:carrier`, fallback `po:status:eta`
3. Store semantic alert state separately from the webhook delivery ledger.
4. Reserve the semantic key before sending the chat notification.
5. If send succeeds, mark the key `sent` with useful metadata.
6. If send fails, clear the reservation so a later retry can alert.
7. When a duplicate semantic key arrives, return success to the webhook sender and log a structured suppressed outcome.
8. Seed the semantic ledger from historical successful event logs before restarting a patched receiver; otherwise old events can re-alert on the first post-deploy duplicate.

## Concurrency pitfall

A `seen? -> send -> mark seen` flow can race under threaded webhook servers. Two deliveries can both check before either marks seen. Reserve first, send second, finalize third.

## Verification checklist

- Compile/lint the receiver.
- Smoke test first reserve succeeds and second reserve fails.
- Smoke test failed-send reservation clearing.
- Confirm duplicate events still return HTTP 200.
- Confirm suppressed duplicates are logged for auditability.
- Confirm the target known duplicate key is present in state.
- Restart/recycle only the specific webhook service, then verify `/health`.

## Safe service recycle note

If the service is a standalone LaunchAgent with `KeepAlive=true` and `launchctl kickstart` is unavailable from the current agent context, terminate only that service PID and verify launchd relaunches it. Do not apply this shortcut to shared gateways or multi-service processes without explicit change-control approval.
