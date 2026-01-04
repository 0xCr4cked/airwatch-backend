import time

# cache structure:
# {
#   "area_id": {
#       "timestamp": 1700000000,
#       "data": {...}
#   }
# }

_CACHE = {}
CACHE_TTL_SECONDS = 60 * 60  #taking ttl  1 hour


def get_cached(area_id: str):
    entry = _CACHE.get(area_id)

    if not entry:
        return None

    age = time.time() - entry["timestamp"]
    if age > CACHE_TTL_SECONDS:
        return None

    return entry["data"]


def set_cache(area_id: str, data: dict):
    _CACHE[area_id] = {
        "timestamp": time.time(),
        "data": data
    }
if __name__ == "__main__":
    set_cache("test-area", {"aqi": 200})

    print(get_cached("test-area"))  # should print data

    time.sleep(2)

    print(get_cached("test-area"))  # still valid
