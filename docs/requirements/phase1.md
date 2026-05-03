# Phase 1 Requirements — Foundation

## Project context

Library: migration-sandbox
Purpose: Process, validate and report on ACD contact events.
Progressively mirrors C#/.NET framework logic in Python.

Existing modules:
- src/migration_sandbox/utils/file_reader.py
- src/migration_sandbox/core/contact_dto.py
- tests/unit/ (8 tests passing)

---

## Group 1 — contact_normalizer

Module: src/migration_sandbox/core/contact_normalizer.py
Tests: tests/unit/core/test_contact_normalizer.py

### US-01: normalize_agent_id(value: str) -> str
- Strip leading and trailing whitespace
- Convert to lowercase
- Remove all characters except letters, digits, hyphens and underscores
- If result is empty string -> raise ValueError("agent_id cannot be empty after normalization")

### US-02: normalize_media_type(value: str) -> str
- Accept case-insensitive variants and map to canonical uppercase:
  "voice", "Voice", "VOICE" -> "VOICE"
  "chat", "Chat", "CHAT" -> "CHAT"
  "email", "Email", "EMAIL" -> "EMAIL"
- Unknown value -> raise ValueError(f"Unknown media_type: {value!r}")

### US-03: parse_contact_start(value: str | int | float) -> datetime
- Accept formats: ISO 8601, "YYYY-MM-DD HH:MM:SS", Unix timestamp (int/float)
- Always return timezone-aware datetime in UTC
- Invalid input -> raise ValueError(f"Cannot parse contact_start from: {value!r}")

### US-04: validate_master_contact_id(value: str) -> str
- Must be exactly 36 characters (UUID format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
- Returns value unchanged if valid
- Invalid -> raise ValueError(f"master_contact_id must be UUID format, got: {value!r}")

### US-05: normalize_contact_dto(dto: ContactDto) -> ContactDto
- Apply US-01 through US-04 to a ContactDto instance
- Return new normalized ContactDto (do not mutate input)
- On failure propagate ValueError with field context:
  raise ValueError(f"Normalization failed for field '{field_name}': {original_error}")

### Test requirements
- Happy path for each normalization function
- At least 3 invalid input cases per function using pytest.mark.parametrize
- Integration test: normalize_contact_dto with valid and invalid DTO
- All tests follow AAA pattern

---

## Group 2 — AI Tools Configuration

### Task A: Create CLAUDE.md in repo root
Content must include:
- Project description and purpose
- Stack (Python 3.13, uv, pytest, ruff, PyCharm)
- Coding conventions (type hints, Google docstrings, AAA tests)
- At least 2 custom slash commands:
  /analyze-coverage: suggest missing tests for a given module
  /review-module: check for SOLID violations and type hint coverage
- When to use Claude Code vs Copilot (based on personal observations)

### Task B: Update .github/copilot-instructions.md to v2
- Add conventions discovered from implementing contact_dto and contact_normalizer
- Add naming convention for tests: test_{method}_{condition}_{expected_result}
- Add preference for pytest.mark.parametrize for multiple invalid input cases
- Add Google docstrings as mandatory for all public functions
- Verify Copilot respects new rules by generating a test with the updated file

### Task C: Review ChatGPT_Prompt_Engineering_for_Developers notes
- Identify 3 techniques not yet applied consistently
- Create one reusable template per technique in ai-test-templates repo
- Each template must include: name, when to use, prompt, example output

---

## Group 3 — contact_validator

Modules:
- src/migration_sandbox/core/validation_result.py
- src/migration_sandbox/core/contact_validator.py
Tests: tests/unit/core/test_contact_validator.py

### US-06: ValidationError dataclass
Fields:
- field: str (name of the field that failed)
- rule: str (name of the rule that was violated)
- message: str (human-readable explanation)

### US-07: ValidationResult dataclass
Fields:
- is_valid: bool
- errors: list[ValidationError]
- validated_at: datetime (UTC, set at creation time)

Methods:
- add_error(field: str, rule: str, message: str) -> None
- finalize() -> ValidationResult (sets is_valid based on errors list)

### US-08: Business validation rules
Function: _run_validation_rules(dto: ContactDto) -> list[ValidationError]

Rules to implement (each as a separate private function):
- _check_contact_id_not_master: contact_id must not equal master_contact_id
- _check_contact_start_not_future: contact_start must be <= datetime.now(UTC)
- _check_agent_id_length: agent_id must be between 3 and 50 characters
- _check_media_type_valid: media_type_name must be one of [VOICE, CHAT, EMAIL]

### US-09: validate_contact(dto: ContactDto) -> ValidationResult
- Does NOT raise exceptions
- Runs all rules from US-08
- Returns ValidationResult with all errors found (not just the first)
- If no errors: is_valid = True, errors = []

### US-10: ContactValidationReport
Class that processes a batch of contact DTOs.

Constructor: __init__(dtos: list[ContactDto])

Properties:
- total: int
- valid_count: int
- invalid_count: int
- errors_by_field: dict[str, int] (field name -> count of errors for that field)

Methods:
- to_markdown() -> str
  Format:
  ## Contact Validation Report
  Generated: {validated_at}
  Total: {total} | Valid: {valid_count} | Invalid: {invalid_count}
  
  ### Errors by field
  | Field | Count |
  |-------|-------|
  | ...   | ...   |

### Test requirements
- Unit tests for each validation rule (valid and invalid cases)
- Test that validate_contact returns ALL errors, not just first
- Integration test: ContactValidationReport with mixed valid/invalid DTOs
- Test to_markdown() output format

### Claude Code objective
Implement US-09 and US-10 using Claude Code (not Copilot).
Document observations in notes/claude-code-vs-copilot.md:
- What Claude Code did better
- What Copilot does better
- Recommended use case for each tool

---

## Group 4 — Legacy Code Analysis

Repo to analyze: https://github.com/realpython/reader
Clone to: analysis/reader-legacy/ (do NOT add to migration-sandbox src)

### US-11: Entry point analysis
File: analysis/01_entry_point.md
Content:
- Where execution starts (file and function)
- Main execution flow (step by step in plain language)
- External dependencies identified at entry point

### US-12: Dependency map
File: analysis/02_dependency_map.md
Content:
- List of all modules with one-line description each
- Dependency table: which module imports which
- Identify circular dependencies if any

### US-13: Code smells inventory
File: analysis/03_code_smells.md
Content:
- Functions longer than 20 lines (list with file, function, line count)
- Missing type hints (count and percentage)
- Missing tests (which modules have no test coverage)
- Mixed responsibilities (describe specific cases)
- Other smells found

### US-14: Refactoring plan
File: analysis/04_refactoring_plan.md
Content:
- Top 5 improvements prioritized by impact
- For each: description, effort estimate (S/M/L), benefit
- Do NOT implement — document only

### US-15: Generic prompt templates for legacy analysis
File: (in ai-test-templates repo) prompt-templates/legacy-analysis-templates.md
Requirements:
- Minimum 4 templates
- Each template must work for ANY Python legacy project, not just reader
- Each template must specify: name, goal, prompt, which tool to use (Copilot/Claude Code)
- Include a template for each: entry point analysis, dependency mapping,
  code smell detection, refactoring suggestions

---

## Group 5 — Phase 1 Checkpoint

Evidence to present in the main chat (Plan para incrementar metricas de IA):

1. GitHub link to migration-sandbox with all 4 modules complete
2. pytest --cov output showing coverage per module
3. GitHub link to ai-test-templates with 10+ templates documented
4. Link to notes/claude-code-vs-copilot.md
5. Link to analysis/ folder with all 4 analysis documents
6. Track A metrics estimation (Premium Requests, LOC Added, Efficiency)
7. Reflection (5-10 lines): what changed in your way of working with AI
   between week 1 and week 4?

### Pass criteria
- All 4 modules exist with tests passing
- Coverage >= 80% on each module
- ai-test-templates has >= 10 templates
- claude-code-vs-copilot.md exists with real observations
- Legacy analysis has all 4 documents
- Track A shows visible improvement vs baseline

