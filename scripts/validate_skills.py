#!/usr/bin/env python3
"""Validate every skill under skills/<category>/<name>/SKILL.md.

Checks:
  - YAML frontmatter present and parseable (PyYAML if installed, else a
    minimal fallback parser for the flat/nested keys we require)
  - required fields: name, description, version, license, metadata.hermes.tags
  - name matches the directory name; license is MIT
  - description starts with "Use when" and is <= 160 characters
  - every relative link/path (markdown links and backticked references/,
    templates/, scripts/ paths) resolves to an existing file
  - no file in the repository is larger than 200 KB

Exit 0 when clean, 1 when any check fails.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")
MAX_BYTES = 200 * 1024
MAX_DESC = 160
LINK_RX = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
TICK_RX = re.compile(r"`((?:\.\./)*(?:references|templates|scripts|assets)/[A-Za-z0-9_./-]+)`")

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - fallback path
    yaml = None


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return None, "missing opening '---'"
    end = text.find("\n---", 4)
    if end < 0:
        return None, "missing closing '---'"
    block = text[4:end]
    if yaml is not None:
        try:
            data = yaml.safe_load(block)
        except yaml.YAMLError as exc:
            return None, f"invalid YAML: {exc}"
        if not isinstance(data, dict):
            return None, "frontmatter is not a mapping"
        return data, None
    data, stack = {}, [(-1, None)]
    stack[0] = (-1, data)
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        key, _, val = line.strip().partition(":")
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        val = val.strip()
        if val == "":
            parent[key] = {}
            stack.append((indent, parent[key]))
        else:
            parent[key] = val.strip("\"'")
    return data, None


def check_skill(skill_md, errors):
    rel = os.path.relpath(skill_md, ROOT)
    text = open(skill_md, encoding="utf-8").read()
    fm, err = parse_frontmatter(text)
    if err:
        errors.append(f"{rel}: {err}")
        return
    for field in ("name", "description", "version", "license"):
        if not fm.get(field):
            errors.append(f"{rel}: missing '{field}'")
    tags = ((fm.get("metadata") or {}).get("hermes") or {}).get("tags")
    if not tags:
        errors.append(f"{rel}: missing metadata.hermes.tags")
    dirname = os.path.basename(os.path.dirname(skill_md))
    if fm.get("name") and fm["name"] != dirname:
        errors.append(f"{rel}: name '{fm['name']}' != directory '{dirname}'")
    if fm.get("license") and str(fm["license"]) != "MIT":
        errors.append(f"{rel}: license must be MIT")
    desc = str(fm.get("description") or "")
    if desc and not desc.startswith("Use when"):
        errors.append(f"{rel}: description must start with 'Use when'")
    if len(desc) > MAX_DESC:
        errors.append(f"{rel}: description is {len(desc)} chars (max {MAX_DESC})")


def check_links(path, skill_dir, errors):
    rel = os.path.relpath(path, ROOT)
    text = open(path, encoding="utf-8", errors="replace").read()
    base = os.path.dirname(path)
    targets = set(LINK_RX.findall(text))
    for t in TICK_RX.findall(text):
        targets.add(t)
    for t in sorted(targets):
        if re.match(r"^[a-z]+:", t) or t.startswith("/") or t.startswith("~"):
            continue
        if any(ch in t for ch in "<>*{}"):
            continue
        cands = [os.path.normpath(os.path.join(base, t))]
        if skill_dir:
            cands.append(os.path.normpath(os.path.join(skill_dir, t)))
        if not any(os.path.exists(c) for c in cands):
            errors.append(f"{rel}: broken relative reference '{t}'")


def main():
    errors, count = [], 0
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d != ".git"]
        for fn in fns:
            p = os.path.join(dp, fn)
            if os.path.getsize(p) > MAX_BYTES:
                errors.append(f"{os.path.relpath(p, ROOT)}: larger than 200 KB")
    for cat in sorted(os.listdir(SKILLS)):
        cdir = os.path.join(SKILLS, cat)
        if not os.path.isdir(cdir):
            continue
        for name in sorted(os.listdir(cdir)):
            sdir = os.path.join(cdir, name)
            md = os.path.join(sdir, "SKILL.md")
            if not os.path.isfile(md):
                errors.append(f"{os.path.relpath(sdir, ROOT)}: no SKILL.md")
                continue
            count += 1
            check_skill(md, errors)
            for dp, _, fns in os.walk(sdir):
                for fn in fns:
                    if fn.endswith(".md"):
                        check_links(os.path.join(dp, fn), sdir, errors)
    for fn in ("README.md", "INDEX.md"):
        p = os.path.join(ROOT, fn)
        if os.path.exists(p):
            check_links(p, None, errors)
    for e in errors:
        print("FAIL", e)
    print(f"{count} skills checked, {len(errors)} problems")
    return 1 if errors or count == 0 else 0


if __name__ == "__main__":
    sys.exit(main())
