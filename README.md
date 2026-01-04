AirWatch Delhi — Backend (Django)

Backend API for AirWatch Delhi, a ward-/area-level air quality monitoring system built for a hackathon.

This backend is API-only, frontend-agnostic, and designed with a clean, production-style pipeline:
- OpenAQ data ingestion
- Pollutant normalization
- AQI calculation (CPCB-based)
- Explainability (reasoning)
- Pollution risk scoring
- Hourly caching


Tech Stack
----------
- Python 3.11
- Django
- python-dotenv
- OpenAQ Python Client
- In-memory caching (hackathon-safe)


Project Structure
-----------------
airwatch-backend/
│
├── config/                     # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── dashboard/                  # Main backend app
│   ├── migrations/
│   ├── services/               # Core backend logic (DO NOT RANDOMLY EDIT)
│   │   ├── __init__.py
│   │   ├── area_service.py     # Orchestrates full AQI pipeline
│   │   ├── cache.py            # Hourly in-memory cache
│   │   ├── calculate_aqi.py    # Generic AQI engine + CPCB breakpoints
│   │   ├── normalisation.py    # Pollutant normalization
│   │   ├── reasoning.py        # Rule-based pollution explanation
│   │   └── risk.py             # Pollution risk score
│   │
│   ├── views.py                # API endpoints
│   ├── urls.py                 # App-level routing
│   ├── models.py               # (unused for now)
│   ├── admin.py
│   └── apps.py
│
├── test_openaq.py               # OpenAQ client sanity test (standalone)
├── manage.py
├── db.sqlite3
├── .env                         # OPENAQ_API_KEY lives here
├── venv/
└── README.md


Core Backend Flow
-----------------
For any given area_id, the backend flow is:

API Request
  → Cache Check (1 hour TTL)
  → (OpenAQ fetch – currently mocked in view)
  → Normalization
  → AQI Calculation (multi-pollutant)
  → Reasoning (why AQI is high)
  → Risk Score
  → Response + Cache Store

All orchestration happens in:
dashboard/services/area_service.py


Current API
-----------
GET /api/dashboard/?area_id=<id>

Returns:
- normalized pollutant values
- AQI + category + dominant pollutant
- human-readable reasons
- pollution risk score

Note:
- The endpoint currently uses mocked pollutant data.
- OpenAQ integration will replace the mock.


Environment Setup
-----------------
Create a .env file:

OPENAQ_API_KEY=your_key_here

Install dependencies:

pip install python-dotenv
pip install openaq

Run server:

python manage.py runserver


What Is DONE
------------
- Generic AQI engine (CPCB-based)
- Multi-pollutant AQI aggregation
- Explainability / reasoning engine
- Pollution risk scoring
- Hourly in-memory cache layer
- Clean orchestration service
- API endpoint wired and running
- OpenAQ client validated via test_openaq.py


What Is LEFT TO DO
------------------
1. Replace mock data with real OpenAQ fetch logic
   - Move OpenAQ calls into a dedicated service
   - Flatten OpenAQ measurements
   - Pass real measurements to area_service

2. Area / Ward Mapping
   - Decide how frontend sends area info (area_id, bbox, polygon)
   - Map area to relevant OpenAQ sensors

3. Forecast / Analytics (Optional)
   - Forecast AQI using historical cached values
   - Feature extraction / trend detection

4. Cache Improvements (Optional)
   - Replace in-memory cache with Redis if needed
   - Persist cache across restarts

5. Frontend Integration
   - Lock API contract
   - Remove mock assumptions


Important Rules for Contributors
--------------------------------
- Do NOT refactor core services casually
- AQI math lives ONLY in calculate_aqi.py
- Add new pollutants by extending breakpoints, not rewriting logic
- Orchestration logic lives ONLY in area_service.py
- Extend functionality by adding new services, not modifying existing ones
- Discuss before touching core pipeline files


Notes
-----
- test_openaq.py is a standalone sanity check for OpenAQ
- It is NOT part of Django runtime
- Backend is intentionally area-agnostic (ward/district safe)
- Focus is on explainability and correctness over black-box ML
