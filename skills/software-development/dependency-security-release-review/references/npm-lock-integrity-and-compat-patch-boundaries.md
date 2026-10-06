# NPM Lock Integrity and Compatibility-Patch Boundaries

## Whole-lock integrity regression probe

During a security remediation, compare every registry-backed non-link entry in the parent and candidate `package-lock.json`, not just changed direct dependencies. Require nonempty `integrity`; normally retain `resolved` too.

```python
import json
from pathlib import Path

lock = json.loads(Path("package-lock.json").read_text())
rows = [
    (path, entry)
    for path, entry in lock["packages"].items()
    if path
    and "node_modules/" in path
    and entry.get("version")
    and not entry.get("link")
    and not entry.get("inBundle")
]
missing = [
    path
    for path, entry in rows
    if not str(entry.get("resolved", "")).startswith("https://")
    or not entry.get("integrity")
]
print(f"registry_entries={len(rows)} missing_identity={len(missing)}")
assert not missing, missing[:20]
```

`inBundle` entries are embedded inside their parent's integrity-checked tarball and intentionally may lack independent `resolved`/`integrity` metadata. Excluding only workspace `link` entries creates false HOLD findings for bundled native/WASM dependencies.

Run equivalent parsing against `git show <parent>:package-lock.json`. A candidate can retain hashes on newly changed headline packages while stripping them from most of the pre-existing graph. Version-floor tests remain green because they commonly inspect only `entry["version"]`.

A broad parent-to-candidate shift from full hash coverage to widespread missing hashes is a **HIGH / HOLD** finding in a dependency-security release: clean installs are no longer byte-bound by the reviewed lockfile.

Check every independent lockfile. A complete documentation-site lock does not repair an incomplete workspace-root lock.

## Safe lock regeneration after metadata loss

When metadata loss is widespread, regenerate from a clean lock input with the repository's supported npm major rather than asking a newer npm to normalize the already-damaged lock in place. Then:

1. run the canonical clean install and lifecycle compatibility probe;
2. require every non-link, non-`inBundle` registry entry to have HTTPS `resolved` plus `integrity`;
3. compare package-path/version maps before and after regeneration, because a fresh solve can change hoisting, optional-platform packages, or versions allowed by ranges;
4. rerun audits, focused lock guards, and every build/test lane affected by the fresh resolution;
5. commit a maintained whole-lock identity regression test, not only direct-package version floors.

Do not hand-copy integrity values between unrelated paths. Bundled entries inherit the reviewed parent tarball identity; ordinary registry entries need their own registry metadata.

## Compatibility patch boundary

A root lifecycle script patches only installs that execute that root's lifecycle. A separately installed website, sidecar, example, or nested application does not inherit the patch unless it participates in the same workspace lifecycle.

For forced transitive major-version overrides:

1. Enumerate every package/lock root resolving the override.
2. Identify legacy consumers and their expected export shape/API.
3. Map each supported install command to the lifecycle script that applies the patch.
4. Prove each root gets the patch or resolves a natively compatible graph.
5. Exercise a branch-triggering positive control; module load alone may not call the incompatible export.

Representative failure class: a named-export-only CommonJS dependency is globally forced over a legacy consumer that directly calls `require(...)`, while the compatibility shim runs only at repository root. A default path without braces or special syntax may appear healthy, so trigger the exact expansion branch before setting severity.

## Additional exact-tip checks

- Verify current config does not intentionally enable lock metadata omission and no repository config declares it.
- Compare manifest/lock root metadata separately from artifact-integrity coverage; one can pass while the other fails.
- Re-hash critical manifests, locks, patch scripts, and tests against the immutable commit before verdict.
- Keep environment absence separate: if a compatible interpreter lacks pytest, run available structural/lock gates and disclose that the maintained suite was unavailable rather than calling it a product failure.
