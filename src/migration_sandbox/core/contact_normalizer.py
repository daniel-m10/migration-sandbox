import re
from datetime import UTC, datetime


def normalize_agent_id(value: str) -> str:
    """Normalize an agent ID to a clean lowercase identifier.

    This helper trims surrounding whitespace, lowercases the input,
    and removes any characters other than ASCII letters, digits,
    hyphens, and underscores.

    Args:
        value: Raw agent ID string.

    Returns:
        Normalized agent ID with only lowercase letters, digits,
        hyphens, and underscores.

    Raises:
        ValueError: If the result after normalization is an empty string.
    """
    result = re.sub(r"[^a-z0-9\-_]", "", value.strip().lower())
    if not result:
        raise ValueError("agent_id cannot be empty after normalization")
    return result


def normalize_media_type(value: str) -> str:
    """Normalize a media type to its canonical uppercase value.

    Args:
        value: Raw media type string.

    Returns:
        Canonical media type value.

    Raises:
        ValueError: If the media type is not recognized.
    """
    canonical = {"voice": "VOICE", "chat": "CHAT", "email": "EMAIL"}
    normalized = canonical.get(value.strip().lower())
    if normalized is None:
        raise ValueError(f"Unknown media_type: {value!r}")
    return normalized


def parse_contact_start(value: str | int | float) -> datetime:
    """Parse contact start into a timezone-aware UTC datetime.

    Args:
        value: Contact start value as ISO 8601 string,
            ``YYYY-MM-DD HH:MM:SS`` string, or Unix timestamp.

    Returns:
        A timezone-aware datetime normalized to UTC.

    Raises:
        ValueError: If the value cannot be parsed into a valid datetime.
    """
    error_message = f"Cannot parse contact_start from: {value!r}"

    if isinstance(value, bool):
        raise ValueError(error_message)

    if isinstance(value, (int, float)):
        try:
            return datetime.fromtimestamp(value, tz=UTC)
        except (OverflowError, OSError, ValueError) as exc:
            raise ValueError(error_message) from exc

    if not isinstance(value, str):
        raise ValueError(error_message)

    normalized_value = value.strip()
    if not normalized_value:
        raise ValueError(error_message)

    iso_candidate = (
        f"{normalized_value[:-1]}+00:00"
        if normalized_value.endswith("Z")
        else normalized_value
    )

    try:
        parsed_datetime = datetime.fromisoformat(iso_candidate)
    except ValueError:
        try:
            parsed_datetime = datetime.strptime(
                normalized_value,
                "%Y-%m-%d %H:%M:%S",
            )
        except ValueError as exc:
            raise ValueError(error_message) from exc

    if parsed_datetime.tzinfo is None:
        return parsed_datetime.replace(tzinfo=UTC)
    return parsed_datetime.astimezone(UTC)
