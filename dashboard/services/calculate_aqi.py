# dashboard/services/aqi.py

from typing import List, Tuple, Dict

# Type alias for readability
Breakpoint = Tuple[float, float, int, int, str]
# (conc_low, conc_high, aqi_low, aqi_high, category)

#this is a general logic for calculating aqi from pm2.5,pm10 etc
def calculate_aqi(value: float, breakpoints: List[Breakpoint]) -> Dict:
    """
    Generic AQI calculator using linear interpolation.
    """

    for c_low, c_high, aqi_low, aqi_high, category in breakpoints:
        if c_low <= value <= c_high:
            aqi = (
                (aqi_high - aqi_low)
                / (c_high - c_low)
                * (value - c_low)
                + aqi_low
            )
            return {
                "aqi": round(aqi),
                "category": category
            }

    return {"aqi": None, "category": "Unknown"}
PM25_BREAKPOINTS: List[Breakpoint] = [
    (0, 30, 0, 50, "Good"),
    (31, 60, 51, 100, "Satisfactory"),
    (61, 90, 101, 200, "Moderate"),
    (91, 120, 201, 300, "Poor"),
    (121, 250, 301, 400, "Very Poor"),
    (251, 1000, 401, 500, "Severe"),
]

PM10_BREAKPOINTS: List[Breakpoint] = [
    (0, 50, 0, 50, "Good"),
    (51, 100, 51, 100, "Satisfactory"),
    (101, 250, 101, 200, "Moderate"),
    (251, 350, 201, 300, "Poor"),
    (351, 430, 301, 400, "Very Poor"),
    (431, 1000, 401, 500, "Severe"),
]

NO2_BREAKPOINTS: List[Breakpoint] = [
    (0, 40, 0, 50, "Good"),
    (41, 80, 51, 100, "Satisfactory"),
    (81, 180, 101, 200, "Moderate"),
    (181, 280, 201, 300, "Poor"),
    (281, 400, 301, 400, "Very Poor"),
    (401, 1000, 401, 500, "Severe"),
]
#calculating only using this pollutants.we are ignoring rest because of complexity
SUPPORTED_POLLUTANTS = {
    "pm25": PM25_BREAKPOINTS,
    "pm10": PM10_BREAKPOINTS,
    "no2": NO2_BREAKPOINTS,
}
def calculate_overall_aqi(pollutants: Dict[str, float]) -> Dict:
    """
    Calculates overall AQI from normalized pollutant values.
    """

    sub_indices = {}

    for pollutant, value in pollutants.items():
        if pollutant in SUPPORTED_POLLUTANTS:
            result = calculate_aqi(value, SUPPORTED_POLLUTANTS[pollutant])
            if result["aqi"] is not None:
                sub_indices[pollutant] = result["aqi"]

    if not sub_indices:
        return {"aqi": None, "category": "Unknown"}

    dominant_pollutant = max(sub_indices, key=sub_indices.get)
    overall_aqi = sub_indices[dominant_pollutant]

    category = calculate_aqi(
        pollutants[dominant_pollutant],
        SUPPORTED_POLLUTANTS[dominant_pollutant]
    )["category"]

    return {
        "aqi": overall_aqi,
        "category": category,
        "dominant_pollutant": dominant_pollutant,
        "sub_indices": sub_indices,
    }
if __name__ == "__main__":
    pollutants = {
        "pm25": 300.0,
        "pm10": 180.0,
        "no2": 42.0,
    }

    print(calculate_overall_aqi(pollutants))
