# ABOUTME: Application configuration including location coordinates and API settings
# ABOUTME: Centralized config to make future multi-location support easy

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""

    # Location: Jupiter, FL (Juno Beach to Carlin Park downwind run)
    LOCATION_NAME = "Jupiter, FL"
    LOCATION_LAT = 26.9
    LOCATION_LON = -80.1

    # Jupiter-specific optimal conditions
    # Coast runs N-S, so wind parallel to coast is best for downwinding
    OPTIMAL_WIND_DIRECTIONS = ["N", "S"]  # Parallel to coast - best
    GOOD_WIND_DIRECTIONS = ["NE", "SE", "NW", "SW"]  # Diagonal - good
    OK_WIND_DIRECTIONS = ["NNE", "SSE", "NNW", "SSW", "ENE", "ESE", "WNW", "WSW"]  # Acceptable
    BAD_WIND_DIRECTIONS = ["E", "W"]  # Perpendicular to coast - bad

    OPTIMAL_WIND_MIN = 15  # knots
    OPTIMAL_WIND_MAX = 25  # knots
    OPTIMAL_WAVE_MIN = 2   # feet
    OPTIMAL_WAVE_MAX = 4   # feet

    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    # Caching
    CACHE_REFRESH_HOURS = int(os.getenv("CACHE_REFRESH_HOURS", "2"))
