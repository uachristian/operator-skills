# sys.modules mock leaks and related timing traps

## Conftest that stubs an optional dependency at collection time

Shape: `conftest.py` runs `_ensure_<pkg>_mock()` at import. It does `sys.modules["pkg"] = MagicMock()` (plus submodules) and never restores it.

Broken guard:
```python
if "pkg" in sys.modules and hasattr(sys.modules["pkg"], "__file__"):
    return  # "real library installed"
```
This checks whether the package is *already imported*, not whether it is *installed*. At collection time nothing has imported it yet, so the stub is installed even when the real library exists. Every later file in the same process that does `from pkg import X` binds to MagicMocks. Typical symptoms: attributes come back as `<MagicMock name='mock.X().attr'>`, "object can't be awaited", and `StopIteration` from a mocked async generator.

Fix:
```python
def _real_library_installed(name):
    import importlib.machinery
    try:
        return importlib.machinery.PathFinder.find_spec(name) is not None
    except (ImportError, ValueError):
        return False

if _real_library_installed("pkg"):
    return
```
Use `PathFinder.find_spec`, not `importlib.util.find_spec`. The latter returns an existing stub's `__spec__` (or raises on a MagicMock), so it can't tell a stub from the real package. Grep for other files that plant the same stub (`sys.modules["pkg"]`, `sys.modules.setdefault("pkg"`, `_ensure_<pkg>_mock`). Ones that use `setdefault` or are guarded by an already-present real module are harmless once the conftest stops planting the stub.

## Fallout: tests that relied on stub semantics

Once the real library loads, some assertions break because the stub skipped real behavior. For example, python-telegram-bot `TelegramError.__init__` strips `Error: ` / `[Error]: ` / `Bad Request: ` and then `str.capitalize()`s the rest, which lowercases URLs and endpoints asserted later. Fix the test input (for instance, drop the prefix) so the test checks the intended invariant against real semantics.

## asyncio done-callback timing

State released inside `task.add_done_callback(...)` runs via `loop.call_soon`. It can still be pending when `await app.stop()` / `await asyncio.gather(...)` returns, so the test intermittently or consistently sees the in-flight entry. Before asserting, yield a bounded number of ticks instead of changing production code:
```python
for _ in range(10):
    if not state:
        break
    await asyncio.sleep(0)
```
To confirm the cause, add temporary prints in the callback and after `stop()`. If the print order is "stopped" then "finished", this is the mechanism.
