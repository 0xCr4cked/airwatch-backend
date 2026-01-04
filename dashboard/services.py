from django.http import JsonResponse
def get_dashboard_data():
        return {
        "meta": {
            "region": "Delhi NCT",
            "last_updated": "2026-01-02T18:05:00Z"
        },
        "city_summary": {
            "avg_aqi": 383,
            "category": "Hazardous",
            "trend_percentage": 16.3
        },
        "wards": [
            {
                "id": 1,
                "name": "East Delhi",
                "aqi": 500,
                "category": "Hazardous"
            },
            {
                "id": 2,
                "name": "North West Delhi",
                "aqi": 474,
                "category": "Hazardous"
            }
        ],
        "weather": {
            "temperature": 18,
            "humidity": 72,
            "wind_speed": 4.2,
            "dispersion": "Moderate"
        },
        "ai_insights": {
            "summary": "Air quality is severely degraded. Immediate action recommended.",
            "citizen_actions": [
                "Avoid outdoor activities",
                "Use air purifiers indoors",
                "Wear N95 masks"
            ]
        }
    }
