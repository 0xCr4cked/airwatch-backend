# dashboard/services/reasoning.py

def infer_pollution_reasons(pollutants: dict) -> dict:
    """
    Infers reasons for high pollution based on pollutant levels
    and environmental factors.
    """

    reasons = []
    primary_reason = None

    pm25 = pollutants.get("pm25")
    pm10 = pollutants.get("pm10")
    wind_speed = pollutants.get("wind_speed")

    # Rule 1: PM2.5 accumulation due to low wind
    if pm25 is not None and pm25 > 90:
        if wind_speed is not None and wind_speed < 2:
            primary_reason = "Low wind speed causing PM2.5 accumulation"
            reasons.append("High PM2.5 concentration")
            reasons.append("Poor atmospheric dispersion")

    # Rule 2: Dust / construction influence
    if pm10 is not None and pm10 > 150:
        reasons.append("High PM10 levels indicate construction or road dust")

        if not primary_reason:
            primary_reason = "Dust and construction activities"

    # Rule 3: Traffic-related pollution
    if pm25 is not None and pm25 > 90 and pm10 is not None and pm10 > 150:
        reasons.append("Vehicular emissions contributing to particulate matter")

        if not primary_reason:
            primary_reason = "Heavy vehicular emissions"

    if not primary_reason:
        primary_reason = "Multiple contributing factors"

    return {
        "primary_reason": primary_reason,
        "contributing_factors": reasons,
    }

if __name__ == "__main__":
    sample = {
        "pm25": 300.0,
        "pm10": 180.0,
        "wind_speed": 1.2,
    }

    print(infer_pollution_reasons(sample))
