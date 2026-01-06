from django.views.decorators.http import require_GET
from django.http import JsonResponse
from dashboard.services.area_service import get_area_air_quality

# Create your views here.
from services.area_service import get_point_air_quality
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def dashboard(request):
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")

    if lat and lon:
        return Response(get_point_air_quality(float(lat), float(lon)))

    # fallback: area-based
    area_id = request.GET.get("area_id")
    raw_measurements = []  # existing behavior
    return Response(get_area_air_quality(area_id, raw_measurements))


@require_GET
def dashboard_view(request):
    """
    Temporary dashboard API endpoint.
    """

    # TEMP: mock measurements (replace with OpenAQ fetch next)
    mock_measurements = [
        {"parameter": "pm25", "value": 300.0},
        {"parameter": "pm10", "value": 180.0},
        {"parameter": "no2", "value": 42.0},
        {"parameter": "wind_speed", "value": 1.2},
    ]

    area_id = request.GET.get("area_id", "default-area")

    result = get_area_air_quality(area_id, mock_measurements)

    return JsonResponse(result, safe=False)


# FOR CHAT BOT

from dashboard.services.chatbot_service import get_chatbot_response


@api_view(["POST"])
def chatbot_view(request):
    """
    Chatbot endpoint for citizens and authorities.
    """

    data = request.data

    user_type = data.get("user_type", "citizen")
    user_query = data.get("query", "")

    aqi_data = data.get("aqi", {})
    pollutants = data.get("pollutants", {})
    weather = data.get("weather", {})

    if not user_query:
        return Response({"error": "Query is required"}, status=400)

    reply = get_chatbot_response(
        user_type=user_type,
        aqi_data=aqi_data,
        pollutants=pollutants,
        weather=weather,
        user_query=user_query,
    )

    return Response({"reply": reply})
