# JSON-Aware Secret Redaction

**Context:** When purging secrets from structured data files (JSON, YAML, TOML), naive string replacement breaks structure. Session in practice where Slack token purge corrupted 12 session JSON files by running `redact_sensitive_text()` on raw file bytes.

## The Problem

**Naive approach (WRONG):**
```python
with open(session_file, 'r') as f:
    content = f.read()

# This breaks JSON escaping when tokens appear inside string values
redacted = redact_sensitive_text(content, force=True)

with open(session_file, 'w') as f:
    f.write(redacted)
```

**What breaks:**
- Partial mask format (`xoxb-2...abcd`) changes string lengths mid-JSON
- If token spans line breaks or is near quotes, JSON structure corrupts
- Result: `json.load()` fails with `Expecting ',' delimiter` errors

**Typical failure:**
```
<session-file-1>.json: Expecting ',' delimiter: line <n> column <n>
<session-file-2>.json: Expecting ',' delimiter: line <n> column <n>
... (10 more files)
```

## The Solution: Recursive Walk-and-Redact

**JSON-aware approach (CORRECT):**
```python
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / '.hermes/hermes-agent'))
from agent.redact import redact_sensitive_text

def walk_and_redact(obj, force=True):
    """Recursively walk a JSON structure and redact string leaves."""
    if isinstance(obj, dict):
        return {k: walk_and_redact(v, force) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [walk_and_redact(item, force) for item in obj]
    elif isinstance(obj, str):
        return redact_sensitive_text(obj, force=force)
    else:
        return obj

# Load JSON, redact, write back
with open(session_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

redacted_data = walk_and_redact(data, force=True)

with open(session_file, 'w', encoding='utf-8') as f:
    json.dump(redacted_data, f, indent=2, default=str, ensure_ascii=False)
```

**Why this works:**
1. Parse JSON into Python objects FIRST
2. Recursively traverse dicts/lists/strings
3. Redact only string leaf values (preserves structure)
4. Re-serialize to JSON with proper escaping

## Verification After Redaction

**Three checks:**
```python
# 1. All files still parse
import json, glob
for f in glob.glob('/path/to/sessions/*.json'):
    json.load(open(f))  # Raises on corrupt JSON
print('ALL PARSE')

# 2. Zero full-format tokens remain
# Example: Slack xoxb-{10-13 digits}-{10-13 digits}-{40 mixed chars}
$ grep -rE 'xoxb-[0-9]{10,13}-[0-9]{10,13}-[A-Za-z0-9]{40}' sessions/ | wc -l
0

# 3. Masked tokens present (proves redaction ran)
$ grep -rE 'xoxb-[A-Za-z0-9]{1,3}\.\.\.' sessions/ | wc -l
951  # (or some >0 count)
```

## When to Use This Pattern

Apply JSON-aware redaction when:
- Purging secrets from existing session/log files
- Post-processing structured data with sensitive fields
- Migrating data between systems with different secret policies
- **Any time you need to redact secrets from `.json`, `.yaml`, `.toml` files**

**DO NOT use naive string replacement on structured data files.**

## Extend to Other Formats

**YAML:**
```python
import yaml
with open(file, 'r') as f:
    data = yaml.safe_load(f)
redacted = walk_and_redact(data)
with open(file, 'w') as f:
    yaml.dump(redacted, f)
```

**TOML:**
```python
import tomli, tomli_w
with open(file, 'rb') as f:
    data = tomli.load(f)
redacted = walk_and_redact(data)
with open(file, 'wb') as f:
    tomli_w.dump(redacted, f)
```

## Integration with agent/redact.py

**Key facts about Hermes redactor:**
- Module: `~/.hermes/hermes-agent/agent/redact.py`
- Function: `redact_sensitive_text(text: str, *, force: bool = False, code_file: bool = False) -> str`
- **NOT** `redact_secrets()` — verify function names before proposing diffs
- Mask format: partial (`xoxb-2...abcd`), not `[REDACTED_SECRET]`
- Patterns: 20+ vendor prefixes (Slack, OpenAI, GitHub, AWS, etc.)

**Always verify:**
```bash
grep -n "^def redact" ~/.hermes/hermes-agent/agent/redact.py
```

Before proposing imports in diffs.

## Real Session Recovery

**Timeline:**
1. Naive purge corrupted 12 session files
2. Restored from backup tarball
3. Applied JSON-aware re-purge (85 tokens redacted)
4. Verified: ALL PARSE + 0 full tokens + 951 masked tokens

**Lesson:** Always parse → redact → serialize for structured data. Never redact raw bytes.
