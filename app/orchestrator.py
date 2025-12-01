# ABOUTME: Main application orchestrator coordinating all components
# ABOUTME: Handles weather fetch, scoring, LLM generation, caching, and foil recommendations

from typing import Optional
from app.config import Config
from app.weather.fetcher import WeatherFetcher
from app.scoring.calculator import ScoreCalculator
from app.scoring.foil_recommender import FoilRecommender
from app.scoring.models import ConditionRating
from app.ai.llm_client import LLMClient
from app.cache.manager import CacheManager


class AppOrchestrator:
    """Orchestrates all app components to generate ratings"""

    def __init__(self, api_key: str):
        self.weather_fetcher = WeatherFetcher()
        self.score_calculator = ScoreCalculator()
        self.foil_recommender = FoilRecommender()
        self.llm_client = LLMClient(api_key=api_key)
        self.cache = CacheManager(refresh_hours=Config.CACHE_REFRESH_HOURS)

    def get_sup_rating(self) -> Optional[ConditionRating]:
        """
        Get SUP foil rating (cached or fresh)

        Returns:
            ConditionRating or None if weather unavailable
        """
        # Check cache first
        cached = self.cache.get_rating("sup")
        if cached:
            return cached

        # Fetch fresh data
        return self._generate_rating("sup")

    def get_parawing_rating(self) -> Optional[ConditionRating]:
        """
        Get parawing rating (cached or fresh)

        Returns:
            ConditionRating or None if weather unavailable
        """
        # Check cache first
        cached = self.cache.get_rating("parawing")
        if cached:
            return cached

        # Fetch fresh data
        return self._generate_rating("parawing")

    def get_foil_recommendations(self) -> dict:
        """
        Get foil recommendations for current conditions

        Returns:
            Dict with CODE and KT recommendations
        """
        conditions = self.weather_fetcher.fetch_current_conditions(
            Config.LOCATION_LAT,
            Config.LOCATION_LON
        )

        if not conditions:
            return {"code": "Weather unavailable", "kt": "Weather unavailable"}

        return {
            "code": self.foil_recommender.recommend_code(conditions),
            "kt": self.foil_recommender.recommend_kt(conditions)
        }

    def _generate_rating(self, mode: str) -> Optional[ConditionRating]:
        """Generate fresh rating for given mode"""
        # Fetch weather
        conditions = self.weather_fetcher.fetch_current_conditions(
            Config.LOCATION_LAT,
            Config.LOCATION_LON
        )

        if not conditions:
            return None

        # Calculate score
        if mode == "sup":
            score = self.score_calculator.calculate_sup_score(conditions)
        else:
            score = self.score_calculator.calculate_parawing_score(conditions)

        # Generate snarky description
        description = self.llm_client.generate_description(
            wind_speed=conditions.wind_speed_kts,
            wind_direction=conditions.wind_direction,
            wave_height=conditions.wave_height_ft,
            swell_direction=conditions.swell_direction,
            rating=score,
            mode=mode
        )

        # Create rating
        rating = ConditionRating(score=score, mode=mode, description=description)

        # Cache it
        self.cache.set_rating(mode, rating)

        return rating
