import json
from pathlib import Path

import pytest

from migration_sandbox.core.contact_dto import ContactDto
from migration_sandbox.utils.file_reader import read_latest_contacts


def build_contact_payload(**overrides: object) -> dict[str, object]:
    """Build a valid contact payload for tests.

    Args:
        **overrides: Field values that should override the defaults.

    Returns:
        A JSON-serializable contact payload.
    """
    payload: dict[str, object] = {
        "agent_id": "agent-01",
        "contact_id": "contact-01",
        "contact_start": "2026-05-02T12:30:00Z",
        "master_contact_id": "master-01",
        "media_type_name": "Voice",
    }
    payload.update(overrides)
    return payload


def test_read_latest_contacts_returns_contact_dto(tmp_path: Path) -> None:
    run_dir = tmp_path / "Basic"
    run_dir.mkdir(parents=True)
    data = build_contact_payload()
    (run_dir / "_latest.json").write_text(json.dumps(data), encoding="utf-8")

    result = read_latest_contacts(str(tmp_path), "Basic")

    assert result == ContactDto.from_dict(data)


def test_read_latest_contacts_supports_nested_run_type(tmp_path: Path) -> None:
    run_dir = tmp_path / "Basic" / "SCH"
    run_dir.mkdir(parents=True)
    data = build_contact_payload(contact_id="nested-contact")
    (run_dir / "_latest.json").write_text(json.dumps(data), encoding="utf-8")

    result = read_latest_contacts(str(tmp_path), "Basic/SCH")

    assert result.contact_id == "nested-contact"
    assert result.master_contact_id == "master-01"


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
    data = build_contact_payload(
        agent_id="José",
        media_type_name="Voz 📁",
    )
    (run_dir / "_latest.json").write_text(
        json.dumps(data, ensure_ascii=False),
        encoding="utf-8",
    )

    result = read_latest_contacts(str(tmp_path), "Basic")

    assert result.agent_id == "José"
    assert result.media_type_name == "Voz 📁"


def test_read_latest_contacts_supports_empty_run_type(tmp_path: Path) -> None:
    data = build_contact_payload(contact_id="root-contact")
    (tmp_path / "_latest.json").write_text(json.dumps(data), encoding="utf-8")

    result = read_latest_contacts(str(tmp_path), "")

    assert result.contact_id == "root-contact"


def test_read_latest_contacts_raises_type_error_when_json_is_not_an_object(
    tmp_path: Path,
) -> None:
    run_dir = tmp_path / "Basic"
    run_dir.mkdir(parents=True)
    data = [1, 2, 3]
    (run_dir / "_latest.json").write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(TypeError, match="Contact payload must be a JSON object"):
        read_latest_contacts(str(tmp_path), "Basic")


def test_read_latest_contacts_raises_value_error_when_required_field_is_missing(
    tmp_path: Path,
) -> None:
    run_dir = tmp_path / "Basic"
    run_dir.mkdir(parents=True)
    data = build_contact_payload()
    data.pop("master_contact_id")
    (run_dir / "_latest.json").write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="master_contact_id"):
        read_latest_contacts(str(tmp_path), "Basic")


def test_read_latest_contacts_raises_value_error_when_required_field_is_empty(
    tmp_path: Path,
) -> None:
    run_dir = tmp_path / "Basic"
    run_dir.mkdir(parents=True)
    data = build_contact_payload(media_type_name="")
    (run_dir / "_latest.json").write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="media_type_name"):
        read_latest_contacts(str(tmp_path), "Basic")

