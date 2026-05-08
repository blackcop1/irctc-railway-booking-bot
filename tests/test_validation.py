"""Tests for input validation helpers."""

import json
from datetime import datetime, timedelta

import pytest

from src.utils.validation import parse_passengers, validate_booking_config


def test_parse_passengers_from_json():
    payload = json.dumps(
        [
            {
                "name": "Alice",
                "age": 29,
                "gender": "F",
                "berth_preference": "LB",
            },
            {"name": "Bob", "age": "31", "gender": "M"},
        ]
    )

    passengers = parse_passengers(passengers_json=payload)

    assert len(passengers) == 2
    assert passengers[0]["name"] == "Alice"
    assert passengers[0]["age"] == "29"
    assert passengers[1]["gender"] == "M"


def test_parse_passengers_rejects_bad_age():
    payload = json.dumps([{"name": "Alice", "age": "abc", "gender": "F"}])

    with pytest.raises(ValueError):
        parse_passengers(passengers_json=payload)


def test_validate_booking_config_accepts_valid_config():
    future_date = (datetime.now() + timedelta(days=30)).strftime("%d-%m-%Y")
    config = {
        "username": "demo_user",
        "password": "demo_password",
        "captcha_api_key": "demo_key",
        "from_station": "NDLS",
        "to_station": "MMCT",
        "travel_date": future_date,
        "class_type": "SL",
        "quota": "GN",
    }

    validate_booking_config(config)


def test_validate_booking_config_rejects_past_date():
    past_date = (datetime.now() - timedelta(days=30)).strftime("%d-%m-%Y")
    config = {
        "username": "demo_user",
        "password": "demo_password",
        "captcha_api_key": "demo_key",
        "from_station": "NDLS",
        "to_station": "MMCT",
        "travel_date": past_date,
        "class_type": "SL",
        "quota": "GN",
    }

    with pytest.raises(ValueError):
        validate_booking_config(config)
