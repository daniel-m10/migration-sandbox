from datetime import UTC, datetime

import pytest

from migration_sandbox.core.contact_dto import ContactDto
from migration_sandbox.core.contact_normalizer import (
    normalize_agent_id,
    normalize_contact_dto,
    normalize_media_type,
    parse_contact_start,
    validate_master_contact_id,
)


class TestNormalizeAgentId:
    def test_normalize_agent_id_when_value_has_whitespace_then_returns_lowercase(
        self,
    ) -> None:
        # Arrange
        value = "  Agent_01  "

        # Act
        result = normalize_agent_id(value)

        # Assert
        assert result == "agent_01"

    def test_normalize_agent_id_when_value_has_special_chars_then_removes_them(
        self,
    ) -> None:
        # Arrange
        value = "Agent@01!"

        # Act
        result = normalize_agent_id(value)

        # Assert
        assert result == "agent01"

    def test_normalize_agent_id_when_value_has_hyphen_underscore_then_preserves_them(
        self,
    ) -> None:
        # Arrange
        value = "agent-id_01"

        # Act
        result = normalize_agent_id(value)

        # Assert
        assert result == "agent-id_01"

    @pytest.mark.parametrize(
        "invalid_value",
        [
            "   ",  # only whitespace
            "!!!",  # only special chars
            "@#$%",  # no valid chars
        ],
    )
    def test_normalize_agent_id_when_result_is_empty_then_raises_value_error(
        self,
        invalid_value: str,
    ) -> None:
        # Arrange / Act / Assert
        with pytest.raises(
            ValueError,
            match="agent_id cannot be empty after normalization",
        ):
            normalize_agent_id(invalid_value)


class TestNormalizeMediaType:
    @pytest.mark.parametrize(
        "input_value, expected",
        [
            ("voice", "VOICE"),
            ("Voice", "VOICE"),
            ("VOICE", "VOICE"),
            ("chat", "CHAT"),
            ("Chat", "CHAT"),
            ("CHAT", "CHAT"),
            ("email", "EMAIL"),
            ("Email", "EMAIL"),
            ("EMAIL", "EMAIL"),
        ],
    )
    def test_normalize_media_type_when_value_is_known_then_returns_canonical(
        self,
        input_value: str,
        expected: str,
    ) -> None:
        # Arrange / Act
        result = normalize_media_type(input_value)

        # Assert
        assert result == expected

    @pytest.mark.parametrize(
        "invalid_value",
        [
            "sms",
            "whatsapp",
            "",
            "  ",
            "voi ce",
        ],
    )
    def test_normalize_media_type_when_value_is_unknown_then_raises_value_error(
        self,
        invalid_value: str,
    ) -> None:
        # Arrange / Act / Assert
        with pytest.raises(ValueError, match="Unknown media_type"):
            normalize_media_type(invalid_value)


class TestParseContactStart:
    def test_parse_contact_start_when_iso_with_offset_then_returns_utc_datetime(
        self,
    ) -> None:
        # Arrange
        value = "2026-05-04T10:30:45-03:00"

        # Act
        result = parse_contact_start(value)

        # Assert
        assert result == datetime(2026, 5, 4, 13, 30, 45, tzinfo=UTC)
        assert result.tzinfo is UTC

    def test_parse_contact_start_when_iso_with_z_suffix_then_returns_utc_datetime(
        self,
    ) -> None:
        # Arrange
        value = "2026-05-04T10:30:45Z"

        # Act
        result = parse_contact_start(value)

        # Assert
        assert result == datetime(2026, 5, 4, 10, 30, 45, tzinfo=UTC)
        assert result.tzinfo is UTC

    def test_parse_contact_start_when_iso_without_tz_then_returns_utc_datetime(
        self,
    ) -> None:
        # Arrange
        value = "2026-05-04T10:30:45"

        # Act
        result = parse_contact_start(value)

        # Assert
        assert result == datetime(2026, 5, 4, 10, 30, 45, tzinfo=UTC)
        assert result.tzinfo is UTC

    def test_parse_contact_start_when_space_format_then_returns_utc_datetime(
        self,
    ) -> None:
        # Arrange
        value = "2026-05-04 10:30:45"

        # Act
        result = parse_contact_start(value)

        # Assert
        assert result == datetime(2026, 5, 4, 10, 30, 45, tzinfo=UTC)
        assert result.tzinfo is UTC

    def test_parse_contact_start_when_unix_int_then_returns_utc_datetime(
        self,
    ) -> None:
        # Arrange
        value = 1_714_818_645

        # Act
        result = parse_contact_start(value)

        # Assert
        assert result == datetime(2024, 5, 4, 10, 30, 45, tzinfo=UTC)
        assert result.tzinfo is UTC

    def test_parse_contact_start_when_unix_float_then_returns_utc_datetime(
        self,
    ) -> None:
        # Arrange
        value = 1_714_818_645.5

        # Act
        result = parse_contact_start(value)

        # Assert
        assert result == datetime(2024, 5, 4, 10, 30, 45, 500000, tzinfo=UTC)
        assert result.tzinfo is UTC

    @pytest.mark.parametrize(
        "invalid_value",
        [
            "",
            "   ",
            "not-a-date",
            "2026-02-30 10:30:45",
            None,
            True,
        ],
    )
    def test_parse_contact_start_when_value_is_invalid_then_raises_value_error(
        self,
        invalid_value: object,
    ) -> None:
        # Arrange
        expected_message = f"Cannot parse contact_start from: {invalid_value!r}"

        # Act / Assert
        with pytest.raises(ValueError) as exc_info:
            parse_contact_start(invalid_value)  # type: ignore[arg-type]

        assert str(exc_info.value) == expected_message


class TestValidateMasterContactId:
    def test_validate_master_contact_id_when_value_is_canonical_uuid_then_returns_value(
        self,
    ) -> None:
        # Arrange
        value = "123e4567-e89b-12d3-a456-426614174000"

        # Act
        result = validate_master_contact_id(value)

        # Assert
        assert result == value

    @pytest.mark.parametrize(
        "invalid_value",
        [
            "",
            "123e4567e89b12d3a456426614174000",
            "123e4567-e89b-12d3-a456-42661417400",
            "123e4567-e89b-12d3-a456-4266141740000",
            "123e4567-e89b-12d3-a456-42661417400g",
            " 123e4567-e89b-12d3-a456-426614174000 ",
        ],
    )
    def test_validate_master_contact_id_when_value_is_invalid_then_raises_value_error(
        self,
        invalid_value: str,
    ) -> None:
        # Arrange
        expected_message = (
            f"master_contact_id must be UUID format, got: {invalid_value!r}"
        )

        # Act / Assert
        with pytest.raises(ValueError) as exc_info:
            validate_master_contact_id(invalid_value)

        assert str(exc_info.value) == expected_message


class TestNormalizeContactDto:
    def test_normalize_contact_dto_when_valid_then_returns_new_dto(
        self,
    ) -> None:
        # Arrange
        dto = ContactDto(
            agent_id="  Agent-01!  ",
            contact_id="contact-123",
            contact_start="2026-05-04T10:30:45-03:00",
            master_contact_id="123e4567-e89b-12d3-a456-426614174000",
            media_type_name="Voice",
        )

        # Act
        result = normalize_contact_dto(dto)

        # Assert
        assert result is not dto
        assert result == ContactDto(
            agent_id="agent-01",
            contact_id="contact-123",
            contact_start="2026-05-04T13:30:45+00:00",
            master_contact_id="123e4567-e89b-12d3-a456-426614174000",
            media_type_name="VOICE",
        )
        assert dto == ContactDto(
            agent_id="  Agent-01!  ",
            contact_id="contact-123",
            contact_start="2026-05-04T10:30:45-03:00",
            master_contact_id="123e4567-e89b-12d3-a456-426614174000",
            media_type_name="Voice",
        )

    @pytest.mark.parametrize(
        ("field_name", "dto"),
        [
            (
                "agent_id",
                ContactDto(
                    agent_id="!!!",
                    contact_id="contact-123",
                    contact_start="2026-05-04T10:30:45Z",
                    master_contact_id="123e4567-e89b-12d3-a456-426614174000",
                    media_type_name="VOICE",
                ),
            ),
            (
                "media_type_name",
                ContactDto(
                    agent_id="agent_01",
                    contact_id="contact-123",
                    contact_start="2026-05-04T10:30:45Z",
                    master_contact_id="123e4567-e89b-12d3-a456-426614174000",
                    media_type_name="sms",
                ),
            ),
            (
                "contact_start",
                ContactDto(
                    agent_id="agent_01",
                    contact_id="contact-123",
                    contact_start="not-a-date",
                    master_contact_id="123e4567-e89b-12d3-a456-426614174000",
                    media_type_name="VOICE",
                ),
            ),
            (
                "master_contact_id",
                ContactDto(
                    agent_id="agent_01",
                    contact_id="contact-123",
                    contact_start="2026-05-04T10:30:45Z",
                    master_contact_id="invalid-uuid",
                    media_type_name="VOICE",
                ),
            ),
        ],
    )
    def test_normalize_contact_dto_when_invalid_then_raises_wrapped_error(
        self,
        field_name: str,
        dto: ContactDto,
    ) -> None:
        # Act / Assert
        with pytest.raises(
            ValueError,
            match=rf"^Normalization failed for field '{field_name}':",
        ):
            normalize_contact_dto(dto)


