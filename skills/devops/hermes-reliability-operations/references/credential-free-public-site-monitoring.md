# Credential-Free Public Site Monitoring from an Independent Host

Use this pattern when the owner asks for external uptime monitoring that must remain independent of Hermes profiles and must not copy existing business/profile tokens.

## Source-of-truth sequence

1. Read the relevant site operations notes for known domains, routes, privacy locks, and historical caveats.
2. Verify every proposed endpoint against the live public source. Prefer `robots.txt`, canonical sitemap indexes, page sitemaps, HTML titles/markers, and public DNS/TLS—not memory or guessed route names.
3. Record contradictions as findings rather than inheriting stale notes. Typical examples: a previously broken `www` alias now works, or `robots.txt` advertises a hostname that no longer resolves.
4. Do not modify the site, DNS, credentials, workflows, or monitor host during a read-only design request.

## Endpoint classes

### Frequent core checks

Use ordinary HTTPS `GET`, not `HEAD`, because CMS/CDN/serverless stacks can handle `HEAD` differently. For each business-critical path verify:

- expected HTTP status
- final URL after no more than five redirects
- expected MIME type
- a small stable title/body marker
- total latency

Pair wrapper and dependency checks. Example: a CMS page that embeds a third-party widget can return 200 while the embedded host is unavailable, so monitor both the wrapper page and the embedded source origin.

### Daily/configuration checks

- `robots.txt`
- canonical sitemap index and page sitemap(s)
- all current sitemap page locations, discovered dynamically
- legal/privacy pages required by public integrations
- DNS resolution and authoritative nameservers
- TLS hostname/chain validation and expiry

Do not hard-code dynamic detail-page URLs. Discover them from the current sitemap and treat list churn as normal.

### Safe route-contract probes

For credential-free serverless/auth routes, a non-200 response may be the healthy contract:

- anonymous session endpoint: expected `401` JSON
- protected data endpoint: expected `403` JSON
- POST-only endpoint probed with GET: expected `405` JSON

These checks prove route loading and method/auth boundaries only. They do not prove authenticated dependencies, databases, LLM providers, or notification delivery. Never routine-POST to lead, chat, form, booking, payment, or customer-write endpoints merely to test uptime.

## DNS and TLS rules

- Resolve A/AAAA/CNAME and distinguish NXDOMAIN/SERVFAIL/no-answer from normal CDN IP rotation.
- Do not pin CDN edge IPs; they rotate normally.
- Validate hostname and certificate chain, not only TCP/443.
- Suggested TLS thresholds: warning 30 days, critical 14 days, emergency 7 days.
- Treat a dead hostname advertised by `robots.txt` or a sitemap as a public configuration defect, even if the working canonical hostname can be inferred.

## Noise and safety controls

- Connect timeout 5s; total timeout 15s.
- Alert after two consecutive hard failures.
- Warn on sustained latency above 2.5s; critical on timeout or sustained 5s+.
- Send one recovery message.
- Suppress repeated identical alerts for 30–60 minutes.
- Use jitter on timers.
- Never include fetched response bodies, arbitrary headers, cookies, tokens, signed URLs, customer data, or raw logs in alert text. Emit only configured labels, status, latency, TLS days, DNS result class, and a stable truncated fingerprint.
- Privacy/indexing invariants such as `Disallow: /` and `noindex,nofollow` should be monitored as configuration checks until the owner explicitly launches the site.

## Independent private Slack alert path

For a true private Slack alert path that does not reuse Hermes/profile credentials:

1. The owner/workspace owner creates a dedicated app such as `Site Monitor`.
2. Grant only bot scope `chat:write`.
3. Install it to the workspace and send with Slack `chat.postMessage`, passing the owner's already-known user ID as `channel`. Slack can open the app's own 1:1/App Home conversation from that user ID.
4. Do not request `users:read`, history, channel-read, files, admin, Socket Mode, `chat:write.public`, or `im:write` unless a live install proves an additional scope is genuinely required.
5. Do not reuse another bot's DM channel ID; DM/App Home relationships are app-specific.
6. Store the new bot token only on the monitoring host via a root-readable systemd credential or mode-0600 environment file.

An incoming webhook is acceptable for a dedicated private channel, but it is not the preferred true-DM design: Slack binds it to the install-selected channel and does not permit overriding that channel per request.

## Credential boundary

Everything except private delivery can be built and tested credential-free:

- endpoint manifest
- HTTP/marker, DNS, TLS, and latency probes
- local state and deduplication
- recovery/throttle logic
- systemd service/timer
- local alert spool and dry-run output
- disabled transport adapter and tests

The unavoidable owner-created credential for Slack DM delivery is a new low-scope bot token for the dedicated monitor app. It must be supplied directly to the monitoring host, never copied from the agent's own config or any profile.

## Reporting contract

A read-only design report should include:

- exact verified URLs and expected statuses/markers
- probe timestamp
- current DNS/TLS findings and expiry dates
- stale-notes/live-source contradictions
- endpoints deliberately excluded because a safe GET cannot prove them
- what is buildable now without credentials
- the one owner-created credential still required
- explicit confirmation that no files, workflows, credentials, DNS, or production settings were changed
