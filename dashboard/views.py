from django.views.decorators.http import require_GET
from django.http import JsonResponse
from dashboard.services.area_service import get_area_air_quality

# Create your views here.
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
