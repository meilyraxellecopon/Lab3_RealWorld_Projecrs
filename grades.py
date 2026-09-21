# grades.py

import random
from functools import wraps


DIAGNOSTIC_LOG = []


def record_diagnostic(function):
    """Record each call to a diagnostic function."""
    @wraps(function)
    def wrapper(*args, **kwargs):
        DIAGNOSTIC_LOG.append(f"Started {function.__name__}")
        result = function(*args, **kwargs)
        DIAGNOSTIC_LOG.append(f"Completed {function.__name__}")
        if isinstance(result, dict) and "logged_by" in result:
            result["logged_by"] = "; ".join(DIAGNOSTIC_LOG)
        return result

    return wrapper


def validate_reading(reading):
    """Validate the required equipment reading fields and ranges."""
    required_fields = {"temperature", "vibration", "pressure"}
    if not isinstance(reading, dict):
        raise TypeError("Each reading must be a dictionary")
    if not required_fields.issubset(reading):
        raise ValueError("Reading is missing a required field")

    temperature = float(reading["temperature"])
    vibration = float(reading["vibration"])
    pressure = float(reading["pressure"])
    if not -50 <= temperature <= 150:
        raise ValueError("Temperature must be between -50 and 150 C")
    if not 0 <= vibration <= 100:
        raise ValueError("Vibration must be between 0 and 100 mm/s")
    if not 0 <= pressure <= 300:
        raise ValueError("Pressure must be between 0 and 300 psi")
    return True


def calculate_health_score(reading):
    """Calculate a 0-100 equipment health score from validated readings."""
    temperature_penalty = abs(reading["temperature"] - 70) * 0.5
    vibration_penalty = reading["vibration"] * 1.5
    pressure_penalty = abs(reading["pressure"] - 100) * 0.25
    return round(max(0, min(100, 100 - temperature_penalty - vibration_penalty - pressure_penalty)), 2)


def classify_condition(health_score):
    """Classify equipment condition from its health score."""
    if health_score >= 80:
        return "Healthy"
    if health_score >= 60:
        return "Monitor"
    return "Critical"


def generate_readings(last_name, seed_num, favorite_artist, count=5):
    """Generate deterministic readings unique to the supplied student values."""
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
    return [
        {
            "reading_id": index,
            "temperature": round(generator.uniform(60, 95), 2),
            "vibration": round(generator.uniform(1, 12), 2),
            "pressure": round(generator.uniform(90, 115), 2),
        }
        for index in range(1, count + 1)
    ]


def generate_fault_code(last_name, seed_num, favorite_artist):
    """Generate a deterministic positive fault code for the student."""
    if not isinstance(last_name, str) or not last_name.strip():
        raise ValueError("LAST_NAME must be a non-empty string")
    if not isinstance(favorite_artist, str) or not favorite_artist.strip():
        raise ValueError("FAVORITE_ARTIST must be a non-empty string")
    if not isinstance(seed_num, int):
        raise TypeError("SEED_NUM must be an integer")

    name_value = sum((index + 1) * ord(char) for index, char in enumerate(last_name.upper()))
    artist_value = sum((index + 1) * ord(char) for index, char in enumerate(favorite_artist.upper()))
    return name_value + artist_value + (seed_num * 100)


def trace_fault(fault_code, termination_value=10):
    """Recursively trace a fault until it reaches the termination value."""
    if not isinstance(fault_code, int) or fault_code <= 0:
        raise ValueError("fault_code must be a positive integer")
    if not isinstance(termination_value, int) or termination_value <= 0:
        raise ValueError("termination_value must be a positive integer")

    if fault_code <= termination_value:
        return {
            "trace": [fault_code],
            "recursive_calls": 1,
            "final_result": f"Fault stabilized at {fault_code}",
        }

    next_code = fault_code // 2
    result = trace_fault(next_code, termination_value)
    return {
        "trace": [fault_code] + result["trace"],
        "recursive_calls": 1 + result["recursive_calls"],
        "final_result": result["final_result"],
    }


@record_diagnostic
def process_readings(readings):
    """Validate and process readings while retaining errors for invalid entries."""
    if not isinstance(readings, list):
        raise TypeError("readings must be a list")

    processed = []
    errors = []
    for index, reading in enumerate(readings, start=1):
        try:
            validate_reading(reading)
            health_score = calculate_health_score(reading)
            processed.append({
                **reading,
                "health_score": health_score,
                "status": classify_condition(health_score),
            })
        except (TypeError, ValueError) as error:
            errors.append(f"Reading {index}: {error}")

    scores = [reading["health_score"] for reading in processed]
    status_counts = {"Healthy": 0, "Monitor": 0, "Critical": 0}
    for reading in processed:
        status_counts[reading["status"]] += 1
    return {
        "readings": processed,
        "errors": errors,
        "average_health": round(sum(scores) / len(scores), 2) if scores else 0,
        "status_counts": status_counts,
        "logged_by": "; ".join(DIAGNOSTIC_LOG),
    }


def compute_average(scores):
    return sum(scores) / len(scores)


def assign_grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 80:
        return "B"
    elif avg >= 70:
        return "C"
    elif avg >= 60:
        return "D"
    else:
        return "F"


def generate_remark(grade):
    remarks = {
        "A": "Excellent Performance",
        "B": "Good Performance",
        "C": "Satisfactory Performance",
        "D": "Needs Improvement",
        "F": "Failing Status",
    }
    return remarks.get(grade, "Invalid Grade")

