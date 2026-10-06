# Write Tool Escaping Pitfall — Regex Patterns and Heredocs

## Summary

A real session where write_file tool double-escaped backslashes in regex pattern file, corrupting grep -E patterns. `\b` (word boundary) became `\\b` (literal backslash-b) on disk. Solution: use heredoc in terminal for files containing escape sequences.

## The Problem

### What Happened
1. Agent created `~/.hermes/config/error_patterns.txt` using write_file
2. Content intended: `\bERROR\b` (grep -E word boundary)
3. Content on disk: `\\bERROR\b` (literal backslash + "bERROR" + backslash + "b")
4. First test passed by accident (matched "ERROR" substring, not word boundary)
5. User caught corruption with `cat -e` showing literal backslashes
6. True-negative test would have failed (false positives)

### Why It Happens
The write_file tool serializes content and escapes backslashes during the process. Single `\` becomes `\\` on disk.

### Detection Commands

**macOS:**
```bash
cat -e /path/to/file
```

**Linux:**
```bash
cat -A /path/to/file
```

Both show literal file contents with line endings visible ($ at EOL).

**Expected output:**
```
\bERROR\b$
```

**Corrupted output:**
```
\\bERROR\\b$
```

## The Solution: Heredoc in Terminal

Use single-quoted heredoc delimiter to prevent shell expansion:

```bash
cat > ~/.hermes/config/error_patterns.txt <<'PATTERNS'
\bERROR\b
\bFATAL\b
^Traceback
\bException:
PATTERNS
```

**Key details:**
- Single quotes around `'PATTERNS'` prevent shell variable expansion and preserve literal backslashes
- Without quotes (`<<PATTERNS`), shell would expand `\b` to backspace character
- Works for any escape sequences: `\n`, `\t`, `\d`, `\s`, etc.

## Verification Workflow

### 1. Check Literal File Contents
```bash
cat -e ~/.hermes/config/error_patterns.txt   # macOS
cat -A ~/.hermes/config/error_patterns.txt   # Linux
```

Should show single backslash per escape sequence.

### 2. Test True Positive (should match)
```bash
echo "ERROR: connection failed" | grep -iE "$(grep -v '^#' ~/.hermes/config/error_patterns.txt | grep -v '^[[:space:]]*$' | paste -sd '|' -)" && echo "MATCHED (GOOD)" || echo "NO MATCH (BAD)"
```

Expected: `MATCHED (GOOD)`

### 3. Test True Negative (should NOT match due to word boundaries)
```bash
echo "this is just a normal log line about errors and exceptions" | grep -iE "$(grep -v '^#' ~/.hermes/config/error_patterns.txt | grep -v '^[[:space:]]*$' | paste -sd '|' -)" && echo "MATCHED (BAD)" || echo "NO MATCH (GOOD)"
```

Expected: `NO MATCH (GOOD)`

This line contains "errors" (plural) and "exceptions" (plural), neither of which should match `\bERROR\b` or `\bException:` with proper word boundaries.

## Pattern File Format

```
# Error patterns for error_watcher (case-insensitive grep -E)
# One pattern per line, blank lines and # comments ignored

\bERROR\b          # Word boundary: ERROR (not errors, ERRORS_DIR, etc.)
\bFATAL\b          # Word boundary: FATAL
^Traceback         # Line start: Python tracebacks
\bException:       # Word boundary + colon: Java/Python exceptions
\bdenied\b         # Permission denied, access denied
^Permission denied # Line start: common Unix error
panic:             # Go panics
\bSegmentation fault\b  # Segfaults
\bAuthorizationError\b  # Auth failures
```

## When to Use Heredoc vs Write Tool

| Content Type | Tool | Reason |
|--------------|------|--------|
| Regex patterns | Heredoc | Preserves `\b`, `\d`, `\s`, `^`, `$` literally |
| Shell scripts with escapes | Heredoc | Preserves `\"`, `\'`, `\\`, `\n` |
| Config files with escape sequences | Heredoc | JSON/YAML with `\n`, `\t` |
| Plain text, no escapes | Either | write_file is fine |
| Python/Ruby code | write_file | Language handles its own escaping |
| Markdown, HTML, CSS | write_file | No shell-interpreted escapes |

**Rule of thumb:** If the file contains backslash-escape sequences that must remain literal (not interpreted by shell or write tool), use heredoc with single-quoted delimiter.

## Alternative: Escape the Escapes (Not Recommended)

You could double-escape in write_file:
```
Content: \\bERROR\\b
Result on disk: \bERROR\b (after tool unescapes)
```

**Problems:**
- Fragile (tool implementation might change)
- Hard to review (reader sees doubled backslashes)
- Error-prone (forget one escape, whole pattern breaks)
- Doesn't work for complex nested escaping

**Heredoc is cleaner and more explicit.**

## Real Failure Timeline

1. **Write:** Agent used write_file for error_patterns.txt
2. **Verify (false pass):** `echo "ERROR: test" | grep ...` → MATCHED
   - Passed because "ERROR" substring matched, not word boundary
3. **User inspection:** `cat -e` showed `\\bERROR\\b$`
4. **User test (true negative):** `echo "errors" | grep ...` → MATCHED (BAD)
   - Should NOT match due to word boundary, but did (pattern broken)
5. **Fix:** Rewrote file using heredoc
6. **Verify (correct):**
   - `cat -e` showed `\bERROR\b$` (single backslash)
   - True positive: MATCHED (good)
   - True negative: NO MATCH (good)

**Key lesson:** First test passed by accident. Always test true negative to verify word boundaries actually work.

## Impact on Production

### Without Fix (corrupted patterns)
- **False positives:** Logs containing "errors" (plural), "ERRORS_DIR", "error_handler" all match
- **Alert spam:** Hundreds of irrelevant DMs
- **Missed errors:** If patterns overmatch, user tunes out and misses real issues
- **Silent failure:** Patterns appear to work on simple tests

### With Fix (proper word boundaries)
- **Precision matching:** Only standalone "ERROR" matches, not substrings
- **Clean alerts:** Only real error lines trigger notifications
- **Trust in system:** User believes alerts are actionable

## Other Affected File Types

This issue applies to any file using backslash-escapes:

### Shell Scripts
```bash
cat > script.sh <<'SCRIPT'
echo "Line 1\nLine 2"  # Literal \n, not newline
SCRIPT
```

### JSON Configs
```bash
cat > config.json <<'JSON'
{"pattern": "\\d{3}-\\d{4}"}
JSON
```

### Grep/Sed/Awk Scripts
```bash
cat > transform.sed <<'SED'
s/\bERROR\b/WARN/g
SED
```

All benefit from heredoc to preserve escapes literally.

## Summary Checklist

When creating files with escape sequences:

- [ ] Use heredoc with single-quoted delimiter (`<<'DELIMITER'`)
- [ ] Verify with `cat -e` (macOS) or `cat -A` (Linux)
- [ ] Test true positive (pattern SHOULD match)
- [ ] Test true negative (pattern should NOT match)
- [ ] If patterns overmatch, check for double-backslash corruption

**Bottom line:** For regex patterns, shell escapes, or any backslash sequences that must survive literally on disk → use heredoc, not write_file.
