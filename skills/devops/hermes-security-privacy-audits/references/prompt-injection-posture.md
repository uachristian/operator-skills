# Prompt-injection posture review

No system is "safe" against prompt injection; the deliverable is: live injection evidence (none/some), which defenses are actually wired, and where untrusted text can reach powerful tools. Read-only first; end with a numbered fix plan.

## Checks, in order

1. **Verify defenses are live, not just documented.** For each control named in your defense log, grep the live agent install for its call site and check its log mtime. A log not written in months means that call site is disconnected, even if the file is still locked read-only.
   - Upstream wrapper: find which tool names/prefixes the agent wraps as untrusted (for example `<untrusted_tool_result>` wrapping for web_extract, web_search, `browser_*`, `mcp_*`). Output from terminal, execute_code, read_file and session search is often NOT wrapped upstream; check whether a local guard plugin covers those on each profile that runs ingesting cron jobs or takes bot traffic.
   - `grep -rl <wrapper-function>` across scripts, per-profile scripts and plugins to list wired ingest paths.
   - Any output-gate control: its mode (log-only vs enforce) and its log mtime.
   - Any capability/approval gate: before calling it dead, grep ALL consumers (shared scripts, per-profile scripts, listeners). One hook being removed does not mean every importer is gone; denials-log silence alone does not mean unused.
2. **Inbound exposure per profile** (one execute_code over config.yaml + .env): enabled platforms, their `platform_toolsets`, approvals mode, and `*_ALLOWED_USERS`. Flag any enabled messaging platform with terminal/code/browser/computer_use and no allowlist, even though the gateway default-denies (`gateway/authz_mixin.py`) — the protection is implicit, not configured. Flag profiles with no `approvals` block.
3. **Cron blast radius.** For every enabled LLM cron job (skip no_agent/script jobs) whose prompt/skills ingest outside content (mail, leads, reviews, listings, web, messages, transcripts), list `enabled_toolsets`. `None` means unrestricted — call those out by name.
4. **Injection evidence:** use the state.db scan in SKILL.md step 5.

## Fix-plan menu (owner picks)

- Pin the allowlist on any tool-rich bot lacking one (config + gateway restart).
- Explicit narrow toolsets on ingesting cron jobs.
- Add an approvals block and trim terminal/code from a profile's chat toolsets.
- Wrap terminal/code/file output for cron/bot sessions as untrusted via plugin (no upstream edit).
- Outbound gate for bot/cron final messages (hard-block secrets/suspicious URLs).
- Correct vault docs for gates whose call sites moved; retire a legacy gate only after its consumer grep is empty.

## Applying fixes (after owner approval)

1. **Backup first:** copy every touched config.yaml, .env, cron/jobs.json and plugin dir into `~/.hermes/state/backups/<change>-<ts>/` (0700) with a sha256 MANIFEST.
2. **Allowlists / approvals / toolsets:** `hermes --profile <p> config set TELEGRAM_ALLOWED_USERS <id>` (writes .env, keeps 0600); `config set approvals.mode manual`, `approvals.cron_mode deny`, `platform_toolsets.telegram '[...]'`. Read back the YAML.
3. **Cron toolsets from evidence, not guesses:** for each job, tally tool names in the assistant `tool_calls` JSON of its last ~6 `cron_<jobid>_%` sessions (read-only DB). Pin `enabled_toolsets` to the used built-ins plus needed MCP server names (e.g. `<crm>`), or add `no_mcp` when none are used; skills/obsidian/tool_search bridge tools need no toolset. Apply through `cron.jobs.update_job(job_id, {"enabled_toolsets": [...]})` with `HERMES_HOME` set to the profile; there is no CLI flag. Run that helper script from a clean directory: a stray module in the scratch dir (e.g. `inspect.py`) shadows the stdlib. Cron reloads jobs per tick, so no restart is needed; the first real run is the proof.
4. **Untrusted-output + outbound plugin pattern** (e.g. a local `injection-guards` plugin): register `transform_tool_result` to wrap terminal/execute_code `output`, read_file `content` and session_search results in an `<untrusted_tool_result>` block, keeping the JSON shape (exit_code/success still parse) and defanging forged delimiters; register `transform_llm_output` to run the final text through an output gate (a reference `guards/output_gate.py` ships in the sibling public repo [operator-safety-kit](https://github.com/uachristian/operator-safety-kit)) and replace it with a withheld notice when hard checks fail. Scope both to cron sessions (`HERMES_CRON_SESSION` or platform `cron`) and known bot user IDs/`*bot` usernames so owner sessions are untouched. Wrapping fails open; outbound withholds on gate error only when a secret regex matches. Copy the plugin into each profile's `plugins/` and `hermes --profile <p> plugins enable <name>`; verify hashes match across copies.
5. **Verify:** unit tests with blocking and healthy controls, then a live check that loads the real plugin manager (`get_plugin_manager().discover_and_load()`, `has_hook`, `invoke_hook`) with `HERMES_HOME` set to a profile.
6. **Restarts are the owner's step:** gateway restart is blocked from inside a running gateway. `plugins enable` live-reloads transform hooks into the running gateway, but allowlist/toolset/approval config changes need `hermes --profile <p> gateway restart` from a separate terminal. Say which changes are inactive until then.
7. Capture applied state and rollback path in the vault under the security hub.

State unverified items explicitly: gateway restarts, a live negative test of the default-deny, and the first cron run under new toolsets.
