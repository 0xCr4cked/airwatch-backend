from .cache  import get_cached, set_cache
from .normalisation import normalize_pollutants
from .calculate_aqi import calculate_overall_aqi
from .reasoning import infer_pollution_reasons
from .risk import calculate_pollution_risk


def get_area_air_quality(area_id: str, raw_measurements: list) -> dict:
    """
    Orchestrates the full air quality pipeline for one area.
    """

    # 1 Check cache
    cached = get_cached(area_id)
    if cached:
        return cached

    # 2 Normalize pollutants
    pollutants = normalize_pollutants(raw_measurements)

    # 3️ AQI calculation
    aqi_result = calculate_overall_aqi(pollutants)

    # 4️ Reasoning
    reasons = infer_pollution_reasons(pollutants)

    # 5️ Risk score
    risk = calculate_pollution_risk(aqi_result, pollutants)

    # 6️ Final response
    response = {
        "area_id": area_id,
        "pollutants": pollutants,
        "aqi": aqi_result,
        "reasons": reasons,
        "risk": risk,
    }

    # 7️ Store in cache
    set_cache(area_id, response)

    return response
