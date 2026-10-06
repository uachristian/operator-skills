# Docker before/after testing (hermes-agent)

## Image

- Core deps in `pyproject.toml` are gated `python_version >= '3.14'` and `uv.lock` supports only >=3.14: a 3.11 image with `pip install -e .` installs no runtime deps (ruamel, dotenv import errors) and `uv sync` refuses the platform. Use `python:3.14-slim`.
- `dev` and `test` are dependency GROUPS, not extras (`.[dev]` silently installs no pytest).

```dockerfile
FROM python:3.14-slim
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends git >/dev/null && pip install -q --no-cache-dir uv
WORKDIR /work
ADD src.tar /work/          # git archive --format=tar -o src.tar origin/main
RUN UV_PROJECT_ENVIRONMENT=/opt/venv uv sync --locked --python /usr/local/bin/python --group dev --group test -q \
 && /opt/venv/bin/python -c "import pytest, ruamel.yaml, dotenv" \
 && git init -q && git -c user.email=t@t -c user.name=t add -A && git -c user.email=t@t -c user.name=t commit -qm base
ENV HERMES_PYTHON=/opt/venv/bin/python
```


## Runner script (mounted read-only at /p)

Export `git diff origin/main..<b>` to `/p/<name>.patch` and test paths to `/p/<name>.tests`, then per branch:

1. `git apply --include='tests/*' /p/N.patch` -> run new tests (expect FAIL).
2. reset -> run sibling dir on unpatched main (baseline).
3. `git apply /p/N.patch` -> new tests (expect PASS) -> sibling dir again.

Filter with `grep -E '^=== Summary|^FAILED|^ERROR|files where no tests'`; `tail -N` drops the summary line when many failures print. Run `docker run --network none -v $S/p:/p:ro IMG bash /p/run.sh ...` as a background terminal job for suites over a few minutes and poll it.

## Known container-only failures on unmodified main

Running as root breaks 0700/0600 permission assertions (`tests/cron/test_file_permissions.py`); some FTS runtime-rebuild tests fail in the container. Always cite them from the same-run baseline on unpatched main, not from memory.
