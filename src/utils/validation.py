"""Input validation helpers."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from .constants import MAX_PASSENGERS_PER_BOOKING, MIN_PASSENGERS_PER_BOOKING

ALLOWED_CLASS_TYPES = {"SL", "AC2", "AC3", "1A", "2A", "3A", "GN"}
ALLOWED_QUOTAS = {"GN", "TQ", "PT", "RL"}
ALLOWED_GENDERS = {"M", "F", "T"}


def parse_passengers(passengers_json: str = "", passengers_file: str = "") -> List[Dict[str, str]]:
    """Parse passengers from JSON string or file."""
    if passengers_json:
        parsed = json.loads(passengers_json)
    elif passengers_file:
        parsed = json.loads(Path(passengers_file).read_text(encoding="utf-8"))
    else:
        parsed = [
            {
                "name": "Test Passenger",
                "age": "30",
                "gender": "M",
                "berth_preference": "LB",
            }
        ]

    if not isinstance(parsed, list):
        raise ValueError("Passengers payload must be a JSON list")
    return normalize_passengers(parsed)


def normalize_passengers(passengers: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Validate and normalize passenger records."""
    if not (MIN_PASSENGERS_PER_BOOKING <= len(passengers) <= MAX_PASSENGERS_PER_BOOKING):
        raise ValueError(
            f"Passengers count must be between {MIN_PASSENGERS_PER_BOOKING} and "
            f"{MAX_PASSENGERS_PER_BOOKING}"
        )

    normalized: List[Dict[str, str]] = []
    for index, passenger in enumerate(passengers):
        name = str(passenger.get("name", "")).strip()
        age = str(passenger.get("age", "")).strip()
        gender = str(passenger.get("gender", "M")).strip().upper()
        berth = str(passenger.get("berth_preference", "")).strip()

        if not name:
            raise ValueError(f"Passenger at index {index} has empty name")
        if not age.isdigit():
            raise ValueError(f"Passenger at index {index} has invalid age")
        age_int = int(age)
        if age_int < 0 or age_int > 120:
            raise ValueError(f"Passenger at index {index} age out of range")
        if gender not in ALLOWED_GENDERS:
            raise ValueError(f"Passenger at index {index} has invalid gender")

        normalized.append(
            {
                "name": name,
                "age": str(age_int),
                "gender": gender,
                "berth_preference": berth,
            }
        )
    return normalized


def validate_booking_config(config: Dict[str, Any]) -> None:
    """Validate required booking configuration fields."""
    required_fields = [
        "username",
        "password",
        "captcha_api_key",
        "from_station",
        "to_station",
        "travel_date",
    ]
    missing = [field for field in required_fields if not str(config.get(field, "")).strip()]
    if missing:
        raise ValueError(f"Missing required configuration: {', '.join(missing)}")

    from_station = str(config["from_station"]).strip().upper()
    to_station = str(config["to_station"]).strip().upper()
    if len(from_station) < 2 or len(to_station) < 2:
        raise ValueError("Station codes appear invalid")

    if from_station == to_station:
        raise ValueError("From and To stations cannot be the same")

    travel_date = str(config["travel_date"]).strip()
    try:
        parsed_date = datetime.strptime(travel_date, "%d-%m-%Y")
    except ValueError as exc:
        raise ValueError("travel_date must be in DD-MM-YYYY format") from exc

    if parsed_date.date() < datetime.now().date():
        raise ValueError("travel_date cannot be in the past")

    class_type = str(config.get("class_type", "SL")).upper()
    quota = str(config.get("quota", "GN")).upper()
    if class_type not in ALLOWED_CLASS_TYPES:
        raise ValueError(f"Unsupported class_type: {class_type}")
    if quota not in ALLOWED_QUOTAS:
        raise ValueError(f"Unsupported quota: {quota}")
