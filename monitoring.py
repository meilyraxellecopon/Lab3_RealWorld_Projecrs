"""Telemetry processing, anomaly analysis, and report generation."""

from functools import wraps

from telemetry import validate_telemetry

PROCESSING_LOG = []


def monitor_processing(function):
    """Record the start and completion of the main monitoring operation."""
    @wraps(function)
    def wrapper(*args, **kwargs):
        PROCESSING_LOG.append(f"Started {function.__name__}")
        try:
            result = function(*args, **kwargs)
        except Exception:
            PROCESSING_LOG.append(f"Failed {function.__name__}")
            raise
        PROCESSING_LOG.append(f"Completed {function.__name__}")
        result["execution_log"] = list(PROCESSING_LOG)
        return result

    return wrapper


def trace_abnormal_condition(reading, depth=0, maximum_depth=3):
    """Recursively trace an abnormal reading to a defined depth."""
    trace_entry = {
        "depth": depth,
        "reading_id": reading["reading_id"],
        "status": "abnormal" if depth < maximum_depth else "investigation complete",
    }
    if depth >= maximum_depth:
        return [trace_entry]
    return [trace_entry] + trace_abnormal_condition(
        reading, depth + 1, maximum_depth
    )


@monitor_processing
def process_telemetry(stream):
    """Consume, transform, validate, and analyze a telemetry stream."""
    processed_count = 0
    valid_count = 0
    invalid_count = 0
    invalid_values = []
    abnormal_conditions = []

    # This lambda creates a compact health value for each valid measurement.
    add_health_value = lambda item: {
        **item,
        "health_value": round(
            100
            - abs(item["temperature"] - 70) * 0.5
            - item["vibration"] * 1.5
            - abs(item["pressure"] - 100) * 0.25,
            2,
        ),
    }

    for raw_reading in stream:
        processed_count += 1
        try:
            validate_telemetry(raw_reading)
            reading = add_health_value(raw_reading)
            valid_count += 1
            reasons = []
            if reading["temperature"] > 100:
                reasons.append("high temperature")
            if reading["vibration"] > 10:
                reasons.append("high vibration")
            if reading["pressure"] < 95 or reading["pressure"] > 110:
                reasons.append("pressure variance")
            if reasons:
                abnormal_conditions.append({
                    "reading_id": reading["reading_id"],
                    "sensor_id": reading["sensor_id"],
                    "reasons": reasons,
                    "trace": trace_abnormal_condition(reading),
                })
        except (TypeError, ValueError) as error:
            invalid_count += 1
            invalid_values.append({
                "reading_id": raw_reading.get("reading_id", processed_count)
                if isinstance(raw_reading, dict) else processed_count,
                "error": str(error),
            })

    if abnormal_conditions:
        overall_status = "ALERT"
    elif invalid_count:
        overall_status = "MONITOR"
    else:
        overall_status = "NORMAL"

    return {
        "processed_count": processed_count,
        "valid_count": valid_count,
        "invalid_count": invalid_count,
        "invalid_values": invalid_values,
        "abnormal_conditions": abnormal_conditions,
        "overall_status": overall_status,
        "execution_log": list(PROCESSING_LOG),
    }
