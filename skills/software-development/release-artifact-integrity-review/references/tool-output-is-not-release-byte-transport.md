# Tool output is not a release-byte transport

Use this when materializing exact source/runtime files from Git objects, predecessor files, archives, or generated artifacts.

## Rule

Never reconstruct release files by taking `git show <commit>:<path>`, a file-reader response, terminal stdout, or any other structured/display-oriented tool result and writing its returned text field back to disk. Tool transports may truncate a long line or total output, add line-number prefixes or decoration, redact credential-shaped source fragments into literal placeholders, normalize trailing newlines/encoding, suppress repeated content, or append presentation artifacts while the reconstructed files still look plausible. A manifest generated over those altered bytes is only self-consistent; it is not source or predecessor authority.

This applies even when the source is plain text and the derived file merely changes a version suffix. Use byte-preserving filesystem/Git operations for unchanged content and targeted patches for intentional edits; do not round-trip source bytes through the model-visible response channel.

## Binary-safe materialization

Prefer one of these:

1. `git archive <commit> <allowlisted-paths> | tar -x -C <private-temp-root>` with `pipefail` and archive safety checks; or
2. direct Git object streaming whose raw bytes never pass through a display-oriented tool-output field.

Then prove every materialized file before manifest generation:

```text
git hash-object <materialized-file>
==
git rev-parse <commit>:<path>
```

For a complete source archive, force-stage the reconstructed tree and require `git write-tree` to equal the approved tree.

## Installed runtime readback

After copying the reviewed bundle into its fixed runtime path:

- compare each installed file's `git hash-object` to the exact commit blob;
- verify the external manifest digest independently;
- run the credential-free check/preflight;
- only then load profile credentials or start the worker.

If installed blob parity fails, preserve the rejected copy as evidence, replace it atomically from the binary-safe extraction, and invalidate any runtime result produced by the nonexact copy.
