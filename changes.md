---
# AirWatch Delhi – Recent Backend Enhancements

This update extends the existing **AirWatch Delhi** backend with **location-aware AQI fetching**, **robust OpenAQ integration**, and an **AI-powered chatbot**, while preserving the original architecture and design principles.

All changes were implemented as **additive extensions**, ensuring **no refactoring or breakage** of existing services.
---

## Summary of Changes (Today)

### 1. Point + Radius–Based AQI Fetching (User Location Support)

- Added support for fetching air quality data based on **user latitude and longitude**
- Uses **OpenAQ point + radius queries** instead of fixed sensor IDs
- Enables personalized, location-aware AQI responses

**Why this matters**

- Pollution varies significantly within cities
- Ward or city averages are insufficient for individual users
- This allows accurate AQI insights even when users are not near a predefined area

---

### 2. Progressive Radius Expansion (Fault Tolerance)

- Implemented **automatic radius expansion** when no sensors are found nearby
- Starts with a small radius (e.g. 5 km) and gradually expands (up to a safe maximum)
- Prevents empty or failed AQI responses in low-sensor-density regions

**How it works**

- Logic lives entirely in `openaq_point_service.py`
- The system retries OpenAQ queries with increasing radius until data is found or the maximum radius is reached
- Returns metadata such as:

  - `used_radius_km`
  - `sensor_count`

This ensures transparency and explainability.

---

### 3. Clean Integration into Existing AQI Pipeline

No changes were made to:

- AQI calculation logic
- Pollutant normalization
- Risk scoring
- Reasoning engine
- Cache behavior

Instead:

- A new orchestration entrypoint `get_point_air_quality()` was added
- This function fetches OpenAQ data and **reuses the existing pipeline** (`get_area_air_quality`)
- Caching remains centralized and consistent

**Result**

- Area-based AQI and point-based AQI now coexist
- Both flows share the same AQI math, reasoning, and risk logic

---

### 4. Metadata-Aware Caching

- Cache keys for point-based AQI include the **actual radius used**
- Prevents incorrect cache hits when fallback radius expansion occurs

Example cache key:

```
point:28.6139,77.2090:15km
```

This ensures correctness and avoids subtle data inconsistencies.

---

### 5. AI-Powered Chatbot Integration (Google Gemini)

- Integrated a **context-aware chatbot** using **Google Gemini Free Tier**
- Chatbot provides:

  - Safety advice for citizens
  - Mitigation and policy suggestions for authorities

- Responses are generated using **real AQI, pollutant, and weather data**

**Key design choices**

- AI logic is isolated in `chatbot_service.py`
- Views do not talk to Gemini directly
- API keys are never exposed to the frontend
- Prompts are dynamically generated using live environmental data

---

## New Services Added

### `services/openaq_point_service.py`

Handles:

- OpenAQ point + radius queries
- Progressive radius expansion
- Raw pollutant aggregation
- Sensor metadata collection

No AQI math or orchestration logic lives here.

---

### `services/chatbot_service.py`

Handles:

- Dynamic prompt construction
- Google Gemini API calls
- Context-aware AI responses

This service consumes:

- AQI results
- Pollutant values
- Weather data
- User role (citizen / authority)

---

## Updated Orchestration Flow

### Point-Based AQI Flow

```
Frontend (lat, lon)
   ↓
get_point_air_quality()
   ↓
OpenAQ point + radius fetch (with fallback)
   ↓
Existing normalization
   ↓
Existing AQI calculation
   ↓
Existing reasoning engine
   ↓
Existing risk scoring
   ↓
Cached + response returned
```

### Chatbot Flow

```
Frontend (query + AQI + weather)
   ↓
chatbot_view
   ↓
chatbot_service (Gemini)
   ↓
Contextual safety / mitigation advice
```

---

## API Endpoints Added / Updated

### Point-Based AQI

```
GET /api/point-aqi/?lat=<lat>&lon=<lon>&radius=<km>
```

### Chatbot

```
POST /api/chatbot/
```

---

## Architectural Principles Preserved

- AQI math lives **only** in `calculate_aqi.py`
- Orchestration lives **only** in `area_service.py`
- Cache logic lives **only** in `cache.py`
- Views handle HTTP only
- External APIs are isolated in service layers
- All new features are **additive and reversible**

---

## Why This Approach Is Robust

- Works even with sparse sensor coverage
- Fully explainable and auditable
- No hardcoded sensor dependencies
- Safe for hackathons and real-world deployment
- Ready for future extensions (forecasting, confidence scoring, persistence)

---

## Next Possible Enhancements (Future Work)

- AQI trend analysis using cached history
- Confidence score based on sensor count and dispersion
- Staleness filtering for OpenAQ measurements
- Multilingual chatbot responses
- Redis-backed persistent caching

---

**AirWatch Delhi now supports real-time, location-aware air quality insights with explainable reasoning and AI-assisted guidance—without compromising system stability.**

---
