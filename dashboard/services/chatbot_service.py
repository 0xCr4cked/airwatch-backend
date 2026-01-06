# dashboard/services/chatbot_service.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

"""
FRONT END WILL SEND THIS    
{
  "user_type": "citizen",
  "query": "Is it safe to go for a morning walk today?",
  "aqi": {
    "aqi": 235,
    "category": "Poor",
    "dominant_pollutant": "pm25"
  },
  "pollutants": {
    "pm25": 168,
    "pm10": 240,
    "no2": 42
  },
  "weather": {
    "wind_speed": 1.5,
    "temperature": 28,
    "humidity": 62
  }
}
"""

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def build_prompt(
    user_type: str,
    aqi_data: dict,
    pollutants: dict,
    weather: dict,
    user_query: str,
) -> str:
    """
    Builds a dynamic, context-rich prompt for the chatbot.
    """

    return f"""
You are an air quality and public health assistant.

USER TYPE:
{user_type}

CURRENT AIR QUALITY:
- AQI: {aqi_data.get("aqi")} ({aqi_data.get("category")})
- Dominant Pollutant: {aqi_data.get("dominant_pollutant")}

POLLUTANT LEVELS:
{', '.join([f"{k.upper()}: {v}" for k, v in pollutants.items()])}

WEATHER CONDITIONS:
{', '.join([f"{k.replace('_', ' ').title()}: {v}" for k, v in weather.items()])}

TASK:
Based on the above data:
- Explain the current pollution situation
- Provide actionable safety advice
- Suggest mitigation steps

If the user is a citizen:
- Focus on health precautions and daily activities

If the user is a government authority:
- Focus on policy, enforcement, and short-term mitigation actions

USER QUESTION:
"{user_query}"

Respond in clear, concise, and practical language.
"""


def get_chatbot_response(
    user_type: str,
    aqi_data: dict,
    pollutants: dict,
    weather: dict,
    user_query: str,
) -> str:
    """
    Sends prompt to Gemini and returns response text.
    """

    prompt = build_prompt(
        user_type=user_type,
        aqi_data=aqi_data,
        pollutants=pollutants,
        weather=weather,
        user_query=user_query,
    )

    response = model.generate_content(prompt)

    return response.text.strip()
