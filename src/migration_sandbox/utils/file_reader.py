from pathlib import Path
import json


def read_latest_contacts(base_path: str, run_type: str) -> dict:
    """Reads the _latest.json pointer from VCDataGeneration output.
    Args:
        base_path (str): Root path of the VCDataGeneration output.
        run_type: Run type folder name (e.g. 'Basic/SCH').

    Returns:
        Parsed contact data as dictionary.
    """
    latest_path = Path(base_path) / run_type / "_latest.json"
    with open(latest_path, encoding="utf-8") as f:
        return json.load(f)