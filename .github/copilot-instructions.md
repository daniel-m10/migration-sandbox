# Copilot Instructions — migration-sandbox

## Project context
Python migration of data-acd-automation-core (C#/.NET framework).
This repo mirrors the structure and patterns of the C# framework progressively.

## Stack
- Python 3.13, uv, pytest, ruff

## Patterns
- Type hints on all public functions
- Google-style docstrings
- Tests in tests/unit/ mirroring src/ structure
- JSON reading follows VcDataGeneration _latest.json pointer pattern

## Do NOT
- No bare except clauses
- No hardcoded paths — use pathlib.Path
- No print() in production code