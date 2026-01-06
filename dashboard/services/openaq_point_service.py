# services/openaq_point_service.py
# from .services.openaq_point_service import fetch_measurements_by_point
# services/openaq_point_service.py

from openaq import OpenAQ
import os
from dotenv import load_dotenv

load_dotenv()

_client = OpenAQ(api_key=os.getenv("OPENAQ_API_KEY"))


def fetch_measurements_by_point(
    lat: float,
    lon: float,
    radius_km: int = 5,
    max_radius_km: int = 25,
    step_km: int = 5,
    limit: int = 50,
):
    """
    Fetch OpenAQ measurements using point + radius.
    If no sensors are found, progressively increase radius.

    Returns:
    {
        "pollutants": { "pm25": [...], "pm10": [...] },
        "used_radius_km": int,
        "sensor_count": int
    }
    """

    current_radius = radius_km

    while current_radius <= max_radius_km:
        response = _client.measurements.list(
            coordinates=(lat, lon),
            radius=current_radius * 1000,  # meters
            limit=limit,
            sort="desc",
            order_by="datetime",
        )

        results = response.results or []

        if results:
            pollutants = {}
            for m in results:
                param = m.parameter.name.lower()
                value = m.value

                if value is None:
                    continue

                pollutants.setdefault(param, []).append(value)

            return {
                "pollutants": pollutants,
                "used_radius_km": current_radius,
                "sensor_count": len(results),
            }

        # No data → expand radius
        current_radius += step_km

    # No data found even at max radius
    return {
        "pollutants": {},
        "used_radius_km": current_radius - step_km,
        "sensor_count": 0,
    }
