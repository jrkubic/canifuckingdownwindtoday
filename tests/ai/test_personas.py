# ABOUTME: Tests for persona rotation system
# ABOUTME: Validates persona definitions and random selection

from app.ai.personas import PERSONAS, get_random_persona


def test_personas_exist():
    """Should have 5-6 persona definitions"""
    assert len(PERSONAS) >= 5
    assert len(PERSONAS) <= 6


def test_each_persona_has_required_fields():
    """Each persona needs id, name, and prompt_style"""
    for persona in PERSONAS:
        assert "id" in persona
        assert "name" in persona
        assert "prompt_style" in persona
        assert len(persona["prompt_style"]) > 50  # Substantial prompt


def test_persona_ids_are_unique():
    """Persona IDs must be unique for tracking"""
    ids = [p["id"] for p in PERSONAS]
    assert len(ids) == len(set(ids))


def test_get_random_persona_returns_persona():
    """get_random_persona should return a valid persona"""
    persona = get_random_persona()
    assert persona in PERSONAS


def test_get_random_persona_excludes_specified():
    """get_random_persona should not return excluded persona"""
    # Run multiple times to be confident
    for _ in range(20):
        persona = get_random_persona(exclude_id="drill_sergeant")
        assert persona["id"] != "drill_sergeant"


def test_get_random_persona_with_none_exclude():
    """get_random_persona with None exclude should work"""
    persona = get_random_persona(exclude_id=None)
    assert persona in PERSONAS
