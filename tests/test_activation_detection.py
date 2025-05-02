import pytest
from zinochka.services.activation import contains_activation_phrase


def test_contains_activation_phrase_positive():
    """Test that the activation phrase detection works for positive cases."""
    # Test with the Russian phrase
    assert contains_activation_phrase("привет зиночка, добавь задачу") is True
    
    # Test with the transliterated phrase
    assert contains_activation_phrase("hey zinochka, add a task") is True
    
    # Test with mixed case
    assert contains_activation_phrase("Hey ZINOCHKA, add a task") is True
    assert contains_activation_phrase("Привет ЗиНоЧкА, добавь задачу") is True
    
    # Test with phrase in the middle of text
    assert contains_activation_phrase("I need to tell zinochka to do something") is True


def test_contains_activation_phrase_negative():
    """Test that non-activation phrases are correctly identified."""
    # Empty string
    assert contains_activation_phrase("") is False
    
    # No activation phrase
    assert contains_activation_phrase("add a task to my list") is False
    
    # Similar but not exact phrases
    assert contains_activation_phrase("zinocka help me") is False  # Missing 'h'
    assert contains_activation_phrase("зиноча, добавь задачу") is False  # Missing 'к'
    
    # Phrases with extra characters directly attached
    assert contains_activation_phrase("zinochka123") is True  # Should still match
    assert contains_activation_phrase("зиночка!") is True  # Should still match