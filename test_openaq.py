from openaq import OpenAQ
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAQ(api_key=os.getenv("OPENAQ_API_KEY"))


response = client.locations.list(
    bbox=(76.8, 28.4, 77.4, 28.9),
    limit=5
)

locations = response.results
print("Locations fetched:", [loc.id for loc in locations])


measurements = client.measurements.list(
    sensors_id=13864,
    limit=5
)
sample = measurements.results[0]

flat = {
    "parameter": sample.parameter.name,
    "value": sample.value,
    "unit": sample.parameter.units,
    "datetime": sample.period.datetime_to.utc,
}

print(flat)


print(measurements)

client.close()
