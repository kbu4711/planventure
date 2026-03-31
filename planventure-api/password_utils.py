"""
Password hashing and salt utility functions for secure user authentication
"""
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import hashlib


def hash_password(password: str, salt: str = None, method: str = 'pbkdf2:sha256', rounds: int = 260000) -> str:
    """
    Hash a password with salt using werkzeug's secure hashing.
    
    Args:
        password: The plain text password to hash
        salt: Optional custom salt. If None, werkzeug generates one
        method: Hashing method (default: pbkdf2:sha256)
        rounds: Number of rounds for the hashing algorithm
        
    Returns:
        A hashed password string that can be stored in database
        
    Example:
        >>> hashed = hash_password("my_secure_password")
        >>> hashed.startswith('pbkdf2:sha256$')
    """
    if not password:
        raise ValueError("Password cannot be empty")
    
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    
    return generate_password_hash(
        password,
        method=method,
        salt_length=16 if salt is None else len(salt)
    )


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify a plain text password against a stored hash.
    
    Args:
        password: The plain text password to verify
        password_hash: The stored password hash from database
        
    Returns:
        True if password matches the hash, False otherwise
        
    Example:
        >>> hashed = hash_password("my_password")
        >>> verify_password("my_password", hashed)
        True
        >>> verify_password("wrong_password", hashed)
        False
    """
    if not password or not password_hash:
        return False
    
    return check_password_hash(password_hash, password)


def generate_salt(length: int = 32) -> str:
    """
    Generate a secure random salt for password hashing.
    
    Args:
        length: Length of the salt in bytes (default: 32)
        
    Returns:
        A hex-encoded salt string
        
    Example:
        >>> salt = generate_salt()
        >>> len(salt) == 64  # 32 bytes = 64 hex characters
    """
    if length < 1:
        raise ValueError("Salt length must be at least 1 byte")
    
    return secrets.token_hex(length)


def hash_with_custom_salt(password: str, salt: str = None) -> tuple[str, str]:
    """
    Hash a password and return both the hash and salt separately.
    Useful for storing salt and hash in separate database columns.
    
    Args:
        password: The plain text password to hash
        salt: Optional custom salt. If None, one is generated
        
    Returns:
        A tuple of (password_hash, salt)
        
    Example:
        >>> hashed, salt = hash_with_custom_salt("my_password")
        >>> len(salt) == 64  # 32 bytes hex-encoded
    """
    if not password:
        raise ValueError("Password cannot be empty")
    
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    
    if salt is None:
        salt = generate_salt()
    
    # Create hash with the salt
    combined = f"{password}:{salt}"
    password_hash = hashlib.pbkdf2_hmac(
        'sha256',
        combined.encode('utf-8'),
        salt.encode('utf-8'),
        260000
    ).hex()
    
    return password_hash, salt


def verify_with_custom_salt(password: str, password_hash: str, salt: str) -> bool:
    """
    Verify a password against a hash created with hash_with_custom_salt.
    
    Args:
        password: The plain text password to verify
        password_hash: The stored password hash
        salt: The stored salt
        
    Returns:
        True if password matches the hash, False otherwise
        
    Example:
        >>> hashed, salt = hash_with_custom_salt("my_password")
        >>> verify_with_custom_salt("my_password", hashed, salt)
        True
    """
    if not password or not password_hash or not salt:
        return False
    
    # Recreate hash with provided salt
    combined = f"{password}:{salt}"
    computed_hash = hashlib.pbkdf2_hmac(
        'sha256',
        combined.encode('utf-8'),
        salt.encode('utf-8'),
        260000
    ).hex()
    
    return computed_hash == password_hash


def is_password_strong(password: str) -> dict:
    """
    Check if a password meets strength requirements.
    
    Requirements:
        - At least 8 characters long
        - Contains uppercase letter
        - Contains lowercase letter
        - Contains digit
        - Contains special character
        
    Args:
        password: The password to check
        
    Returns:
        A dictionary with strength assessment:
        {
            'is_strong': bool,
            'length': bool,
            'has_uppercase': bool,
            'has_lowercase': bool,
            'has_digit': bool,
            'has_special': bool,
            'score': int (0-5)
        }
        
    Example:
        >>> result = is_password_strong("MyPass123!")
        >>> result['is_strong']
        True
    """
    if not password:
        return {
            'is_strong': False,
            'length': False,
            'has_uppercase': False,
            'has_lowercase': False,
            'has_digit': False,
            'has_special': False,
            'score': 0
        }
    
    checks = {
        'length': len(password) >= 8,
        'has_uppercase': any(c.isupper() for c in password),
        'has_lowercase': any(c.islower() for c in password),
        'has_digit': any(c.isdigit() for c in password),
        'has_special': any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
    }
    
    score = sum(checks.values())
    is_strong = all(checks.values())
    
    return {
        'is_strong': is_strong,
        **checks,
        'score': score
    }
