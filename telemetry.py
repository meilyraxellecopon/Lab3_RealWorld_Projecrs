"""Streaming telemetry generation and validation."""

import random


def generate_telemetry(last_name, seed_num, favorite_artist, count=20):
    """Yield student-specific sensor readings without storing the stream."""
    if not isinstance(last_name, str) or not last_name.strip():
        raise ValueError("LAST_NAME must be a non-empty string")
    if not isinstance(favorite_artist, str) or not favorite_artist.strip():
        raise ValueError("FAVORITE_ARTIST must be a non-empty string")
    if not isinstance(seed_num, int):
        raise TypeError("SEED_NUM must be an integer")
    if not isinstance(count, int) or count <= 0:
        raise ValueError("count must be a positive integer")

    student_seed = seed_num + sum(ord(char) for char in last_name.upper())
    student_seed += sum(ord(char) for char in favorite_artist.upper())
    generator = random.Random(student_seed)

    for reading_id in range(1, count + 1):
        reading = {
            "reading_id": reading_id,
            "sensor_id": f"S-{(reading_id - 1) % 3 + 1}",
            "temperature": round(generator.uniform(60, 95), 2),
            "vibration": round(generator.uniform(1, 12), 2),
            "pressure": round(generator.uniform(90, 115), 2),
        }
        if reading_id % 7 == 0:
            reading["temperature"] = 125.0
        yield reading


def validate_telemetry(reading):
    """Validate one telemetry record and raise a useful error if invalid."""
    required = {"reading_id", "sensor_id", "temperature", "vibration", "pressure"}
    if not isinstance(reading, dict):
        raise TypeError("Telemetry value must be a dictionary")
    if not required.issubset(reading):
        raise ValueError("Telemetry value is missing a required field")
    if not isinstance(reading["sensor_id"], str):
        raise TypeError("sensor_id must be a string")

    temperature = float(reading["temperature"])
    vibration = float(reading["vibration"])
    pressure = float(reading["pressure"])
    if not -50 <= temperature <= 120:
        raise ValueError("temperature is outside the safe sensor range")
    if not 0 <= vibration <= 100:
        raise ValueError("vibration is outside the valid range")
    if not 0 <= pressure <= 300:
        raise ValueError("pressure is outside the valid range")
    return True
