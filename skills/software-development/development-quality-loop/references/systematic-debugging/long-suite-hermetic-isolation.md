# Long-suite hermetic test isolation pitfalls

Use this reference when a single targeted test passes but the same test fails only after thousands of earlier tests in one Python process.

## Pattern: module-level path constants computed before HERMES_HOME isolation

Some modules compute legacy path constants at import time, e.g. `PAIRING_DIR = get_hermes_dir(...)`. In long `pytest -q -x` runs, another test can import the module before the autouse fixture redirects `HERMES_HOME` to a per-test tempdir. Later tests may then use the stale path and touch real/default profile state, even though `os.environ["HERMES_HOME"]` is isolated.

Symptoms:
- Targeted test passes alone.
- A long ordered run fails with state that looks stale or impossible.
- The failure involves rate limits, caches, persistent JSON stores, or other stateful module-level path constants.

Fix pattern:
- In the hermetic autouse fixture, after setting the fake `HERMES_HOME`, check whether the module is already imported via `sys.modules.get(...)`.
- If present, patch the module-level path constant to the current per-test home with `monkeypatch.setattr(..., raising=False)`.
- Verify by running the state-mutating predecessor test immediately followed by the previously failing test in the same pytest command.

Example shape:

```python
monkeypatch.setenv("HERMES_HOME", str(fake_hermes_home))

mod = sys.modules.get("gateway.pairing")
if mod is not None:
    monkeypatch.setattr(
        mod,
        "PAIRING_DIR",
        fake_hermes_home / "platforms" / "pairing",
        raising=False,
    )
```

Do not capture this as a claim that a specific feature is broken. The durable lesson is the long-suite isolation pattern: module-level constants can bypass later env isolation unless the fixture realigns already-imported modules.
