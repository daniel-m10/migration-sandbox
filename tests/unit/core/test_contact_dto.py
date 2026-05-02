import pytest

from migration_sandbox.core.contact_dto import ContactDto


def build_contact_payload(**overrides: object) -> dict[str, object]:
    """Build a valid contact payload for tests.

    Args:
        **overrides: Field values that should override the defaults.

    Returns:
        A JSON-like contact payload.
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


def test_from_dict_returns_contact_dto() -> None:
    payload = build_contact_payload()

    result = ContactDto.from_dict(payload)

    assert result == ContactDto(
        agent_id="agent-01",
        contact_id="contact-01",
        contact_start="2026-05-02T12:30:00Z",
        master_contact_id="master-01",
        media_type_name="Voice",
    )


def test_from_dict_raises_value_error_when_required_value_is_none() -> None:
    payload = build_contact_payload(contact_id=None)

    with pytest.raises(ValueError, match="contact_id"):
        ContactDto.from_dict(payload)


def test_from_dict_raises_type_error_when_required_value_is_not_a_string() -> None:
    payload = build_contact_payload(contact_start=123)

    with pytest.raises(TypeError, match="contact_start"):
        ContactDto.from_dict(payload)
