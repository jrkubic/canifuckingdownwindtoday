# ABOUTME: Tests for foil setup recommendation logic
# ABOUTME: Validates CODE and KT foil recommendations based on conditions and score

from app.scoring.foil_recommender import FoilRecommender
from app.weather.models import WeatherConditions


def make_conditions(wind: float, waves: float) -> WeatherConditions:
    """Helper to create test conditions"""
    return WeatherConditions(
        wind_speed_kts=wind,
        wind_direction="S",
        wave_height_ft=waves,
        swell_direction="S",
        timestamp="2025-11-26T14:30:00"
    )


# --- CODE Foil Tests ---

def test_code_light_conditions():
    """Light wind (score 1-4) should recommend 1250R"""
    recommender = FoilRecommender()
    result = recommender.recommend_code(score=3)

    assert "1250R" in result
    assert "135R stab" in result.lower() or "135r stab" in result.lower()


def test_code_good_conditions():
    """Good wind (score 5-7) should recommend 960R"""
    recommender = FoilRecommender()
    result = recommender.recommend_code(score=6)

    assert "960R" in result
    assert "135R stab" in result.lower() or "135r stab" in result.lower()


def test_code_great_conditions():
    """Great conditions (score 8-10) should recommend 770R"""
    recommender = FoilRecommender()
    result = recommender.recommend_code(score=9)

    assert "770R" in result


# --- KT Atlas Tests ---

def test_kt_light_conditions():
    """Light wind (score 1-4) should recommend Atlas 1130"""
    recommender = FoilRecommender()
    result = recommender.recommend_kt(score=3)

    assert "Atlas 1130" in result
    assert "145" in result  # Paka'a stabilizer


def test_kt_good_conditions():
    """Good wind (score 5-7) should recommend Atlas 790 or 960"""
    recommender = FoilRecommender()
    result = recommender.recommend_kt(score=6)

    assert "Atlas 790" in result or "Atlas 960" in result
    assert "145" in result  # Paka'a stabilizer


def test_kt_great_conditions():
    """Great conditions (score 8-10) should recommend Atlas 680"""
    recommender = FoilRecommender()
    result = recommender.recommend_kt(score=9)

    assert "Atlas 680" in result
    assert "170" in result  # Larger stabilizer for big days


# --- Integration with conditions (backwards compat) ---

def test_recommend_code_accepts_conditions():
    """Should still work when passed conditions (for backwards compat)"""
    recommender = FoilRecommender()
    conditions = make_conditions(wind=10.0, waves=1.5)

    # When passed conditions, should calculate score internally
    result = recommender.recommend_code(conditions=conditions)
    assert result is not None
    assert len(result) > 0


def test_recommend_kt_accepts_conditions():
    """Should still work when passed conditions (for backwards compat)"""
    recommender = FoilRecommender()
    conditions = make_conditions(wind=18.0, waves=3.0)

    result = recommender.recommend_kt(conditions=conditions)
    assert result is not None
    assert len(result) > 0
