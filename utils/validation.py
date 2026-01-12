"""
Input validation and sanitization utilities
"""
from config.settings import MIN_PRICE, MAX_PRICE

def validate_price(value: float) -> bool:
    """Validate price inputs are within acceptable range"""
    return MIN_PRICE < value < MAX_PRICE

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent injection attacks"""
    # Remove potentially harmful characters
    dangerous_chars = ['<', '>', '{', '}', '`']
    for char in dangerous_chars:
        text = text.replace(char, '')
    return text.strip()[:500]  # Limit length

def validate_api_key(api_key: str) -> bool:
    """Validate OpenAI API key format"""
    return api_key.startswith('sk-') and len(api_key) > 20