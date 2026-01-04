from collections import defaultdict
from typing import Dict, List


def normalize_pollutants(raw_measurements: List[Dict]) -> Dict:
    grouped = defaultdict(list)

    for m in raw_measurements:
        parameter = m.get("parameter")
        value = m.get("value")

        if parameter and value is not None:
            grouped[parameter].append(value)
    normalised  ={}
    for parameter,values in grouped.items():
        normalised[parameter] = max(values)

    return normalised
if __name__ == "__main__":
    sample = [
        {"parameter": "pm25", "value": 300.0},
        {"parameter": "pm25", "value": 93.0},
        {"parameter": "pm10", "value": 180.0},
    ]

    print(normalize_pollutants(sample))
