# ABOUTME: Cache management with time-based expiration
# ABOUTME: Stores ratings and weather data to minimize API calls

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from app.scoring.models import ConditionRating


class CacheManager:
    """Manages cached ratings with time-based expiration"""

    def __init__(self, refresh_hours: int = 2):
        self.refresh_hours = refresh_hours
        self._cache: Dict[str, Dict[str, Any]] = {}

    def set_rating(self, mode: str, rating: ConditionRating) -> None:
        """
        Store rating in cache

        Args:
            mode: "sup" or "parawing"
            rating: ConditionRating to cache
        """
        self._cache[mode] = {
            "rating": rating,
            "timestamp": datetime.now()
        }

    def get_rating(self, mode: str) -> Optional[ConditionRating]:
        """
        Retrieve rating from cache if not expired

        Args:
            mode: "sup" or "parawing"

        Returns:
            Cached ConditionRating or None if expired/missing
        """
        if mode not in self._cache:
            return None

        cached = self._cache[mode]
        age = datetime.now() - cached["timestamp"]

        if age > timedelta(hours=self.refresh_hours):
            # Expired
            del self._cache[mode]
            return None

        return cached["rating"]

    def is_expired(self, mode: str) -> bool:
        """Check if cache is expired for given mode"""
        return self.get_rating(mode) is None
