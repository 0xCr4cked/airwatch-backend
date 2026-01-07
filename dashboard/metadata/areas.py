# dashboard/metadata/areas.py

AREAS = {
    "central_delhi": {
        "name": "Central Delhi",
        "lat": 28.6139,
        "lon": 77.2090,
    },
    "south_delhi": {
        "name": "South Delhi",
        "lat": 28.5244,
        "lon": 77.1855,
    },
    "south_east_delhi": {
        "name": "South East Delhi",
        "lat": 28.5441,
        "lon": 77.2732,
    },
    "north_delhi": {
        "name": "North Delhi",
        "lat": 28.7041,
        "lon": 77.1025,
    },
    "north_west_delhi": {
        "name": "North West Delhi",
        "lat": 28.7484,
        "lon": 77.0565,
    },
    "east_delhi": {
        "name": "East Delhi",
        "lat": 28.6508,
        "lon": 77.3152,
    },
    "west_delhi": {
        "name": "West Delhi",
        "lat": 28.6692,
        "lon": 77.0689,
    },
    "north_east_delhi": {
        "name": "North East Delhi",
        "lat": 28.6925,
        "lon": 77.2789,
    },
}


def get_area_metadata(area_id: str):
    return AREAS.get(area_id)
