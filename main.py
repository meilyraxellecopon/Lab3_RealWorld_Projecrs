# main.py

import grades
import monitoring
import telemetry

LAST_NAME = "COPON"
SEED_NUM = 2
FAVORITE_ARTIST = "LEVERFALL"


def display_summary(summary):
    """Present the processed diagnostic data in a readable summary."""
    print("=" * 55)
    print("EQUIPMENT DIAGNOSTIC SUMMARY")
    print("\nAssessment Data:")
    print(f"Student: {LAST_NAME}")
    print(f"Favorite artist: {FAVORITE_ARTIST}")

    print("\nGenerated Equipment Data:")
    for reading in summary["readings"]:
        print(
            f"  Reading {reading['reading_id']}: "
            f"temperature={reading['temperature']} C, "
            f"vibration={reading['vibration']} mm/s, "
            f"pressure={reading['pressure']} psi"
        )

    print("\nValidation Results:")
    print(f"  Valid readings: {len(summary['readings'])}")
    print(f"  Invalid readings: {len(summary['errors'])}")
    if summary["errors"]:
        for error in summary["errors"]:
            print(f"  {error}")

    print("\nDiagnostic Results:")
    for reading in summary["readings"]:
        print(
            f"  Reading {reading['reading_id']}: "
            f"score={reading['health_score']} ({reading['status']})"
        )
    print(f"  Average health score: {summary['average_health']}")
    print(f"  Status counts: {summary['status_counts']}")

    print("\nExecution Log:")
    for event in summary["logged_by"].split("; "):
        print(f"  {event}")

    print("\nFinal Output:")
    final_status = (
        "CRITICAL"
        if summary["status_counts"]["Critical"]
        else "MONITOR"
        if summary["status_counts"]["Monitor"]
        else "HEALTHY"
    )
    print(f"  Overall equipment condition: {final_status}")
    print("=" * 55)


def run_diagnostic():
    """Generate and process the student's equipment readings."""
    try:
        readings = grades.generate_readings(
            LAST_NAME, SEED_NUM, FAVORITE_ARTIST
        )
        summary = grades.process_readings(readings)
    except (TypeError, ValueError) as error:
        print(f"Diagnostic input error: {error}")
        return None

    display_summary(summary)
    return summary


def run_fault_trace():
    """Generate and recursively trace the student's equipment fault code."""
    try:
        fault_code = grades.generate_fault_code(
            LAST_NAME, SEED_NUM, FAVORITE_ARTIST
        )
        trace_result = grades.trace_fault(fault_code)
    except (TypeError, ValueError) as error:
        print(f"Fault trace input error: {error}")
        return None

    print("\n" + "=" * 55)
    print("RECURSIVE FAULT TRACE")
    print("\nAssessment Data:")
    print(f"  Student: {LAST_NAME}")
    print(f"  Seed number: {SEED_NUM}")
    print(f"  Favorite artist: {FAVORITE_ARTIST}")
    print("\nGenerated Fault Data:")
    print(f"  {fault_code}")
    print("\nRecursive Trace:")
    print("  " + " -> ".join(str(code) for code in trace_result["trace"]))
    print("\nNumber of Recursive Calls:")
    print(f"  {trace_result['recursive_calls']}")
    print("\nExecution Log:")
    print("  Fault code generated")
    print("  Recursive trace completed")
    print("  Base condition reached")
    print("\nFinal Output:")
    print(f"  {trace_result['final_result']}")
    print("=" * 55)
    return trace_result


def run_telemetry_monitoring():
    """Stream telemetry through the modular monitoring system."""
    try:
        telemetry_stream = telemetry.generate_telemetry(
            LAST_NAME, SEED_NUM, FAVORITE_ARTIST
        )
        report = monitoring.process_telemetry(telemetry_stream)
    except (TypeError, ValueError) as error:
        print(f"Telemetry input error: {error}")
        return None

    print("\n" + "=" * 55)
    print("REMOTE TELEMETRY MONITORING REPORT")
    print("\nStudent-Specific Inputs:")
    print(f"  Student: {LAST_NAME}")
    print(f"  Seed number: {SEED_NUM}")
    print(f"  Favorite artist: {FAVORITE_ARTIST}")

    print("\nGenerated Telemetry Data:")
    print("  Telemetry stream generated lazily from student-specific inputs")
    print(f"  Total readings generated: {report['processed_count']}")

    print("\nValid/Invalid Results:")
    print(f"  Valid readings: {report['valid_count']}")
    print(f"  Invalid readings: {report['invalid_count']}")
    for invalid_value in report["invalid_values"]:
        print(f"    Reading {invalid_value['reading_id']}: {invalid_value['error']}")

    print("\nProcessed Results:")
    print(f"  Processed readings: {report['processed_count']}")

    print("\nRecursive Analysis:")
    if report["abnormal_conditions"]:
        for condition in report["abnormal_conditions"]:
            print(
                f"  Reading {condition['reading_id']} "
                f"({condition['sensor_id']}): {', '.join(condition['reasons'])}"
            )
            trace = " -> ".join(
                f"depth {entry['depth']}" for entry in condition["trace"]
            )
            print(f"    Recursive trace: {trace}")
    else:
        print("  None")

    print("\nFinal Diagnostic Summary:")
    print(f"  Abnormal conditions detected: {len(report['abnormal_conditions'])}")
    print(f"  Overall equipment status: {report['overall_status']}")

    print("\nExecution Log:")
    for event in report["execution_log"]:
        print(f"  {event}")

    print("\nFinal Output:")
    print(f"  Overall equipment status: {report['overall_status']}")
    print("=" * 55)
    return report


if __name__ == "__main__":
    run_diagnostic()
    run_fault_trace()
    run_telemetry_monitoring()