# Leak patterns and fixes

## sys.modules fake installed at collection

Shape: a `conftest.py` calls `_ensure_<lib>_mock()` at import time and writes `sys.modules["lib"] = MagicMock()` (plus submodules) without ever removing it. Files elsewhere that import the real library later in the same process bind to the mock. Symptom: values like `<MagicMock name='mock.X().attr'>` in assertions, `'MagicMock' object can't be awaited`, `StopIteration` inside async generators.

Why the guard misses: `if "lib" in sys.modules and hasattr(sys.modules["lib"], "__file__"): return` only detects an already-imported real library. At collection nothing has imported it yet, so the mock is installed even when the library is installed.

Fix: only mock when the real package is not importable:

```python
def _real_library_installed(name):
    import importlib.machinery
    try:
        return importlib.machinery.PathFinder.find_spec(name) is not None
    except (ImportError, ValueError):
        return False
```

Use `PathFinder` rather than `importlib.util.find_spec`, which trusts a stub's `__spec__` already in `sys.modules`. Per-test fakes should use `monkeypatch.setitem(sys.modules, ...)` so they're undone.

## Tests that depended on the fake

Once the real library loads, some assertions break because the real library behaves differently, e.g. python-telegram-bot strips `"Bad Request: "` from error text and `str.capitalize()`s the rest, lowercasing URLs. Change the test input (drop the prefix) rather than weakening the assertion.

## Async teardown timing (not a leak)

A claim or in-flight entry released from a task done-callback runs via `call_soon`, which can land one loop tick after the awaited `stop()` returns. Before asserting cleanup, yield a bounded number of ticks:

```python
for _ in range(10):
    if not state:
        break
    await asyncio.sleep(0)
```

Diagnose with temporary prints in a copy (restore the file afterward) showing callback order relative to `stop()`.
