import re
from typing import List, Set


def contains_activation_phrase(text: str) -> bool:
    """
    Check if the given text contains an activation phrase.
    
    Activation phrases are:
    - "зиночка" (Russian)
    - "zinochka" (transliterated)
    
    Args:
        text: The text to check for activation phrases
        
    Returns:
        True if an activation phrase is found, False otherwise
    """
    if not text:
        return False
    
    # Convert to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Define activation phrases
    activation_phrases: List[str] = ["зиночка", "zinochka"]
    
    # Check if any activation phrase is in the text
    for phrase in activation_phrases:
        # Using word boundary for more accurate matching
        # This will match the phrase even when it's part of a word
        if re.search(rf'\b{re.escape(phrase)}\b', text_lower) or phrase in text_lower:
            return True
    
    return False