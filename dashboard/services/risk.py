def calculate_pollution_risk(aqi_result: dict, pollutants: dict) -> dict:
    """
    Calculates a pollution risk score (0–1) based on AQI
    and environmental conditions.
    """

    aqi = aqi_result.get("aqi")
    dominant = aqi_result.get("dominant_pollutant")

    if aqi is None:
        return {"risk_score": 0.0, "risk_level": "Unknown"}

    # 1️ormalize AQI (0–500 → 0–1)
    aqi_factor = min(aqi / 500, 1.0)

    # 2️ Pollutant severity bias
    pollutant_factor = 0.0
    if dominant == "pm25":
        pollutant_factor = 0.2
    elif dominant == "pm10":
        pollutant_factor = 0.15
    elif dominant == "no2":
        pollutant_factor = 0.1

    # 3️ Environmental penalty (low wind)
    wind_speed = pollutants.get("wind_speed")
    wind_penalty = 0.0
    if wind_speed is not None and wind_speed < 2:
        wind_penalty = 0.15

    # 4️ Final weighted risk score
    risk_score = (
        0.6 * aqi_factor +
        pollutant_factor +
        wind_penalty
    )

    risk_score = min(round(risk_score, 2), 1.0)

    # Map to qualitative level
    if risk_score >= 0.8:
        level = "High"
    elif risk_score >= 0.5:
        level = "Moderate"
    else:
        level = "Low"

    return {
        "risk_score": risk_score,
        "risk_level": level
    }
