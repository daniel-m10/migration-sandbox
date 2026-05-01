# migration-sandbox

Python migration sandbox for patterns and components inspired by `data-acd-automation-core`.

This repository is being built incrementally to mirror the structure and behavior of the original C#/.NET framework in Python.

## Requirements

- Python 3.13+
- `uv`

## Project structure

```text
src/
  migration_sandbox/
    core/
    kinesis/
    utils/
tests/
  unit/
```

## Getting started

Clone the repository and install the project dependencies:

```powershell
uv sync
```

## Running tests

```powershell
uv run pytest
```

## Running lint checks

```powershell
uv run ruff check .
```

## Current example

The utility in `src/migration_sandbox/utils/file_reader.py` reads a `_latest.json` file from a `VCDataGeneration`-style folder structure and returns the parsed JSON payload.

## Notes

- Tests live under `tests/unit/` and mirror the `src/` structure.
- Paths should be handled with `pathlib.Path`.
- Production code should avoid `print()` and bare `except` clauses.

