from .cache import get_cached, set_cache
from .normalisation import normalize_pollutants
from .calculate_aqi import calculate_overall_aqi
from .reasoning import infer_pollution_reasons
from .risk import calculate_pollution_risk

from services.openaq_point_service import fetch_measurements_by_point
from dashboard.metadata.areas import get_area_metadata


def _fetch_raw_measurements_from_point(lat: float, lon: float):
    """
    Fetch OpenAQ data using point + progressive radius
    and adapt it to AQI pipeline format.
    """

    result = fetch_measurements_by_point(lat=lat, lon=lon)

    pollutants = result["pollutants"]
    raw_measurements = []

    for parameter, values in pollutants.items():
        for value in values:
            raw_measurements.append({
                "parameter": parameter,
                "value": value
            })

    meta = {
        "used_radius_km": result["used_radius_km"],
        "measurement_count": result["sensor_count"],
    }

    return raw_measurements, meta


def _run_aqi_pipeline(area_id: str, raw_measurements: list) -> dict:
    """
    Pure AQI pipeline. No fetching, no caching.
    """

    pollutants = normalize_pollutants(raw_measurements)
    aqi_result = calculate_overall_aqi(pollutants)
    reasons = infer_pollution_reasons(pollutants)
    risk = calculate_pollution_risk(aqi_result, pollutants)

    return {
        "area_id": area_id,
        "pollutants": pollutants,
        "aqi": aqi_result,
        "reasons": reasons,
        "risk": risk,
    }


def get_point_air_quality(lat: float, lon: float, area_id: str | None = None) -> dict:
    """
    Canonical AQI entrypoint for any location.
    """

    raw_measurements, meta = _fetch_raw_measurements_from_point(lat, lon)

    if not raw_measurements:
        return {
            "area_id": area_id or "custom-point",
            "status": "no_data",
            "meta": meta,
        }

    cache_key = f"point:{lat:.4f},{lon:.4f}:{meta['used_radius_km']}km"
    cached = get_cached(cache_key)
    if cached:
        return cached

    response = _run_aqi_pipeline(
        area_id=area_id or "custom-point",
        raw_measurements=raw_measurements,
    )

    response["meta"] = meta
    set_cache(cache_key, response)
    return response


def get_area_air_quality(area_id: str) -> dict:
    """
    Area AQI = point AQI using predefined center coordinates.
    """

    meta = get_area_metadata(area_id)
    if not meta:
        return {"error": "Unknown area_id"}

    return get_point_air_quality(
        lat=meta["lat"],
        lon=meta["lon"],
        area_id=area_id,
    )
