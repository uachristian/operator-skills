# Python Atomic State File Writes

**Context:** Production automation scripts that persist state (offsets, rate limits, dedup hashes, muted lines) must handle crashes and concurrent runs gracefully. Direct writes (`open(file, 'w').write(data)`) can corrupt JSON files if the process dies mid-write or two instances run simultaneously.

**Pattern:** Write to temp file, then atomic rename.

## Implementation

```python
import json
import os
from pathlib import Path

def save_json(path: Path, data: dict):
    """Atomically save JSON file using temp + rename."""
    tmp_path = path.with_suffix(f'.tmp.{os.getpid()}')
    try:
        with open(tmp_path, 'w') as f:
            json.dump(data, f, indent=2)
        os.replace(tmp_path, path)  # Atomic on POSIX
    except Exception as e:
        print(f"ERROR: Failed to save {path}: {e}", file=sys.stderr)
        if tmp_path.exists():
            tmp_path.unlink()
        raise
```

## Corrupted File Recovery

If a state file gets corrupted despite atomic writes (disk failure, manual edit gone wrong):

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

**Recovery policy:**
- Log the error to stderr (captured by launchd StandardErrorPath)
- Reinitialize to `{}` and continue (don't crash)
- State resets, but system keeps running
- User sees the warning in logs and can investigate

**Why `{}` is safe:** For offset tracking, missing offset → first-run guard triggers → skip existing content. For rate limits/dedup, missing data → allow the alert (prefer false positive over missing critical error).

## Why os.replace() is Atomic

On POSIX systems (macOS, Linux), `os.replace()` is implemented via `rename(2)`, which:
1. Is atomic at the filesystem level
2. Overwrites destination file in a single operation
3. Cannot leave a half-written file visible to other processes

**Not atomic:**
- `open(file, 'w').write(...)` — visible to readers mid-write
- `shutil.copy() then os.remove()` — gap between operations
- `write_file` tool — no atomicity guarantee

## PID in Temp Filename

Using `tmp.{os.getpid()}` prevents collisions if:
- Two instances of the script run simultaneously (one via launchd, one manual)
- Script crashes and leaves temp file behind
- Multiple scripts in same directory use this pattern

Next run will create a new temp file with different PID, won't conflict.

## Worked example

**Problem:** a log-error watcher (`error_watcher.py`) needs to persist:
- `error_watcher_offsets.json` — byte offsets per log file
- `error_watcher_ratelimit.json` — last alert timestamp per job
- `error_watcher_dedup.json` — occurrence timestamps per line hash
- `error_watcher_muted.json` — mute expiration timestamps per line hash

Runs every 60 seconds via launchd. Crashes mid-write → corrupt JSON → watcher can't start → no error alerts → production blind.

**Solution:** All state writes use atomic pattern + corrupted-file recovery.

## Full Example (error_watcher.py excerpt)

```python
def main():
    # Load state (with corruption recovery)
    offsets = load_json(OFFSETS_FILE)
    ratelimits = load_json(RATELIMIT_FILE)
    dedup = load_json(DEDUP_FILE)
    muted = load_json(MUTED_FILE)
    
    # ... process logs, update state ...
    
    # Save updated state (atomically)
    save_json(OFFSETS_FILE, offsets)
    save_json(RATELIMIT_FILE, ratelimits)
    save_json(DEDUP_FILE, dedup)
    save_json(MUTED_FILE, muted)
```

If script crashes between saving offsets and saving ratelimits:
- ✅ offsets.json is complete (atomic write succeeded)
- ✅ ratelimits.json unchanged (write never started)
- ✅ Next run: loads old ratelimits, re-processes that minute's logs
- ✅ Worst case: duplicate alert (acceptable)

## Testing

```bash
# Simulate crash mid-write
python -c "
import json
f = open('test.json', 'w')
f.write('{\"partial\":')  # No closing brace
# Process killed here
"

# Try to load
python -c "
import json
print(json.load(open('test.json')))
"
# JSONDecodeError: Expecting property name

# With atomic writes + recovery
python error_watcher.py
# WARNING: Corrupted or unreadable test.json: ...
# Continues with {} initialization
```

## Trade-offs

**Pros:**
- Prevents corruption from crashes
- Safe for concurrent runs
- Simple to implement
- Standard POSIX behavior

**Cons:**
- Temp file creates filesystem noise (cleaned up on success)
- Small window where old and new data differ (acceptable for monitoring)
- Requires write permission in state directory (already needed)

**Not solved:**
- Disk full errors (write fails, raise exception, launchd logs to stderr)
- Filesystem corruption (handled by load_json recovery)
- Multiple processes writing same file simultaneously (prevented by rate limit logic + 60s interval)

## Related Patterns

- **bash atomic writes:** `echo "$content" > "$file.tmp.$$" && mv "$file.tmp.$$" "$file"`
- **Database transactions:** BEGIN → UPDATE → COMMIT (all-or-nothing)
- **Config management:** Ansible/Terraform use temp files then atomic swap

## References

- Python docs: [os.replace()](https://docs.python.org/3/library/os.html#os.replace) — "If dst exists, it will be replaced atomically (subject to platform limitations)."
- POSIX: [rename(2)](https://man7.org/linux/man-pages/man2/rename.2.html) — "If newpath already exists, it will be atomically replaced."
