# `patch` tool: wrong-block corruption on non-unique `old_string`

When hot-patching production code with the `patch` tool, an `old_string` that matches multiple locations — or one that becomes unique only after a few extra lines but matches the *wrong* unique location — will silently land the edit in the wrong block. The tool reports success, lint may pass, and the regression ships.

This is the same family of failure mode as the other "tool reports success but corrupts the artifact" pitfalls in the parent skill (`read_file`/`write_file` secret redaction, plist binary corruption, terminal output redaction). Same root cause: trusting a tool's success signal without independently verifying the outcome.

## Symptoms

- `patch` returns `success: true` and a diff
- `lint: ok` (or syntax-checks pass) — Python in particular accepts many wrong-shape edits
- The actual program behavior is broken: orphan `except:` clauses, dedented blocks under the wrong `try:`, duplicated content, inserted blocks dangling outside their intended parent
- The bug only surfaces at runtime, or when you re-read the diff hunk and notice it landed somewhere unexpected
- A second `patch` to "fix" the corruption matches multiple times again, deepening the mess

## Why this happens

Real codebases have repeated patterns. Examples:

```python
            except Exception as _err:
                log(f"some error: {_err}")
```

```python
        try:
            ...
        except Exception:
            pass
```

```bash
if [[ $? -ne 0 ]]; then
    echo "error"
    exit 1
fi
```

A 3-5 line `old_string` window will often match every instance of these. The `patch` tool dutifully refuses with `Found N matches`. The reflex is to add "a few more lines" — but if the additional lines are themselves boilerplate (the next `except:`, the next `if:`, the next blank line), the result is one of the matches becoming unique by coincidence, not by intent. The patch lands in the first/last block that happens to match the extended snippet.

`lint: ok` is a weak signal: Python parses dedented-into-wrong-scope code happily. Bash accepts orphan branches. You need to inspect the *diff hunk's line numbers* to confirm correctness, not the lint result.

## Correct approach

### 1. Anchor on a unique line, not on boilerplate

When `patch` reports multiple matches, the fix is **not** "more context." It's "**find the unique line within ~3 lines of your insertion point**" and rebuild `old_string` around that.

Good anchors:
- A unique log message (`log(f"proposal_handler correction check error: {_ph_err}")`)
- A specific function call (`handle_signal_message(...)`)
- A unique comment (`# ── Run decision layer ──`)
- A specific variable name only used in one branch

Bad anchors (boilerplate):
- `except Exception as e:`
- `return`
- `try:` / `pass`
- Blank lines

### 2. Read the returned diff hunk

After every `patch` call, the tool returns a diff like:

```
@@ -707,23 +707,13 @@
```

Read those line numbers. Confirm they match where you intended to edit. If the diff shows the change landed at line 707 but you meant to insert at line 640, **revert immediately** — don't continue.

### 3. Verify with parse / runtime, not just lint

```bash
# Python: confirm AST parses
python3 -c "import ast; ast.parse(open('/path/to/file.py').read())" && echo PARSE OK

# Bash: syntax check
bash -n /path/to/script.sh && echo PARSE OK

# JSON: parse
python3 -c "import json; json.load(open('/path/to/file.json'))" && echo PARSE OK
```

These catch some wrong-block landings (e.g. an `except:` with no matching `try:`) but **not all**. Reading the diff hunk is the primary defense; parse-ok is the secondary.

### 4. Recovery from a wrong-block patch

If you catch the corruption:

1. **Stop.** Don't attempt another `patch` against the now-broken file without a plan — the broken shape will produce new multi-match problems.
2. **Read the file at the wrong-block range** to confirm exactly what got corrupted.
3. **Revert the wrong-block patch first.** Use the corrupted block + its surrounding lines (which are now unique because the corruption made them unique) as the `old_string`, and the original pre-corruption block as `new_string`.
4. **Re-apply the actual fix** with a new, properly-anchored `old_string` — usually a unique log message or function call adjacent to the insertion point.
5. Run parse-check and re-read the diff hunk to confirm.

### 5. Prefer `mode=replace` over `replace_all=True` for repeated patterns

`replace_all=True` will rewrite every match. If your intent is to update *one* block, that's wrong. If your intent is to update *every* instance of a boilerplate (e.g. rename `oldFunc` to `newFunc` across all call sites), `replace_all=True` is correct — but verify the count of replacements in the response matches your expected number of call sites.

## Worked example: listener.py

Hot-patching a long-running event listener (`listener.py`) to fix a `NameError` firing on every event.

**The intended fix:** insert a context-fetch call inside the event handler, between one specific `except` block and the `if handled:` branch that follows it.

**Attempt 1:** a 4-line `old_string`:
```python
            except Exception as err:
                log(f"correction check error: {err}")


            if handled:
```

`patch` returned `Found 4 matches for old_string` and refused — correct behavior; the handler repeats this boilerplate across several branches.

**Attempt 2:** one extra trailing line was added (a call that follows the `if handled:`). `patch` accepted it, but **the change landed in the wrong block** — a different branch further down whose trailing call happened to match.

**Detection:** lint reported `SyntaxError: expected 'except' or 'finally' block`, because the misplaced insertion orphaned an `except:`. If the boilerplate had matched differently it could have parsed fine and only failed at runtime.

**Recovery:**

1. Read the region around the reported line to see the actual corruption.
2. Revert with `old_string` = the corrupted block (now unique because of the corruption) and `new_string` = the original pre-corruption block.
3. Re-apply the fix using a properly unique anchor: the exact log message inside the intended `except` block. Boilerplate `except Exception as err:` repeats; a branch-specific log message usually does not.
4. Lint passes; restart the process through its supervisor so the fix is loaded.

**Cost:** a handful of extra tool calls, caught fast because lint failed loudly. Worst case if lint had passed: the process would run with corrupted control flow, the original bug would persist, and a new one would be introduced.

## Pattern checklist when patching

- [ ] Read the file at the target line range first (`read_file` with offset/limit)
- [ ] Identify a unique anchor within ~3 lines of the insertion point (unique log message, function call, comment, or variable)
- [ ] Build `old_string` around that anchor with enough trailing/leading context to make the *full string* unique
- [ ] After `patch` returns, read the diff hunk's `@@ -X,Y +X,Z @@` line numbers and confirm they match intent
- [ ] Run a parse-check (`ast.parse`, `bash -n`, `json.load`) as a secondary signal
- [ ] If parse fails OR diff hunk landed in the wrong place, revert before doing anything else
- [ ] Re-read the patched region to confirm semantic correctness, not just syntactic
