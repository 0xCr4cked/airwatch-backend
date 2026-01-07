from rest_framework.decorators import api_view
from rest_framework.response import Response

from dashboard.services.area_service import (
    get_area_air_quality,
    get_point_air_quality,
)

@api_view(["GET"])
def dashboard(request):
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")
    area_id = request.GET.get("area_id")

    if lat and lon:
        return Response(
            get_point_air_quality(float(lat), float(lon))
        )

    if area_id:
        return Response(
            get_area_air_quality(area_id)
        )

    return Response(
        {"error": "Provide lat/lon or area_id"},
        status=400
    )
