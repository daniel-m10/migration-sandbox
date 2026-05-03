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

The utility in `src/migration_sandbox/utils/file_reader.py` reads a `_latest.json` file from a `VCDataGeneration`-style folder structure and returns a validated `ContactDto` instance.

## Contact DTO

The module `src/migration_sandbox/core/contact_dto.py` defines `ContactDto` as the core payload model for contact events.

Fields:

- `agent_id: str`
- `contact_id: str`
- `contact_start: str`
- `master_contact_id: str`
- `media_type_name: str`

`ContactDto` includes:

- `from_dict(data: dict[str, object]) -> ContactDto` to construct a DTO from JSON data.
- `__post_init__` validations to ensure required fields are not `None` or empty strings.

## Notes

- Tests live under `tests/unit/` and mirror the `src/` structure.
- Paths should be handled with `pathlib.Path`.
- Production code should avoid `print()` and bare `except` clauses.

