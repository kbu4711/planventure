import re

def validate_email(email: str) -> bool:
    """Validate email format using regex pattern"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_username(username: str) -> bool:
    """
    Validates a username according to the following rules:
    - Between 3 and 16 characters
    - Starts with a letter or single underscore
    - Can contain letters, numbers, and underscores after first character
    - No spaces or special characters
    
    Args:
        username: The username to validate
        
    Returns:
        bool: True if username is valid, False otherwise
        
    Raises:
        TypeError: If username is None
        AttributeError: If username is not a string
    """
    if username is None:
        raise TypeError("Username cannot be None")
    
    # Raise AttributeError for non-string types
    if not isinstance(username, str):
        raise AttributeError(f"Username must be a string, not {type(username).__name__}")
        
    # Check for empty string
    if not username:
        return False
        
    # Check length (3-16 characters)
    if len(username) < 3 or len(username) > 16:
        return False
        
    # Pattern explanation:
    # ^                                    - Start of string
    # (                                    - Start of alternation
    #   [a-zA-Z][a-zA-Z0-9_]{2,15}       - Starts with letter, followed by 2-15 chars (letters, numbers, underscores)
    #   |                                  - OR
    #   _[a-zA-Z0-9][a-zA-Z0-9_]{1,14}   - Starts with single underscore, then letter/number, then 1-14 chars
    # )                                    - End of alternation
    # $                                    - End of string
    # Total length: letter (1) + 2-15 chars = 3-16, or underscore (1) + letter/number (1) + 1-14 chars = 3-16
    pattern = r'^([a-zA-Z][a-zA-Z0-9_]{2,15}|_[a-zA-Z0-9][a-zA-Z0-9_]{1,14})$'
    
    return bool(re.match(pattern, username))
