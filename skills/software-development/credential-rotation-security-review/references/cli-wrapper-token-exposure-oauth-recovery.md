# CLI wrapper token exposure and OAuth recovery

Use this reference when an account token is exposed by a CLI/npm wrapper, or when a supported browser/OAuth login can replace a long-lived local token.

## Exposure pattern

A command can be semantically safe yet leak through its wrapper. `npx`, npm scripts, package runners, paginated CLIs, and shell tracing may print the fully expanded command line—including a token passed through `--token`—before the underlying tool emits a sanitized response.

Do not treat “the command only returned a username” as proof the full output was secret-safe. Review wrapper notices, suggested continuation commands, argv, stdout, and stderr separately.

## Proven containment and recovery sequence

1. Stop using the exposed token immediately; never rerun it to confirm exposure.
2. Notify the owner privately and classify the actual surface. Rotation remains the default even for a private local session log.
3. Use an already authenticated account dashboard to identify the exact token by **name plus recent activity**, not by guessing from row order.
4. Open only that row's action menu. Require the destructive confirmation to name the expected token and exact count.
5. Revoke it, then read back that the row disappeared while unrelated tokens remain.
6. Remove the stale local secret reference atomically without printing its value. Preserve secret-file owner/mode and verify the key name is absent.
7. Prefer the provider's browser/OAuth CLI login if interactive workstation access does not require a long-lived account token.
8. Verify identity with a tokenless command such as `whoami`; do not add `--token` after OAuth succeeds.
9. Keep deploy/apply/records/DNS held: credential incident response does not inherit production-change authority.

## Browser/OAuth execution discipline

- OAuth callback windows can have short deadlines. Start a fresh flow only when the authorization window can be handled immediately.
- Do not fall back from expired OAuth to typing an API key through tool input, argv, chat, or session logs.
- Background input is preferred. If the browser's AX route is unavailable, foreground only after explicit approval, click the exact verified authorization control, verify the callback receipt, then restore the prior app.
- Treat `effect=unverifiable` as delivered but unconfirmed: read the CLI callback or fresh page state before retrying.
- Never capture or copy a replacement token reveal screen. If OAuth suffices, do not create a replacement token at all.

## If API/CI still requires a token

Create a new least-privilege/project-scoped token when supported. The owner or an approved local secret bridge must store it without token-bearing argv, screenshots, clipboard/session history, or chat. Verify with a bounded request that constructs the Authorization header inside the process and emits only sanitized account/project metadata.

## Completion evidence

- Exact exposed token removed from provider list.
- Unrelated credentials unchanged.
- Stale local secret key absent; file mode preserved.
- OAuth/CLI identity readback succeeds without a token argument.
- No production mutation occurred during recovery.
