# ABOUTME: Tests for cache management and refresh logic
# ABOUTME: Validates in-memory caching and expiration behavior

from datetime import datetime, timedelta
from app.cache.manager import CacheManager
from app.scoring.models import ConditionRating


def test_cache_stores_and_retrieves_rating():
    """CacheManager should store and retrieve ratings"""
    cache = CacheManager(refresh_hours=2)
    rating = ConditionRating(score=7, mode="sup", description="Test")

    cache.set_rating("sup", rating)
    result = cache.get_rating("sup")

    assert result == rating


def test_cache_returns_none_when_empty():
    """CacheManager should return None for missing keys"""
    cache = CacheManager(refresh_hours=2)
    result = cache.get_rating("sup")

    assert result is None


def test_cache_expires_after_refresh_period():
    """CacheManager should expire cache after refresh hours"""
    cache = CacheManager(refresh_hours=2)
    rating = ConditionRating(score=7, mode="sup", description="Test")

    cache.set_rating("sup", rating)

    # Manually expire the cache by setting old timestamp
    cache._cache["sup"]["timestamp"] = datetime.now() - timedelta(hours=3)

    result = cache.get_rating("sup")
    assert result is None  # Should be expired


def test_cache_not_expired_within_refresh_period():
    """CacheManager should return cached value within refresh period"""
    cache = CacheManager(refresh_hours=2)
    rating = ConditionRating(score=7, mode="sup", description="Test")

    cache.set_rating("sup", rating)

    # Set timestamp to 1 hour ago (within 2 hour window)
    cache._cache["sup"]["timestamp"] = datetime.now() - timedelta(hours=1)

    result = cache.get_rating("sup")
    assert result == rating  # Should still be valid
