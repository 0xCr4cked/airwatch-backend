from .cache import get_cached, set_cache
from .normalisation import normalize_pollutants
from .calculate_aqi import calculate_overall_aqi
from .reasoning import infer_pollution_reasons
from .risk import calculate_pollution_risk
from services.openaq_point_service import fetch_measurements_by_point


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


def _fetch_raw_measurements_from_point(lat: float, lon: float, radius_km: int = 5):
    result = fetch_measurements_by_point(
        lat=lat,
        lon=lon,
        radius_km=radius_km,
    )

    pollutants = result["pollutants"]
    measurements = []

    for parameter, values in pollutants.items():
        for value in values:
            measurements.append({"parameter": parameter, "value": value})

    return measurements, {
        "used_radius_km": result["used_radius_km"],
        "sensor_count": result["sensor_count"],
    }


def get_point_air_quality(lat: float, lon: float, radius_km: int = 5) -> dict:
    """
    Orchestrates air quality pipeline using point + radius OpenAQ data.
    """

    # 1️ Check cache
    # not checking the cache as we do already do so in get area air quality

    # 2️ Fetch raw OpenAQ measurements
    raw_measurements, meta = _fetch_raw_measurements_from_point(lat, lon, radius_km)

    if not raw_measurements:
        return {
            "status": "no_data",
            "message": "No OpenAQ sensors found even after expanding search radius",
            "meta": meta,
        }
    area_id = f"point:{lat:.4f},{lon:.4f}:{radius_km}km"
    response = get_area_air_quality(area_id, raw_measurements)
    response["meta"] = meta

    return response
