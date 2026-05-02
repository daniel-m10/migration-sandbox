from dataclasses import dataclass
from typing import cast


@dataclass(slots=True)
class ContactDto:
    """Represents a contact payload produced by VcDataGeneration.

    Attributes:
        agent_id: Identifier of the agent assigned to the contact.
        contact_id: Identifier of the contact.
        contact_start: Contact start timestamp as provided by the JSON payload.
        master_contact_id: Identifier linking related contacts together.
        media_type_name: Media type name associated with the contact.
    """

    agent_id: str
    contact_id: str
    contact_start: str
    master_contact_id: str
    media_type_name: str

    def __post_init__(self) -> None:
        """Validate required contact fields after initialization.

        Raises:
            TypeError: If any required field is not a string.
            ValueError: If any required field is None or an empty string.
        """
        required_fields = {
            "agent_id": self.agent_id,
            "contact_id": self.contact_id,
            "contact_start": self.contact_start,
            "master_contact_id": self.master_contact_id,
            "media_type_name": self.media_type_name,
        }

        for field_name, value in required_fields.items():
            if value is None:
                raise ValueError(f"{field_name} is required and cannot be None.")
            if not isinstance(value, str):
                raise TypeError(f"{field_name} must be a string.")
            if value == "":
                raise ValueError(
                    f"{field_name} is required and cannot be an empty string."
                )

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "ContactDto":
        """Build a contact DTO from a JSON dictionary.

        Args:
            data: Parsed JSON dictionary containing the contact fields.

        Returns:
            A validated contact DTO.

        Raises:
            TypeError: If ``data`` is not a dictionary.
            ValueError: If any required field is missing, None, or an empty string.
        """
        if not isinstance(data, dict):
            raise TypeError("Contact payload must be a JSON object.")

        return cls(
            agent_id=cast(str, data.get("agent_id")),
            contact_id=cast(str, data.get("contact_id")),
            contact_start=cast(str, data.get("contact_start")),
            master_contact_id=cast(str, data.get("master_contact_id")),
            media_type_name=cast(str, data.get("media_type_name")),
        )
