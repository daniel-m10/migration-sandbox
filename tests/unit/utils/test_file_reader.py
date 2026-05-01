import json
from pathlib import Path

import pytest

from migration_sandbox.utils.file_reader import read_latest_contacts


def test_read_latest_contacts_returns_expected_dict(tmp_path: Path) -> None:
    run_dir = tmp_path / "Basic"
    run_dir.mkdir(parents=True)
    data = {"ContactId": "abc123", "AgentId": "agent01"}
    (run_dir / "_latest.json").write_text(json.dumps(data), encoding="utf-8")

    result = read_latest_contacts(str(tmp_path), "Basic")

    assert result == data


def test_read_latest_contacts_supports_nested_run_type(tmp_path: Path) -> None:
    run_dir = tmp_path / "Basic" / "SCH"
    run_dir.mkdir(parents=True)
    data = {"ContactId": "abc123", "AgentId": "agent01"}
    (run_dir / "_latest.json").write_text(json.dumps(data), encoding="utf-8")

    result = read_latest_contacts(str(tmp_path), "Basic/SCH")

    assert result == data


def test_read_latest_contacts_raises_file_not_found_when_latest_missing(
    tmp_path: Path,
) -> None:
    with pytest.raises(FileNotFoundError):
        read_latest_contacts(str(tmp_path), "Basic/SCH")


def test_read_latest_contacts_raises_json_decode_error_for_invalid_json(
    tmp_path: Path,
) -> None:
    run_dir = tmp_path / "Basic" / "SCH"
    run_dir.mkdir(parents=True)
    (run_dir / "_latest.json").write_text('{"contacts": [}', encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        read_latest_contacts(str(tmp_path), "Basic/SCH")


def test_read_latest_contacts_raises_json_decode_error_for_empty_file(
    tmp_path: Path,
) -> None:
    run_dir = tmp_path / "Basic"
    run_dir.mkdir(parents=True)
    (run_dir / "_latest.json").write_text("", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        read_latest_contacts(str(tmp_path), "Basic")


def test_read_latest_contacts_reads_utf8_content(tmp_path: Path) -> None:
    run_dir = tmp_path / "Basic"
    run_dir.mkdir(parents=True)
    data = {"name": "José", "city": "Bogotá", "emoji": "📁"}
    (run_dir / "_latest.json").write_text(
        json.dumps(data, ensure_ascii=False),
        encoding="utf-8",
    )

    result = read_latest_contacts(str(tmp_path), "Basic")

    assert result == data


def test_read_latest_contacts_supports_empty_run_type(tmp_path: Path) -> None:
    data = {"ContactId": "root-contact"}
    (tmp_path / "_latest.json").write_text(json.dumps(data), encoding="utf-8")

    result = read_latest_contacts(str(tmp_path), "")

    assert result == data


def test_read_latest_contacts_returns_list_when_json_is_not_an_object(
    tmp_path: Path,
) -> None:
    run_dir = tmp_path / "Basic"
    run_dir.mkdir(parents=True)
    data = [1, 2, 3]
    (run_dir / "_latest.json").write_text(json.dumps(data), encoding="utf-8")

    result = read_latest_contacts(str(tmp_path), "Basic")

    assert result == data

