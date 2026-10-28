
import json
from pathlib import Path


CACHE_FILE = Path(__file__).parent / "rate_cache.json"


def load_json():
    """Load cached exchange rates from the JSON file."""
    if not CACHE_FILE.exists():
        return {}

    try:
        with CACHE_FILE.open("r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        if isinstance(data, dict):
            return data

        return {}

    except (json.JSONDecodeError, OSError):
        return {}


def save_to_json(data):
    """Save exchange-rate data to the JSON file."""
    try:
        with CACHE_FILE.open("w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)

    except OSError as e:
        raise RuntimeError(
            "Unable to save exchange-rate cache."
        ) from e
