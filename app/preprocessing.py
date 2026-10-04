from typing import Mapping


def transform(payload: Mapping[str, object]) -> tuple[float, float, int, int]:
    """Prepare the four serving features defined by the Lab 2 contract."""
    return (
        float(payload["temperature"]),
        float(payload["vibration_amplitude"]),
        int(payload["operating_hours"]),
        int(payload["error_code_last_24h"]),
    )
