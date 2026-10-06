# Bash vs Python for Production Automation Scripts

## Summary

A real session building error_watcher script for launchd. Initial bash implementation failed due to bash 3.2 limitation on macOS (associative arrays). Decision: rewrite in Python instead of adding Homebrew bash dependency or bash 3.2 compatibility hacks.

## The Problem: Bash Version Assumptions

### What Happened
1. Agent wrote `error_watcher.sh` using `declare -A line_counts` for dedup tracking
2. Syntax check passed (`bash -n`) — user had bash 5.x in PATH via Homebrew
3. Script deployed to launchd, first run failed:
   ```
   declare: usage: declare [-afFirtx] [-p] [name[=value] ...]
   EXIT: 2
   ```
4. launchd uses system bash at `/bin/bash` (v3.2.57) regardless of user PATH
5. Bash 4+ features (associative arrays) don't exist in system bash

### Why macOS Ships Bash 3.2
macOS ships bash 3.2.57 due to GPL2 licensing (bash 4+ is GPL3). Apple won't upgrade system bash.

### Symptoms
- Script works when run manually (if user has `/usr/local/bin/bash` in PATH)
- Script fails when run by launchd, cron, or other automation (uses `/bin/bash`)
- `declare: -A: invalid option` error
- Exit code 2 instead of expected 0

## The Decision: Python Over Bash

User was presented three options:
1. **Install bash via Homebrew** → Adds dependency to bulletproofing infrastructure (wrong direction)
2. **Bash 3.2 compatibility rewrite** → Uglier code, parallel arrays, harder to maintain
3. **Python rewrite** → Already a dependency, better error handling, cleaner state management

**User chose Option 3: Python rewrite**

Rationale:
- Python 3 already guaranteed present on macOS
- Hermes venv already has Full Disk Access permissions
- Better data structures (dict > parallel arrays)
- JSON handling native (no jq dependency)
- HTTP requests with error handling (requests library)
- Atomic file writes cleaner (`os.replace` vs temp+mv in bash)
- Avoids shell escaping pitfalls

## Python Production Script Template

### Shebang
Use a portable shebang in the script itself, and pin the exact interpreter in the scheduler entry instead (see the launchd section below):
```python
#!/usr/bin/env python3
```

Why:
- The script stays portable across machines and users (no hard-coded home path)
- The scheduler entry names the exact venv interpreter, so the runtime environment (venv packages like requests) is still deterministic
- On macOS, privacy permissions (e.g. Full Disk Access) attach to the interpreter binary the scheduler launches, so grant them to that exact path

### Structure
```python
#!/usr/bin/env python3
"""
script_name.py — Brief description

Longer description of what this does
"""

import json
import os
import sys
from pathlib import Path

# Constants at top
HERMES_ROOT = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
STATE_DIR = HERMES_ROOT / "state"

def main():
    # Main logic here
    pass

if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print(f"FATAL: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
```

### Atomic State Writes
```python
def save_json(path: Path, data: dict):
    """Atomically save JSON file using temp + rename."""
    tmp_path = path.with_suffix(f'.tmp.{os.getpid()}')
    try:
        with open(tmp_path, 'w') as f:
            json.dump(data, f, indent=2)
        os.replace(tmp_path, path)
    except Exception as e:
        print(f"ERROR: Failed to save {path}: {e}", file=sys.stderr)
        if tmp_path.exists():
            tmp_path.unlink()
        raise
```

### Corrupted JSON Recovery
```python
def load_json(path: Path) -> dict:
    """Load JSON file, return {} if corrupted or missing."""
    try:
        if path.exists():
            with open(path, 'r') as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"WARNING: Corrupted or unreadable {path}: {e}", file=sys.stderr)
    return {}
```

### Error Handling for External APIs
```python
def send_slack_dm(token: str, channel: str, message: str) -> bool:
    """Send a Slack message to `channel` (a user ID opens the app DM).

    Returns True on success, False on failure.
    """
    try:
        response = requests.post(
            'https://slack.com/api/chat.postMessage',
            headers={'Authorization': f'Bearer {token}'},
            json={'channel': channel, 'text': message},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        if not data.get('ok'):
            print(f"ERROR: Slack API returned ok=false: {data}", file=sys.stderr)
            return False
        return True
    except Exception as e:
        print(f"ERROR: Failed to send Slack DM: {e}", file=sys.stderr)
        return False
```

**Key principle:** Return False on failure, don't crash. Caller decides whether to update rate limits (if False, retry next run).

## Bash 3.2 Compatibility (If You Must)

If you absolutely must use bash, avoid these bash 4+ features:

| Feature | Bash 4+ | Bash 3.2 Alternative |
|---------|---------|---------------------|
| Associative arrays | `declare -A map` | Encoded keys or parallel arrays |
| Regex matching | `[[ $str =~ pattern ]]` | `echo "$str" \| grep -E 'pattern'` |
| readarray/mapfile | `readarray -t arr < file` | `while IFS= read -r line; do arr+=("$line"); done < file` |
| &>> redirect | `cmd &>> file` | `cmd >> file 2>&1` |

**Parallel array pattern for dedup:**
```bash
# Instead of: declare -A line_counts
# Use two parallel arrays:
declare -a line_hashes
declare -a line_texts

for line in "${error_lines[@]}"; do
    hash=$(echo -n "$line" | md5 -q)
    
    # Check if hash already seen
    found=false
    for i in "${!line_hashes[@]}"; do
        if [[ "${line_hashes[$i]}" == "$hash" ]]; then
            found=true
            break
        fi
    done
    
    if ! $found; then
        line_hashes+=("$hash")
        line_texts+=("$line")
    fi
done
```

This is **significantly uglier** than Python's `dict` or bash 4's `declare -A`, which is why Python was chosen.

## Verification Before Deployment

Test with system bash explicitly:
```bash
# Syntax check
/bin/bash -n script.sh

# Runtime test
/bin/bash script.sh

# NOT: bash -n (uses whatever's in PATH)
```

For Python, test with venv interpreter:
```bash
# Syntax check
/path/to/venv/bin/python -m py_compile script.py

# AST parse check
/path/to/venv/bin/python -c "import ast; ast.parse(open('script.py').read())"

# Runtime test
/path/to/venv/bin/python script.py
```

## launchd Configuration for Python Scripts

```xml
<key>ProgramArguments</key>
<array>
    <string>/absolute/path/to/venv/bin/python</string>
    <string>/absolute/path/to/script.py</string>
</array>
```

**Not:**
```xml
<!-- DON'T USE /usr/bin/env -->
<array>
    <string>/usr/bin/env</string>
    <string>python3</string>
    <string>/path/to/script.py</string>
</array>
```

Why direct path:
- launchd doesn't source user PATH
- `/usr/bin/env` uses minimal PATH, won't find venv
- Direct path ensures correct interpreter with correct packages

## When to Choose Python vs Bash

| Use Case | Bash 3.2 | Python |
|----------|----------|--------|
| Simple glue (< 50 lines, no state) | ✓ | Overkill |
| Log tailing + regex matching | ✓ | ✓ (cleaner) |
| JSON state persistence | Requires jq | ✓ Native |
| HTTP API calls | curl + jq | ✓ requests library |
| Deduplication / hash maps | Ugly parallel arrays | ✓ dict |
| Complex error handling | Fragile | ✓ try/except |
| Multi-file state management | Error-prone | ✓ Pathlib |
| Atomic writes | `tmp=$$.tmp; echo > $tmp && mv $tmp $file` | ✓ os.replace() |

**Rule of thumb:** If you need `declare -A`, `readarray`, or complex JSON manipulation → use Python.

## Example: error_watcher.py

A log-error watcher built this way had these properties:

- Monitors the agent's `logs/*.err.log` for new errors
- Tracks byte offsets per file in JSON state
- First-run guard: skip existing content on new files
- Rate limiting: max 1 DM per job per 5 min
- Deduplication: same line >3x in 10 min → mute for 1 hour
- Slack DM alerts via requests library
- Atomic JSON state writes
- Corrupted state file recovery (log warning, reinit to {})
- 290 lines, 9.5KB
- Would have been 400+ lines in bash 3.2 with parallel arrays

## Key Takeaways

1. **macOS production automation = bash 3.2 or Python** (Homebrew bash adds dependency)
2. **Test with system tools** (`/bin/bash`, not `bash` in PATH)
3. **Python preferred for:**
   - State persistence
   - API calls
   - Complex data structures
   - Atomic file writes
   - Error handling
4. **Portable `/usr/bin/env python3` shebang** in the script itself
5. **Direct venv interpreter path in the launchd/cron entry** (not `/usr/bin/env`), so the environment is deterministic
6. **Bash 3.2 is fine for simple glue** (< 50 lines, no state, no dicts)
