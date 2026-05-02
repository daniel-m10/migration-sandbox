import json
from pathlib import Path

from migration_sandbox.core.contact_dto import ContactDto


def read_latest_contacts(base_path: str, run_type: str) -> ContactDto:
    """Read the latest contact payload from VcDataGeneration output.

    Args:
        base_path: Root path of the VcDataGeneration output.
        run_type: Run type folder name, for example ``Basic/SCH``.

    Returns:
        Parsed contact data as a ``ContactDto`` instance.
    """
    latest_path = Path(base_path) / run_type / "_latest.json"
    with open(latest_path, encoding="utf-8") as f:
        return ContactDto.from_dict(json.load(f))
