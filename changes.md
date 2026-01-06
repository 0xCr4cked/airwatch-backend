# AirWatch Delhi – Service-Level Explanation (New Additions)

This document explains the **new backend services introduced today**, their responsibilities, and how they integrate with the existing AQI pipeline.
All services were designed to be **additive**, **isolated**, and **non-invasive**.

---

## 1. `openaq_point_service.py`

### Purpose

Handles **all interaction with the OpenAQ API** for **point + radius–based air quality data fetching**, including fallback logic when nearby sensors are unavailable.

This service is the **only place** where OpenAQ is accessed.

---

### Why This Service Exists

- Users provide **latitude and longitude**, not sensor IDs
- Sensor coverage can be sparse or uneven
- The system must be robust to missing data
- External API logic must remain isolated from orchestration and AQI math

---

### Core Function

```python
fetch_measurements_by_point(
    lat,
    lon,
    radius_km=5,
    max_radius_km=25,
    step_km=5
)
```

---

### How It Works (Step-by-Step)

1. Starts querying OpenAQ using a **small radius** around the given point
2. If **no sensors are found**, the radius is increased incrementally
3. Retries until:

   - Measurements are found, or
   - The maximum radius is reached

4. Aggregates raw measurements by pollutant
5. Returns both data and metadata for transparency

---

### Output Format

```json
{
  "pollutants": {
    "pm25": [120.0, 135.2],
    "pm10": [210.4],
    "no2": [42.1]
  },
  "used_radius_km": 15,
  "sensor_count": 3
}
```

---

### Key Design Decisions

- **Progressive radius expansion** avoids silent failures
- **No AQI math** performed here
- **No caching** performed here
- Returns **raw values**, not averages, to preserve flexibility
- Metadata enables explainability and confidence scoring downstream

---

## 2. `_fetch_raw_measurements_from_point` (in `area_service.py`)

### Purpose

Acts as a **bridge** between OpenAQ data and the existing AQI pipeline.

The AQI pipeline expects `raw_measurements` in a specific format; this helper adapts OpenAQ output without modifying downstream logic.

---

### Why This Exists

- Avoids refactoring `normalize_pollutants`
- Keeps OpenAQ-specific structures out of AQI logic
- Maintains backward compatibility with area-based AQI

---

### What It Does

1. Calls `fetch_measurements_by_point`
2. Converts pollutant buckets into a flat list of measurements
3. Returns:

   - `raw_measurements` (pipeline-compatible)
   - `meta` (radius and sensor information)

---

### Example Output

```python
[
  {"parameter": "pm25", "value": 120.0},
  {"parameter": "pm25", "value": 135.2},
  {"parameter": "pm10", "value": 210.4}
]
```

Metadata:

```json
{
  "used_radius_km": 15,
  "sensor_count": 3
}
```

---

### Important Notes

- Does **not** normalize values
- Does **not** calculate AQI
- Does **not** cache results

---

## 3. `get_point_air_quality` (in `area_service.py`)

### Purpose

Provides a **new orchestration entrypoint** for **location-based AQI**, while fully reusing the existing AQI pipeline.

This function is the **only correct way** to calculate AQI from `(lat, lon)`.

---

### Why This Function Exists

- Keeps orchestration logic centralized
- Allows point-based and area-based AQI to coexist
- Avoids branching logic in views
- Preserves cache semantics

---

### High-Level Flow

```
(lat, lon)
   ↓
OpenAQ point + radius fetch
   ↓
Convert to raw measurements
   ↓
Reuse get_area_air_quality()
```

---

### Detailed Steps

1. Fetch raw measurements using point + radius logic
2. If no sensors are found:

   - Return a safe, explainable `no_data` response

3. Construct a **cache key using the actual radius used**
4. Check cache
5. Reuse `get_area_air_quality` to run:

   - Normalization
   - AQI calculation
   - Reasoning
   - Risk scoring

6. Attach metadata to final response

---

### Example Cache Key

```
point:28.6139,77.2090:15km
```

This prevents incorrect cache reuse when fallback radius expansion occurs.

---

### Why This Is Architecturally Correct

- No AQI math duplication
- No OpenAQ calls in views
- No changes to existing pipeline
- Fully backward compatible

---

## 4. `chatbot_service.py`

### Purpose

Provides **AI-generated, context-aware guidance** based on:

- AQI data
- Pollutant composition
- Weather conditions
- User role (citizen / authority)

Uses **Google Gemini Free Tier**.

---

### Why This Service Exists

- Chatbot logic must be isolated from HTTP handling
- AI prompts must be dynamically constructed
- External AI APIs must not leak into views
- Easy replacement or removal of AI layer if needed

---

### Core Responsibilities

1. Build a **structured, data-rich prompt**
2. Send the prompt to Gemini
3. Return clean, readable text for the frontend

---

### Prompt Structure (Conceptual)

```
Role (Citizen / Authority)
↓
Current AQI & category
↓
Dominant pollutant
↓
Pollutant levels
↓
Weather context
↓
User question
↓
Actionable response
```

---

### Example Prompt Context

- AQI: 235 (Poor)
- Dominant pollutant: PM2.5
- Wind speed: 1.5 m/s
- User: Citizen
- Question: “Is it safe to exercise outdoors?”

This ensures responses are **situational, not generic**.

---

### What This Service Does NOT Do

- Does not fetch AQI data
- Does not store chat history
- Does not perform caching (optional future enhancement)
- Does not expose API keys

---

## 5. `chatbot_view` (API Layer)

### Purpose

Exposes the chatbot as an **HTTP API endpoint**.

---

### Responsibilities

- Validate request payload
- Extract AQI, pollutant, and weather data
- Call `chatbot_service`
- Return AI-generated text

---

### Why This Is Kept Thin

- Views should only handle HTTP concerns
- All logic lives in services
- Easier testing and maintenance

---

## Integration Summary

### AQI Pipeline (Unchanged)

```
normalize_pollutants
→ calculate_overall_aqi
→ infer_pollution_reasons
→ calculate_pollution_risk
```

### New Additions

- OpenAQ point-based ingestion feeds into the pipeline
- Chatbot consumes pipeline outputs to generate advice

---

## Key Architectural Guarantees

- No service knows more than it should
- External APIs are isolated
- AQI math remains a single authority
- Cache behavior is consistent
- All additions are reversible

---

## For New Contributors

If you are adding features:

- **AQI logic → `calculate_aqi.py`**
- **Orchestration → `area_service.py`**
- **External APIs → service modules**
- **HTTP logic → views only**

Following this rule keeps the system stable.

---
